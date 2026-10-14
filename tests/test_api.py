#!/usr/bin/env python3
"""
Quick test script for Geometry Vault API.
Run after building and starting the Docker container.
"""

import requests
import json
import sys
from pathlib import Path


BASE_URL = "http://localhost:8080/api"


def test_health():
    """Test health check endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    return response.status_code == 200


def test_preview():
    """Test preview endpoint."""
    print("Testing preview endpoint...")
    params = {
        "seed": "API Test Preview",
        "colors": "#8B1A1A, #2A2520, #7A7068",
        "ratio_w": 1,
        "ratio_h": 1
    }
    response = requests.get(f"{BASE_URL}/preview", params=params)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Sequence ID: {data.get('sequence_id')}")
    print(f"Hash: {data.get('hash')}\n")
    return response.status_code == 200


def test_generate_svg():
    """Test SVG generation (POST)."""
    print("Testing SVG generation (POST)...")
    payload = {
        "seed": "API Test SVG Generation",
        "colors": "#8B1A1A, #2A2520, #7A7068, #E8E0D0",
        "ratio_w": 1,
        "ratio_h": 1,
        "format": "svg"
    }
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Sequence ID: {response.headers.get('X-Sequence-ID')}")
    print(f"Hash: {response.headers.get('X-Hash')}")
    
    if response.status_code == 200:
        output_file = Path("test_specimen.svg")
        output_file.write_bytes(response.content)
        print(f"Saved: {output_file.absolute()}\n")
        return True
    return False


def test_generate_png():
    """Test PNG generation (GET)."""
    print("Testing PNG generation (GET)...")
    params = {
        "seed": "API Test PNG Generation",
        "colors": "#8B1A1A, #2A2520",
        "ratio_w": 16,
        "ratio_h": 9,
        "format": "png",
        "scale": 2400
    }
    response = requests.get(f"{BASE_URL}/generate", params=params)
    print(f"Status: {response.status_code}")
    print(f"Sequence ID: {response.headers.get('X-Sequence-ID')}")
    print(f"Hash: {response.headers.get('X-Hash')}")
    
    if response.status_code == 200:
        output_file = Path("test_specimen.png")
        output_file.write_bytes(response.content)
        print(f"Saved: {output_file.absolute()}\n")
        return True
    return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Geometry Vault API Test Suite")
    print("=" * 60 + "\n")
    
    tests = [
        ("Health Check", test_health),
        ("Preview", test_preview),
        ("SVG Generation", test_generate_svg),
        ("PNG Generation", test_generate_png),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except requests.exceptions.ConnectionError:
            print(f"ERROR: Cannot connect to {BASE_URL}")
            print("Make sure the Docker container is running:\n")
            print("  docker build -t geometry-vault .")
            print("  docker run -d -p 8080:80 --name geometry-vault geometry-vault\n")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR in {name}: {e}\n")
            results.append((name, False))
    
    print("=" * 60)
    print("Test Results:")
    print("=" * 60)
    for name, success in results:
        status = "PASS" if success else "FAIL"
        symbol = "✓" if success else "✗"
        print(f"{symbol} {name}: {status}")
    
    total = len(results)
    passed = sum(1 for _, success in results if success)
    print(f"\nPassed: {passed}/{total}")
    
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
