# Gemini Powered Assistant
## Unlock the Hidden Knowledge: An AI-Powered Conversation with Your Images, PDFs, and YouTube Videos

Introducing the future of information interaction: a revolutionary generative AI application that leverages the power of a multimodal model. Imagine seamlessly conversing with images, PDFs, and YouTube videos, unlocking a new dimension of understanding and knowledge extraction. No longer constrained by traditional search methods, this application empowers users to engage directly with content, asking questions, seeking clarification, or even requesting summaries in a conversational manner.

With the ability to understand and interpret various media formats, this AI-powered tool transforms the way we interact with information. From analyzing complex diagrams within images to extracting key insights from lengthy PDF documents or summarizing informative YouTube videos, the possibilities are endless. Whether you're a student seeking a deeper understanding of educational material, a researcher navigating a vast amount of scientific literature, or simply a curious individual eager to learn, this application opens a world of knowledge at your fingertips. Experience the power of multimodal conversation and unlock a new level of information interaction.

## If running the code locally

Create the virtual environment
```
$ python3 -m venv env
```
Activate the virtual environment
```
$ source env/bin/activate
```
Install dependencies using
```
$ pip install -r requirements.txt
```

## Run Streamlit app Locally (from the project root directory)

```
$ streamlit run Home.py
```

# Deploy Streamlit-Gemini

```
export GOOGLE_CLOUD_PROJECT=""
export CONTAINER_NAME='streamlit-gemini'
export APP_NAME='streamlit-gemini'
export REGION="us-central1"
export AR_NAME="streamlit" 
export AR_URI=${REGION}-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/${AR_NAME}
export SERVICE_ACCOUNT=""
```
```
gcloud auth print-access-token | sudo docker login -u oauth2accesstoken --password-stdin https://us-central1-docker.pkg.dev

sudo docker build --no-cache -t ${AR_URI}/${CONTAINER_NAME} . && sudo docker push ${AR_URI}/${CONTAINER_NAME} && gcloud run deploy ${APP_NAME} \
--image=${AR_URI}/${CONTAINER_NAME} \
--platform=managed \
--service-account=${SERVICE_ACCOUNT} \
--region=${REGION} \
--cpu=2 --memory=1Gi \
--max-instances=2 \
--allow-unauthenticated \
--port 8501
```
