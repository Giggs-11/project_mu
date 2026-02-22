# Build Docker image
docker-build:
	docker build -t my-python-app .

# Run Docker container
docker-run:
	docker run -p 8000:8000 my-python-app

# Run Django commands inside container
docker-manage:
	docker exec -it $(docker ps -lq) python src/manage.py $(cmd)
