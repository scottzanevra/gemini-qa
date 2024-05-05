import streamlit as st

from utils.config_utils import get_config

config = get_config(config_file="config.yml")


def reset_session() -> None:
    st.session_state['temperature'] = 1
    st.session_state['model_name'] = config['llm']['model_options'][0]
    st.session_state['max_output_tokens'] = 8192
    st.session_state['top_p'] = 0.05


def hard_reset_session() -> None:
    st.session_state = {states : [] for states in st.session_state}


def create_session_state():
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 1
    if 'max_output_tokens' not in st.session_state:
        st.session_state['max_output_tokens'] = 8192
    if 'top_p' not in st.session_state:
        st.session_state['top_p'] = 0.95
    if 'model_name' not in st.session_state:
        st.session_state['model_name'] = config['llm']['model_options'][0]
