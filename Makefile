.PHONY: install venv docker-build docker-run manual-setup run-bot clean

# Default make target
all: install

# Create a virtual environment
venv:
	python3 -m venv env

# Activate the virtual environment and install requirements
install: venv
	. env/bin/activate; \
	pip3 install -r requirements.txt

# Build the Docker container
docker-build:
	docker-compose build

# Run the Docker container
docker-run:
	docker-compose up -d

# Run the bot (you need to activate venv before running this)
run-bot:
	. env/bin/activate; \
	cd src/bot; \
	python3 bot.py &

# Clean up the environment
clean:
	rm -rf env
