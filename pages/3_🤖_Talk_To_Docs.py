import streamlit as st
import logging
from utils.config_utils import get_config
from utils.helpers import input_data_setup, get_gemini_response
from utils.st_utils import create_session_state
from streamlit_pdf_viewer import pdf_viewer


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
st.subheader("Talk to large PDF's")

tab1, tab2, tab3 = st.tabs(["Full Context", "Retrieval-augmented generation (RAG)", "Help"])

with tab1:
    st.markdown("Gemini's large context window allows for the comprehension of extensive PDF documents, including "
                "complex charts and tables. By incorporating the entire document into its analysis, "
                "Gemini can accurately answer questions about specific data points, relationships between different "
                "sections, and overall trends. This comprehensive understanding eliminates the need for manual scrolling "
                "and searching, streamlining the process of extracting valuable insights from lengthy and intricate PDFs.")

    query = st.text_input("Input Prompt: ", key="input")
    submit=st.button("Submit Question")
    st.title("")
    uploaded_file = st.file_uploader("Choose Your PDF File", type='pdf')

    with st.expander("Show uploaded Doc"):
        container_pdf, container_chat = st.columns([50, 50])
        try:
            if uploaded_file is not None:
                docs_data = input_data_setup(uploaded_file)
                binary_data = uploaded_file.getvalue()
                pdf_viewer(input=binary_data, width=700, height=1000)
        except Exception as e:
            st.error(f"An Error occurred {e}")

    if submit:
        with st.spinner(f"Gemini is responding... Please hold"):
            try:

                response=get_gemini_response(query, docs_data)
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

    # query = st.text_input("Input Prompt: ", key="input.rag")
    #
    # submit = st.button("Submit Question", key="submit.rag")
    # st.title("")
    # uploaded_file = st.file_uploader("Choose Your PDF File", type='pdf', key='upload.rag')
    #
    # temp_path = upload_to_temp(uploaded_file, suffix=".pdf")
    #
    # with st.expander("Show uploaded Doc"):
    #     container_pdf, container_chat = st.columns([50, 50])
    #     try:
    #         if uploaded_file is not None:
    #             docs_data = input_data_setup(uploaded_file)
    #             binary_data = uploaded_file.getvalue()
    #             pdf_viewer(input=binary_data, width=700, height=1000)
    #     except Exception as e:
    #         st.error(f"An Error occurred {e}")
    #
    # if temp_path and submit:
    #     with st.spinner(f"Populating Local Vector DB... Please hold"):
    #         try:
    #             # load the document and split it into chunks
    #             # split it into chunks
    #             texts = load_pdf_split(temp_path)
    #             # create the open-source embedding function
    #             embedding = load_embedding()
    #             # load it into Chroma
    #             db = Chroma.from_texts(texts, embedding)
    #             retriever = db.as_retriever(search_kwargs={"k": 6})
    #         except Exception as e:
    #             st.error(f"An Error occurred {e}")
    #
    # if submit:
    #     with st.spinner(f"Gemini processing... Please hold"):
    #         # Prompt
    #         prompt = hub.pull("rlm/rag-prompt")
    #         llm = VertexAI(model_name="gemini-pro", max_output_tokens=1000, temperature=0.3)
    #
    #         # Post-processing
    #         def format_docs(docs):
    #             return "\n\n".join(doc.page_content for doc in docs)
    #
    #         rag_chain = (
    #                 {"context": retriever | format_docs, "question": RunnablePassthrough()}
    #                 | prompt
    #                 | llm
    #                 | StrOutputParser()
    #         )
    #         # Question
    #         response = rag_chain.invoke("query")
    #         st.subheader("The Response is")
    #         st.write(response)


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

with st.expander("Example Use Cases"):
    st.markdown("Here are some example use case to get you started. Feel free to download the respective image/pdf, etc"
                "and upload it via the upload option. There are also a couple of question to ask alongside each of the "
                "images/pdfs if you want some ideas.")

    tab_docs1, tab_docs2, tab_docs3 = st.tabs(["Alphabet Earning Report", "Centrica Annual Report", "Climate Risk Assessment"])
    with tab_docs1:
        try:
            st.markdown("## Document")
            google_url = "https://www.abc.xyz/assets/43/44/675b83d7455885c4615d848d52a4/goog-10-k-2023.pdf"
            st.markdown("### Alphabet Investor Relations - 2023 Q4 Earning Report [link](%s)" % google_url)
            st.markdown("Page count: 92")
            st.markdown("## Questions")
            st.markdown("1) breakdown the revenue streams of alphabet by dollars (answer on Page 33)")
            st.markdown("2) cloud revenue between 2021 and 2022 (answer on Pages 23)")
            st.markdown("3) What are the operational cost of youtube?")

        except Exception as e:
            st.error(f"An Error occurred {e}")

    with tab_docs2:
        try:
            st.markdown("## Document")
            google_url = "https://www.centrica.com/media/lj2nlycx/centrica-annual-report-and-accounts-2022.pdf"
            st.markdown("### Centrica annual report and accounts-2022 [link](%s)" % google_url)
            st.markdown("Page count: 264")
            st.markdown("## Questions")
            st.markdown("1) provide a summary of Scott Wheway Chairman’s Statement (answer on Page 4)")
            st.markdown("2) What was the Group adjusted operating profit (answer on Pages 3, 18, 19, 123)")
        except Exception as e:
            st.error(f"An Error occurred {e}")

    with tab_docs2:
        try:
            st.markdown("## Document")
            rt_url = ""
            st.markdown("### [link](%s)" % rt_url)
            st.markdown("")
            st.markdown("## Questions")
            st.markdown("1) Are greenhouse gas (GHG) emissions independently assured?")
            st.markdown("2) How are they performing against its targets?")
            st.markdown("3) What climate-related transition risks is the customer vulnerable to?")
            st.markdown("4) What are the potential financial impacts to the customer due to physical risks?")
        except Exception as e:
            st.error(f"An Error occurred {e}")


