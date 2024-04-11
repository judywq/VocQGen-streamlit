import os
import pandas as pd
import streamlit as st

from vocqgen.core import generate_from_df
from vocqgen.config import Config
from components.sidebar import sidebar
from components.introduction import introduction
from components.faq import faq


from utils import to_excel
from vocqgen.utils import setup_log

setup_log()


config = Config()

if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False
    
# st.secrets.MODEL_LIST = ["gpt-3.5-turbo", "gpt-4", "gpt-4-1106-preview"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="VocQGen", page_icon="📖", layout="wide")

introduction()

sidebar()

st.write("## Get started")

api_key_input = st.text_input(
    "OpenAI API Key",
    type="password",
    placeholder="Paste your OpenAI API key here (sk-...)",
    help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
    value=os.environ.get("OPENAI_API_KEY", None)
    or st.session_state.get("OPENAI_API_KEY", ""),
)

st.session_state["OPENAI_API_KEY"] = api_key_input

openai_api_key = st.session_state.get("OPENAI_API_KEY")
if not openai_api_key:
    st.warning(
        "Please enter your OpenAI API key. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
else:
    os.environ["OPENAI_API_KEY"] = openai_api_key



uploaded_file = st.file_uploader(
    "Upload your Excel file",
    type=["xlsx", "xls"],
)


with st.expander("Advanced Options", expanded=True):
    model: str = st.selectbox("Model", options=st.secrets.MODEL_LIST)  # type: ignore
    config.LLM_MODEL = model
    
    config.HEADWORD_COL = st.text_input("Headword Column", value=config.HEADWORD_COL, help="The column name in your input data for the headword")
    config.WORD_PER_FAMILY = st.number_input("Questions per family", min_value=-1, max_value=1000, value=config.WORD_PER_FAMILY, step=1, help="Number of questions you want to generate for each word family. (-1 means all)")


if not uploaded_file:
    faq()
    st.stop()

st.write("### Original Data:")
original_data = pd.read_excel(uploaded_file)
st.write(original_data)

my_bar = None
if st.button("Generate Cloze!", disabled=st.session_state.running, key='run_button'):
    my_bar = st.progress(0, text="Initializing...")
    # Process the data
    result = generate_from_df(original_data, config, 
                              lambda i, n, w: my_bar.progress(i / n, text=f"[{i}/{n}] Generating cloze for word `{w}`..."))
    st.session_state.result = result
    # https://discuss.streamlit.io/t/disable-the-button-until-the-end-of-the-script-execution/42443/8
    st.rerun()


if 'result' in st.session_state:
    result = st.session_state.result
    df_result = result['result']

    if my_bar:
        my_bar.empty()

    st.write("### Result:")
    st.write(df_result)

    # Download link for the processed data
    excel_data = to_excel(df_result)
    st.download_button(label='📥 Download Result',
                        data=excel_data ,
                        file_name= 'result.xlsx')

    st.write("### Log:")
    st.write(result['log'])
    
    st.write("### Inflections:")
    st.write(result['inflections'])
    
    st.write("### Failure:")
    st.write(result['failure'])

faq()

