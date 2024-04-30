import pandas as pd
import streamlit as st
import logging
from utils.config_utils import get_config
from utils.helpers import pdf_to_temp, display_pdf, input_data_setup, get_gemini_response
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

st.title(f"Q&A with :blue[{st.session_state['model_name']}]")
st.subheader("Talk to large PDF's")

tab1, tab2, tab3 = st.tabs(["Full Context", "Retrieval-augmented generation (RAG)", "Help"])

with tab1:
    st.markdown("Gemini's large context window allows for the comprehension of extensive PDF documents, including "
                "complex charts and tables. By incorporating the entire document into its analysis, "
                "Gemini can accurately answer questions about specific data points, relationships between different "
                "sections, and overall trends. This comprehensive understanding eliminates the need for manual scrolling "
                "and searching, streamlining the process of extracting valuable insights from lengthy and intricate PDFs.")

    input = st.text_input("Input Prompt: ", key="input")
    submit=st.button("Submit Question")
    st.title("")
    uploaded_file = st.file_uploader("Choose Your PDF File", type='pdf')

    with st.expander("Show uploaded Doc"):
        try:
            if uploaded_file is not None:
                uploaded_file_temp = pdf_to_temp(uploaded_file)
                st.markdown(display_pdf(uploaded_file_temp), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An Error occurred {e}")

    if submit:
        with st.spinner(f"Gemini is responding... Please hold"):
            try:
                image_data = input_data_setup(uploaded_file)
                response=get_gemini_response(input, image_data)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                st.error(f"An Error occurred {e}")

with tab2:
    st.markdown("Retrieval-augmented generation (RAG) is a technique in natural language processing that combines "
                "pre-trained language models with information retrieval systems. It allows the model to access "
                "external knowledge sources like databases or documents during the generation process. "
                "RAG enhances the model's ability to generate accurate and informative responses by grounding "
                "its outputs in relevant factual information, making it useful in applications like question "
                "answering, summarization, and chatbot conversations.")

    # input = st.text_input("Input Prompt: ", key="input.rag")
    # uploaded_file = st.file_uploader("Choose Your PDF File", type='pdf', key='uploaded.rag')
    # pdf = ''
    #
    # submit = st.button("Ask the question")
    # if uploaded_file and submit:
    #     with st.spinner(f"Data processing underway... Please hold"):
    #         texts = load_pdf_split(uploaded_file)
    #         embeddings_model = load_embedding_model()
    #         vector_database = store_vector(texts, embeddings_model)
    #     with st.spinner(f"Gemini is responding... Please hold"):
    #         response = question_chain_response(vector_database, input)
    #         st.subheader("The Response is")
    #         st.write(response['output_text'])

with tab3:
    st.markdown("RAG (Retrieval-Augmented Generation) and long context windows are two approaches to enhance the knowledge and capabilities of language models.")
    st.markdown("# RAG")
    st.markdown("### Pros:")
    st.markdown("- Access to up-to-date information: Retrieves the latest information from external sources.")
    st.markdown("- Memory efficient: Selectively retrieves relevant information, reducing memory load.")
    st.markdown("- Scalable: Handles long documents and conversations efficiently.")
    st.markdown("- Fact-checking: Validates information against external sources for accuracy.")
    st.markdown("### Cons:")
    st.markdown("- Additional complexity: Requires an information retrieval system and integration with the language model.")
    st.markdown("- Latency: Retrieval process can introduce some latency in generating responses.")
    st.markdown("- Potential for noise: Retrieved information may not always be perfectly relevant.")
    st.markdown("# Long Context Windows")
    st.markdown("")
    st.markdown("### Pros:")
    st.markdown("- Contextual understanding: Maintains a broader context for better coherence and understanding.")
    st.markdown("- Simpler implementation: No need for external retrieval systems.")
    st.markdown("- Lower latency: No additional retrieval step involved.")
    st.markdown("### Cons:")
    st.markdown("- Memory intensive: Requires storing and processing large amounts of context.")
    st.markdown("- Limited knowledge: Relies on pre-trained knowledge within the context window.")
    st.markdown("- Less scalable: Can become computationally expensive with very long texts.")
    st.markdown("**In summary**, RAG is better suited for applications that require access to the latest information, "
                "fact-checking, and handling long texts efficiently. Long context windows are beneficial "
                "when maintaining a broader context within the text itself is essential for understanding and "
                "generating coherent responses.")

with st.expander("See some example Documents, questions, and answers"):
    tab_docs1, tab_docs2 = st.tabs(["Alphabet Earning Report", "Product T&C's"])
    with tab_docs1:
        try:
            st.markdown("## Document")
            google_url = "https://www.abc.xyz/assets/43/44/675b83d7455885c4615d848d52a4/goog-10-k-2023.pdf"
            st.markdown("### Alphabet Investor Relations - 2023 Q4 Earning Report [link](%s)" % google_url)
            st.markdown("Page count: 92")
            google_q1 = {
                "Example Questions": ["breakdown the revenue streams of alphabet by dollars",
                                      "cloud revenue between 2021 and 2022"],
                "Answer References": ["Page 33", "Page 23"],
                "Demonstrates": ["Analytics of detailed financial tables", "Analytics of detailed financial tables"]
            }
            # load data into a DataFrame object:
            df = pd.DataFrame(google_q1)
            st.table(df)
        except Exception as e:
            st.error(f"An Error occurred {e}")

    with tab_docs2:
        try:
            st.markdown("## Document")
            google_url = "https://www.centrica.com/media/lj2nlycx/centrica-annual-report-and-accounts-2022.pdf"
            st.markdown("### Centrica annual report and accounts-2022 [link](%s)" % google_url)
            st.markdown("Page count: 264")
            google_q1 = {
                "Example Questions": ["provide a summary of Scott Wheway Chairman’s Statement",
                                      "What was the Group adjusted operating profit"],
                "Answer References": ["Page 4", "Page 3, 18, 19, 123"],
                "Demonstrates": ["Summary of text", "financial tables"]
            }
            # load data into a DataFrame object:
            df = pd.DataFrame(google_q1)
            st.table(df)
        except Exception as e:
            st.error(f"An Error occurred {e}")


