import datetime
import json
import os
import pickle
import re

import logging
logger = logging.getLogger(__name__)


class ExtendableDict(dict):
    def extend(self, key, value: set):
        if key not in self.keys():
            self[key] = set()
        self[key].update(value)
    
    def merge(self, other: dict):
        for key, value in other.items():
            if key not in self.keys():
                self[key] = set()
            self[key].update(value)
            

def setup_log(level='INFO', log_path='./log/txt', need_file=True):
    if not os.path.exists(log_path):
        os.makedirs(log_path)    
        
    log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s: %(message)s")
    
    handlers = []
    if need_file:
        filename = get_date_str()
        file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, filename))
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(level=level)
    handlers.append(console_handler)

    # https://stackoverflow.com/a/11111212
    logging.basicConfig(level=logging.DEBUG,
                        handlers=handlers)


def cloze_sentence(sentence, word):
    """Replace the word in the sentence with a blank (4 underscores)
    """
    return sentence.replace(word, '_' * 4)


def fill_cloze(sentence, word):
    """Fill the blank in the sentence with the word
    """
    return sentence.replace('_' * 4, word)


def replace_article(sentence):
    """Replace the article "a" or "an" into "a/an" before the cloze

    Args:
        sentence (str): the clozed sentence
    """
    pat = re.compile(r"\b(a|an) +_{2,}\b")
    return pat.sub("a/an " + "_" * 4, sentence)


cache_dir = './cache'
def get_cache_path(path, sublist):
    head, tail = os.path.split(path)
    fn = os.path.join(cache_dir, f"{tail}.sublist{sublist}.cache")
    return fn
    
def read_from_cache(path, sublist):
    fn = get_cache_path(path, sublist)
    if not os.path.exists(fn):
        return None
    with(open(fn, 'rb')) as f:
        return pickle.load(f)

def write_to_cache(path, sublist, obj):
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fn = get_cache_path(path, sublist)
    with(open(fn, 'wb')) as f:
        pickle.dump(obj, f)


def get_date_str():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")


def load_config(file='./config.json'):
    if not os.path.exists(file):
        logger.error(f"Config file does not exist: {file}")
        exit(-1)

    with open(file, 'r') as f:
        config = json.load(f)
    return config

def get_general_pos(tag):
    """Get the general POS tag from a fine-grained POS tag
    """
    if tag.startswith('NN'):
        return 'NN'
    elif tag.startswith('VB'):
        return 'VB'
    elif tag.startswith('JJ'):
        return 'JJ'
    elif tag.startswith('RB'):
        return 'RB'
    else:
        return tag

import re

def remove_curly_braces_content(input_string):
    pattern = re.compile(r'{.*?}')
    cleaned_string = re.sub(pattern, '', input_string)
    return cleaned_string
