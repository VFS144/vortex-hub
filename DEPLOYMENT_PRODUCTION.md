# 🚀 Production Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Generate secure JWT_SECRET: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] Set strong database passwords
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up WAF (Web Application Firewall)
- [ ] Enable database backups
- [ ] Review CORS_ORIGINS settings
- [ ] Disable DEBUG mode

### Infrastructure
- [ ] Set up PostgreSQL server (managed or self-hosted)
- [ ] Configure database connection pooling
- [ ] Set up monitoring (CPU, memory, disk)
- [ ] Configure logging aggregation
- [ ] Set up log rotation
- [ ] Configure backups
- [ ] Set up CDN for static assets

### Configuration
- [ ] Update `.env` with production values
- [ ] Set ENVIRONMENT=production
- [ ] Configure CORS_ORIGINS with your domain
- [ ] Set proper LOG_LEVEL
- [ ] Update VITE_API_URL and VITE_WS_URL

---

## Deployment Methods

### Option 1: Docker Compose (Recommended for small-medium)

#### Setup
```bash
# 1. Clone repository
git clone <repo> vortex-hub
cd vortex-hub

# 2. Create production .env file
cp .env.example .env
# Edit .env with production values

# 3. Build and start services
docker-compose -f docker-compose.prod.yml up -d

# 4. Check status
docker-compose -f docker-compose.prod.yml ps
```

#### Monitoring
```bash
# View logs
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f frontend

# Check health
curl http://localhost:8000/health
curl http://localhost/health
```

#### Updates
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up -d --build
```

---

### Option 2: Kubernetes (For scale)

#### Build Images
```bash
# Build backend image
docker build -t yourdomain/vortex-backend:1.0.0 ./backend
docker push yourdomain/vortex-backend:1.0.0

# Build frontend image
docker build -t yourdomain/vortex-frontend:1.0.0 ./frontend
docker push yourdomain/vortex-frontend:1.0.0
```

#### Deploy to Kubernetes
```bash
# Create namespace
kubectl create namespace vortex-hub

# Create secrets
kubectl create secret generic vortex-secrets \
  --from-literal=jwt_secret=YOUR_SECRET \
  --from-literal=db_password=YOUR_DB_PASSWORD \
  -n vortex-hub

# Apply manifests (create k8s/ directory with manifests)
kubectl apply -f k8s/ -n vortex-hub

# Check status
kubectl get pods -n vortex-hub
```

---

### Option 3: Cloud Platforms

#### AWS ECS
```bash
# Push to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin YOUR_ECR_URI

docker tag vortex-backend:1.0.0 YOUR_ECR_URI/vortex-backend:1.0.0
docker push YOUR_ECR_URI/vortex-backend:1.0.0
```

#### Google Cloud Run
```bash
# Backend
gcloud run deploy vortex-backend \
  --source . \
  --platform managed \
  --set-env-vars ENVIRONMENT=production
```

#### Heroku
```bash
# Login
heroku login

# Create app
heroku create vortex-hub

# Deploy
git push heroku main
```

---

## HTTPS/SSL Setup

### Using Let's Encrypt with Nginx

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Update nginx.conf with SSL configuration
# Restart nginx
sudo systemctl restart nginx
```

### Using AWS Certificate Manager
```bash
# Request certificate in ACM
# Attach to ALB
# Update VITE_API_URL to https://yourdomain.com
```

---

## Environment Configuration

### Production .env Template
```env
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING

# Database
DATABASE_URL=postgresql://prod_user:SECURE_PASSWORD@prod-db.example.com:5432/vortex_hub
DATABASE_POOL_SIZE=50
DATABASE_MAX_OVERFLOW=100

# JWT
JWT_SECRET=your-generated-secure-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
REFRESH_TOKEN_EXPIRATION=604800

# CORS
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Frontend URLs
VITE_API_URL=https://api.yourdomain.com
VITE_WS_URL=wss://api.yourdomain.com

# Database Credentials (for Docker)
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=SECURE_PASSWORD
POSTGRES_DB=vortex_hub
```

---

## Monitoring & Logging

### Health Checks
```bash
# Backend health
curl https://api.yourdomain.com/health

# Frontend health
curl https://yourdomain.com/health
```

### Logging Setup

#### With ELK Stack
```bash
# Elasticsearch, Logstash, Kibana
# Container logs are aggregated and searchable
```

#### With CloudWatch (AWS)
```bash
# Logs automatically sent to CloudWatch
# Set up alarms and dashboards
```

