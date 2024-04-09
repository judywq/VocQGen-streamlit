# flake8: noqa
import streamlit as st


def faq():
    st.markdown(
        """
# FAQ
## How does VocQGen work?
VocQGen will take the word list you uploaded and generate vocabulary tests
for each of the word with the following step:

1. Collect a list of inflections (with POS tagging) for each word
2. For each of the inflections, generate a cloze test with GPT
3. Find n (default 3) distractors with the same POS tag from the word list you provided for each cloze test
4. Ask GPT to check whether these distractors are appropriate for the cloze test


## Why is the number of distractors less than expected?
The distractors are selected from the word list you provided. 
If there are not enough appropriate distractors for a word, the column will be left empty.


"""
    )
