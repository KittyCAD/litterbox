DOCKER_IMAGE_NAME := kittycad/litterbox-dev

INTERACTIVE := $(shell [ -t 0 ] && echo 1 || echo 0)
ifeq ($(INTERACTIVE), 1)
	DOCKER_FLAGS += -t
endif

.PHONY: test
test: docker-image ## Test all the python files.
	docker run --rm -i $(DOCKER_FLAGS) \
		--name litterbox-dev \
		-e KITTYCAD_API_TOKEN \
		--disable-content-trust \
		-v $(CURDIR):/home/user/src \
		--workdir /home/user/src \
		$(DOCKER_IMAGE_NAME) #TODO

.PHONY: format
format: docker-image ## Format all the python files.
	docker run --rm -i $(DOCKER_FLAGS) \
		--name litterbox-dev \
		-e KITTYCAD_API_TOKEN \
		--disable-content-trust \
		-v $(CURDIR):/home/user/src \
		--workdir /home/user/src \
		$(DOCKER_IMAGE_NAME) sh -c 'isort . */*/*.py && ruff format && ruff check --fix . */*/*.py'

.PHONY: shell
shell: docker-image ## Pop into a shell in the docker image.
	docker run --rm -i $(DOCKER_FLAGS) \
		--name litterbox-dev-shell \
		-e KITTYCAD_API_TOKEN \
		--disable-content-trust \
		-v $(CURDIR):/home/user/src \
		--workdir /home/user/src \
		$(DOCKER_IMAGE_NAME) /bin/bash


.PHONY: docker-image
docker-image:
	docker build -t $(DOCKER_IMAGE_NAME) .

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
