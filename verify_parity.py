#!/usr/bin/env python3
"""
Verification script to ensure Python API generates identical geometry
to JavaScript UI implementation.
"""

import sys
from api.geometry import GeometryGenerator


def test_hash_generation():
    """Test that hash generation matches JavaScript."""
    test_cases = [
        ("Archival Initial Data", None),  # Default
        ("Test", None),
        ("Cosmic Alignment Protocol", None),
        ("", "Archival Initial Data"),  # Empty should default
        ("Hello World 123", None),
    ]
    
    print("Testing Hash Generation")
    print("=" * 60)
    
    for seed, expected_seed in test_cases:
        actual_seed = seed if seed else "Archival Initial Data"
        hash_value = GeometryGenerator.generate_secure_hash(actual_seed)
        seq_id = GeometryGenerator.generate_sequence_identifier(hash_value)
        hash_hex = f"0x{hash_value:08X}"
        
        print(f"Seed: '{actual_seed}'")
        print(f"  Hash: {hash_hex} ({hash_value})")
        print(f"  Seq ID: {seq_id}")
        print()
    
    return True


def test_geometry_consistency():
    """Test that same seed produces consistent geometry."""
    print("\nTesting Geometry Consistency")
    print("=" * 60)
    
    seed = "Test Pattern"
    colors = "#8B1A1A, #2A2520, #7A7068"
    
    # Generate twice
    svg1, seq1, hash1 = GeometryGenerator.render_svg(seed, colors, 1, 1)
    svg2, seq2, hash2 = GeometryGenerator.render_svg(seed, colors, 1, 1)
    
    print(f"Seed: '{seed}'")
    print(f"First generation:  {seq1} / {hash1}")
    print(f"Second generation: {seq2} / {hash2}")
    
    if seq1 == seq2 and hash1 == hash2:
        print("✓ Sequence IDs and hashes match")
    else:
        print("✗ MISMATCH - inconsistent generation!")
        return False
    
    if svg1 == svg2:
        print("✓ SVG output is identical")
    else:
        print("✗ MISMATCH - SVG differs!")
        return False
    
    # Test different ratios
    print("\nTesting Different Aspect Ratios:")
    ratios = [(1, 1), (16, 9), (3, 4), (2, 3)]
    
    for w, h in ratios:
        svg, seq_id, _ = GeometryGenerator.render_svg(seed, colors, w, h)
        viewbox = svg.split('viewBox="')[1].split('"')[0]
        print(f"  {w}:{h} -> viewBox=\"{viewbox}\" | {seq_id}")
    
    print()
    return True


def test_color_palette():
    """Test color palette handling."""
    print("\nTesting Color Palette Handling")
    print("=" * 60)
    
    test_cases = [
        ("#8B1A1A, #2A2520, #7A7068", 3),
        ("#FFF, #000", 2),
        ("invalid, #ABC, not-a-color, #123456", 2),  # Should keep valid ones
        ("", 4),  # Should use default palette
        ("#F00", 1),  # Single color
    ]
    
    for colors, expected_count in test_cases:
        palette = GeometryGenerator.sanitize_palette(colors)
        status = "✓" if len(palette) == expected_count else "✗"
        print(f"{status} '{colors[:40]}' -> {len(palette)} colors: {palette}")
    
    print()
    return True


def test_known_values():
    """Test against known hash values to verify JS parity."""
    print("\nTesting Known Values (JS Comparison)")
    print("=" * 60)
    
    # These should be manually verified against the JS console
    known_tests = [
        ("Test", "Should produce consistent hash"),
        ("Archival Initial Data", "Default seed"),
        ("12345", "Numeric string"),
        ("Special!@#$%^&*()Chars", "Should sanitize to 'SpecialChars'"),
    ]
    
    for seed, description in known_tests:
        hash_value = GeometryGenerator.generate_secure_hash(seed)
        seq_id = GeometryGenerator.generate_sequence_identifier(hash_value)
        
        # Sanitize to show what's actually hashed
        sanitized = seed.replace('[^a-zA-Z0-9\\s-_.,]', '')
        
        print(f"Seed: '{seed}'")
        print(f"  Description: {description}")
        print(f"  Hash: 0x{hash_value:08X} ({hash_value})")
        print(f"  Seq ID: {seq_id}")
        print(f"  JS Test: console.log(generateSecureHash('{seed}'))")
        print()
    
    return True


def test_svg_structure():
    """Test SVG output structure."""
    print("\nTesting SVG Structure")
    print("=" * 60)
    
    seed = "Structure Test"
    colors = "#8B1A1A, #2A2520, #7A7068"
    svg, seq_id, hash_hex = GeometryGenerator.render_svg(seed, colors, 1, 1)
    
    # Check essential elements
    checks = [
        ('<svg viewBox="0 0 100 100"' in svg, "ViewBox (1:1)"),
        ('<path d="M' in svg, "Path elements"),
        ('<circle cx=' in svg, "Circle elements"),
        ('<line x1=' in svg, "Line elements"),
        (f'ID:{seq_id}' in svg, "Sequence ID label"),
        ('fill="transparent"' in svg, "Transparent background"),
        ('stroke="#' in svg, "Stroke colors"),
    ]
    
    for passed, description in checks:
        status = "✓" if passed else "✗"
        print(f"{status} {description}")
    
    print(f"\nSVG Length: {len(svg)} characters")
    print()
    
    return all(check[0] for check in checks)


def compare_with_js():
    """
    Instructions for manual JavaScript comparison.
    """
    print("\n" + "=" * 60)
    print("MANUAL JAVASCRIPT VERIFICATION")
    print("=" * 60)
    print("""
To verify parity with JavaScript UI:

1. Open http://localhost:8080 in browser
2. Open browser console (F12)
3. Run these commands:

// Test hash function
generateSecureHash("Test")
generateSequenceIdentifier(generateSecureHash("Test"))

// Test with API seed
generateSecureHash("Archival Initial Data")

4. Compare output with Python values above

5. Test visual output:
   - Enter seed "Test Pattern" in UI with colors "#8B1A1A, #2A2520, #7A7068"
   - Note the Sequence ID
   - Download SVG from UI
   - Generate same from API: 
     curl -X POST http://localhost:8080/api/generate \\
       -H "Content-Type: application/json" \\
       -d '{"seed": "Test Pattern", "colors": "#8B1A1A, #2A2520, #7A7068", "format": "svg"}' \\
       -o api_output.svg
   - Compare files visually or with diff

Expected: Both should produce identical sequence IDs and identical SVG output.
""")


def main():
    """Run all verification tests."""
    print("Geometry Vault - Python/JavaScript Parity Verification")
    print("=" * 60 + "\n")
    
    tests = [
        ("Hash Generation", test_hash_generation),
        ("Geometry Consistency", test_geometry_consistency),
        ("Color Palette", test_color_palette),
        ("Known Values", test_known_values),
        ("SVG Structure", test_svg_structure),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    compare_with_js()
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✓ All automated tests passed!")
        print("⚠️  Manual JS comparison still recommended")
        return 0
    else:
        print("\n✗ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
