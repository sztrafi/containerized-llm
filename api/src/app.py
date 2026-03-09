import os
import streamlit as st
from dotenv import load_dotenv

# Azure SDKs
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
from openai import AzureOpenAI

# Load .env if present (local dev)
load_dotenv()

# ---------------------------------------------------------------------------
# Config — read from environment, fall back to None for local mock mode
# ---------------------------------------------------------------------------
DOC_INTELLIGENCE_ENDPOINT = os.getenv("DOC_INTELLIGENCE_ENDPOINT")
DOC_INTELLIGENCE_KEY      = os.getenv("DOC_INTELLIGENCE_KEY")
AZURE_OPENAI_ENDPOINT     = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_KEY          = os.getenv("AZURE_OPENAI_KEY")
CHAT_MODEL                = os.getenv("CHAT_MODEL", "gpt-4o")   # your deployment name

AZURE_MODE = all([
    DOC_INTELLIGENCE_ENDPOINT,
    DOC_INTELLIGENCE_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
])

# ---------------------------------------------------------------------------
# Azure helpers
# ---------------------------------------------------------------------------

def analyse_document(file_bytes: bytes) -> dict:
    """
    Send document bytes to Azure Document Intelligence (prebuilt-read).
    Returns a dict with extracted text, page count, languages, and confidence.
    """
    client = DocumentAnalysisClient(
        endpoint=DOC_INTELLIGENCE_ENDPOINT,
        credential=AzureKeyCredential(DOC_INTELLIGENCE_KEY),
    )

    poller = client.begin_analyze_document("prebuilt-read", file_bytes)
    result = poller.result()

    # Collect full text across all pages
    full_text = ""
    page_count = len(result.pages)
    paragraph_count = 0

    for page in result.pages:
        for line in page.lines:
            full_text += line.content + "\n"
        paragraph_count += len(page.lines)

    # Languages detected
    languages = [lang.locale for lang in result.languages] if result.languages else ["unknown"]

    # Average word confidence (prebuilt-read exposes word-level confidence)
    confidences = []
    for page in result.pages:
        for word in page.words:
            confidences.append(word.confidence)
    avg_confidence = (
        f"{(sum(confidences) / len(confidences) * 100):.1f}%"
        if confidences else "N/A"
    )

    return {
        "full_text": full_text.strip(),
        "statistics": {
            "Pages": page_count,
            "Lines extracted": paragraph_count,
            "Avg word confidence": avg_confidence,
        },
        "languages": languages,
    }


def generate_insights(extracted_text: str) -> str:
    """
    Pass extracted text to Azure OpenAI and return a summary with key points.
    """
    client = AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_KEY,
    )

    system_prompt = (
        "You are a document analysis assistant. "
        "Given the extracted text of a document, provide:\n"
        "1. A concise executive summary (3-5 sentences)\n"
        "2. Key points as a bullet list (max 6 bullets)\n"
        "3. Document type inference (e.g. invoice, contract, report, letter)\n\n"
        "Format your response in clean Markdown."
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": f"Document text:\n\n{extracted_text[:8000]}"},
        ],
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content


# ---------------------------------------------------------------------------
# Mock fallbacks (local dev without Azure)
# ---------------------------------------------------------------------------

MOCK_ANALYSIS = {
    "full_text": "This is mock extracted text. Connect Azure Document Intelligence to see real content.",
    "statistics": {
        "Pages": 1,
        "Lines extracted": 5,
        "Avg word confidence": "95.0%",
    },
    "languages": ["en"],
}

MOCK_INSIGHTS = """\
**Executive Summary**

This is a mock analysis generated for local development. Connect Azure OpenAI to see real insights.

**Key Points**
- Document uploaded successfully
- Local development environment working
- Azure Document Intelligence not connected
- Azure OpenAI not connected
- Ready for Azure integration

**Document Type**

Unknown — mock mode active
"""

# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Document Intelligence Pipeline",
    page_icon="📄",
    layout="wide",
)

st.title("Document Intelligence Pipeline")
st.markdown("Upload a document for automated text extraction and AI-powered analysis.")

# Sidebar
with st.sidebar:
    st.header("Mode")
    if AZURE_MODE:
        st.success("Azure mode — live AI services")
    else:
        st.warning("Local mock mode\n\nSet env vars to enable Azure.")

    st.header("Tech Stack")
    st.code(
        "Python + Streamlit\n"
        "Azure Document Intelligence\n"
        "Azure OpenAI\n"
        "Docker + Terraform\n"
        "GitHub Actions"
    )

    st.header("About")
    st.info(
        "Extracts text with Azure Document Intelligence "
        "(prebuilt-read), then summarises with Azure OpenAI."
    )

# File upload
uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "jpg", "jpeg", "png"],
    help="Supported formats: PDF, JPG, JPEG, PNG",
)

if uploaded_file is not None:
    st.success(f"Uploaded: **{uploaded_file.name}** ({uploaded_file.size:,} bytes)")

    col1, col2 = st.columns(2)

    # ---- Document Analysis ------------------------------------------------
    with col1:
        st.subheader("Document Analysis")

        with st.spinner("Extracting text…"):
            if AZURE_MODE:
                try:
                    analysis = analyse_document(uploaded_file.getvalue())
                except Exception as e:
                    st.error(f"Document Intelligence error: {e}")
                    analysis = MOCK_ANALYSIS
            else:
                import time; time.sleep(0.8)   # simulate latency in mock mode
                analysis = MOCK_ANALYSIS

        st.markdown("**Statistics**")
        st.json(analysis["statistics"])

        st.markdown("**Languages detected**")
        st.write(", ".join(analysis["languages"]))

        with st.expander("View extracted text"):
            st.text(analysis["full_text"] or "No text extracted.")

    # ---- AI Insights -------------------------------------------------------
    with col2:
        st.subheader("AI Insights")

        with st.spinner("Generating insights…"):
            if AZURE_MODE:
                try:
                    insights = generate_insights(analysis["full_text"])
                except Exception as e:
                    st.error(f"Azure OpenAI error: {e}")
                    insights = MOCK_INSIGHTS
            else:
                import time; time.sleep(0.8)
                insights = MOCK_INSIGHTS

        st.markdown(insights)

else:
    st.info("Upload a document above to start.")

    st.markdown("""
    **How it works**

    1. Upload a PDF, JPG, or PNG
    2. Azure Document Intelligence extracts text, structure, and confidence scores
    3. Azure OpenAI summarises the content and identifies key points
    4. Results appear side by side in this interface
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:gray;'>Document Intelligence Pipeline • Azure AI Services</div>",
    unsafe_allow_html=True,
)
