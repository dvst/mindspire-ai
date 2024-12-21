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
   cd mindspire-ai
   ```

## Deployment Process

### Prerequisites

- Azure CLI installed: [Install Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- Access to an Azure subscription.
- An Azure App Service resource created for hosting the app.

### Deployment Steps

1. **Login to Azure:**
   ```bash
   az login
   ```

2. **Navigate to the project directory:**
   Ensure all project files are in the root directory.

3. **Create a ZIP package of the project:**
   ```bash
   zip -r app.zip .
   ```

4. **Deploy the ZIP file to Azure App Services:**
   Replace `your-app-service-name` with the name of your Azure App Service.
   ```bash
   az webapp deployment source config-zip \
     --resource-group your-resource-group-name \
     --name your-app-service-name \
     --src app.zip
   ```

5. **Verify the deployment:**
   Once the deployment is complete, open the application URL to ensure it is working correctly:
   ```bash
   az webapp browse --name your-app-service-name --resource-group your-resource-group-name
   ```

### Notes

- Make sure to update your `resource-group-name` and `app-service-name` with the correct values.
- Regularly test the app for responsiveness and accessibility compliance.

## Contributing

Feel free to fork this repository and submit pull requests for any improvements or features you'd like to see.


# Useful commands to deploy frontend into Azure App Services

```bash
az appservice plan create --name mindspire-plan --resource-group diciembre11 --sku F1 --location "centralus"
```

```bash
az appservice plan list --output table
```

```bash
az webapp create --name mindspire-webapp --resource-group diciembre11 --plan mindspire-plan
```

```bash
az webapp list --output table
```

```bash
az webapp deployment source config-zip --resource-group diciembre11 --name mindspire-webapp --src site.zip
```

```bash
az webapp show --name mindspire-webapp --resource-group diciembre11 --query "state"
```
