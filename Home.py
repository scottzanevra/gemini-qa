import random

import streamlit as st
import logging

from utils.config_utils import get_config
from utils.st_utils import create_session_state

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = get_config(config_file="config.yml")
create_session_state()


# SET APPLICATION DETAILS
st.set_page_config(page_title=config['application']['name'],
                   page_icon=":robot:",
                   layout=config['application']['layout'],
                   initial_sidebar_state="auto",
                   menu_items=None)

st.title("Q&A with :blue[Gemini Pro]")

