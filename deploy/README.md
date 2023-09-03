# First option
## Docker

default build:
```bash
docker-compose up --build
```
build and run in the background:
```bash
docker-compose up -d --build
```

Check status:
```bash
docker-compose ps
```

# Second option
## Create daemon process

```bash
cd /etc/systemd/system && touch bot.service
```

#### Clone the text from lokatir-bot/deploy/bot.service 
### (make changes!!!)
#### to /etc/systemd/system/bot.service

   
 Start the process:

```bash
systemctl start bot.service
sudo systemctl restart bot.service
```



 


