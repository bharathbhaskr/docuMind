import PyPDF2
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Takes raw PDF bytes and returns all the text inside it.
    file_bytes: the raw binary content of the uploaded PDF
    """
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    
    full_text = ""
    for page_num, page in enumerate(pdf_reader.pages):
        page_text = page.extract_text()
        if page_text:
            # Add page marker so we know where text came from
            full_text += f"\n[Page {page_num + 1}]\n{page_text}"
    
    return full_text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Splits a long text into overlapping chunks.
    
    chunk_size: how many characters per chunk
    overlap:    how many characters to repeat between chunks
                (overlap helps avoid cutting a sentence mid-thought)
    
    Example with chunk_size=20, overlap=5:
    "The cat sat on the mat"
    chunk 1: "The cat sat on the m"
    chunk 2: "e mat" + next 15 chars...
    """
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        # Only add non-empty chunks
        if chunk.strip():
            chunks.append(chunk.strip())
        
        # Move forward by chunk_size minus overlap
        start += chunk_size - overlap
    
    return chunks