# Docker Build and Test Plan

Comprehensive testing procedure for the Geometry Vault Docker container.

## Current Status

**Network Issue:** Docker build currently failing with DNS resolution errors for `deb.debian.org`. This is a temporary network/DNS problem, not a code issue.

## Prerequisites

- Docker installed and running
- Stable internet connection
- Port 8080 available
- Python 3.x (for test scripts)
- curl (for API testing)

## Build Instructions

### Step 1: Build the Image

```bash
cd /home/azzar/project/geometry-vault
docker build -t geometry-vault .
```

**Expected time:** 5-10 minutes (first build)

**What it does:**
- Multi-stage build (builder + runtime)
- Installs Python dependencies in builder stage
- Sets up nginx + FastAPI + supervisord in runtime
- Configures reverse proxy for API endpoints

### Step 2: Run the Container

```bash
docker run -d -p 8080:80 --name geometry-vault geometry-vault
```

**Container includes:**
- Nginx (static frontend + reverse proxy)
- FastAPI backend on port 8000 (internal)
- Supervisord managing both services

### Step 3: Wait for Services to Start

```bash
# Wait 10 seconds for services to initialize
sleep 10

# Check container is running
docker ps | grep geometry-vault

# Check logs
docker logs geometry-vault
```

## Test Suite

### Test 1: Container Health Check

```bash
# Check both services are running inside container
docker exec geometry-vault ps aux | grep -E "nginx|uvicorn"
```

**Expected output:**
```
root         1  0.0  0.0  ...  /usr/bin/supervisord
root        10  0.0  0.0  ...  nginx: master process
www-data    11  0.0  0.0  ...  nginx: worker process
root        12  0.5  1.5  ...  uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### Test 2: Frontend Access

```bash
# Test static frontend
curl -I http://localhost:8080/

# Should return 200 OK
# Content-Type: text/html
```

```bash
# Test PWA manifest
curl http://localhost:8080/manifest.json

# Should return JSON with app manifest
```

### Test 3: API Health Check

```bash
# Test API health endpoint
curl http://localhost:8080/api/health

# Expected output:
# {"status":"healthy","service":"geometry-vault-api","version":"1.0.0"}
```

### Test 4: API Preview Endpoint

```bash
# Test preview endpoint
curl "http://localhost:8080/api/preview?seed=Docker%20Test&colors=%238B1A1A,%20%232A2520"

# Expected: JSON with sequence_id, hash, svg_base64
```

### Test 5: SVG Generation

```bash
# Generate SVG
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": "Docker Build Test",
    "colors": "#8B1A1A, #2A2520, #7A7068",
    "ratio_w": 1,
    "ratio_h": 1,
    "format": "svg"
  }' \
  -o /tmp/docker_test.svg

# Verify file was created
ls -lh /tmp/docker_test.svg

# Check it's valid SVG
head -5 /tmp/docker_test.svg
```

**Expected:**
```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" style="aspect-ratio: 1/1;">
    <rect width="100" height="100" fill="transparent"/>
    ...
```

### Test 6: PNG Generation

```bash
# Generate PNG
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": "PNG Test",
    "colors": "#8B1A1A, #2A2520",
    "ratio_w": 16,
    "ratio_h": 9,
    "format": "png",
    "scale": 2400
  }' \
  -o /tmp/docker_test.png

# Verify PNG file
file /tmp/docker_test.png

# Expected: /tmp/docker_test.png: PNG image data
```

### Test 7: Rate Limiting

```bash
# Test rate limiting (20 req/min)
for i in {1..25}; do
  echo "Request $i:"
  curl -s -o /dev/null -w "%{http_code}\n" \
    "http://localhost:8080/api/preview?seed=RateTest$i"
  sleep 0.1
done

# Expected: First 20 return 200, subsequent return 429 (rate limited)
```

### Test 8: Automated Python Tests

```bash
# Run verification script (requires Python)
python3 verify_parity.py

# Expected: 5/5 tests pass
```

```bash
# Run API test suite
python3 test_api.py

# Expected: All 4 tests pass (health, preview, SVG, PNG)
```

### Test 9: Browser Tests

Open these URLs in browser:

1. **Main UI:** `http://localhost:8080/`
   - Enter seed: "Browser Test"
   - Verify geometry renders
   - Check sequence ID appears

2. **Parity Test:** `http://localhost:8080/test_js_parity.html`
   - Should auto-run all tests
   - Verify all tests pass (green checkmarks)

3. **API Docs:** `http://localhost:8080/api/docs`
   - Interactive Swagger UI
   - Try "Execute" on /api/health endpoint

4. **Embed Mode:** `http://localhost:8080/?mode=embed&seed=Embed%20Test`
   - Should show minimal view (no UI controls)
   - Only geometry visible

