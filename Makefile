.PHONY:	setup import teardown

setup:
	docker-compose up -d postgres
	docker-compose up -d backend
import:
	docker-compose run import

teardown:
	docker-compose down
