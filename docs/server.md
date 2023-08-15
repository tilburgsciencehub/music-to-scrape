# Configure server for being reachable on top-level domain (EC2)

(thanks to ChatGPT..., using this prompt: "I'm running a flask frontend and fast API backend on ports 8000 and 8080 on an ec2 server. I launched both with docker compose. I have access to Route 53. I would now like to make the frontend available at HTTPS at a top level domain (music-to-scrape.com) and the api fast api (originally port 8080) at api.music-to-scrape.com. How do I do that?"

### Step 1: Update Docker Compose

Modify your Docker Compose configuration to include the following labels for both the frontend and backend services:

```yaml
services:
  frontend:
    # ... your existing configuration ...
    labels:
      - "traefik.http.routers.frontend.rule=Host(`music-to-scrape.com`)"

  backend:
    # ... your existing configuration ...
    labels:
      - "traefik.http.routers.backend.rule=Host(`api.music-to-scrape.com`)"
```

### Step 2: Configure Route 53

In the Route 53 console, create 
- three A records pointing to your EC instance's public IP address, and
- three CAA records stating `0 issue "letsencrypt.org"`

Do this for the three subdomains:
- `music-to-scrape.com` 
- `api.music-to-scrape.com`
- `www.music-to-scrape.com`

### Step 3: Set Up Nginx as Reverse Proxy

SSH into your EC2 instance and install Nginx:

```bash
sudo apt update
sudo apt install nginx
```

Create Nginx server blocks for each domain:

```bash
sudo nano /etc/nginx/sites-available/music-to-scrape.com
```

Add the following configuration for `music-to-scrape.com`:

```nginx
server {
    listen 80;
    server_name music-to-scrape.com www.music-to-scrape.com;

    location / {
        proxy_pass http://localhost:8000;  # Your Flask frontend container
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Create a similar configuration for `api.music-to-scrape.com`:

```bash
sudo nano /etc/nginx/sites-available/api.music-to-scrape.com
```

Add the following configuration for `api.music-to-scrape.com`:

```nginx
server {
    listen 80;
    server_name api.music-to-scrape.com;

    location / {
        proxy_pass http://localhost:8080;  # Your FastAPI backend container
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the configurations and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/music-to-scrape.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api.music-to-scrape.com /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Obtain certificates for HTTPS

- Install `certbot`, following the instructions on [https://certbot.eff.org](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal).

After running `docker compose up`, your frontend should be accessible at `https://music-to-scrape.com`, and your FastAPI backend should be accessible at `https://api.music-to-scrape.com`.
