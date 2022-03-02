DOCKER_IMAGE_NAME=docker.io/pedrorangelbraga/bigquery-query-runner
DOCKER_IMAGE_TAG=$(TAG)

resources/install:
	mkdir -p resources/
	pip install -e . --upgrade --no-cache-dir
	touch resources/install

resources/uninstall:
	pip3 uninstall -y PyGithub jinjasql==0.1.8 google-cloud-bigquery==1.25.0 smart-open[all]==4.2.0 click==7.1.2

docker/package:
	python3 setup.py bdist_wheel --dist-dir=docker/package
	rm -rf build

docker/image: docker/package
	docker build docker -f docker/Dockerfile -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	touch docker/image

docker/push: docker/image
	docker push $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)
	touch docker/push

docker/push-latest: docker/image
	docker tag $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) $(DOCKER_IMAGE_NAME):latest
	docker push $(DOCKER_IMAGE_NAME):latest
	touch docker/push-latest

clean:
	rm -rf docker/package
	rm -rf docker/image
	rm -rf docker/push
	rm -rf docker/push-latest