#### With Datadog
```bash
# Add Datadog agent
# Monitor performance and logs
```

---

## Backup Strategy

### Database Backups
```bash
# Daily automated backups
# Store in S3/Cloud Storage
# Test restore procedures monthly

# Manual backup
pg_dump -U prod_user -h prod-db.example.com vortex_hub > backup.sql

# Restore
psql -U prod_user -h prod-db.example.com vortex_hub < backup.sql
```

### Application Backups
```bash
# Backup uploaded files (if any)
# Version control with git
# Backup .env file separately (encrypted)
```

---

## Performance Optimization

### Frontend
- [ ] Enable gzip compression (done in nginx.conf)
- [ ] Minify CSS/JS (done in build)
- [ ] Configure CDN for assets
- [ ] Enable browser caching (done in nginx.conf)
- [ ] Use image optimization

### Backend
- [ ] Enable database connection pooling
- [ ] Configure query caching (Redis)
- [ ] Use database indexes
- [ ] Load test before production
- [ ] Set up rate limiting

### Infrastructure
- [ ] Use managed databases
- [ ] Configure auto-scaling
- [ ] Set up load balancing
- [ ] Use edge caching (CloudFlare)
- [ ] Monitor resource usage

---

## Scaling

### Horizontal Scaling
```bash
# Add more backend instances
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# Or in Kubernetes
kubectl scale deployment vortex-backend --replicas=3
```

### Database Scaling
- Read replicas for query scaling
- Connection pooling (PgBouncer)
- Partitioning for large tables

### Caching Layer
```bash
# Add Redis for caching
# Session storage
# Rate limiting
```

---

## Rollback Procedure

```bash
# If deployment goes wrong

# Check previous versions
docker images | grep vortex

# Rollback to previous image
docker-compose -f docker-compose.prod.yml pull vortex-backend:1.0.0
docker-compose -f docker-compose.prod.yml up -d

# Or with git
git checkout <previous-commit>
docker-compose -f docker-compose.prod.yml up -d --build
```

---

## Emergency Contacts & Runbooks

### Critical Issues
1. **Database Down** - Check logs, restart service
2. **Memory Leak** - Check application logs, restart container
3. **Disk Full** - Clean up logs, add storage
4. **High CPU** - Check for infinite loops, restart

### Support Escalation
- Level 1: Check logs and health endpoints
- Level 2: Restart services
- Level 3: Rollback to previous version
- Level 4: Contact development team

---

## Compliance & Security

### Data Protection
- [ ] GDPR compliance (if serving EU)
- [ ] Data encryption in transit (HTTPS)
- [ ] Data encryption at rest
- [ ] PII data handling procedures

### Access Control
- [ ] SSH key-based authentication only
- [ ] VPN for database access
- [ ] Role-based access control
- [ ] Audit logging

### Compliance Checks
```bash
# Run security scanner
docker run --rm -v $(pwd):/app trivy image yourdomain/vortex-backend:1.0.0

# Check dependencies
npm audit
pip audit
```

---

## Support & Debugging

### Production Logs
```bash
# Real-time logs
docker-compose -f docker-compose.prod.yml logs -f

# Historical logs
docker-compose -f docker-compose.prod.yml logs --since 1h
```

### Database Access
```bash
# Connect to production database
psql postgresql://prod_user@prod-db.example.com:5432/vortex_hub

# Check status
SELECT version();
SELECT count(*) FROM users;
```

### API Testing
```bash
# Test API endpoint
curl -X GET https://api.yourdomain.com/health

# With authentication
curl -X GET https://api.yourdomain.com/api/projects \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Checklist for Go-Live

- [ ] All environment variables configured
- [ ] Database backed up
- [ ] SSL certificates installed
- [ ] Health checks passing
- [ ] Monitoring and alerts enabled
- [ ] Logging set up
- [ ] Backups automated
- [ ] Team trained on deployment
- [ ] Rollback procedure documented
- [ ] Incident response plan ready
- [ ] Load testing completed
- [ ] Security audit passed

---

**Status**: ✅ DEPLOYMENT READY

Once complete, Vortex Hub will be production-grade with:
- ✅ Optimized Docker images
- ✅ Security best practices
- ✅ Monitoring & logging
- ✅ Backup & recovery
- ✅ Auto-scaling ready
- ✅ High availability setup

**Next Step**: Follow the deployment method for your infrastructure!
