import streamlit as st

from components.faq import faq
# from dotenv import load_dotenv
import os

# load_dotenv()


def sidebar():
    with st.sidebar:
        st.markdown(
            "## How to use\n"
            "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
            "2. Upload a excel file📄\n"
            "3. Under the `Advanced Options` section, specify the column name of the head words in your excel file\n"
            "4. Click the `Generate Cloze!` button\n"
        )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "📖VocQGen (**Voc**abulary **Q**uestion **Gen**erator) generates vocabulary tests based on the word list you uploaded."
        )
        st.markdown(
            "This tool is a work in progress. "
            "You can contribute to the project on [GitHub](https://github.com/judywq/VocQGen-streamlit) "  # noqa: E501
            "with your feedback and suggestions💡"
        )
        st.markdown("Made by [Judy Wang](https://github.com/judywq)")
        st.markdown("---")

        faq()
