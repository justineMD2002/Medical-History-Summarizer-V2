# pdf-service

FastAPI microservice that extracts text from PDF files, with OCR fallback for scanned pages.

## Environment Variables

| Variable | Description |
|---|---|
| `SERVICE_SECRET` | Shared secret required in the `X-Service-Secret` header |

Copy `.env.example` to `.env` and fill in the values.

## Run Locally

```bash
pip install -r requirements.txt
# tesseract must also be installed: https://github.com/tesseract-ocr/tesseract
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Run with Docker

```bash
docker build -t pdf-service .
docker run -p 8001:8001 -e SERVICE_SECRET=your-secret-here pdf-service
```

## Endpoints

### GET /health

```bash
curl http://localhost:8001/health
```

### POST /extract

```bash
curl -X POST http://localhost:8001/extract \
  -H "X-Service-Secret: your-secret-here" \
  -F "file=@/path/to/document.pdf"
```

**Response:**

```json
{
  "pages": [
    {"page": 1, "text": "[PDF PAGE 1] ...extracted text...", "ocr_used": false}
  ],
  "sections": [
    {"title": "Introduction", "start_page": 1, "end_page": 3}
  ]
}
```
