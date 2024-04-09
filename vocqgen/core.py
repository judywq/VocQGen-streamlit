import pandas as pd
from vocqgen.chat import MyBotWrapper
from vocqgen.parser import SenseRankParser, SentGenParser, DerivativeParser, RationalParser
from vocqgen.utils import fill_cloze, get_date_str, get_general_pos, read_from_cache, write_to_cache, setup_log
from vocqgen.io import read_data, write_data
from vocqgen.word_cluster import WordCluster, WordFamily
from vocqgen.nlp_helper import pos_check, is_good_position
from vocqgen.dict_helper import fetch_words_from_dict, get_senses_of_keyword
from vocqgen.config import Config
import streamlit as st


import logging
logger = logging.getLogger(__name__)


def generate_from_df(df, config: Config, progress_cb=None):
    headword_col = config.HEADWORD_COL
    
    df = clean_data(df, config)
    keywords = df[headword_col].tolist()
    selected_keywords = keywords

    logger.info(f"Fetching words from dictionary...")
    fetch_words_from_dict(keywords=keywords, api_key=st.secrets.DICT_API_KEY)

    logger.info(f"Loading WordClusters...")
    word_cluster = parse_as_word_cluster(df)
    
    # df_inflections = pd.DataFrame(word_cluster.inflection_log, columns=inflection_columns)
    df_inflections = pd.DataFrame(word_cluster.inflection_log)
    
    # word_cluster.print()
    # Return here if only inflections are needed
    # return

    word_families = select_word_families(word_cluster, keywords=selected_keywords)
    n_total = len(word_families)
    logger.info(f"Start generating cloze sentences for {n_total} words...")

    bot_sent_gen = MyBotWrapper(parser=SentGenParser(), model=config.LLM_MODEL, temperature=0.9)
    bot_rational = MyBotWrapper(parser=RationalParser(), model=config.LLM_MODEL, temperature=0)

    log_columns = ['Date', 'Task', 'Keyword', 'Tag', 'Prompt', 'Raw Response', 'Parsed Result', 'Success']
    log_data = []
    
    columns = [headword_col, 'POS', 'Collocation', 'Sentence', 'Correct Answer', *[f'Distractor {i}' for i in range(1, config.DISTRACTOR_COUNT+1)]]
    data = []
    failure_columns = ['word']
    failure_list = []
    for i, word_family in enumerate(word_families):
        if progress_cb:
            progress_cb(i+1, n_total, word_family.headword)
        logger.info(f"Processing word family {i+1}/{n_total}: {repr(word_family)}")
        count_per_family = 0
        for word in word_family.get_shuffled_words():
            if not word:
                logger.warning(f"Empty word in word family: {repr(word_family)}")
                continue

            keyword = word.surface
            keyword_tag = word.tag
            headword = word_family.headword
            
            clozed_sentence = None
            collocation = None
            for trial in range(config.RETRY_COUNT_FOR_SINGLE_WORD):
                # print(f"{repr(w)}: {candidates}")
                r = bot_sent_gen.run(inputs={"word": keyword, "tag": keyword_tag,
                                             "domain": config.DOMAIN, "level_start": config.LEVEL_START, "level_end": config.LEVEL_END,
                                             "student_type": config.STUDENT_TYPE})
                suc = r.get('success')
                log_data.append([get_date_str(), bot_sent_gen.task_name, keyword, keyword_tag, r.get('prompt'), r.get('raw_response'), r.get('result'), suc])
                
                if suc:
                    result = r.get('result')
                    clozed_sentence = result.get('sentence')
                    collocation = result.get('collocation')
                    sentence = fill_cloze(clozed_sentence, keyword)

                    suc = pos_check(inputs={"word": keyword, "tag": keyword_tag, "sentence": sentence})
                    log_data.append([get_date_str(), "POS Check", keyword, keyword_tag, f"Tag: {keyword_tag}, Sentence: {sentence}", "-", "-", suc])
                    
                    if suc:
                        suc = is_good_position(sentence, keyword)
                        log_data.append([get_date_str(), "Position Check", keyword, keyword_tag, f"Tag: {keyword_tag}, Sentence: {sentence}", "-", "-", suc])
                
                if suc:
                    break
                
            if not suc:
                logger.error(f"Failed to generate sentence for '{repr(word)}'")
                failure_list.append(word)
            else:
                if config.NEED_DISTRACTOR:
                    # Successfully generated a sentence, now generate distractors
                    distractors = fill_distractors(bot_rational, word_cluster, word, clozed_sentence, n_distractors=config.DISTRACTOR_COUNT, test_distractor_count=config.TEST_DISTRACTOR_COUNT, log_data=log_data)
                else:
                    distractors = [''] * config.DISTRACTOR_COUNT
                
                if len(distractors) < config.DISTRACTOR_COUNT:
                    logger.warn(f"Failed to generate enough distractors for '{word}', need {config.DISTRACTOR_COUNT} but got {len(distractors)}")
                    distractors.extend([''] * (config.DISTRACTOR_COUNT - len(distractors)))
                else:
                    pass
                data.append([headword, keyword_tag, collocation, clozed_sentence, keyword, *distractors])
                msg = "\n".join([f"{i+1}/{n_total}: " + "-" * 80,
                        f"Sentence: {clozed_sentence}",
                        f"Keyword: {keyword}",
                        "Distractors: " + ", ".join(distractors),])
                logger.info(msg)
                count_per_family += 1
                if config.WORD_PER_FAMILY > 0 and count_per_family >= config.WORD_PER_FAMILY:
                    # Successfully generated enough number of words for this word family,
                    #  break the word loop, goto next word family
                    break

            df_log = pd.DataFrame(log_data, columns=log_columns)
            df_failure = pd.DataFrame(failure_list, columns=failure_columns)
            # End of word loop
        # End of word family loop
    
    logger.info(f"Done.")
    df_result = pd.DataFrame(data, columns=columns)
    return {
        "result": df_result,
        "inflections": df_inflections,
        "failure": df_failure,
        "log": df_log,
    }


