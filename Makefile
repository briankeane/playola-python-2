test:
	docker-compose exec server pytest -W ignore::DeprecationWarning
