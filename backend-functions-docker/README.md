# Mindspire Accessibility Checker - Backend Service

This project is a backend service written in Python 3.11, designed to run on Azure Functions in a Dockerized environment. It serves as an accessibility checker enhanced with AI functionality to provide actionable insights and suggestions for improving web accessibility. The service:

- Analyzes AXE accessibility reports to provide detailed code suggestions for fixes.
- Summarizes AXE reports, explaining the impact of detected issues on populations with disabilities.

## Features
- **AI-Powered Fix Suggestions**: Automatically generate code fixes based on AXE accessibility reports.
- **Impact Summaries**: Provide context on how accessibility issues affect individuals with disabilities.
- **Dockerized**: Easily deploy and scale using containerized environments.
- **Azure Functions Integration**: Seamless deployment to Azure's serverless compute platform.

---

## Configure
To configure the backend service, use the `dotenv` Python module for managing environment variables. Create a `.env` file in the project root with the following variables:

```env

OPENAI_API_KEY=your_azure_openai_api_key
OPENAI_API_BASE=your-azure-openai-endpoint
OPENAI_API_TYPE="azure"
OPENAI_API_VERSION=azure-openai-api-version
CHAT_MODEL_NAME=the_name_of_your_deployed_model

# CORS Configuration
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

Ensure to replace placeholders with actual values specific to your environment.

---

## Build
1. Clone the repository:
   ```bash
   git clone https://github.com/dvst/mindspire-ai
   cd backend-functions-docker
   ```
2. Build the Docker image:
   ```bash
   docker build -t mindspire-mindspire-accessibility-checker .
   ```

---

## How to Run Locally
### Prerequisites
1. Install the [Azure Functions Core Tools (func)](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local):
   - **On Windows**:
     ```powershell
     npm install -g azure-functions-core-tools@4 --unsafe-perm true
     ```
   - **On macOS/Linux**:
     ```bash
     npm install -g azure-functions-core-tools@4 --unsafe-perm true
     ```

2. Ensure Docker is installed and running on your machine.

3. Create a `.env` file as described in the **Configure** section.

4. Set up a Python virtual environment and install dependencies:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

### Steps
1. Start the Azure Function in a Docker container:
   ```bash
   func start
   ```

2. Access the backend service at `http://localhost:7071`.

3. Test the endpoints using tools like Postman or curl.

---

## Prepare Azure Resources
1. Log in to Azure:
   ```bash
   az login
   ```
2. Create a Resource Group:
   ```bash
   az group create --name AccessibilityCheckerGroup --location eastus
   ```
3. Create an Azure Storage Account:
   ```bash
   az storage account create --name yourstorageaccount --resource-group AccessibilityCheckerGroup --location eastus --sku Standard_LRS
   ```
4. Create an Azure Function App:
   ```bash
   az functionapp create --name AccessibilityCheckerApp --storage-account yourstorageaccount --resource-group AccessibilityCheckerGroup --consumption-plan-location eastus --runtime python --functions-version 4
   ```

To set these environment variables in Azure, use the following commands:

```bash
az functionapp config appsettings set --name AccessibilityCheckerApp \
  --resource-group AccessibilityCheckerGroup \
  --settings "OPENAI_API_KEY=your_azure_openai_api_key" \
             "OPENAI_API_BASE=your-azure-openai-endpoint" \
             "OPENAI_API_TYPE=azure" \
             "OPENAI_API_VERSION=azure-openai-api-version" \
             "CHAT_MODEL_NAME=the_name_of_your_deployed_model"
```


---

## Push Docker Image to Azure Container Registry and Deploy
### Prerequisites
1. Ensure you have an Azure Container Registry (ACR) set up:
   ```bash
   az acr create --resource-group AccessibilityCheckerGroup --name youracrname --sku Basic
   ```
2. Log in to the ACR:
   ```bash
   az acr login --name youracrname
   ```

### Steps
1. Tag the Docker image with the ACR name:
   ```bash
   docker tag mindspire-accessibility-checker youracrname.azurecr.io/mindspire-accessibility-checker:latest
   ```

2. Push the Docker image to the ACR:
   ```bash
   docker push youracrname.azurecr.io/mindspire-accessibility-checker:latest
   ```

3. Update the Azure Function App to use the custom Docker image:
   ```bash
   az functionapp config container set --name AccessibilityCheckerApp \
     --resource-group AccessibilityCheckerGroup \
     --docker-custom-image-name youracrname.azurecr.io/mindspire-accessibility-checker:latest \
     --docker-registry-server-url https://youracrname.azurecr.io
   ```

4. Deploy the application:
   ```bash
   func azure functionapp publish AccessibilityCheckerApp --docker
   ```
5. Configure CORS for the frontend to access the backend:
   ```bash
   az functionapp cors add --name AccessibilityCheckerApp --resource-group AccessibilityCheckerGroup --allowed-origins "https://your-frontend-domain.com"
   ```

6. Restart the Azure Function App to apply the changes:
   ```bash
   az functionapp restart --name AccessibilityCheckerApp --resource-group AccessibilityCheckerGroup
   ```

7. Test the deployed Azure Function App:
   - Retrieve the Function App URL:
     ```bash
     az functionapp show --name AccessibilityCheckerApp --resource-group AccessibilityCheckerGroup --query defaultHostName -o tsv
     ```
   - Test the endpoints using the retrieved URL and tools like Postman or curl.


---

## Notes
- **CORS Configuration**: Ensure that your frontend domain is included in the `ALLOWED_ORIGINS` variable and added to the Azure Function CORS settings.
- **AXE Integration**: Ensure you have valid access to AXE APIs if needed for the enhanced AI functionality.
- **Testing**: Use tools like Postman or curl to test API endpoints locally and on Azure.

## Troubleshooting

1. Verify environment variables are set correctly
2. Ensure all required dependencies are listed in requirements.txt
4. Check Azure Function App logs through the Azure portal

For further details or troubleshooting, please refer to the [Azure Functions Documentation](https://learn.microsoft.com/en-us/azure/azure-functions/).


