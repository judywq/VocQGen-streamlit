import streamlit as st

from components.faq import faq
# from dotenv import load_dotenv
import os

# load_dotenv()


def sidebar():
    with st.sidebar:
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
