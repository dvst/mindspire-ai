# Mindspire Frontend Web App

Mindspire is a responsive and WCAG-compliant web application built using vanilla JavaScript. It offers an accessible user interface that adapts seamlessly across devices, ensuring inclusivity for all users.

The app is hosted on Azure App Services and deployed using the Azure CLI via the ZIP file method. 

## Features

- **Responsive Design**: Optimized for various screen sizes and devices.
- **Accessibility**: Compliant with WCAG standards to ensure usability for everyone.
- **Vanilla JavaScript**: Built without additional frameworks for simplicity and performance.

## Live Demo

Access the app here: [Mindspire Web App](https://mindspire-webapp.azurewebsites.net)

## Build Process

1. Clone the repository:
   ```bash
   git clone https://github.com/dvst/mindspire-ai.git
   cd mindspire-ai/frontend
   ```

2. Create a ZIP package of the project:
   ```bash
   zip -r app.zip .
   ```

## Deployment Process

### Prerequisites

- Azure CLI installed: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Access to an Azure subscription.

### Deployment Steps

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Create an Azure Resource Group (if not already created):**
   Replace `your-resource-group-name` and `your-region` with your desired values.
   ```bash
   az group create --name your-resource-group-name --location your-region
   ```

3. **Create an Azure App Service Plan:**
   Replace `your-app-service-plan` with the name for your plan.
   ```bash
   az appservice plan create --name your-app-service-plan --resource-group your-resource-group-name --sku F1
   ```

   Validate appservice plan creation:
   ```bash
   az appservice plan list --output table
   ```

4. **Create the Web App:**
   Replace `your-app-service-name` with your desired app name.
   ```bash
   az webapp create --name your-app-service-name --plan your-app-service-plan --resource-group your-resource-group-name
   ```

   Validate webapp creation:
   ```bash
   az webapp list --output table
   ```

   You can also query details of the webapp just created:
   ```bash
   az webapp show --name your-app-service-name --resource-group your-resource-group-name --query "state"
   ```

5. **Deploy the ZIP file to Azure App Services:**
   Replace `your-app-service-name` with the name of your Azure App Service.
   ```bash
   az webapp deployment source config-zip \
     --resource-group your-resource-group-name \
     --name your-app-service-name \
     --src app.zip
   ```

6. **Verify the deployment:**
   Once the deployment is complete, open the application URL to ensure it is working correctly:
   ```bash
   az webapp browse --name your-app-service-name --resource-group your-resource-group-name
   ```

### Notes

- Make sure to update your `resource-group-name`, `app-service-plan`, and `app-service-name` with the correct values.
- Regularly test the app for responsiveness and accessibility compliance.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or features you'd like to see.

