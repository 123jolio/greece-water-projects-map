# This file is the entry point for Streamlit Cloud
try:
    from map_projects import main
    
    if __name__ == "__main__":
        main()
except Exception as e:
    import traceback
    import streamlit as st
    
    st.error("An error occurred while running the app:")
    st.exception(e)
    st.text("\nFull traceback:")
    st.code(traceback.format_exc())
    
    # Add debug information
    st.sidebar.subheader("Debug Information")
    st.sidebar.write("Python version:", st.__version__)
    st.sidebar.write("Pandas version:", pd.__version__ if 'pd' in globals() else 'Not loaded')
    st.sidebar.write("Working directory:", os.getcwd())
    st.sidebar.write("Files in directory:", ", ".join(os.listdir('.')))
    
    raise e