### Test 10: JS/Python Parity Verification

```bash
# Generate from UI (use browser console)
# Open http://localhost:8080
# In console, type:
# generateSecureHash("Parity Test")

# Generate from API
curl "http://localhost:8080/api/preview?seed=Parity%20Test" | jq '.hash'

# Both should return identical hash value
```

### Test 11: Container Logs

```bash
# Check API logs
docker exec geometry-vault tail -50 /var/log/supervisor/api.log

# Check nginx logs
docker exec geometry-vault tail -50 /var/log/supervisor/nginx.log

# Check error logs
docker exec geometry-vault tail -50 /var/log/supervisor/api.err.log
```

### Test 12: Performance Test

```bash
# Quick load test (requires apache-bench or similar)
ab -n 100 -c 10 "http://localhost:8080/api/health"

# Or simple bash loop
time for i in {1..50}; do
  curl -s "http://localhost:8080/api/health" > /dev/null
done

# Should complete in reasonable time (< 10s for 50 requests)
```

## Expected Results Summary

| Test | Status | Details |
|------|--------|---------|
| Container runs | ✓ | Supervisord managing 2 services |
| Frontend loads | ✓ | HTML + JS + CSS served |
| API health | ✓ | Returns healthy status |
| SVG generation | ✓ | Valid SVG output |
| PNG generation | ✓ | Valid PNG image |
| Rate limiting | ✓ | 429 after limit |
| JS/Python parity | ✓ | Identical hashes |
| Browser UI | ✓ | Interactive geometry tool |
| API docs | ✓ | Swagger UI accessible |
| Logs clean | ✓ | No critical errors |

## Troubleshooting

### Container won't start
```bash
# Check logs
docker logs geometry-vault

# Check supervisord status
docker exec geometry-vault supervisorctl status

# Restart services
docker exec geometry-vault supervisorctl restart all
```

### API not responding
```bash
# Check if uvicorn is running
docker exec geometry-vault ps aux | grep uvicorn

# Check API logs for errors
docker exec geometry-vault tail -100 /var/log/supervisor/api.err.log

# Restart API only
docker exec geometry-vault supervisorctl restart api
```

### PNG generation fails
```bash
# Check cairosvg is installed
docker exec geometry-vault python3 -c "import cairosvg; print('OK')"

# Check dependencies
docker exec geometry-vault pip list | grep -E "(cairo|Pillow)"
```

### Port already in use
```bash
# Use different port
docker stop geometry-vault && docker rm geometry-vault
docker run -d -p 9090:80 --name geometry-vault geometry-vault

# Access via http://localhost:9090
```

## Cleanup

```bash
# Stop container
docker stop geometry-vault

# Remove container
docker rm geometry-vault

# Remove image (optional)
docker rmi geometry-vault

# Remove test files
rm /tmp/docker_test.svg /tmp/docker_test.png
```

## Performance Benchmarks

Expected performance on average hardware:

- **Container start time:** 5-10 seconds
- **SVG generation:** < 100ms
- **PNG generation:** 200-500ms (depends on scale)
- **API health check:** < 10ms
- **Container size:** ~400MB (compressed)
- **Memory usage:** ~150MB (idle), ~250MB (under load)
- **CPU usage:** < 5% (idle), 20-40% (generating)

## Security Checks

```bash
# Check no exposed secrets
docker exec geometry-vault env | grep -i pass

# Verify non-root processes
docker exec geometry-vault ps aux | grep nginx

# Check file permissions
docker exec geometry-vault ls -la /app/api/

# Verify rate limiting works
# (See Test 7 above)
```

## CI/CD Integration

For automated testing in CI pipelines:

```bash
#!/bin/bash
set -e

# Build
docker build -t geometry-vault:test .

# Run
docker run -d -p 8080:80 --name gv-test geometry-vault:test

# Wait for startup
sleep 10

# Test health
curl -f http://localhost:8080/api/health || exit 1

# Test generation
curl -f -X POST http://localhost:8080/api/generate \
  -H "Content-Type: application/json" \
  -d '{"seed":"CI Test","format":"svg"}' \
  -o /tmp/ci_test.svg || exit 1

# Verify SVG
grep -q "viewBox" /tmp/ci_test.svg || exit 1

# Cleanup
docker stop gv-test && docker rm gv-test

echo "All CI tests passed!"
```

## Next Steps

Once build succeeds:

1. Run all tests sequentially
2. Document any failures
3. Test with real workloads
4. Deploy to staging/production
5. Set up monitoring and alerts

## Support

For issues:
1. Check logs first
2. Verify all tests pass
3. Review error messages in supervisord logs
4. Check GitHub issues for similar problems
