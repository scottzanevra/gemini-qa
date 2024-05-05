import streamlit as st
import logging
from PIL import Image

from utils.config_utils import get_config

from utils.helpers import get_gemini_response, input_data_setup
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

st.subheader(f"Talk to Images")
st.markdown("Gemini's advanced image understanding capabilities allow users to ask detailed "
             "questions about images. By simply uploading or linking to an image, users can inquire "
             "about its content, context, or even hidden details. Gemini can identify objects, analyze scenes, "
             "and provide insightful interpretations, making it a powerful tool for exploring visual information.")


input=st.text_input("Input Prompt: ", key="input")
submit=st.button("Submit Question")
st.title("")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

with st.expander("Show uploaded Image"):
    image=""
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", width=1000)
        except Exception as e:
            st.error("Image can not be loaded")

if submit:
    with st.spinner(f"Gemini is responding... Please hold"):
        try:
            image_data = input_data_setup(uploaded_file)
            response=get_gemini_response(input, image_data)
            st.subheader("The Response is")
            st.write(response)
        except Exception as e:
            st.error(f"An Error occurred {e}")

with st.expander("Example Use Cases"):
    st.markdown("Here are some example use case to get you started. Feel free to download the respective image/pdf, etc"
                "and upload it via the upload option. There are also a couple of question to ask alongside each of the "
                "images/pdfs if you want some ideas.")

    tab_img1, tab_img2, tab_img3, tab_img4, tab_img5 = st.tabs(["Financial Line Chart", "Draw Code", "Damaged Car Assessment",
                                                      "Electrical Diagram", "Terraform"])
    with tab_img1:
        st.markdown("## Questions")
        st.markdown("1) What does this chart represent")
        st.markdown("2) Which company has the highest return in march 2022")
        st.markdown("3) Which months has Alphabet Inc Class A stock out performed the NASDAQ Composite")
        st.markdown("## Image")
        st.image('images/alphabet_compare.png', width=500)

    with tab_img2:
        st.markdown("## Questions")
        st.markdown("1) Translate this into python code")
        st.markdown("2) What other features could be included in this game")
        st.markdown("## Image")
        st.image('images/number_guessing_game.png', width=500)

    with tab_img3:
        st.markdown("## Questions")
        st.markdown("1) What parts have been damaged")
        st.markdown("2) Provided a breakdown of parts that need to be replaced or repaired and the estimated costs")
        st.markdown("3) What is the likely extent of any injuries")
        st.markdown("## Image")
        st.image('images/damagedcar1.png', width=500)
        st.image('images/damagedcar3.png', width=500)

    with tab_img4:
        st.markdown("## Questions")
        st.markdown("1) How may double powerpoints are installed")
        st.markdown("2) Provide a breakdown of the rooms, and how many lights switches per room")
        st.markdown("## Image")
        st.image('images/elec_level_0.png', width=500)
        st.image('images/elec_level_1.png', width=500)

    with tab_img5:
        st.markdown("## Questions")
        st.markdown("1) Write the terraform code for this architecture")
        st.markdown("2) What IAM permission are required")
        st.markdown("## Image")
        st.image('images/architecture.png', width=500)


