from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import re


class GenerateRequest(BaseModel):
    """Request model for geometry generation."""
    
    seed: str = Field(
        default="Archival Initial Data",
        max_length=128,
        description="Narrative sequence for geometry generation"
    )
    colors: str = Field(
        default="#8B1A1A, #2A2520, #7A7068, #E8E0D0",
        max_length=256,
        description="Comma-separated hex color palette"
    )
    ratio_w: int = Field(
        default=1,
        ge=1,
        le=16,
        description="Aspect ratio width"
    )
    ratio_h: int = Field(
        default=1,
        ge=1,
        le=16,
        description="Aspect ratio height"
    )
    format: Literal["svg", "png"] = Field(
        default="svg",
        description="Output format (svg or png)"
    )
    scale: Optional[int] = Field(
        default=2400,
        ge=800,
        le=4800,
        description="PNG export scale (longest edge in pixels, only for PNG format)"
    )
    
    @validator('seed')
    def validate_seed(cls, v):
        if not v or not v.strip():
            return "Archival Initial Data"
        return v.strip()
    
    @validator('colors')
    def validate_colors(cls, v):
        if not v or not v.strip():
            return "#8B1A1A, #2A2520, #7A7068, #E8E0D0"
        
        colors = v.split(',')
        hex_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        valid_colors = [c.strip() for c in colors if hex_regex.match(c.strip())]
        
        if not valid_colors:
            return "#8B1A1A, #2A2520, #7A7068, #E8E0D0"
        
        return ', '.join(valid_colors)


class GenerateResponse(BaseModel):
    """Response model for successful generation."""
    
    success: bool = True
    sequence_id: str = Field(description="Unique sequence identifier")
    hash: str = Field(description="Hexadecimal hash value")
    format: str = Field(description="Output format")
    download_url: Optional[str] = Field(None, description="Direct download URL if applicable")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = "healthy"
    service: str = "geometry-vault-api"
    version: str = "1.0.0"
