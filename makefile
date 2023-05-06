run-action-server:
	python -m rasa_sdk --auto-reload -vv --actions actions

validate:
	rasa data validate

train: validate
	rasa train

run-bot: train
	rasa run \
		--enable-api \
		-vv \
		--cors "*"
	
shell: train
	rasa shell -vv

format:
	black . && \
		isort .