up:
	docker-compose up --build -d
	docker exec -it -e RUNTYPE=bash $$(docker ps|grep inrad-api |awk '{ print $$1 }') bash
down:
	docker-compose down