def fill_distractors(bot_rational, word_cluster, word, sentence, n_distractors, test_distractor_count, log_data=[], max_trials=5):
    excepts = [word]
    distractors = []
    for i in range(max_trials):
        candidates = word_cluster.find_distractors(word.tag, excepts=excepts, n=test_distractor_count)
        excepts += candidates
        
        if len(candidates) == 0:
            logger.warning(f"No more distractor candidates for '{word}'")
            break
        
        r = bot_rational.run(inputs={"keyword": word, "candidates": candidates, "sentence": sentence})
        suc = r.get('success')
        good_candidates = r.get('good_candidates')
        log_data.append([get_date_str(), bot_rational.task_name, word.surface, word.tag, r.get('prompt'), r.get('raw_response'), good_candidates, suc])
        if not suc:
            logger.error(f"Failed to decide proper distractors for {word}")
            continue
        # Make sure the distractors do not exceed the max count
        distractors += [str(w) for w in good_candidates]
        
        if len(distractors) == n_distractors:
            break
        elif len(distractors) > n_distractors:
            distractors = distractors[:n_distractors]
            break
        else:
            logger.debug(f"Trial {i}: {len(distractors)} distractors collected in total.")
    return distractors


# def load_sublist(path, sublist=1):
#     """Load a sublist from a file as a DataFrame
#     """
#     df = read_data(path=path)
#     df['Sublist'] = df['Sublist'].astype('int')
#     df = df[df['Sublist'] == sublist]
#     df = df.astype({ 'Headword': 'str' })
#     # df = df.astype({'Related word forms': 'str'})
#     logger.info("Shape of data: {}\n{}".format(df.shape, df.head()))
#     return df

def clean_data(df, config: Config):
    headword_col = config.HEADWORD_COL
    df = df.astype({ headword_col: 'str' })
    return df


@st.cache_data(show_spinner=False)
def parse_as_word_cluster(df, max_count=-1):
    """Load a sublist from a dataframe as a WordCluster object
    """
    wc = WordCluster()
    for i, row in df.iterrows():
        headword = row['Headword']
        logger.info(f"Adding to wordcluster for '{headword}'")
        # related_words = row['Related word forms'].split(',')
        # Do not derive for now
        related_words = []
        wc.add_item(headword, related_words)
        if max_count > 0 and i >= max_count:
            break
    # wc.print()
    return wc


def select_word_families(word_cluster: WordCluster, keywords: list[str] = None, start=1, max_count=-1) -> list[WordFamily]:
    start = max(start - 1, 0)
    word_families = []
    for wf in word_cluster.word_family_list[start:]:
        if keywords is None or str(wf.headword) in keywords:
            word_families.append(wf)
        if max_count > 0 and len(word_families) >= max_count:
            break
    return word_families


def select_senses(headword, pos):
    """Select all senses of a POS tag for a word
    """
    sense_map = get_senses_of_keyword(headword)
    general_pos = get_general_pos(pos)
    senses = sense_map.get(general_pos, [])
    return senses
################################

