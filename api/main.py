import streamlit as st
import os
from azure_services import AzureAIServices
from utils import setup_logging, format_analysis_result
import logging

# Configure page
st.set_page_config(
    page_title="AI Document Processor",
    page_icon="📄",
    layout="wide"
)

# Initialize logging
logger = setup_logging()

@st.cache_resource
def get_azure_services():
    """Initialize Azure AI services (cached for performance)"""
    try:
        return AzureAIServices()
    except Exception as e:
        st.error(f"Failed to initialize Azure services: {str(e)}")
        return None

def main():
    st.title("🤖 AI Document Processing Demo")
    st.markdown("Upload a document to extract text and generate AI insights")
    
    # Sidebar for info
    with st.sidebar:
        st.header("📋 About")
        st.info(
            "This demo showcases:\n"
            "- Azure Document Intelligence\n"
            "- Azure OpenAI integration\n"
            "- Containerized deployment\n"
            "- Infrastructure as Code"
        )
        
        st.header("🔧 Tech Stack")
        st.code(
            "• Python + Streamlit\n"
            "• Azure AI Services\n"
            "• Docker + Terraform\n"
            "• GitHub Actions CI/CD"
        )
    
    # Initialize services
    azure_services = get_azure_services()
    if not azure_services:
        st.stop()
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a document",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Supported formats: PDF, JPG, JPEG, PNG"
    )
    
    if uploaded_file is not None:
        # Display file info
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Create columns for results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Document Analysis")
            
            with st.spinner("Analyzing document..."):
                try:
                    # Analyze document
                    analysis_result = azure_services.analyze_document(uploaded_file.getvalue())
                    
                    if analysis_result and not analysis_result.get('error'):
                        # Display formatted results
                        formatted_result = format_analysis_result(analysis_result)
                        st.json(formatted_result)
                        
                        # Store in session state for AI processing
                        st.session_state.document_content = analysis_result.get('content', '')
                        
                    else:
                        st.error("Failed to analyze document")
                        
                except Exception as e:
                    logger.error(f"Document analysis error: {e}")
                    st.error(f"Analysis failed: {str(e)}")
        
        with col2:
            st.subheader("🧠 AI Insights")
            
            if hasattr(st.session_state, 'document_content') and st.session_state.document_content:
                with st.spinner("Generating AI insights..."):
                    try:
                        # Generate insights using OpenAI
                        insights = azure_services.generate_insights(st.session_state.document_content)
                        st.markdown(insights)
                        
                    except Exception as e:
                        logger.error(f"AI insights error: {e}")
                        st.error(f"Failed to generate insights: {str(e)}")
            else:
                st.info("Upload and analyze a document first to see AI insights")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with Azure AI Services, Streamlit, and ❤️"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()