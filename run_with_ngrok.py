from pyngrok import ngrok
import subprocess
import time
import os

def main():
    # Set your ngrok authtoken if you have one
    # ngrok.set_auth_token("your_auth_token_here")
    
    # Start Streamlit in a separate process
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "map_projects.py", "--server.port", "8501", "--server.address", "0.0.0.0"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give Streamlit a moment to start
    time.sleep(2)
    
    try:
        # Create an HTTP tunnel on port 8501
        public_url = ngrok.connect(addr="8501", proto="http", bind_tls=True)
        print(f"Streamlit app is running at: {public_url}")
        print("Press Ctrl+C to stop")
        
        # Keep the script running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Shutting down...")
        ngrok.kill()
        streamlit_process.terminate()
        print("Done!")

if __name__ == "__main__":
    main()
