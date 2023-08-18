<div align="center">


# Create daemon process



```bash
cd /etc/systemd/system && touch bot.service
```

#### Clone the text from lokatir/bot/bot.service 
### (make changes!!!)
#### to /etc/systemd/system/bot.service

   
 Start the process:

```bash
systemctl start bot.service
sudo systemctl restart bot.service
```

---

## Ii you haven't set up CI-CD or don't want to manually do a git pull:


 Make file executable:
 ### (make changes!!!)
```bash
chmod +x auto_pull.sh
```

 Transfer your ssh key to the server so you don't have to enter a password:
    
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub -p $VPS_PORT $VPS_USER@$VPS_IP
```
 Run the file:

```bash
./auto_pull.sh
```


