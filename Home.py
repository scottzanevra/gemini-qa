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
                   page_icon='✨',
                   layout=config['application']['layout'],
                   initial_sidebar_state="auto",
                   menu_items=None)

st.title("Q&A with :blue[Gemini Pro]")

st.subheader(" About this app")
st.markdown("## Your All-in-One Conversational Companion")
st.markdown("This app leverages Gemini's multimodal capabilities to transform the way users interact with various "
            "forms of "
            "media. Engage in dynamic conversations that seamlessly incorporate videos, podcasts, YouTube content, "
            "and images.")

st.subheader(f"Talk to Images")
st.markdown("Gemini's advanced image understanding capabilities allow users to ask detailed "
             "questions about images. By simply uploading or linking to an image, users can inquire "
             "about its content, context, or even hidden details. Gemini can identify objects, analyze scenes, "
             "and provide insightful interpretations, making it a powerful tool for exploring visual information.")

st.subheader(f"Talk to Large Documents using the large context window of Gemini")
st.markdown("Gemini's large context window allows for the comprehension of extensive PDF documents, including "
                "complex charts and tables. By incorporating the entire document into its analysis, "
                "Gemini can accurately answer questions about specific data points, relationships between different "
                "sections, and overall trends. This comprehensive understanding eliminates the need for manual scrolling "
                "and searching, streamlining the process of extracting valuable insights from lengthy and intricate PDFs.")

st.subheader(f"Talk to Youtube")
st.markdown(" interact with any YouTube video through natural conversation, asking questions, seeking summaries, "
            "or even getting translations. Whether you're a student, researcher, or simply curious, "
            "Talk to YouTube unlocks a new way to engage with video content and extract valuable insights.")

st.subheader(f"Talk to a Video")
st.markdown("Upload your own video file and start asking questions. Gemini will process the video's content, "
            "including speech and on-screen text, and provide insightful answers, summaries, or even translations. "
            "It's like having a personal assistant that understands and responds to your questions about any video.")