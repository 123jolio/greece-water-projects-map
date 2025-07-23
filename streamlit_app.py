# This file is the entry point for Streamlit Cloud
import sys
import os
import traceback

# Add the current directory to the path so we can import map_projects
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Try to import with error handling
    try:
        from map_projects import main
    except ImportError as e:
        st.error(f"Failed to import map_projects: {e}")
        st.code(traceback.format_exc())
        raise
    
    # Set page config at the very beginning
    st.set_page_config(
        page_title="Greek Water Projects Map",
        page_icon="🌊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the main function
    if __name__ == "__main__":
        main()
        
except Exception as e:
    import streamlit as st
    
    # Basic error display
    st.error("## 🚨 An error occurred while running the app")
    st.exception(e)
    
    # Debug information
    with st.expander("🔍 Debug Information"):
        st.subheader("System Information")
        st.write(f"Python version: {sys.version}")
        st.write(f"Streamlit version: {st.__version__}")
        try:
            import pandas as pd
            st.write(f"Pandas version: {pd.__version__}")
        except ImportError:
            st.write("Pandas: Not installed")
            
        st.subheader("Environment")
        st.write(f"Working directory: {os.getcwd()}")
        st.write("Files in directory:")
        st.code('\n'.join(os.listdir('.')))
        
        st.subheader("Full Traceback")
        st.code(traceback.format_exc())
    
    # Add a button to try again
    if st.button("🔄 Try Again"):
        st.experimental_rerun()
