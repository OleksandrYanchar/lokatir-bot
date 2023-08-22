## File for automatic Git pull

#### Make file executable:
 ### (make changes!!!)
```bash
chmod +x auto_pull.sh
```

 Transfer your ssh key to the server so you don't have to enter a password(no need to repeat if you have already done it):

    
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub -p $VPS_PORT $VPS_USER@$VPS_IP
```
 Run the file:

```bash
./auto_pull.sh
```

---

## File for backup logs

#### Make file executable:
 ### (make changes!!!)
```bash
chmod +x log_backup.sh
```

 Transfer your ssh key to the server so you don't have to enter a password(no need to repeat if you have already done it):

    
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub -p $VPS_PORT $VPS_USER@$VPS_IP
```
 Run the file:

```bash
./log_backup.sh.sh
```

---

## File for backup databases

#### Make file executable:
 ### (make changes!!!)
```bash
chmod +x db_backup.sh
```

 Transfer your ssh key to the server so you don't have to enter a password(no need to repeat if you have already done it):

    
```bash
ssh-copy-id -i ~/.ssh/id_rsa.pub -p $VPS_PORT $VPS_USER@$VPS_IP
```
 Run the file:

```bash
./db_backup.sh
```