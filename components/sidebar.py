import streamlit as st


def sidebar():
    with st.sidebar:
        st.markdown(
            """# Contact us
This tool is a work in progress. 
In future iterations, user adjustable variables such as length of question and learner proficiency level will be introduced. 
You can contribute to the project on [GitHub](https://github.com/judywq/VocQGen-streamlit) with your feedback and suggestions.

Made by Judy Wang, Ralph Rose, Ayaka Sugawara and Naho Orita from Center for English Language Education, 
Faculty of Science and Engineering (CELESE), Waseda University, Japan.

Contact info: judy.wang@aoni.waseda.jp
"""
        )
        st.markdown(
            "**Version 1.0.0**"
        )
