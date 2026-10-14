# ADR-001: Open-Access SaaS Architecture

**Status:** ACCEPTED
**Date:** 2026-05-02
**Decision Makers:** Azzar Budiyanto (Architect)
**Reviewed by:** Frea (Security Analysis)

## Context

Geometry Vault is a procedural geometry synthesis engine designed as an embeddable service. The project needs to decide whether to restrict API access to specific domains or allow open access from any origin.

## Decision

**We will implement an OPEN-ACCESS architecture with the following characteristics:**

1. **Unrestricted CORS Policy**
   - `allow_origins=["*"]` in FastAPI
   - Any domain can make API requests

2. **Open postMessage API**
   - No origin validation on `window.addEventListener('message')`
   - Any website can embed and control the geometry engine via iframe

3. **Public Embedding**
   - `?mode=embed` parameter provides clean iframe view
   - External sites can integrate without authentication

## Rationale

### Benefits
1. **Frictionless Integration**
   - Developers can embed without API keys or registration
   - Zero configuration required
   - Instant experimentation and testing

2. **Maximum Reach**
   - Any website, blog, or documentation can use the service
   - Viral growth potential through organic embedding
   - Educational and portfolio use cases

3. **Simplicity**
   - No authentication infrastructure needed
   - No user management system
   - Reduced operational complexity

4. **Archival Philosophy**
   - Aligns with "public specimen vault" concept
   - Knowledge and art should be freely accessible
   - Democratizes procedural design tools

### Risks & Mitigations

| Risk | Mitigation | Status |
|------|-----------|--------|
| API abuse/DDoS | Rate limiting (20 req/min generation) | [OK] Implemented |
| Resource exhaustion | PNG scale limits (800-4800px), SVG only by default | [OK] Implemented |
| Spam/malicious content | Input validation (max 128 chars seed, hex color regex) | [OK] Implemented |
| Cost explosion | Nginx proxy cache (24h), LRU memory cache (1024 entries) | [OK] Implemented |
| Attribution loss | Sequence ID & hash in SVG metadata | [OK] Implemented |

## Alternatives Considered

### Alternative 1: API Key System
**Rejected** - Adds friction, requires user management, reduces adoption

### Alternative 2: Domain Whitelist
**Rejected** - Impossible to maintain, breaks embedded use cases

### Alternative 3: Freemium Model (Open + Premium)
**Deferred** - May implement later with:
- Free tier: 20 req/min (current)
- Premium tier: Higher limits, batch API, priority rendering

## Implementation Details

### Rate Limiting Strategy
```python
# SlowAPI configuration
@limiter.limit("20/minute")  # Generation endpoints
@limiter.limit("30/minute")  # Preview/Health endpoints
```

### Caching Strategy
```python
# LRU cache (server-side)
@functools.lru_cache(maxsize=1024)
def cached_render_svg(seed, colors, ratio_w, ratio_h)

# Nginx proxy cache
proxy_cache_valid 200 24h;
proxy_cache_use_stale error timeout;
```

### Input Validation
```python
seed: str = Field(max_length=128)
colors: str = Field(max_length=256)  # Regex validated
ratio_w/h: int = Field(ge=1, le=16)
scale: int = Field(ge=800, le=4800)
```

## Monitoring Recommendations

To ensure open-access doesn't lead to abuse, implement:

1. **Usage Analytics**
   - Track requests by IP/Referer
   - Identify top consumers
   - Monitor rate limit hits

2. **Abuse Detection**
   - Alert on sustained rate limit violations
   - Track unusual parameter patterns
   - Monitor resource consumption

3. **Cost Tracking**
   - Monitor bandwidth usage
   - Track cache hit ratios
   - Measure CPU/memory per request

## Success Metrics

- **Adoption:** Number of unique embedding domains
- **Performance:** 95%+ requests served from cache
- **Reliability:** <0.1% rate limit violations
- **Cost:** <$50/month operational cost at 100K req/month

## Review Criteria

This decision should be reviewed if:
- Monthly operational cost exceeds $200
- Sustained abuse patterns emerge (>5% rate limit violations)
- 50+ production embeddings achieved (consider premium tier)
- Security vulnerabilities discovered in open-access model

## References

- [Open SaaS Examples: Unsplash API, Lorem Picsum]
- [Rate Limiting Best Practices: IETF RFC 6585]
- [Public API Design: REST API Design Rulebook]

---

**Approved by:** Azzar Budiyanto
**Implementation Status:** COMPLETE
**Last Updated:** 2026-05-02
