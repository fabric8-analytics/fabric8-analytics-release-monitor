ifeq ($(TARGET),rhel)
  DOCKERFILE := Dockerfile.rhel
  REPOSITORY := openshiftio/rhel-fabric8-analytics-release-monitor
else
  DOCKERFILE := Dockerfile
  REPOSITORY := openshiftio/fabric8-analytics-release-monitor
endif

REGISTRY?=quay.io
DEFAULT_TAG=latest
TESTS_IMAGE=fabric8-analytics-release-monitor-tests

.PHONY: all docker-build fast-docker-build test get-image-name get-image-repository mypy

all: fast-docker-build

docker-build:
	docker build --no-cache -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

fast-docker-build:
	docker build -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) .

fast-docker-build-tests:
	docker build -t $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) -f $(DOCKERFILE) .
	docker tag $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG) $(TESTS_IMAGE)

test: fast-docker-build-tests
	./runtest.sh

get-image-name:
	@echo $(REGISTRY)/$(REPOSITORY):$(DEFAULT_TAG)

get-image-repository:
	@echo $(REPOSITORY)

get-push-registry:
	@echo $(REGISTRY)

mypy:
	mypy --ignore-missing-imports release_monitor/*.py # you need to run pip install mypy by hand

coverage:
	pytest --cov="release_monitor/" --cov-report html:/tmp/cov_report -vv release_monitor/ tests/
