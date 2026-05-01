from fastapi import FastAPI, HTTPException, Query, Response, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from io import BytesIO
import base64
import logging
import functools

from .models import GenerateRequest, GenerateResponse, HealthResponse
from .geometry import GeometryGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server-side cache for SVG generation (Precache mechanism)
@functools.lru_cache(maxsize=1024)
def cached_render_svg(seed: str, colors: str, ratio_w: int, ratio_h: int):
    return GeometryGenerator.render_svg(seed, colors, ratio_w, ratio_h)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Geometry Vault API",
    description="Procedural geometry synthesis engine with SVG/PNG generation",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health", response_model=HealthResponse, tags=["System"])
@limiter.limit("30/minute")
async def health_check(request: Request):
    """Health check endpoint."""
    return HealthResponse()


@app.post("/api/generate", response_model=GenerateResponse, tags=["Generation"])
@limiter.limit("20/minute")
async def generate_geometry_post(request: Request, body: GenerateRequest):
    """
    Generate procedural geometry from narrative sequence.
    
    Accepts JSON body with generation parameters and returns SVG or PNG.
    Rate limited to 20 requests per minute per IP.
    """
    try:
        svg_content, seq_id, hash_hex = cached_render_svg(
            body.seed,
            body.colors,
            body.ratio_w,
            body.ratio_h
        )
        
        if body.format == "svg":
            return StreamingResponse(
                BytesIO(svg_content.encode('utf-8')),
                media_type="image/svg+xml",
                headers={
                    "Content-Disposition": f'attachment; filename="specimen_{seq_id}.svg"',
                    "X-Sequence-ID": seq_id,
                    "X-Hash": hash_hex
                }
            )
        
        elif body.format == "png":
            try:
                import cairosvg
                from PIL import Image
                
                ratio = body.ratio_w / body.ratio_h
                if ratio > 1:
                    width = body.scale
                    height = round(body.scale / ratio)
                else:
                    height = body.scale
                    width = round(body.scale * ratio)
                
                png_data = cairosvg.svg2png(
                    bytestring=svg_content.encode('utf-8'),
                    output_width=width,
                    output_height=height,
                    background_color='#EFE9DC'
                )
                
                return StreamingResponse(
                    BytesIO(png_data),
                    media_type="image/png",
                    headers={
                        "Content-Disposition": f'attachment; filename="specimen_{seq_id}.png"',
                        "X-Sequence-ID": seq_id,
                        "X-Hash": hash_hex
                    }
                )
            except ImportError:
                raise HTTPException(
                    status_code=501,
                    detail="PNG generation not available. Install cairosvg and PIL."
                )
        
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")


@app.get("/api/generate", tags=["Generation"])
@limiter.limit("20/minute")
async def generate_geometry_get(
    request: Request,
    seed: str = Query("Archival Initial Data", max_length=128, description="Narrative sequence"),
    colors: str = Query("#8B1A1A, #2A2520, #7A7068, #E8E0D0", max_length=256, description="Color palette"),
    ratio_w: int = Query(1, ge=1, le=16, description="Aspect ratio width"),
    ratio_h: int = Query(1, ge=1, le=16, description="Aspect ratio height"),
    format: str = Query("svg", pattern="^(svg|png)$", description="Output format"),
    scale: int = Query(2400, ge=800, le=4800, description="PNG scale (pixels)")
):
    """
    Generate geometry via GET request with query parameters.
    
    Convenient for direct browser access and simple integrations.
    Rate limited to 20 requests per minute per IP.
    """
    body = GenerateRequest(
        seed=seed,
        colors=colors,
        ratio_w=ratio_w,
        ratio_h=ratio_h,
        format=format,
        scale=scale
    )
    return await generate_geometry_post(request, body)


@app.get("/api/preview", response_model=GenerateResponse, tags=["Generation"])
@limiter.limit("30/minute")
async def preview_geometry(
    request: Request,
    seed: str = Query("Archival Initial Data", max_length=128),
    colors: str = Query("#8B1A1A, #2A2520, #7A7068, #E8E0D0", max_length=256),
    ratio_w: int = Query(1, ge=1, le=16),
    ratio_h: int = Query(1, ge=1, le=16)
):
    """
    Preview generation metadata without downloading the file.
    
    Returns sequence ID, hash, and generation parameters.
    Rate limited to 30 requests per minute per IP.
    """
    try:
        svg_content, seq_id, hash_hex = cached_render_svg(
            seed, colors, ratio_w, ratio_h
        )
        
        svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        
        return JSONResponse({
            "success": True,
            "sequence_id": seq_id,
            "hash": hash_hex,
            "format": "svg",
            "svg_base64": svg_base64,
            "parameters": {
                "seed": seed,
                "colors": colors,
                "ratio_w": ratio_w,
                "ratio_h": ratio_h
            }
        })
    except Exception as e:
        logger.error(f"Preview error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
