test-server:
	docker-compose exec server pytest -W ignore::DeprecationWarning

reset-db:
	rm -rf ./server/migrations
	docker-compose exec server aerich init -t playola.db.TORTOISE_ORM
	docker-compose exec server aerich init-db
