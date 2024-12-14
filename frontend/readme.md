# Useful commands to deploy frontend into Azure App Services
zip site.zip index.html script.js

az appservice plan create --name mindspire-plan --resource-group diciembre11 --sku F1 --location "centralus"
az appservice plan list --output table

az webapp create --name mindspire-webapp --resource-group diciembre11 --plan mindspire-plan
az webapp list --output table

az webapp deployment source config-zip --resource-group diciembre11 --name mindspire-webapp --src site.zip

az webapp show --name mindspire-webapp --resource-group diciembre11 --query "state"
