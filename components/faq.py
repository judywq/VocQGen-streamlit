# flake8: noqa
import streamlit as st


def faq():
    st.markdown(
        """# FAQ

## Why is the number of distractors less than expected?

The distractors are selected from the word list you provided. 
If there are not enough appropriate distractors for a key, the respective distrator cells will be left empty. 
The suggested minimum number of words in a user word list is 50.

"""
    )
