import os
import io
from fastapi import FastAPI, File, UploadFile, Header, HTTPException
from fastapi.responses import JSONResponse
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

SERVICE_SECRET = os.getenv("SERVICE_SECRET")

app = FastAPI()


def verify_secret(x_service_secret: str):
    if not SERVICE_SECRET or x_service_secret != SERVICE_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/extract")
async def extract(
    file: UploadFile = File(...),
    x_service_secret: str = Header(...),
):
    verify_secret(x_service_secret)

    contents = await file.read()
    doc = fitz.open(stream=contents, filetype="pdf")

    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        ocr_used = False

        if not text:
            # Render at 2x scale and run OCR
            mat = fitz.Matrix(2, 2)
            pix = page.get_pixmap(matrix=mat)
            img_bytes = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_bytes))
            text = pytesseract.image_to_string(img).strip()
            ocr_used = True

        tagged_text = f"[PDF PAGE {page_num + 1}] {text}"
        pages.append({
            "page": page_num + 1,
            "text": tagged_text,
            "ocr_used": ocr_used,
        })

    # Extract sections from PDF bookmarks/outline
    sections = []
    toc = doc.get_toc()  # [[level, title, page], ...]
    for i, entry in enumerate(toc):
        level, title, start_page = entry
        if i + 1 < len(toc):
            end_page = toc[i + 1][2] - 1
        else:
            end_page = len(doc)
        sections.append({
            "title": title,
            "start_page": start_page,
            "end_page": end_page,
        })

    doc.close()

    return JSONResponse(content={"pages": pages, "sections": sections})
