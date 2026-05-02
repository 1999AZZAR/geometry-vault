import math
import re
from typing import List, Tuple


class GeometryGenerator:
    """
    Procedural geometry generator ported from JavaScript.
    Generates SVG markup based on deterministic hash values.
    """
    
    BASE_RESOLUTION = 240
    MAX_LAYERS = 7
    ARCHIVAL_PALETTE = ['#8B1A1A', '#2A2520', '#7A7068', '#5A5048']
    
    @staticmethod
    def sanitize_palette(input_string: str) -> List[str]:
        """Extract valid hex colors from comma-separated string."""
        raw_colors = input_string.split(',')
        valid_colors = []
        hex_regex = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        
        for color in raw_colors:
            trimmed = color.strip()
            if hex_regex.match(trimmed):
                valid_colors.append(trimmed)
        
        return valid_colors if valid_colors else GeometryGenerator.ARCHIVAL_PALETTE
    
    @staticmethod
    def generate_secure_hash(input_string: str) -> int:
        """Generate FNV-1a hash from sanitized input string."""
        sanitized = re.sub(r'[^a-zA-Z0-9\s\-_.,]', '', input_string).strip()
        hash_value = 0x811c9dc5
        
        for char in sanitized:
            hash_value ^= ord(char)
            hash_value = (hash_value * 0x01000193) & 0xFFFFFFFF
        
        return abs(hash_value) if hash_value < 0x80000000 else abs(hash_value - 0x100000000)
    
    @staticmethod
    def generate_sequence_identifier(hash_value: int) -> str:
        """Generate human-readable sequence identifier from hash."""
        dictionary = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        prefix = (hash_value % 89) + 10
        suffix = ""
        mutable_hash = hash_value
        
        for _ in range(6):
            suffix += dictionary[mutable_hash % len(dictionary)]
            mutable_hash //= len(dictionary)
        
        return f"{prefix}-{suffix}"
    
    @staticmethod
    def build_geometry_path(
        cx: float,
        cy: float,
        scale: float,
        params: Tuple[float, float, float, float],
        mod_freq: float = 0,
        mod_amp: float = 0
    ) -> str:
        """Build SVG path using superformula parameters."""
        m, n1, n2, n3 = params
        m_div_4 = m / 4
        inv_n1 = -1 / n1
        step = (math.pi * 2) / GeometryGenerator.BASE_RESOLUTION
        points = []
        
        for i in range(GeometryGenerator.BASE_RESOLUTION + 1):
            theta = i * step
            m_theta_div_4 = m_div_4 * theta
            term1 = abs(math.cos(m_theta_div_4)) ** n2
            term2 = abs(math.sin(m_theta_div_4)) ** n3
            radius = (term1 + term2) ** inv_n1
            
            if mod_freq > 0:
                radius += math.sin(theta * mod_freq) * mod_amp
            
            x = round((cx + radius * scale * math.cos(theta)) * 100) / 100
            y = round((cy + radius * scale * math.sin(theta)) * 100) / 100
            points.append(f"{x},{y}")
        
        return "M " + " L ".join(points) + " Z"
    
    @staticmethod
    def synthesize_geometry(
        hash_value: int,
        palette: List[str],
        cx: float,
        cy: float,
        view_scale: float
    ) -> str:
        """Generate complete geometry SVG markup."""
        svg_markup = []
        core_symmetry = (hash_value % 8) + 2
        core_params = (
            core_symmetry,
            (hash_value % 30) / 10 + 0.5,
            (hash_value % 40) / 10 + 0.2,
            ((hash_value >> 2) % 40) / 10 + 0.2
        )
        sub_symmetry = ((hash_value >> 4) % 12) + 3
        sub_params = (sub_symmetry, 1.2, 0.8, 1.2)
        
        scale_multiplier = view_scale / 100
        
        for layer in range(1, GeometryGenerator.MAX_LAYERS + 1):
            layer_scale = (layer / GeometryGenerator.MAX_LAYERS) * 36 * scale_multiplier
            rotation_angle = (hash_value % 360) + (layer * 22.5)
            stroke_width = max(0.08, 0.25 - (layer * 0.02))
            stroke_color = palette[layer % len(palette)]
            
            path_a = GeometryGenerator.build_geometry_path(cx, cy, layer_scale, core_params)
            svg_markup.append(
                f'<path d="{path_a}" fill="none" stroke="{stroke_color}" '
                f'stroke-width="{stroke_width}" transform="rotate({rotation_angle} {cx} {cy})" />'
            )
            
            if layer % 2 == 0:
                mod_freq = (hash_value % 6) + 2
                mod_amp = 0.05 * layer
                secondary_color = palette[(layer + 1) % len(palette)]
                path_b = GeometryGenerator.build_geometry_path(
                    cx, cy, layer_scale * 0.75, sub_params, mod_freq, mod_amp
                )
                svg_markup.append(
                    f'<path d="{path_b}" fill="none" stroke="{secondary_color}" '
                    f'stroke-width="{stroke_width * 0.8}" '
                    f'transform="rotate({-rotation_angle * 1.5} {cx} {cy})" '
                    f'stroke-dasharray="0.3 0.6" />'
                )
        
        orbit_count = (hash_value % 4) + 2
        for orbit in range(orbit_count):
            angle = (orbit * (360 / orbit_count)) + (hash_value % 90)
            rad = math.radians(angle)
            radius_dist = (20 + (hash_value % 15)) * scale_multiplier
            ox = round((cx + radius_dist * math.cos(rad)) * 100) / 100
            oy = round((cy + radius_dist * math.sin(rad)) * 100) / 100
            
            svg_markup.append(
                f'<circle cx="{ox}" cy="{oy}" r="1.2" fill="none" '
                f'stroke="{palette[0]}" stroke-width="0.15" />'
            )
            svg_markup.append(
                f'<line x1="{cx}" y1="{cy}" x2="{ox}" y2="{oy}" '
                f'stroke="{palette[min(2, len(palette) - 1)]}" stroke-width="0.05" stroke-dasharray="0.2 0.8" />'
            )
        
        return '\n'.join(svg_markup)
    
    @staticmethod
    def render_svg(
        seed: str,
        colors: str,
        ratio_w: int = 1,
        ratio_h: int = 1
    ) -> Tuple[str, str, str]:
        """
        Generate complete SVG document.
        Returns: (svg_content, sequence_id, hash_hex)
        """
        hash_value = GeometryGenerator.generate_secure_hash(seed)
        identifier = GeometryGenerator.generate_sequence_identifier(hash_value)
        palette = GeometryGenerator.sanitize_palette(colors)
        
        view_w = 100
        view_h = 100
        
        if ratio_w > ratio_h:
            view_h = round((100 * (ratio_h / ratio_w)) * 100) / 100
        elif ratio_h > ratio_w:
            view_w = round((100 * (ratio_w / ratio_h)) * 100) / 100
        
        cx = round((view_w / 2) * 100) / 100
        cy = round((view_h / 2) * 100) / 100
        min_dim = min(view_w, view_h)
        
        core_symmetry = (hash_value % 8) + 2
        geometry_markup = GeometryGenerator.synthesize_geometry(
            hash_value, palette, cx, cy, min_dim
        )
        
        hash_hex = f"0x{hash_value:08X}"
        
        svg_content = f'''<svg viewBox="0 0 {view_w} {view_h}" xmlns="http://www.w3.org/2000/svg" style="aspect-ratio: {ratio_w}/{ratio_h};">
    <rect width="{view_w}" height="{view_h}" fill="transparent"/>
    
    <g opacity="0.15">
        <circle cx="{cx}" cy="{cy}" r="{(min_dim / 2) * 0.92}" fill="none" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.2 1" />
        <line x1="{cx}" y1="1" x2="{cx}" y2="{view_h - 1}" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.5 1.5" />
        <line x1="1" y1="{cy}" x2="{view_w - 1}" y2="{cy}" stroke="#7A7068" stroke-width="0.1" stroke-dasharray="0.5 1.5" />
    </g>
    
    <g>{geometry_markup}</g>

    <text x="2" y="{view_h - 2}" font-size="1.2" font-family="'JetBrains Mono', monospace" fill="#7A7068" letter-spacing="0.1em">ID:{identifier}</text>
    <text x="{view_w - 2}" y="3" font-size="1.2" font-family="'JetBrains Mono', monospace" fill="#7A7068" letter-spacing="0.1em" text-anchor="end">PTR:{hash_hex}</text>
</svg>'''
        
        return svg_content, identifier, hash_hex
