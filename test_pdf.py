from backend.app.services.pdf_service import extract_text_from_pdf

pdf_path = "backend/app/uploads/Maincrafts Offer Letter++-38 (1).pdf"
text = extract_text_from_pdf(pdf_path)

print(text[:1000])