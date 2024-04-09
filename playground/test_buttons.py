import streamlit as st
import time

if 'run_button' in st.session_state and st.session_state.run_button == True:
    st.session_state.running = True
else:
    st.session_state.running = False

if st.button('Do a thing', disabled=st.session_state.running, key='run_button'):
    status = st.progress(0)
    for t in range(10):
        time.sleep(.2)
        status.progress(10*t+10)
    st.session_state.output = 'Selenium Output'
    st.rerun()

if 'output' in st.session_state:
    st.write(st.session_state.output)