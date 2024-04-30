import streamlit as st
import logging

from utils.config_utils import get_config
from utils.helpers import get_gemini_response, upload_to_temp, input_data_setup
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

st.title(f"Q&A with :blue[{st.session_state['model_name']}]")

st.subheader(f"Talk to a Video")
st.markdown("Upload your own video file and start asking questions. Gemini will process the video's content, "
            "including speech and on-screen text, and provide insightful answers, summaries, or even translations. "
            "It's like having a personal assistant that understands and responds to your questions about any video.")

prompt = """Welcome, Video Summarizer! Your task is to distill the essence of a given video  into a 
concise summary. Your summary should capture the key points and essential information, 
presented in bullet points, within a 250-word limit. """

tab1, tab2 = st.tabs(["Upload a Video", "Record a video"])

with tab1:
    question = st.text_input("Input Prompt: ", key="input")
    submit = st.button("Submit Question")
    st.title("")
    uploaded_file = st.file_uploader("Choose an image...", type=["mp4", "mpeg"])

    if uploaded_file:
        uploaded_file_temp = upload_to_temp(uploaded_file)
        video_data = input_data_setup(uploaded_file)


    # Button to trigger summary generation
    if st.button("Summarise Video") and uploaded_file:
        with st.spinner(f"Gemini is responding... Please hold"):
            try:
                summary = get_gemini_response(prompt, video_data)
                st.markdown("## Video Summary:")
                st.write(summary)
            except Exception as e:
                st.error(f"An Error occurred {e}")

    if submit:
        with st.spinner(f"Gemini is responding... Please hold"):
            try:
                response = get_gemini_response(question, video_data)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                st.error(f"An Error occurred {e}")

with st.expander("See some example Documents, questions, and answers"):
    tab_img1, tab_img2 = st.tabs(["Bike Accident", "Something elese"])
    with tab_img1:
        st.markdown("## Questions")

    with tab_img2:
        st.markdown("## Questions")

