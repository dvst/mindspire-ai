# Variables
RESOURCE_GROUP=diciembre11
FUNCTION_APP_NAME=mindspire-backenddemo
STORAGE_NAME=mindspirebackendstorage
LOCATION=centralus
PYTHON_VERSION=3.11
SKU=B1

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make create-storage   - Create Azure Storage Account"
	@echo "  make create-function  - Create Azure Function App"
	@echo "  make install-deps     - Install Python dependencies"
	@echo "  make build           - Build the function app"
	@echo "  make deploy          - Deploy to Azure Functions"
	@echo "  make clean           - Clean build artifacts"
	@echo "  make all-in-one      - Complete deployment process"

# Create Storage Account
.PHONY: create-storage
create-storage:
	@echo "Creating Storage Account..."
	az storage account create \
		--name $(STORAGE_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--location $(LOCATION) \
		--sku Standard_LRS \
		--kind StorageV2

# Create Function App
.PHONY: create-function
create-function:
	@echo "Creating Function App..."
	az functionapp create \
		--name $(FUNCTION_APP_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--storage-account $(STORAGE_NAME) \
		--runtime python \
		--runtime-version $(PYTHON_VERSION) \
		--functions-version 4 \
		--consumption-plan-location $(LOCATION)

# Install dependencies
.PHONY: install-deps
install-deps:
	@echo "Installing Python dependencies..."
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

# Build the function app
.PHONY: build
build: clean install-deps
	@echo "Building Function App..."
	mkdir -p build
	cp -r function_app.py host.json requirements.txt build/
	[ -f local.settings.json ] && cp local.settings.json build/ || true

# Deploy to Azure
.PHONY: deploy
deploy: build
	@echo "Deploying to Azure Functions..."
	cd build && func azure functionapp publish $(FUNCTION_APP_NAME) \
		--python \
		--build remote

# Clean build artifacts
.PHONY: clean
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build
	rm -rf .python_packages
	rm -rf __pycache__
	rm -rf .pytest_cache

# Check function app status
.PHONY: check-status
check-status:
	@echo "Checking Function App status..."
	az functionapp show \
		--name $(FUNCTION_APP_NAME) \
		--resource-group $(RESOURCE_GROUP) \
		--query state

# Complete deployment process
.PHONY: all-in-one
all-in-one: create-storage create-function deploy check-status

# Start function app locally
.PHONY: start-local
start-local: install-deps
	@echo "Starting Function App locally..."
	func start

# Get function app logs
.PHONY: logs
logs:
	@echo "Fetching Function App logs..."
	az functionapp logs tail \
		--name $(FUNCTION_APP_NAME) \
		--resource-group $(RESOURCE_GROUP)
