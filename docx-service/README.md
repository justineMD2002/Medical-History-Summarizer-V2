# docx-service

FastAPI microservice that generates a formatted `.docx` medical summary document from structured JSON input.

## Environment Variables

| Variable | Description |
|---|---|
| `SERVICE_SECRET` | Shared secret required in the `X-Service-Secret` header |

Copy `.env.example` to `.env` and fill in the values.

## Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002
```

## Run with Docker

```bash
docker build -t docx-service .
docker run -p 8002:8002 -e SERVICE_SECRET=your-secret-here docx-service
```

## Endpoints

### GET /health

```bash
curl http://localhost:8002/health
```

### POST /generate

Returns a `.docx` file as a binary download.

```bash
curl -X POST http://localhost:8002/generate \
  -H "X-Service-Secret: your-secret-here" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Jane Doe",
    "dob": "1985-04-12",
    "dol": "2024-11-01",
    "sections": [
      {
        "title": "Chief Complaint",
        "classification": "post",
        "summary": "Patient presents with lower back pain following motor vehicle accident."
      },
      {
        "title": "Past Medical History",
        "classification": "pre",
        "summary": "Hypertension diagnosed in 2019. No prior musculoskeletal injuries."
      }
    ]
  }' \
  --output summary_Jane_Doe.docx
```
