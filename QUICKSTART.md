# Geometry Vault API Quick Start

Get the Geometry Vault API running locally in minutes.

## Prerequisites

- Docker installed and running
- Port 8080 available

## Build and Run

### 1. Build the Container

```bash
docker build -t geometry-vault .
```

This creates a multi-service container with:
- Nginx (static frontend)
- FastAPI backend (Python)
- Supervisor (process manager)

Build time: 3-5 minutes on first run.

### 2. Start the Service

```bash
docker run -d -p 8080:80 --name geometry-vault geometry-vault
```

The service will be available at `http://localhost:8080`

### 3. Verify It's Running

Check the health endpoint:

```bash
curl http://localhost:8080/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "geometry-vault-api",
  "version": "1.0.0"
}
```

## Quick Test

### Generate Your First Specimen

SVG format:
```bash
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": "My First Specimen",
    "colors": "#8B1A1A, #2A2520, #7A7068",
    "format": "svg"
  }' \
  -o my_specimen.svg
```

PNG format:
```bash
curl "http://localhost:8080/api/generate?seed=Test&format=png" \
  -o specimen.png
```

### Run Test Suite

```bash
python3 tests/test_api.py
```

This will:
- Test all API endpoints
- Generate sample SVG and PNG files
- Display test results

## Access the Web Interface

Open your browser and navigate to:
```
http://localhost:8080
```

The interactive web UI will load with the synthesis engine.

## API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8080/api/docs`
- ReDoc: `http://localhost:8080/api/redoc`

## Container Management

### View Logs

```bash
# All logs
docker logs geometry-vault

# Follow logs
docker logs -f geometry-vault

# API logs only
docker exec geometry-vault tail -f /var/log/supervisor/api.log

# Nginx logs only
docker exec geometry-vault tail -f /var/log/supervisor/nginx.log
```

### Stop the Service

```bash
docker stop geometry-vault
```

### Start Again

```bash
docker start geometry-vault
```

### Remove Container

```bash
docker stop geometry-vault
docker rm geometry-vault
```

### Rebuild After Changes

```bash
docker stop geometry-vault
docker rm geometry-vault
docker build -t geometry-vault .
docker run -d -p 8080:80 --name geometry-vault geometry-vault
```

## Cloudflare Tunnel Integration

To expose the service to the internet via Cloudflare Tunnel:

```bash
# Install cloudflared
# https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation

# Start tunnel
cloudflared tunnel --url http://localhost:8080
```

Cloudflare will provide a public URL (e.g., `https://random-name.trycloudflare.com`)

## Troubleshooting

### Port Already in Use

Change the port mapping:
```bash
docker run -d -p 9090:80 --name geometry-vault geometry-vault
```

Then access via `http://localhost:9090`

### API Not Responding

Check if the API process is running:
```bash
docker exec geometry-vault ps aux | grep uvicorn
```

Restart the container:
```bash
docker restart geometry-vault
```

### PNG Generation Fails

Ensure cairosvg dependencies are installed. Check logs:
```bash
docker exec geometry-vault tail -100 /var/log/supervisor/api.err.log
```

### Container Won't Start

Check Docker logs:
```bash
docker logs geometry-vault
```

Verify Dockerfile syntax and rebuild.

## Production Deployment

For production use:

1. Use environment variables for configuration
2. Add SSL/TLS termination (via reverse proxy or Cloudflare)
3. Configure persistent logging
4. Set up monitoring and alerts
5. Implement backup strategies for any persistent data
6. Review rate limiting settings in `api/main.py`
7. Update CORS settings for your domain

## Next Steps

- Read `API_EXAMPLES.md` for integration examples
- Explore the API at `/api/docs`
- Customize the frontend in `index.html`
- Modify geometry parameters in `api/geometry.py`

## Support

For issues or questions:
- Check the logs first
- Review the API documentation at `/api/docs`
- Examine the source code in the `api/` directory
