# Backend Functions Docker

This repository contains a Dockerized version of the backend functions for the accessibility analysis service.

## Prerequisites

- [nerdctl](https://github.com/containerd/nerdctl) installed
- [containerd](https://containerd.io/) installed and running
- Azure CLI (optional, for deployment to Azure)

## Building the Docker Image

To build the Docker image using nerdctl:

```bash
nerdctl build -t accessibility-backend:latest .
```

## Running Locally

To run the container locally:

```bash
nerdctl run -d -p 8080:8080 \
  -e OPENAI_API_KEY="your-api-key" \
  -e OPENAI_API_BASE="your-api-base" \
  -e OPENAI_API_TYPE="azure" \
  -e OPENAI_API_VERSION="2023-05-15" \
  -e CHAT_MODEL_NAME="your-model-name" \
  accessibility-backend:latest
```

## Deploying to Azure Functions App Service

1. Tag your image for Azure Container Registry:

```bash
nerdctl tag accessibility-backend:latest <acr-name>.azurecr.io/accessibility-backend:latest
```

2. Log in to Azure Container Registry:

```bash
az acr login --name <acr-name>
```

3. Push the image:

```bash
nerdctl push <acr-name>.azurecr.io/accessibility-backend:latest
```

4. Create an Azure Function App:

```bash
az functionapp create \
  --name <function-app-name> \
  --resource-group <resource-group> \
  --storage-account <storage-account> \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --image <acr-name>.azurecr.io/accessibility-backend:latest
```

## Environment Variables

The following environment variables need to be configured:

- `OPENAI_API_KEY`: Your Azure OpenAI API key
- `OPENAI_API_BASE`: Your Azure OpenAI endpoint
- `OPENAI_API_TYPE`: Set to "azure"
- `OPENAI_API_VERSION`: Azure OpenAI API version
- `CHAT_MODEL_NAME`: The name of your deployed model

## Development

To modify the application:

1. Update the code in the respective Python files
2. Rebuild the Docker image
3. Test locally
4. Push to Azure Container Registry
5. Update the Function App

## Troubleshooting

If you encounter any issues:

1. Check the logs:
```bash
nerdctl logs <container-id>
```

2. Verify environment variables are set correctly
3. Ensure all required dependencies are listed in requirements.txt
4. Check Azure Function App logs through the Azure portal

## Notes

- The Dockerfile uses multi-stage building to reduce the final image size
- Only necessary system dependencies are installed
- The image is based on python:3.9-slim for minimal size
- Playwright is installed with only the Chromium browser to save space
```

You'll also need to create a requirements.txt file if you haven't already. Here's what it should contain based on your current setup:

```text:backend-functions-docker/requirements.txt
flask
playwright
beautifulsoup4
openai
python-dotenv
requests
azure-functions
```

This setup provides a lightweight, production-ready Docker image that's compatible with Azure Functions App Service. The multi-stage build helps reduce the final image size by separating the build environment from the runtime environment. The README provides comprehensive instructions for both local development using nerdctl and deployment to Azure.