import streamlit as st

# Configure page
st.set_page_config(
    page_title="Document Intelligence Demo",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("Document Intelligence Demo")
    st.markdown("Upload documents for automated text extraction and analysis")
    
    # Sidebar
    with st.sidebar:
        st.header("About")
        st.info(
            "Demo features:\n"
            "- Azure Document Intelligence\n"
            "- Azure OpenAI integration\n"
            "- Containerized deployment\n"
            "- Infrastructure as Code"
        )
        
        st.header("Tech Stack")
        st.code(
            "Python + Streamlit\n"
            "Azure AI Services\n"
            "Docker + Terraform\n"
            "GitHub Actions"
        )
        
        st.header("Status")
        st.warning("LOCAL MODE - Using mock data\n\n(Azure integration in Step 4)")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a document",
        type=['pdf', 'jpg', 'jpeg', 'png'],
        help="Supported: PDF, JPG, JPEG, PNG"
    )
    
    if uploaded_file is not None:
        st.success(f"Uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
        
        # Create columns for results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Document Analysis")
            
            with st.spinner("Analyzing document..."):
                # MOCK DATA - will be replaced with Azure Document Intelligence
                mock_analysis = {
                    "Content Preview": f"[Mock] Content from {uploaded_file.name}...",
                    "Statistics": {
                        "Pages": 1,
                        "Tables": 0,
                        "Paragraphs": 5,
                        "Confidence": "95.5%"
                    },
                    "Languages": ["en"],
                    "Key-Value Pairs": {
                        "Document Type": "Sample",
                        "Status": "Mock Data"
                    }
                }
                
                st.json(mock_analysis)
                st.info("Note: This is mock data. Connect to Azure in Step 4.")
        
        with col2:
            st.subheader("AI Insights")
            
            with st.spinner("Generating insights..."):
                # MOCK DATA - will be replaced with Azure OpenAI
                mock_insights = """
                **Executive Summary**
                
                This is a mock analysis for local testing.
                
                **Key Points**
                - Document uploaded successfully
                - Local development environment working
                - Ready for Azure integration
                
                **Document Type**
                
                Sample document for testing the application flow
                
                **Notes**
                
                Currently running in local mock mode without Azure services
                
                **Next Steps**
                1. Complete Terraform setup (Step 3)
                2. Deploy Azure resources
                3. Connect application to Azure (Step 4)
                """
                
                st.markdown(mock_insights)
                st.info("Note: This is mock data. Connect to Azure OpenAI in Step 4.")
    
    else:
        # Welcome message when no file uploaded
        st.info("Upload a document above to see the analysis")
        
        st.markdown("""
        **How It Works**
        
        1. Upload a document (PDF, JPG, PNG)
        2. Extract text and structure with Azure Document Intelligence
        3. Analyze with Azure OpenAI for insights
        4. View results in this interface
        
        **Current Progress**
        
        - Step 1: Local app structure (CURRENT)
        - Step 2: Add helper files
        - Step 3: Terraform setup
        - Step 4: Azure integration
        - Step 5: GitHub Actions
        """)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Azure AI Services Demo"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()