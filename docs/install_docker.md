# Notes for installing Docker on EC2

## Launching VM

- Launch VM with Ubuntu
- Ideally start with smaller server to run the setup, but be aware that you may need a bit of memory for the initial builds (say, 8 GB)
- Attach hard disk with sufficient space
- Download `.pem` key file and store at secure location
  
## Installing Docker
- SSH into the machine: `ssh -i key.pem ubuntu@ecX-XXXXXXXX.eu-central-1.compute.amazonaws.com`
- Remember to get the permissions right for your key file: `chmod 400 key.pem`.


- Follow Docker setup (see https://docs.docker.com/engine/install/ubuntu/)

```
for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- give sudo rights
  
```
sudo usermod -aG docker ubuntu
logout # first logout
```

- test whether docker works

`sudo docker run hello-world`
