# Geometry Vault API Examples

Complete integration examples for the Geometry Vault API.

## cURL Examples

### Basic SVG Generation
```bash
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "seed": "Cosmic Alignment",
    "colors": "#8B1A1A, #2A2520",
    "ratio_w": 1,
    "ratio_h": 1,
    "format": "svg"
  }' \
  -o output.svg
```

### PNG with Custom Ratio
```bash
curl "http://localhost:8080/api/generate?seed=Archival%20Specimen&format=png&ratio_w=16&ratio_h=9&scale=3000" \
  -o output.png
```

### Preview Generation
```bash
curl "http://localhost:8080/api/preview?seed=Test%20Pattern&colors=%238B1A1A,%20%232A2520" | jq
```

## Python Examples

### Basic Usage
```python
import requests

response = requests.post("http://localhost:8080/api/generate", json={
    "seed": "Python Test",
    "colors": "#8B1A1A, #2A2520, #7A7068",
    "format": "svg"
})

with open("specimen.svg", "wb") as f:
    f.write(response.content)

print(f"Generated: {response.headers['X-Sequence-ID']}")
```

### Batch Generation
```python
import requests
from pathlib import Path

seeds = [
    "Geometric Pattern Alpha",
    "Geometric Pattern Beta",
    "Geometric Pattern Gamma"
]

output_dir = Path("specimens")
output_dir.mkdir(exist_ok=True)

for seed in seeds:
    response = requests.post("http://localhost:8080/api/generate", json={
        "seed": seed,
        "colors": "#8B1A1A, #2A2520, #7A7068, #E8E0D0",
        "ratio_w": 1,
        "ratio_h": 1,
        "format": "png",
        "scale": 2400
    })
    
    seq_id = response.headers['X-Sequence-ID']
    filename = output_dir / f"specimen_{seq_id}.png"
    filename.write_bytes(response.content)
    print(f"Generated: {filename}")
```

### Preview Before Download
```python
import requests

response = requests.get("http://localhost:8080/api/preview", params={
    "seed": "Preview Test",
    "colors": "#8B1A1A, #2A2520"
})

data = response.json()
print(f"Sequence ID: {data['sequence_id']}")
print(f"Hash: {data['hash']}")

if data['success']:
    gen_response = requests.post("http://localhost:8080/api/generate", json={
        "seed": "Preview Test",
        "colors": "#8B1A1A, #2A2520",
        "format": "png"
    })
    
    with open(f"specimen_{data['sequence_id']}.png", "wb") as f:
        f.write(gen_response.content)
```

## JavaScript/Node.js Examples

### Node.js with Fetch
```javascript
const fs = require('fs');
const fetch = require('node-fetch');

async function generateSpecimen() {
  const response = await fetch('http://localhost:8080/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      seed: 'Node.js Test',
      colors: '#8B1A1A, #2A2520, #7A7068',
      ratio_w: 3,
      ratio_h: 4,
      format: 'svg'
    })
  });
  
  const buffer = await response.buffer();
  const seqId = response.headers.get('X-Sequence-ID');
  
  fs.writeFileSync(`specimen_${seqId}.svg`, buffer);
  console.log(`Generated: specimen_${seqId}.svg`);
}

generateSpecimen();
```

### Browser JavaScript
```javascript
async function downloadSpecimen() {
  const response = await fetch('http://localhost:8080/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      seed: 'Browser Test',
      colors: '#8B1A1A, #2A2520',
      ratio_w: 16,
      ratio_h: 9,
      format: 'png',
      scale: 2400
    })
  });
  
  const blob = await response.blob();
  const seqId = response.headers.get('X-Sequence-ID');
  const url = URL.createObjectURL(blob);
  
  const a = document.createElement('a');
  a.href = url;
  a.download = `specimen_${seqId}.png`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

## PHP Example

```php
<?php
$url = 'http://localhost:8080/api/generate';

$data = [
    'seed' => 'PHP Integration Test',
    'colors' => '#8B1A1A, #2A2520, #7A7068',
    'ratio_w' => 1,
    'ratio_h' => 1,
    'format' => 'svg'
];

$options = [
    'http' => [
        'header' => "Content-Type: application/json\r\n",
        'method' => 'POST',
        'content' => json_encode($data)
    ]
];

$context = stream_context_create($options);
$response = file_get_contents($url, false, $context);

if ($response !== false) {
    $headers = $http_response_header;
    $seqId = '';
    
    foreach ($headers as $header) {
        if (stripos($header, 'X-Sequence-ID') !== false) {
            $seqId = trim(explode(':', $header)[1]);
            break;
        }
    }
    
    file_put_contents("specimen_{$seqId}.svg", $response);
    echo "Generated: specimen_{$seqId}.svg\n";
}
?>
```

## Rust Example

```rust
use reqwest;
use std::fs::File;
use std::io::Write;
use serde_json::json;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = reqwest::Client::new();
    
    let response = client
        .post("http://localhost:8080/api/generate")
        .json(&json!({
            "seed": "Rust Integration Test",
            "colors": "#8B1A1A, #2A2520, #7A7068",
            "ratio_w": 1,
            "ratio_h": 1,
            "format": "png",
            "scale": 2400
        }))
        .send()
        .await?;
    
    let seq_id = response
        .headers()
        .get("X-Sequence-ID")
        .and_then(|v| v.to_str().ok())
        .unwrap_or("unknown");
    
    let bytes = response.bytes().await?;
    
    let mut file = File::create(format!("specimen_{}.png", seq_id))?;
    file.write_all(&bytes)?;
    
    println!("Generated: specimen_{}.png", seq_id);
    
    Ok(())
}
```

## Go Example

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "os"
)

type GenerateRequest struct {
    Seed   string `json:"seed"`
    Colors string `json:"colors"`
    RatioW int    `json:"ratio_w"`
    RatioH int    `json:"ratio_h"`
    Format string `json:"format"`
    Scale  int    `json:"scale"`
}

func main() {
    payload := GenerateRequest{
        Seed:   "Go Integration Test",
        Colors: "#8B1A1A, #2A2520, #7A7068",
        RatioW: 1,
        RatioH: 1,
        Format: "png",
        Scale:  2400,
    }
    
    jsonData, _ := json.Marshal(payload)
    
    resp, err := http.Post(
        "http://localhost:8080/api/generate",
        "application/json",
        bytes.NewBuffer(jsonData),
    )
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    seqID := resp.Header.Get("X-Sequence-ID")
    filename := fmt.Sprintf("specimen_%s.png", seqID)
    
    file, _ := os.Create(filename)
    defer file.Close()
    
    io.Copy(file, resp.Body)
    
    fmt.Printf("Generated: %s\n", filename)
}
```

## Rate Limiting

All endpoints are rate-limited:
- Generation endpoints: 20 requests/minute
- Preview/Health: 30 requests/minute

When rate limit is exceeded, the API returns HTTP 429 with:
```json
{
  "error": "Rate limit exceeded: 20 per 1 minute"
}
```

## Error Handling

### Invalid Parameters
```bash
curl -X POST "http://localhost:8080/api/generate" \
  -H "Content-Type: application/json" \
  -d '{"seed": "", "ratio_w": 0}'
```

Response (422):
```json
{
  "detail": [
    {
      "loc": ["body", "ratio_w"],
      "msg": "ensure this value is greater than or equal to 1",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### Service Unavailable
```bash
curl "http://localhost:8080/api/health"
```

Response (200):
```json
{
  "status": "healthy",
  "service": "geometry-vault-api",
  "version": "1.0.0"
}
```
