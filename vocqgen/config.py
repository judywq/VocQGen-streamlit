from dataclasses import dataclass

@dataclass
class Config:
    HEADWORD_COL: str = 'Headword'
    TARGET_COL: str = 'IsKeyword'
    DEFAULT_LOG_LEVEL = "INFO"
    # DEFAULT_LOG_LEVEL = "DEBUG"

    LLM_MODEL = 'gpt-3.5-turbo-0301'
    # LLM_MODEL = 'gpt-3.5-turbo'
    # LLM_MODEL = 'gpt-4'
    # LLM_MODEL: str = 'gpt-4-1106-preview'

    REQUEST_TIMEOUT_SECS: int = 60

    # Number of words to generate for each word family
    WORD_PER_FAMILY: int = -1

    DOMAIN: str = 'General Academic'
    LEVEL_START: str = 'A2'
    LEVEL_END: str = 'lower B2'
    STUDENT_TYPE: str = 'Japanese university students without domain-specific English knowledge whose proficiency level is A2-B2'
    # The number of times to retry when ChatGPT fails to generate a sentence for a word
    RETRY_COUNT_FOR_SINGLE_WORD: int = 3

    # The start position of keyword selection (count from 1, inclusive)
    # KEYWORD_START_POS = 1
    # KEYWORD_START_POS = 11

    # The number of keywords for generating sentences, -1 means all
    # KEYWORD_COUNT = -1
    # KEYWORD_COUNT = 10

    NEED_DISTRACTOR: bool = True
    # NEED_DISTRACTOR = False
    DISTRACTOR_COUNT: int = 3 # The number of distractors to output to result
    TEST_DISTRACTOR_COUNT: int = 10 # The number of distractors to ask ChatGPT to test rationality in one trial
