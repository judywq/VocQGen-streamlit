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

setup_log(need_file=False)


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
    options = st.secrets.MODEL_LIST + ["Another option..."]
    model: str = st.selectbox("Model", options=options)  # type: ignore
    
    if model == "Another option...": 
        otherOption = st.text_input("Enter your model name...", help="Enter the name of the model you want to use. (e.g. 'gpt-4o-mini')")
        config.LLM_MODEL = otherOption
    else:
        config.LLM_MODEL = model
    
    config.HEADWORD_COL = st.text_input("Headword Column", value=config.HEADWORD_COL, help="The column name in your input data for the headword")
    config.WORD_PER_FAMILY = st.number_input("Questions per family", min_value=-1, max_value=1000, value=config.WORD_PER_FAMILY, step=1, help="Number of questions you want to generate for each word family. (-1 means all)")
    config.DOMAIN = st.text_input("Domain", value=config.DOMAIN, help="The domain of the words you want to generate questions for. (General Academic, Medical, etc.)")
    config.LEVEL_START = st.text_input("CEFR Level Range From", value=config.LEVEL_START, help="The starting level of the words you want to generate questions for. (A1, B1, etc.)")
    config.LEVEL_END = st.text_input("CEFR Level Range To", value=config.LEVEL_END, help="The ending level of the words you want to generate questions for. (B2, C1, etc.)")
    config.STUDENT_TYPE = st.text_input("Student Type", value=config.STUDENT_TYPE, help="The type of students you want to generate questions for. ")


if not uploaded_file:
    faq()
    st.stop()

st.write("### Original Data:")
original_data = pd.read_excel(uploaded_file)
st.write(original_data)

my_bar = None
if st.button("Generate Cloze!", disabled=st.session_state.running, key='run_button'):
    my_bar = st.progress(0, text="Initializing...")
    result_slot = st.empty()
    
    # Process the data
    for result in generate_from_df(original_data, config, 
                              lambda i, n, w: my_bar.progress(i / n, text=f"[{i}/{n}] Generating cloze for word `{w}`...")):
        with result_slot.container():
            df_result = result['result']

            st.write("### Result:")
            st.write(df_result)

            st.write("### Log:")
            st.write(result['log'])
            
            st.write("### Inflections:")
            st.write(result['inflections'])
            
            st.write("### Failure:")
            st.write(result['failure'])
        st.session_state.result = result
    # https://discuss.streamlit.io/t/disable-the-button-until-the-end-of-the-script-execution/42443/8
    st.rerun()



if 'result' in st.session_state:
    # if my_bar:
    #     my_bar.empty()
        
    result = st.session_state.result
    df_result = result['result']

    st.write("### Result:")
    st.write(df_result)

    st.write("### Log:")
    st.write(result['log'])
    
    st.write("### Inflections:")
    st.write(result['inflections'])
    
    st.write("### Failure:")
    st.write(result['failure'])
    # Download link for the processed data
    excel_data = to_excel(df_result)
    st.download_button(label='📥 Download Result',
                        data=excel_data ,
                        file_name= 'result.xlsx')


faq()
