compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

dev-deploy:
	make compose-down
	make compose-up
	git add . 
	git commit -m "update"