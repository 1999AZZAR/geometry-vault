# Geometry Vault: Specimen Vault

The Geometry Vault Specimen Vault is a high-end digital synthesis engine and archival repository designed for technical minimalism and structural honesty. It facilitates the generation, visualization, and preservation of procedural geometry specimens based on narrative input sequences.

## Architectural Principles

The system is built on the Swiss-Archival design system, emphasizing three core pillars:
1. **Technical Minimalism:** A focus on structural clarity and the removal of ornamental redundancy.
2. **Structural Honesty:** Visible blueprint grids and technical metadata as primary aesthetic elements.
3. **Physicality:** Use of fractal noise filters and specific typographic choices to mimic 300gsm matte-printed archival media.

## Technical Stack

- **Frontend:** HTML5, Vanilla CSS, Tailwind CSS (Utility layer), JavaScript (ES6+).
- **Engine:** Procedural geometry generation via SVG path synthesis and secure hashing.
- **Deployment:** Docker (Nginx/Alpine), Cloudflare Tunnel.
- **Optimization:** Hyper-SEO & AIO (AI Optimization) via JSON-LD Knowledge Graph and passage indexing compliance.

## Service Features

### 1. Archival Synthesis
The engine utilizes a secure hashing algorithm to transform narrative strings into deterministic geometric parameters, including core symmetry, layer depth, and orbital complexity.

### 2. Embeddable Architecture
The system functions as a standalone service supporting:
- **URL Parameter Syncing:** Real-time state persistence via browser address bar.
- **Embed Mode:** Minimalist view for iframe integration (`?mode=embed`).
- **PostMessage API:** External control interface for parent-window coordination.

### 3. Interaction Engine
- **Custom Cursor:** Hardware-accelerated tactile trailing effect using `translate3d`.
- **Export Protocol:** High-resolution SVG and PNG export capabilities with embedded archival identifiers.

### 4. Progressive Web App (PWA)
The system is a fully compliant PWA, providing:
- **Offline Capability:** Service worker caching for core assets and external CDNs.
- **Installability:** Web App Manifest for home-screen integration on mobile and desktop.
- **Performance:** Hardware-accelerated rendering and asset pre-caching.

### 5. REST API
A production-grade REST API enables programmatic geometry generation:
- **POST/GET /api/generate:** Generate and download SVG or PNG specimens.
- **GET /api/preview:** Preview generation metadata without downloading.
- **GET /api/health:** Service health check.
- **Rate Limiting:** 20 requests/minute for generation, 30 for preview/health.
- **OpenAPI Documentation:** Interactive docs available at `/api/docs`.

## Deployment Instructions

### Prerequisites
- Docker
- Cloudflare Tunnel (optional for internet exposure)

### Local Execution
To build and run the container locally:

```bash
docker build -t geometry-vault .
docker run -d -p 8080:80 --name geometry-vault geometry-vault
```

The service will be accessible at `http://localhost:8080`.

## API Usage

The system provides a REST API for programmatic geometry generation and download.

### Base URL
```
http://localhost:8080/api
```

### Endpoints

#### Generate Geometry (POST)
```bash
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": "Cosmic Alignment Protocol",
    "colors": "#8B1A1A, #2A2520, #7A7068",
    "ratio_w": 1,
    "ratio_h": 1,
    "format": "svg"
  }' \
  -o specimen.svg
```

#### Generate Geometry (GET)
```bash
curl "http://localhost:8080/api/generate?seed=Archival%20Test&format=png&ratio_w=16&ratio_h=9" \
  -o specimen.png
```

#### Preview Metadata
```bash
curl "http://localhost:8080/api/preview?seed=Preview%20Test&colors=%238B1A1A,%20%232A2520"
```

Response:
```json
{
  "success": true,
  "sequence_id": "42-A8K3L9",
  "hash": "0x1A2B3C4D",
  "format": "svg",
  "svg_base64": "PHN2ZyB2aWV3Qm94PSIwIDAg...",
  "parameters": {
    "seed": "Preview Test",
    "colors": "#8B1A1A, #2A2520",
    "ratio_w": 1,
    "ratio_h": 1
  }
}
```

#### Health Check
```bash
curl "http://localhost:8080/api/health"
```

Response:
```json
{
  "status": "healthy",
  "service": "geometry-vault-api",
  "version": "1.0.0"
}
```

### Request Parameters

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `seed` | string | "Archival Initial Data" | 1-128 chars | Narrative sequence for generation |
| `colors` | string | "#8B1A1A, #2A2520, #7A7068, #E8E0D0" | Valid hex colors | Comma-separated color palette |
| `ratio_w` | integer | 1 | 1-16 | Aspect ratio width |
| `ratio_h` | integer | 1 | 1-16 | Aspect ratio height |
| `format` | string | "svg" | svg, png | Output format |
| `scale` | integer | 2400 | 800-4800 | PNG export scale (longest edge pixels) |

### Rate Limits

- **Generation endpoints:** 20 requests/minute per IP
- **Preview/Health:** 30 requests/minute per IP
- **Response headers:** `X-Sequence-ID`, `X-Hash` for traceability

### Interactive Documentation

Access the interactive API documentation:
- **Swagger UI:** `http://localhost:8080/api/docs`
- **ReDoc:** `http://localhost:8080/api/redoc`
- **OpenAPI Spec:** `http://localhost:8080/api/openapi.json`

### Python Example

```python
import requests

response = requests.post("http://localhost:8080/api/generate", json={
    "seed": "Python Integration Test",
    "colors": "#8B1A1A, #2A2520, #7A7068",
    "ratio_w": 3,
    "ratio_h": 4,
    "format": "png",
    "scale": 3000
})

with open("specimen.png", "wb") as f:
    f.write(response.content)

print(f"Generated: {response.headers['X-Sequence-ID']}")
```

### JavaScript Example

```javascript
fetch('http://localhost:8080/api/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    seed: 'JavaScript Integration Test',
    colors: '#8B1A1A, #2A2520, #7A7068',
    ratio_w: 16,
    ratio_h: 9,
    format: 'svg'
  })
})
.then(res => res.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'specimen.svg';
  a.click();
});
```

## Metadata and Compliance

This project adheres to the Master Blueprint for Hyper-SEO. It includes structured data for Person, Organization, and FAQPage schemas, ensuring high-fidelity machine-readability for search engines and AI Overview systems.

---
**Version 1.8.0**
**Architect:** Mema (via Glass Gallery Project)
**Status:** PRODUCTION_READY
**API:** FastAPI + Uvicorn + Nginx
