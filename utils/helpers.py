import base64
import io
import tempfile
import vertexai
import streamlit as st
from vertexai.generative_models import GenerativeModel, Part
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from utils.config_utils import get_config
from utils.st_utils import create_session_state

config = get_config(config_file="config.yml")

vertexai.init(project=config['gcp']['project_id'], location=config['gcp']['region'])

create_session_state()


def load_model():
    return GenerativeModel(st.session_state['model_name'])


def get_gemini_response(query, data):
    _generation_config = {
        "max_output_tokens": st.session_state['max_output_tokens'],
        "temperature": st.session_state['temperature'],
        "top_p": st.session_state['top_p'] ,
    }
    model = load_model()
    response = model.generate_content([query, data],
                                      generation_config=_generation_config
                                      # stream=True
                                      )
    return response.text


def input_data_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_part = Part.from_data(
            mime_type=f"{uploaded_file.type}",
            data=bytes_data)
        return image_part
    else:
        raise FileNotFoundError("No file uploaded")


def upload_to_temp(uploaded_file, suffix=".pdf"):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.read()

        # Convert bytes data to a BytesIO object
        file_like_object = io.BytesIO(bytes_data)

        # Save BytesIO object to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_like_object.read())
            tmp_path = tmp.name
            return tmp_path


def display_pdf(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    return pdf_display


def get_transcription(video_id):
    from youtube_transcript_api import YouTubeTranscriptApi
    srt = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_text = ""
    for i in srt:
        transcript_text += f"{ str(i)}"
    return transcript_text


def get_video_id(youtube_link):
    return youtube_link.split("=")[1]


def load_pdf_split(tmp_path):
    loader = PyPDFLoader(tmp_path)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    content = "\n\n".join(str(page.page_content) for page in pages)
    texts = text_splitter.split_text(content)
    return texts


def load_embedding():
    from langchain.embeddings import VertexAIEmbeddings
    return VertexAIEmbeddings()


# def question_chain_response(vector_database, user_input):
#     llm = VertexAI(model_name="gemini-pro", max_output_tokens=1000, temperature=0.3)
#     chain = load_qa_chain(model, chain_type='stuff')
#     docs = vector_database.get_relevant_documents(user_input)
#
#     response = chain({'input_documents': docs, 'question': user_input}, return_only_outputs=True)
#     return response

if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=bTs1uZKri4Y"
    docs = get_transcription(url)
    foo = "me"