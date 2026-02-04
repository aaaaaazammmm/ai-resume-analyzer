# 🚀 Deployment Guide

## Table of Contents
- [Local Deployment](#local-deployment)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)

## Local Deployment

### Quick Start (5 minutes)

1. **Install Python 3.9+**
```bash
python --version  # Should be 3.9 or higher
```

2. **Clone and Setup**
```bash
cd resume_matcher
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
nano .env  # or use any text editor
```

4. **Test Installation**
```bash
python test_setup.py
```

5. **Run Backend**
```bash
# Terminal 1
python -m backend.main
```

6. **Run Frontend**
```bash
# Terminal 2
streamlit run frontend/app.py
```

7. **Access Application**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Development Setup

### VS Code Setup

1. **Install Extensions**
   - Python
   - Pylance
   - Python Docstring Generator

2. **Configure `.vscode/settings.json`**
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "[python]": {
        "editor.tabSize": 4
    }
}
```

3. **Launch Configuration** `.vscode/launch.json`
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Backend",
            "type": "python",
            "request": "launch",
            "module": "backend.main",
            "console": "integratedTerminal"
        },
        {
            "name": "Frontend",
            "type": "python",
            "request": "launch",
            "module": "streamlit",
            "args": ["run", "frontend/app.py"],
            "console": "integratedTerminal"
        }
    ]
}
```

### Hot Reload

Both FastAPI and Streamlit support hot reload:
- **FastAPI**: Automatically reloads on code changes
- **Streamlit**: Press 'R' or select "Rerun" to refresh

## Production Deployment

### Prerequisites
- Ubuntu 20.04+ server
- 2GB+ RAM
- Python 3.9+
- Nginx
- Domain name (optional)

### Step-by-Step Production Setup

#### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.9 python3-pip python3-venv nginx supervisor

# Create application user
sudo useradd -m -s /bin/bash resumeapp
sudo su - resumeapp
```

#### 2. Application Setup
```bash
# Clone repository
git clone <your-repo-url> /home/resumeapp/app
cd /home/resumeapp/app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add production API keys
```

#### 3. Supervisor Configuration

Create `/etc/supervisor/conf.d/resume-backend.conf`:
```ini
[program:resume-backend]
command=/home/resumeapp/app/venv/bin/python -m backend.main
directory=/home/resumeapp/app
user=resumeapp
autostart=true
autorestart=true
stderr_logfile=/var/log/resume-backend.err.log
stdout_logfile=/var/log/resume-backend.out.log
environment=PATH="/home/resumeapp/app/venv/bin"
```

Create `/etc/supervisor/conf.d/resume-frontend.conf`:
```ini
[program:resume-frontend]
command=/home/resumeapp/app/venv/bin/streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0
directory=/home/resumeapp/app
user=resumeapp
autostart=true
autorestart=true
stderr_logfile=/var/log/resume-frontend.err.log
stdout_logfile=/var/log/resume-frontend.out.log
environment=PATH="/home/resumeapp/app/venv/bin"
```

Start services:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start resume-backend
sudo supervisorctl start resume-frontend
```

#### 4. Nginx Configuration

Create `/etc/nginx/sites-available/resume-analyzer`:
```nginx
upstream backend {
    server 127.0.0.1:8000;
}

upstream frontend {
    server 127.0.0.1:8501;
}

server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    # Increase buffer sizes for large PDFs
    client_max_body_size 10M;

    # Backend API
    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Frontend
    location / {
        proxy_pass http://frontend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Streamlit WebSocket
    location /_stcore/stream {
        proxy_pass http://frontend/_stcore/stream;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/resume-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

#### 6. Firewall
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

## Docker Deployment

### Dockerfile
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose ports
EXPOSE 8000 8501

# Create startup script
RUN echo '#!/bin/bash\n\
python -m backend.main &\n\
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]
```

### Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
      - LLM_MODEL=gpt-3.5-turbo
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### Usage
```bash
# Build
docker-compose build

# Run
docker-compose up -d

# Logs
docker-compose logs -f

# Stop
docker-compose down
```

