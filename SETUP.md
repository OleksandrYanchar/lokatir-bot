# Setting Up and Running the Lokatir Bot


## Installation


### Prerequisites

 Update the package list:

```bash
sudo apt update
```
      
 Clone this repository:

```bash
git clone https://github.com/OleksandrYanchar/lokatir-bot
```

### Here you have 2 choices:

### Docker:

default build:
```bash
docker-compose up --build
```
build and run in the background:
```bash
docker-compose up -d --build
```

### Continue manually:

 Set up a virtual environment:

```bash
python3 -m venv env
```

 Activate the virtual environment:
    
```bash
source env/bin/activate
```
 Install required Python packages:

```bash
pip3 install -r requirements.txt
```

### Usage 

Navigate to the src/ directory:

```bash
cd src/bot
```

```bash
python3 bot.py
```
