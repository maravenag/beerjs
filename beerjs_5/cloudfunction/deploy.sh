#!/bin/bash

PROJECT_NAME="gcp-project"
BUCKET="bucket-name"
FUNCTION_NAME="predict_new_file"

gcloud config set project ${PROJECT_NAME}

gcloud functions deploy ${FUNCTION_NAME}\
    --runtime python37 \
    --trigger-resource ${BUCKET} \
    --trigger-event google.storage.object.finalize \
    --timeout 540s \
    --memory 2048MB