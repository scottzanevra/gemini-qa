import streamlit as st
import logging
from langchain_community.document_loaders import YoutubeLoader
from utils.config_utils import get_config
from utils.helpers import get_gemini_response, get_transcription, get_video_id
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

st.subheader(f"Talk to Youtube (using the Transcription)")
st.markdown("Interact with any YouTube video through natural conversation, asking questions, seeking summaries, "
            "or even getting translations. Whether you're a student, researcher, or simply curious, "
            "Talk to YouTube unlocks a new way to engage with video content and extract valuable insights.")

st.markdown("Note: This uses the Youtube transcription, not the video itself. If you want to analyse the video, you"
            "will need to download it and use the Talk to Video page of the application")

st.markdown("Not all Youtube videos have a transcription, you will get an error if this is the case.")


prompt = """Your task is to distill the essence of a given YouTube video transcript into a 
concise summary. Your summary should capture the key points and essential information, 
presented in bullet points, within a 250-word limit. Let's dive into the provided transcript and 
extract the vital details for our audience."""

youtube_link = st.text_input("Enter YouTube Video Link:")
video_id = None
if youtube_link:
    video_id = get_video_id(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", width=500)

# Button to trigger summary generation
if st.button("Summarise Video") and youtube_link:
    with st.spinner(f"Gemini is responding... Please hold"):
        try:
            transcript_docs = get_transcription(video_id)
            if transcript_docs:
                # Generate summary using Gemini Pro
                summary = get_gemini_response(transcript_docs, prompt)
                # Display summary
                st.markdown("## Video Summary:")
                st.write(summary)
        except Exception as e:
            st.error(f"An Error occurred {e}")


question = st.text_input("Ask a Question: ", key="input")
submit = st.button("Submit Question")

if submit and question:
    with st.spinner(f"Gemini is responding... Please hold"):
        try:
            transcript_docs = get_transcription(video_id)
            if transcript_docs:
                response = get_gemini_response(transcript_docs, question)
                st.subheader("The Response is")
                st.write(response)
        except Exception as e:
            st.error(f"An Error occurred {e}")

with st.expander("Example Use Cases"):
    st.markdown("Here are some example use case to get you started. Feel free to download the respective image/pdf, etc"
                "and upload it via the upload option. There are also a couple of question to ask alongside each of the "
                "images/pdfs if you want some ideas.")

    tab_img1, tab_img2, tab_img3, tab_img4 = st.tabs(["Alphabet 2024 Q1 Earnings Call",
                                                      "ANZ Bank Elliott", "Google Next 2024 Keynote",
                                                      "Learn Python"])
    with tab_img1:
        st.markdown("## Video")
        url_1 = "https://www.youtube.com/watch?v=A2O2f5dlzcE"
        url_1_video_id = get_video_id(url_1)
        st.markdown(f"Alphabet 2024 Q1 Earnings Call [link]({url_1})")
        st.markdown(f"URL: {url_1}")
        st.image(f"http://img.youtube.com/vi/{url_1_video_id}/0.jpg", width=500)
        st.markdown("## Questions")
        st.markdown("1) How is Alphabet approaching the integration of AI, particularly in Search?")
        st.markdown("2) How is Alphabet managing the financial implications of its AI focus?")
        st.markdown("3) How is YouTube evolving its offerings and monetization strategies?")
        st.markdown("4) What are the key points mentioned by Sundar and Ruth?")
        st.markdown("5) What were the Google Cloud revenues for the quarter? and what time were they mentioned")
    with tab_img2:
        st.markdown("## Video")
        url_2 = "https://www.youtube.com/watch?v=bTs1uZKri4Y"
        url_2_video_id = get_video_id(url_2)
        st.markdown(f"ANZ Bank Elliott: record result driven by all divisions [link]({url_2})")
        st.markdown(f"URL: {url_2}")
        st.image(f"http://img.youtube.com/vi/{url_2_video_id}/0.jpg", width=500)
        st.markdown("## Questions")
        st.markdown("1) Can you tell us about ANZ Plus and the Suncorp Bank acquisition?")
        st.markdown("2) What are the Emerging opportunities in Asia-Pacific")
    with tab_img3:
        st.markdown("## Video")
        url_3 = "https://www.youtube.com/watch?v=V6DJYGn2SFk"
        url_3_video_id = get_video_id(url_3)
        st.markdown(f"Google Cloud Next '24 Opening Keynote [link]({url_3})")
        st.markdown(f"URL: {url_3}")
        st.image(f"http://img.youtube.com/vi/{url_3_video_id}/0.jpg", width=500)
        st.markdown("## Questions")
        st.markdown("1) What were the major announcements?")
        st.markdown("2) What are agents?")
    with tab_img4:
        st.markdown("## Video")
        url_4 = "https://www.youtube.com/watch?v=kqtD5dpn9C8"
        url_4_video_id = get_video_id(url_4)
        st.markdown(f"Python for Beginners - Learn Python in 1 Hour [link]({url_4})")
        st.markdown(f"URL: {url_4}")
        st.image(f"http://img.youtube.com/vi/{url_4_video_id}/0.jpg", width=500)
        st.markdown("## Questions")
        st.markdown("1) Write me a lesson plan?")
        st.markdown("2) What are the different types of loops?")




