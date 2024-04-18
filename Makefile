up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker build -t streamlit-test-timeout:latest .
