# Vortex Hub - Pre/Post Deployment Checklist

## Pre-Deployment Checklist (48 Hours Before)

### Code Review & Quality
- [ ] All tests pass locally (`./scripts/test.sh`)
- [ ] Code coverage meets minimum (Backend: 80%, Frontend: 70%)
- [ ] Linting passes without errors
- [ ] No security vulnerabilities detected
- [ ] No console errors or warnings
- [ ] Git repository is clean (no uncommitted changes)

### Environment Setup
- [ ] `.env` file exists and is properly configured
- [ ] All required environment variables are set
- [ ] Database URL is correct
- [ ] JWT_SECRET is strong and unique (minimum 32 characters)
- [ ] DEBUG is set to `false`
- [ ] ENVIRONMENT is set to `production`

### Database
- [ ] Latest backup exists
- [ ] Database schema is current
- [ ] Database user has appropriate permissions
- [ ] Connection pooling is configured
- [ ] No pending migrations

### Documentation
- [ ] README.md is up to date
- [ ] API documentation is current
- [ ] Deployment steps are documented
- [ ] Rollback procedure is documented
- [ ] Known issues are documented

### Team Notification
- [ ] Team is notified of deployment date/time
- [ ] Stakeholders are aware of any downtime
- [ ] On-call person is assigned
- [ ] Communication channel is established

---

## Pre-Deployment Checklist (24 Hours Before)

### Final Testing
- [ ] Full test suite passes
- [ ] Smoke tests pass on staging
- [ ] Performance tests show acceptable metrics
- [ ] Security scan passes
- [ ] Database backup successful

### Configuration Validation
- [ ] CORS origins are restricted to production domain
- [ ] API endpoints are correct
- [ ] Asset paths are correct
- [ ] Email templates are correct
- [ ] Error messages are appropriate

### Infrastructure
- [ ] Server has adequate disk space (>20GB free)
- [ ] Server has adequate memory (>8GB)
- [ ] Docker resources are properly allocated
- [ ] Network connectivity is verified
- [ ] DNS is properly configured

### Monitoring
- [ ] Monitoring tools are configured
- [ ] Alerting is enabled
- [ ] Log aggregation is working
- [ ] Health check endpoints are configured
- [ ] Dashboards are ready

---

## Pre-Deployment Checklist (1 Hour Before)

### Final Verification
```bash
# Run final checks
cd backend && pytest tests/ -q
cd ../frontend && npm run lint
cd ..

# Verify Docker images
docker-compose -f docker-compose.prod.yml config

# Check current resource usage
free -h
df -h
```

- [ ] Backend tests pass
- [ ] Frontend linting passes
- [ ] Docker compose config is valid
- [ ] Server resources are available
- [ ] Backup is recent and verified

### Service Status
```bash
# Verify current services
docker-compose -f docker-compose.prod.yml ps

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs --tail=50 | grep ERROR
```

- [ ] All current services are healthy
- [ ] No recent error messages
- [ ] Traffic is at expected levels
- [ ] Database is responsive

### Communication
- [ ] Final notification sent to team
- [ ] Status page updated (if applicable)
- [ ] Support team is on standby
- [ ] Incident response plan is activated

---

## Deployment Checklist

### Pre-Deployment
- [ ] Stop accepting new requests (if needed)
- [ ] Notify users of maintenance window
- [ ] Create backup
- [ ] Document current state

### Deployment
```bash
# Pull latest code
git pull origin main

# Build images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Monitor
docker-compose -f docker-compose.prod.yml logs -f
```

- [ ] Code is pulled from main branch
- [ ] Docker images are built successfully
- [ ] Services are started
- [ ] Services are responding
- [ ] All health checks pass

### Post-Deployment Verification
```bash
# Check services
docker-compose -f docker-compose.prod.yml ps

# Test endpoints
curl http://localhost:8000/health
curl http://localhost/

# Check logs for errors
docker-compose -f docker-compose.prod.yml logs backend
docker-compose -f docker-compose.prod.yml logs frontend
```

- [ ] Backend is running
- [ ] Frontend is running
- [ ] Database is running
- [ ] Health endpoints return 200
- [ ] No error messages in logs

---

## Post-Deployment Checklist (Immediate - 1 Hour)

### Functionality Verification
- [ ] Homepage loads
- [ ] Login page loads
- [ ] User can log in
- [ ] Dashboard loads
- [ ] Projects page loads
- [ ] Tasks page loads
- [ ] Bugs page loads
- [ ] Lore page loads
- [ ] API documentation (/docs) loads

### Error Monitoring
```bash
# Check error logs
docker-compose -f docker-compose.prod.yml logs backend | grep ERROR
docker-compose -f docker-compose.prod.yml logs frontend | grep ERROR

# Check database logs
docker-compose -f docker-compose.prod.yml logs postgres | grep ERROR
```

