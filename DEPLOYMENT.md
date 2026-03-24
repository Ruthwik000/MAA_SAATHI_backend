# VitalSync Backend - Deployment Guide

## Local Development

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload
```

Server: http://localhost:8000
Docs: http://localhost:8000/docs

---

## Production Deployment

### Option 1: Traditional Server (VPS/EC2)

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+
sudo apt install python3.10 python3-pip -y

# Clone repository
git clone <your-repo-url>
cd maa-saathi-backend
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure Environment
```bash
# Create .env file
nano .env

# Add:
FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccountKey.json
ENVIRONMENT=production
LOG_LEVEL=INFO
```

#### 4. Run with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 5. Setup Systemd Service
```bash
sudo nano /etc/systemd/system/vitalsync.service
```

Add:
```ini
[Unit]
Description=VitalSync Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/maa-saathi-backend
Environment="PATH=/home/ubuntu/maa-saathi-backend/venv/bin"
ExecStart=/home/ubuntu/maa-saathi-backend/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable vitalsync
sudo systemctl start vitalsync
sudo systemctl status vitalsync
```

#### 6. Setup Nginx Reverse Proxy
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/vitalsync
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/vitalsync /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 7. SSL with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

### Option 2: Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  vitalsync:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FIREBASE_CREDENTIALS_PATH=/app/serviceAccountKey.json
      - ENVIRONMENT=production
    volumes:
      - ./serviceAccountKey.json:/app/serviceAccountKey.json:ro
    restart: unless-stopped
```

#### 3. Deploy
```bash
docker-compose up -d
```

---

### Option 3: Cloud Platforms

#### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy vitalsync \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.10 vitalsync

# Create environment
eb create vitalsync-env

# Deploy
eb deploy
```

#### Heroku
```bash
# Create Procfile
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create vitalsync-backend
git push heroku main
```

#### Railway
```bash
# Add railway.json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE"
  }
}
```

---

## Environment Variables

Required for all deployments:

```env
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## Firebase Setup

1. Go to Firebase Console
2. Create/select project
3. Enable Firestore Database
4. Generate service account key
5. Add to deployment:
   - VPS: Upload to server
   - Docker: Mount as volume
   - Cloud: Add as secret/environment

---

## Security Checklist

- [ ] Use HTTPS in production
- [ ] Set up Firebase security rules
- [ ] Add authentication (JWT)
- [ ] Enable rate limiting
- [ ] Use environment variables for secrets
- [ ] Restrict CORS origins
- [ ] Enable firewall rules
- [ ] Regular security updates
- [ ] Monitor logs
- [ ] Backup Firestore data

---

## Monitoring

### Health Check
```bash
curl https://your-domain.com/health
```

### Logs
```bash
# Systemd
sudo journalctl -u vitalsync -f

# Docker
docker-compose logs -f

# Cloud platforms have built-in logging
```

---

## Performance Optimization

1. Use multiple workers:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. Enable caching (Redis)
3. Use CDN for static assets
4. Optimize Firestore queries
5. Enable compression

---

## Scaling

### Horizontal Scaling
- Add more server instances
- Use load balancer
- Firestore auto-scales

### Vertical Scaling
- Increase server resources
- More CPU/RAM
- Faster disk I/O

---

## Troubleshooting

### Port already in use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Firebase connection issues
- Check credentials path
- Verify Firestore is enabled
- Check network connectivity

### High memory usage
- Reduce worker count
- Optimize queries
- Add pagination

---

## Backup Strategy

### Firestore Backup
```bash
gcloud firestore export gs://your-bucket/backups
```

### Code Backup
- Use Git version control
- Regular commits
- Tag releases

---

## CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && git pull && systemctl restart vitalsync'
```

---

## Support

For issues:
1. Check logs
2. Verify Firebase connection
3. Test endpoints with curl
4. Review API documentation

---

**Deployment Status:** Ready for Production ✅
