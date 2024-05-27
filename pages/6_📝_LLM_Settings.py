import streamlit as st
import logging

from utils.config_utils import get_config
from utils.st_utils import reset_session, create_session_state

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = get_config(config_file="config.yml")

# SET APPLICATION DETAILS
st.set_page_config(page_title=config['application']['name'],
                   page_icon='✨',
                   layout=config['application']['layout'],
                   initial_sidebar_state="auto",
                   menu_items=None)

create_session_state()
st.title(f"Q&A with :blue[Gemini]")


st.write("Model Settings:")

model_name = st.selectbox("Select A Model", config['llm']['model_options'])
temperature_value = st.slider('Temperature :', 0.0, 1.0, float(st.session_state['temperature']))
model_max_output_tokens = 2048 if st.session_state['model_name'] == "gemini-1.0-pro-vision-001" else 8192
max_output_tokens = st.slider('max_output_tokens:', 1, model_max_output_tokens, st.session_state['max_output_tokens'])
top_p_value = st.slider('Top-P :', 0.0, 1.0, float(st.session_state['top_p']))

submit = st.button("Submit Question")
if submit:
    st.session_state['temperature'] = temperature_value
    st.session_state['max_output_tokens'] = max_output_tokens
    st.session_state['top_p'] = top_p_value
    st.session_state['model_name'] = model_name
    st.success(f"Model updated")


if st.button("Reset Session"):
    reset_session()
