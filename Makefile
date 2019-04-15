.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '(^[a-zA-Z_-]+:.*?##.*$$)|(^##)' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}{printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' \
		| sed -e 's/\[32m##/[33m/'

## Host

.PHONY: provision
provision: ## Run ansible provisioners
	vagrant provision --provision-with ansible_local

## Guest

.PHONY: clean
clean: ## Unintall pipenv virtual environment
	pipenv --rm

.PHONY: install
install: ## Install pipenv virtual environment
	pyenv local 3.7.2 ; \
	pipenv install

.PHONY: run
run: ## Run flask embedded web server
	# --host=0.0.0.0
	# Listen on all public IP addresses
	pipenv run flask run --host=0.0.0.0 --port=5000

