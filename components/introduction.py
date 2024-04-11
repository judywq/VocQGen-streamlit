import streamlit as st

from components.faq import faq
# from dotenv import load_dotenv
import os

# load_dotenv()


def introduction():
    st.markdown("# VocQGen")
    st.markdown(
        """VocQGen (**Voc**abulary **Q**uestion **Gen**erator) generates multiple-choice cloze vocabulary questions 
based on a list of user uploaded words. The questions are generated using OpenAI's GPT models, 
showing contextualized use of words and their inflected forms in the academic context for ESL 
learners of A2-B2 proficiency levels. Distractors are chosen among words of the same part of speech from the same list.

This tool is a work in progress. 
In future iterations, user adjustable variables such as length of question and learner proficiency level will be introduced. 
You can contribute to the project on GitHub with your feedback and suggestions.

Made by Judy Wang, Ralph Rose, Ayaka Sugawara and Naho Orita from Center for English Language Education, 
Faculty of Science and Engineering (CELESE), Waseda University, Japan.
"""
    )
    
    st.markdown("## How does VocQGen work?")
    st.markdown("""VocQGen will take the word list you uploaded and generate vocabulary tests for each of the word with the following step:

1. VocQGen pre-processes each input word in the list into a word family that contains the input word and all its inflected forms 
(inflected through LemmInflect and Unimorph libraries and validated against Google Ngram). Part of Speech (POS) tagged are also assigned to each word in a family.
2. VocQGen randomly selects a word from a family, retrieves it POS and generates a complete sentence with GPT using the selected word (key). 
It then replaces the word with a blank, and finds n (default 3) distractors with the same POS tag from other word families in the word list. 
The distractors are validated by GPT to ensure syntactical appropriateness and semantic remoteness compared to the key. 
The process repeats based on the number of questions a user has specified for each word family.

For details, please refer to the following publications:

Wang, Q., Rose, R. L., Orita, N., \& Sugawara, A. (2023). Automated generation of multiple-choice cloze questions for assessing English vocabulary using GPT-turbo 3.5. Proceedings of the NLP4DH-IWCLUL 2023 Conference. Association for Computational Linguistics. Tokyo, Japan. https://doi.org/10.48550/arXiv.2403.02078 """)        

    # st.markdown("---")

    st.markdown(
    """## How to use
1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) key below.
Please note that your API key will **NOT** be stored by either the developers or Streamlit.

2. Upload the list of words you want to create questions for. 
The words should be in a column and there should be a heading for the column, such as "Headword". 
See [the excel file](https://github.com/judywq/VocQGen-streamlit/raw/main/test-data/Example.xlsx) here for an example.

3. Under the `Advanced Options` section, specify the column heading of the input words in your excel file ("Headword" for example). 
Then, under "Question per family", fill in how many questions you want to generate for each word family. 
If you want to generate questions for every word in the family, please fill in "-1". VocQGen currently generates one question for each word in a family.

4. Click the `Generate Cloze!` button and wait for the response from VoCQgen. 
The results can be viewed on the browser and is available for download. 
A log, inflection and failure list will also be available on the browser. 
"""
)
