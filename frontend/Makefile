# Variables
RESOURCE_GROUP=diciembre11
APP_NAME=mindspire-webapp
PLAN_NAME=mindspire-plan
LOCATION=centralus
SKU=F1
ZIP_NAME=site.zip

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make create-plan    - Create Azure App Service Plan"
	@echo "  make create-webapp  - Create Azure Web App"
	@echo "  make build         - Build and zip the application"
	@echo "  make deploy        - Deploy application to Azure"
	@echo "  make check-status  - Check webapp status"
	@echo "  make clean         - Remove build artifacts"
	@echo "  make all-in-one    - Execute complete deployment process"

# Create App Service Plan
.PHONY: create-plan
create-plan:
	@echo "Creating App Service Plan..."
	az appservice plan create \
		--name $(PLAN_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--sku $(SKU) \
		--location $(LOCATION)
	az appservice plan list --output table

# Create Web App
.PHONY: create-webapp
create-webapp:
	@echo "Creating Web App..."
	az webapp create \
		--name $(APP_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--plan $(PLAN_NAME)
	az webapp list --output table

# Build application
.PHONY: build
build: clean
	@echo "Building application..."
	zip $(ZIP_NAME) index.html styles.css script.js \
		$(wildcard *.svg) \
		$(wildcard *.jpeg) \
		$(wildcard *.png)

# Deploy application
.PHONY: deploy
deploy: build
	@echo "Deploying application..."
	az webapp deployment source config-zip \
		--resource-group $(RESOURCE_GROUP) \
		--name $(APP_NAME) \
		--src $(ZIP_NAME)

# Check webapp status
.PHONY: check-status
check-status:
	@echo "Checking Web App status..."
	az webapp show \
		--name $(APP_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--query "state"

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -f $(ZIP_NAME)

# Build and deploy
.PHONY: build-and-deploy
build-and-deploy: build deploy clean

# Complete deployment process
.PHONY: all-in-one
all-in-one: create-plan create-webapp deploy check-status