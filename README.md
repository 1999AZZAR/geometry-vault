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

## Metadata and Compliance

This project adheres to the Master Blueprint for Hyper-SEO. It includes structured data for Person, Organization, and FAQPage schemas, ensuring high-fidelity machine-readability for search engines and AI Overview systems.

---
**Version 1.7.0**
**Architect:** Mema (via Glass Gallery Project)
**Status:** PRODUCTION_READY
