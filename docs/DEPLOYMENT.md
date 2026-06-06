"""
Deployment guide for production
"""

# Vortex Hub Production Deployment Guide

## Pre-Deployment Checklist

### Security
- [ ] Change all default passwords
- [ ] Set strong JWT secret
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS for production domains
- [ ] Set secure cookie flags
- [ ] Review environment variables

### Database
- [ ] Set strong PostgreSQL password
- [ ] Configure backups
- [ ] Test restore process
- [ ] Set up monitoring
- [ ] Configure connection pooling

### Code
- [ ] Run tests
- [ ] Run security audits (`npm audit`, `pip audit`)
- [ ] Build production bundle
- [ ] Test in staging environment

## Environment Variables

Create `.env` with production values:

```bash
# Database
DATABASE_URL=postgresql://prod_user:STRONG_PASSWORD@db.example.com:5432/vortex_hub_prod

# JWT
JWT_SECRET=generate-with: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
REFRESH_TOKEN_EXPIRATION=604800

# Frontend
VITE_API_URL=https://api.vortexhub.com
VITE_WS_URL=wss://api.vortexhub.com

# Debug
DEBUG=false

# CORS
CORS_ORIGINS=["https://vortexhub.com", "https://www.vortexhub.com"]
```

## Deployment Options

### Option 1: Docker on VPS

```bash
# SSH into server
ssh user@server.com

# Clone repository
git clone https://github.com/vortexframe/vortex-hub.git
cd vortex-hub

# Create .env with production values
nano .env

# Build images
docker-compose -f docker-compose.yml build

# Start services
docker-compose -f docker-compose.yml up -d

# Verify services
docker-compose ps
docker-compose logs -f
```

### Option 2: Cloud Platforms

#### AWS
- **Compute**: EC2 or ECS Fargate
- **Database**: RDS PostgreSQL
- **Storage**: S3 for assets
- **CDN**: CloudFront
- **Domain**: Route 53

#### DigitalOcean
- **Compute**: Droplets
- **Database**: Managed PostgreSQL
- **App Platform**: App Platform for containerized deployment
- **Spaces**: Object storage

#### Heroku
```bash
# Create app
heroku create vortex-hub

# Set environment variables
heroku config:set JWT_SECRET=xxx

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

```nginx
server {
    listen 443 ssl http2;
    server_name api.vortexhub.com;
    
    ssl_certificate /etc/letsencrypt/live/api.vortexhub.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.vortexhub.com/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name api.vortexhub.com;
    return 301 https://$server_name$request_uri;
}
```

## Scaling Considerations

### Horizontal Scaling
```bash
# Run multiple backend instances behind load balancer
docker-compose up -d --scale backend=3

# Use Nginx as load balancer
upstream backend {
    server backend:8000;
    server backend_2:8001;
    server backend_3:8002;
}
```

### Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_tasks_project_id ON tasks(project_id);
CREATE INDEX idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX idx_bugs_project_id ON bugs(project_id);
CREATE INDEX idx_bugs_severity ON bugs(severity);

-- Configure connection pooling
-- Use pgBouncer or similar
```

## Monitoring & Alerting

### Application Monitoring
```bash
# Install monitoring stack (optional)
# Prometheus + Grafana + Loki

# Monitor endpoints
GET /health

# Monitor logs
docker-compose logs -f --tail=100
```

### Error Tracking
Consider integrating:
- Sentry (error tracking)
- DataDog (monitoring)
- New Relic (APM)

## Backup Strategy

### Automated Backups
```bash
#!/bin/bash
# backup.sh
BACKUP_DIR="/backups/vortex-hub"
DB_NAME="vortex_hub"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
pg_dump -h localhost -U vortex_user $DB_NAME | \
  gzip > $BACKUP_DIR/db_backup_$DATE.sql.gz

# Keep only last 30 days
find $BACKUP_DIR -name "db_backup_*.sql.gz" -mtime +30 -delete
```

Schedule with cron:
```bash
# Daily backups at 2 AM
0 2 * * * /path/to/backup.sh
```

## Updates & Maintenance

### Zero-Downtime Updates
```bash
# 1. Build new images
docker-compose build

# 2. Stop old backend, start new
docker-compose up -d --no-deps --build backend

# 3. Run migrations if needed
docker-compose exec backend python -m alembic upgrade head

# 4. Update frontend
docker-compose up -d --no-deps --build frontend
```

## Performance Tuning

### Database Optimization
```python
# Lazy load relationships
task = db.query(Task).options(
    joinedload(Task.assigned_user)
).first()

# Use pagination
offset = (page - 1) * limit
tasks = db.query(Task).offset(offset).limit(limit).all()
```

### Frontend Optimization
```typescript
// Lazy load routes
const ProjectsPage = lazy(() => import('./pages/ProjectsPage'))

// Code splitting
const ProjectDetail = lazy(() => import('./components/ProjectDetail'))
```

## Rollback Procedure

```bash
# Keep previous image version
docker tag vortex-hub:latest vortex-hub:previous

# If issues occur, rollback
docker-compose down
docker-compose up -d  # Uses previous image
```

## Production Checklist

### Pre-Launch
- [ ] Database backed up
- [ ] Monitoring configured
- [ ] Logging enabled
- [ ] SSL certificates valid
- [ ] Load testing completed
- [ ] Security scan passed
- [ ] Documentation updated

### Launch
- [ ] Gradual rollout (5% → 25% → 100%)
- [ ] Monitor error rates
- [ ] Monitor performance
- [ ] Check database performance
- [ ] Verify all features working

### Post-Launch
- [ ] Monitor metrics
- [ ] Collect user feedback
- [ ] Track performance
- [ ] Plan next updates

## Support & Troubleshooting

### Common Issues

**High CPU Usage**
```bash
# Check processes
docker stats

# Profile application
docker-compose exec backend python -m cProfile -o stats.prof app/main.py
```

**Database Connection Issues**
```bash
# Check connection pool
docker-compose exec backend redis-cli info
docker-compose logs postgres
```

**Memory Leaks**
```bash
# Monitor memory
docker stats --no-stream

# Profile memory usage
docker-compose exec backend python -m memory_profiler
```

## Contact & Support

For deployment issues:
1. Check logs: `docker-compose logs`
2. Review monitoring dashboards
3. Consult documentation
4. Create issue with details

---

**Last Updated**: 2024