- [ ] No errors in backend logs
- [ ] No errors in frontend logs
- [ ] No database errors
- [ ] No JavaScript errors in browser console

### Performance Baseline
```bash
# Measure response times
time curl http://localhost:8000/health
time curl http://localhost/

# Check system resources
top
free -h
df -h
```

- [ ] Response times are acceptable
- [ ] CPU usage is normal
- [ ] Memory usage is normal
- [ ] Disk usage is normal

### Database Verification
```bash
# Verify database connectivity
docker-compose -f docker-compose.prod.yml exec postgres psql -U vortex_user -d vortex_hub -c "SELECT COUNT(*) FROM users;"

# Check recent queries
docker-compose -f docker-compose.prod.yml logs postgres | tail -20
```

- [ ] Database is accessible
- [ ] Data is intact
- [ ] Recent queries are successful
- [ ] No locked tables

---

## Post-Deployment Checklist (Short-term - 4 Hours)

### Extended Monitoring
- [ ] Monitor error rates (target: <0.1%)
- [ ] Monitor response times (target: <500ms)
- [ ] Monitor CPU usage (target: <70%)
- [ ] Monitor memory usage (target: <80%)
- [ ] Monitor disk usage (target: <85%)

### User Testing
- [ ] Internal team tests all features
- [ ] Beta users report no issues
- [ ] Support queue is normal
- [ ] Error tracking shows no new issues

### Performance Testing
```bash
# Load test
ab -n 1000 -c 10 http://localhost:8000/

# Check database performance
docker-compose -f docker-compose.prod.yml exec postgres psql -U vortex_user -d vortex_hub -c "\timing" -c "SELECT * FROM projects WHERE user_id = 1;"
```

- [ ] Load test passes
- [ ] Query performance is acceptable
- [ ] No timeouts
- [ ] No connection pool exhaustion

---

## Post-Deployment Checklist (Long-term - 24 Hours)

### Stability Verification
- [ ] System has been running for 24 hours without restart
- [ ] Error rate is within acceptable limits
- [ ] Performance metrics are stable
- [ ] No memory leaks detected
- [ ] Database is performing well

### Data Integrity
```bash
# Run data integrity checks
docker-compose -f docker-compose.prod.yml exec postgres psql -U vortex_user -d vortex_hub -c "SELECT COUNT(*) FROM users; SELECT COUNT(*) FROM projects; SELECT COUNT(*) FROM tasks;"
```

- [ ] Row counts are as expected
- [ ] No orphaned records
- [ ] Foreign keys are valid
- [ ] Indexes are working

### Backup Verification
```bash
# Test restore from backup
backup_file="backup_$(date +%Y%m%d).sql"
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U vortex_user vortex_hub > $backup_file
```

- [ ] Backup was created
- [ ] Backup can be restored
- [ ] Backup size is reasonable

---

## Rollback Checklist

If deployment fails or issues are discovered:

### Decision to Rollback
- [ ] Issue is critical or impacts users
- [ ] Issue cannot be fixed within 1 hour
- [ ] Issue causes data loss or corruption
- [ ] Issue causes service outage

### Rollback Process
```bash
# Stop current services
docker-compose -f docker-compose.prod.yml down

# Restore previous version
git revert HEAD
# or
docker tag vortex-hub-backend:v1.0.0 vortex-hub-backend:latest
docker tag vortex-hub-frontend:v1.0.0 vortex-hub-frontend:latest

# Start services with previous version
docker-compose -f docker-compose.prod.yml up -d

# Verify
docker-compose -f docker-compose.prod.yml ps
curl http://localhost:8000/health
```

- [ ] Previous version is deployed
- [ ] Services are running
- [ ] Health checks pass
- [ ] Data is intact
- [ ] Backups are verified

### Post-Rollback
- [ ] Team is notified
- [ ] Root cause analysis is started
- [ ] Issue is documented
- [ ] New attempt is scheduled

---

## Emergency Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| DevOps Lead | | | |
| Backend Lead | | | |
| Frontend Lead | | | |
| Database Admin | | | |
| Support Lead | | | |

---

## Deployment Notes

### This Deployment (Date: _____)
- **Version**: _____
- **Release Notes**: _____
- **Changes**: _____
- **Known Issues**: _____
- **Rollback Plan**: _____

### Previous Deployment (Date: _____)
- **Version**: _____
- **Status**: Success / Failed
- **Issues**: _____
- **Resolution**: _____

---

## Sign-off

- [ ] Deployment Lead: _________________ Date: _____
- [ ] QA Lead: _________________ Date: _____
- [ ] DevOps Lead: _________________ Date: _____
- [ ] Product Manager: _________________ Date: _____

Last Updated: May 31, 2026
