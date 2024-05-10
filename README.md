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


## Prerequisite

* Enable the Cloud Run API via the [console](https://console.cloud.google.com/apis/library/run.googleapis.com?_ga=2.124941642.1555267850.1615248624-203055525.1615245957) or CLI:

```bash
gcloud services enable run.googleapis.com
```

#### Deploying a Cloud Run service

1. Set Project Id:
    ```bash
    export GOOGLE_CLOUD_PROJECT="dataplex-demo-342803"
    export PROJECT_ID=$(gcloud config get-value project -q)
    export REPOSITORY_ID="streamlit"
    export REGION"=us-central1"
    ```

2. Enable the Artifact Registry API:
    ```bash
    gcloud services enable artifactregistry.googleapis.com
    ```

3. Create an Artifact Registry repo:
    ```bash
       
   gcloud artifacts repositories create $REPOSITORY_ID \
    --repository-format=docker \
    --location=$REGION
   --project=$PROJECT_ID
    ```
4. Service Account
```shell
#!/bin/bash

# This script creates a service account with access to the Gemini API.

PROJECT_ID=$(gcloud config get-value project -q)
SERVICE_ACCOUNT_NAME=gemini-sa

gcloud iam service-accounts create $SERVICE_ACCOUNT_NAME \
    --display-name="Service account for Gemini API" \
    --project=$PROJECT_ID

gcloud iam service-accounts keys create ${SERVICE_ACCOUNT_NAME}.json \
    --iam-account=$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member=serviceAccount:$SERVICE_ACCOUNT_NAME@$PROJECT_ID.iam.gserviceaccount.com \
    --role=roles/aiplatform.modelServiceAgent  

```bash
gcloud run deploy hello --image us-docker.pkg.dev/cloudrun/container/hello --region=us-west1
```

```shell
gcloud compute backend-services create hello-backend-service --global
```

```shell
gcloud compute backend-services add-backend hello-backend-service \
       --global \
       --network-endpoint-group=neg-hello-us-west1 \
       --network-endpoint-group-region=us-west1
```

```shell
gcloud compute network-endpoint-groups create neg-hello-us-west1 \
       --region=us-west1 \
       --network-endpoint-type=serverless  \
       --cloud-run-service=hello
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
