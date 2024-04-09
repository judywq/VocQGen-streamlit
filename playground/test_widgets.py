import time
import streamlit as st
import pandas as pd


num = st.number_input("Number", min_value=-1, max_value=1000, value=-1, step=1)
st.write(type(num))

if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False

uploaded_file = st.file_uploader(
    "Upload an Excel file",
    type=["xlsx", "xls"],
)

if not uploaded_file:
    st.stop()
    
st.write("### Original Data:")
original_data = pd.read_excel(uploaded_file)
st.write(original_data)


# if not st.session_state.clicked:
if st.button("Start!", disabled=st.session_state.running, key='run_button'):
    st.write("Start processing...")

    time.sleep(2)

    st.write("Processing completed!")
    st.session_state.output = ['a', 'b', 'c']
    st.rerun()


if 'output' in st.session_state:
    st.write(st.session_state.output)

