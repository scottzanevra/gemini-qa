# AI Powered -------

This application demonstrates a Cloud Run application that uses the [Streamlit](https://streamlit.io/) framework.

## GCP Setup

```shell
gcloud services enable compute.googleapis.com aiplatform.googleapis.com storage.googleapis.com --project "{PROJECT_ID}"
```

# Change this if you need the VPC to be created.
CREATE_VPC = False

# Set the project id
! gcloud config set project {PROJECT_ID}

# Remove the if condition to run the encapsulated code
if CREATE_VPC:
    # Create a VPC network
    ! gcloud compute networks create {VPC_NETWORK} --bgp-routing-mode=regional --subnet-mode=auto --project={PROJECT_ID}

    # Add necessary firewall rules
    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-icmp --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow icmp

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-internal --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow all --source-ranges 10.128.0.0/9

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-rdp --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow tcp:3389

    ! gcloud compute firewall-rules create {VPC_NETWORK}-allow-ssh --network {VPC_NETWORK} --priority 65534 --project {PROJECT_ID} --allow tcp:22

    # Reserve IP range
    ! gcloud compute addresses create {PEERING_RANGE_NAME} --global --prefix-length=16 --network={VPC_NETWORK} --purpose=VPC_PEERING --project={PROJECT_ID} --description="peering range"

    # Set up peering with service networking
    # Your account must have the "Compute Network Admin" role to run the following.
    ! gcloud services vpc-peerings connect --service=servicenetworking.googleapis.com --network={VPC_NETWORK} --ranges={PEERING_RANGE_NAME} --project={PROJECT_ID}


# Creating bucket.
! gsutil mb -l $REGION -p $PROJECT_ID $BUCKET_URI


initial_config = {
    "id": "banana_id",
    "embedding": [float(x) for x in list(embeddings.numpy()[0])],
}

with open("data.json", "w") as f:
    json.dump(initial_config, f)

!gsutil cp data.json {EMBEDDING_DIR}/file.json

Creating Index
my_index = aiplatform.MatchingEngineIndex.create_tree_ah_index(
    display_name=DISPLAY_NAME,
    contents_delta_uri=EMBEDDING_DIR,
    dimensions=DIMENSIONS,
    approximate_neighbors_count=150,
    distance_measure_type="DOT_PRODUCT_DISTANCE",
)

Creating Endpoint
my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint.create(
    display_name=f"{DISPLAY_NAME}-endpoint",
    network=VPC_NETWORK_FULL,
)

Deploy Index
my_index_endpoint = my_index_endpoint.deploy_index(
    index=my_index, deployed_index_id=DEPLOYED_INDEX_ID
)

my_index_endpoint.deployed_indexes



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
$ streamlit run app.py
```



## Build and Deploy the Application to Cloud Run

To deploy the Streamlit Application in [Cloud Run](https://cloud.google.com/run/docs/quickstarts/deploy-container), we need to perform the following steps:

1. Your Cloud Function requires access to two environment variables:

   - `GCP_PROJECT` : This the Google Cloud Project Id.
   - `GCP_REGION` : This is the region in which you are deploying your Cloud Function. For e.g. us-central1.
  
    These variables are needed since the Vertex AI initialization needs the Google Cloud Project Id and the region. The specific code line from the `main.py`
    function is shown here:
    `vertexai.init(project=PROJECT_ID, location=LOCATION)`

    In Cloud Shell, execute the following commands:

    ```bash
    export GCP_PROJECT='<Your GCP Project Id>'  # Change this
    export GCP_REGION='us-central1'             # If you change this, make sure region is supported by Model Garden. When in doubt, keep this.
    ```

2. We are now going to build the Docker image for the application and push it to Artifact Registry. To do this, we will need one environment variable set that will point to the Artifact Registry name. We have a command that will create this repository for you.

   In Cloud Shell, execute the following commands:

   ```bash
   export AR_REPO='<REPLACE_WITH_YOUR_AR_REPO_NAME>'  # Change this
   export SERVICE_NAME='chat-streamlit-app' # This is the name of our Application and Cloud Run service. Change it if you'd like. 
   gcloud artifacts repositories create "$AR_REPO" --location="$GCP_REGION" --repository-format=Docker
   gcloud auth configure-docker "$GCP_REGION-docker.pkg.dev"
   gcloud builds submit --tag "$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME"
   ```

3. The final step is to deploy the service in Cloud Run with the image that we built and pushed to the Artifact Registry in the previous step:

    In Cloud Shell, execute the following command:

    ```bash
    gcloud run deploy "$SERVICE_NAME" \
      --port=8080 \
      --image="$GCP_REGION-docker.pkg.dev/$GCP_PROJECT/$AR_REPO/$SERVICE_NAME" \
      --allow-unauthenticated \
      --region=$GCP_REGION \
      --platform=managed  \
      --project=$GCP_PROJECT \
      --set-env-vars=GCP_PROJECT=$GCP_PROJECT,GCP_REGION=$GCP_REGION
    ```

On successfully deployment, you will be provided a URL to the Cloud Run service. You can visit that in the browser to view the application that you just deployed. Type in your queries and the application will prompt the Vertex AI Text model and display the response.
