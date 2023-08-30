IMAGE_REPO_URL="geofferyj/fidle-backend"


# ---------------------------------------------------------------------------------------------------------------------
# Local development commands
# ---------------------------------------------------------------------------------------------------------------------

# Run the local development server
run-local:
	docker compose -f local.yml up --build

# Run the local development server with logs
run-local-log:
	make run-local 2>&1 | tee "logs/server_$(date +"%d-%m-%Y-%H-%M-%S").log"

# Build the docker image locally
build-local:
	docker compose -f local.yml build

# Execute the makemigrations command
makemigrations:
	docker compose -f local.yml build
	docker compose --verbose -f local.yml run --rm django python manage.py $@

# Execute the migrate command
migrate:
	docker compose -f local.yml run --rm django python manage.py $@


shell:
	docker compose -f local.yml run --rm django python manage.py $@

shell-in-container:
	docker compose -f local.yml run --rm django bash

shell-log:
	make shell 2>&1 | tee "logs/shell_$(date +"%d-%m-%Y-%H-%M-%S").log"

shell-i:
	docker compose -f local.yml run --rm django python manage.py $@ -i python

drop_all_tables:
	docker compose -f local.yml run --rm django python manage.py makemigrations -n drop_all_tables $(app_name)


createsuperuser:
	docker compose -f local.yml run --rm django python manage.py $@



# ---------------------------------------------------------------------------------------------------------------------
# Docker Production commands
# ---------------------------------------------------------------------------------------------------------------------

# Build the docker image
build-image:
	docker build -f compose/production/django/Dockerfile -t $(IMAGE_REPO_URL) .

# Push the image to the docker hub
push-image:
	docker tag $(IMAGE_REPO_URL) $(IMAGE_REPO_URL):$(tag)
	docker push $(IMAGE_REPO_URL):$(tag)



# ---------------------------------------------------------------------------------------------------------------------
# Kuberbetes commands
# ---------------------------------------------------------------------------------------------------------------------

# Save the kubernetes configurtion file
k8s-config-save:
	doctl kubernetes cluster kubeconfig save d70df694-8a1d-4d61-a1c1-58f5d1d8f4c0

docker-secretes:
	kubectl create secret docker-registry regcred --docker-server=https://index.docker.io/v2/ --docker-username=$(docker-username) --docker-password=$(docker-password) --docker-email=$(docker-email)



# ---------------------------------------------------------------------------------------------------------------------
# Helm commands (Helm is a tool for managing Kubernetes releases)
# ---------------------------------------------------------------------------------------------------------------------


# dry-run the deployment
helm-dry-run:
	helm upgrade --install --debug --dry-run fidle ./compose/helm

# install the deployment
helm-install:
	helm upgrade --install fidle ./compose/helm --set image.repository=$(IMAGE_REPO_URL) --set image.tag=$(tag)

helm-update:
	helm upgrade fidle ./compose/helm --set image.repository=$(IMAGE_REPO_URL) --set image.tag=$(tag)
# uninstall the deployment
helm-uninstall:
	helm uninstall fidle

# Open an interactive shell in the specified pod
shell-in-pod:
	kubectl exec --stdin --tty $(pod) -- /bin/bash

# ---------------------------------------------------------------------------------------------------------------------
# Services Commands
# ---------------------------------------------------------------------------------------------------------------------

start-web:
	/start

start-beat:
	/start-celerybeat

start-worker:
	/start-celeryworker

start-flower:
	/start-flower

relay:
	helm upgrade --install webhookrelay-operator webhookrelay/webhookrelay-operator \
	--set credentials.key=$(RELAY_KEY) --set credentials.secret=$(RELAY_SECRET)




# ---------------------------------------------------------------------------------------------------------------------
# Logging and monitoring commands
# ---------------------------------------------------------------------------------------------------------------------

get-loki-secrets:
	kubectl get secret --namespace loki-stack loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode

launch-logs-dashboard:
	kubectl --namespace loki-stack port-forward svc/loki-grafana 8080:80

launch-grafana:
	kubectl port-forward svc/kube-prometheus-stack-grafana 8080:80 -n kube-prometheus-stack



# Run the local development server
run-prod:
	docker compose -f production.yml up --build -d

stop-prod:
	docker compose -f production.yml down

migrate-prod:
	docker compose -f production.yml run --rm django python manage.py migrate


# seeders
seed_currencies:
	docker compose -f local.yml run --rm django python manage.py $@

seed_wallet_type:
	docker compose -f local.yml run --rm django python manage.py $@
