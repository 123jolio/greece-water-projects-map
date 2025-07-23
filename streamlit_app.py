import streamlit as st
import sys
import os
import traceback

# Set page config at the very beginning
st.set_page_config(
    page_title="Greek Water Projects Map",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    # Add the current directory to the path so we can import map_projects
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # Try to import with error handling
    try:
        from map_projects import main
    except ImportError as e:
        st.error(f"❌ Failed to import map_projects: {e}")
        st.code(traceback.format_exc())
        raise
    
    # Run the main function
    if __name__ == "__main__":
        main()
        
except Exception as e:
    # Error handling with debug information
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
        try:
            st.code('\n'.join(os.listdir('.')))
        except Exception as dir_error:
            st.error(f"Could not list directory contents: {dir_error}")
        
        st.subheader("Full Traceback")
        st.code(traceback.format_exc())
    
    # Add a button to try again
    if st.button("🔄 Try Again"):
        st.experimental_rerun()