## Cloud Deployment

### AWS EC2

1. **Launch Instance**
   - AMI: Ubuntu 20.04
   - Instance Type: t2.medium (2GB RAM minimum)
   - Storage: 20GB
   - Security Group: Allow ports 22, 80, 443, 8000, 8501

2. **Connect and Setup**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Follow Production Setup** above

4. **Use Elastic IP** for persistent IP address

### Google Cloud Platform

1. **Create VM**
```bash
gcloud compute instances create resume-analyzer \
    --machine-type=e2-medium \
    --image-family=ubuntu-2004-lts \
    --image-project=ubuntu-os-cloud \
    --boot-disk-size=20GB
```

2. **SSH and Setup**
```bash
gcloud compute ssh resume-analyzer
```

3. **Follow Production Setup**

### Heroku

1. **Create `Procfile`**
```
web: python -m backend.main & streamlit run frontend/app.py --server.port=$PORT
```

2. **Deploy**
```bash
heroku create resume-analyzer
heroku config:set OPENAI_API_KEY=your-key
git push heroku main
```

### DigitalOcean

1. **Create Droplet**
   - Image: Ubuntu 20.04
   - Size: Basic $12/month (2GB RAM)
   - Datacenter: Closest to users

2. **Follow Production Setup**

## Performance Optimization

### 1. Caching
Add Redis for caching:
```bash
pip install redis
```

### 2. Load Balancing
Use multiple workers:
```bash
uvicorn backend.main:app --workers 4 --host 0.0.0.0 --port 8000
```

### 3. CDN
Use CloudFlare for static assets

### 4. Database
For user data, add PostgreSQL:
```bash
pip install psycopg2-binary
```

## Monitoring

### Logging
```bash
# View logs
sudo tail -f /var/log/resume-backend.out.log
sudo tail -f /var/log/resume-frontend.out.log
```

### Health Checks
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:8501/_stcore/health
```

### Monitoring Tools
- **Prometheus**: Metrics collection
- **Grafana**: Visualization
- **Sentry**: Error tracking
- **New Relic**: Performance monitoring

## Backup

```bash
# Backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf backup-$DATE.tar.gz /home/resumeapp/app
aws s3 cp backup-$DATE.tar.gz s3://your-bucket/backups/
```

## Scaling

### Horizontal Scaling
1. Set up load balancer
2. Deploy multiple instances
3. Use shared Redis for state
4. Centralized logging

### Vertical Scaling
- Increase instance size
- Add GPU for faster embeddings
- Optimize chunk sizes

## Security Checklist

- [ ] Change default passwords
- [ ] Enable firewall
- [ ] Install SSL certificate
- [ ] Set up fail2ban
- [ ] Regular updates
- [ ] API rate limiting
- [ ] Input validation
- [ ] Secure file uploads
- [ ] Environment variables (no hardcoded keys)
- [ ] Regular backups

## Troubleshooting

### Port Already in Use
```bash
# Find process
sudo lsof -i :8000
sudo lsof -i :8501

# Kill process
kill -9 <PID>
```

### Permission Denied
```bash
sudo chown -R resumeapp:resumeapp /home/resumeapp/app
```

### Out of Memory
```bash
# Increase swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## Maintenance

### Update Application
```bash
cd /home/resumeapp/app
git pull
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart resume-backend resume-frontend
```

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

## Cost Estimation

### AWS EC2 (t2.medium)
- Instance: ~$34/month
- Storage: ~$2/month
- Data Transfer: ~$10/month
- **Total: ~$46/month**

### DigitalOcean
- Droplet: $12/month
- Backups: $2/month
- **Total: ~$14/month**

### Heroku
- Dyno: $25/month
- **Total: ~$25/month**

### API Costs (OpenAI)
- GPT-3.5-turbo: $0.002 per 1K tokens
- Average request: ~2K tokens = $0.004
- 1000 requests: ~$4/month

---

**Choose the deployment method that best fits your needs and budget!**
