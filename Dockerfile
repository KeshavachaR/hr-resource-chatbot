# Base image with Python
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl wget git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install Python requirements
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit sentence-transformers faiss-cpu

# Expose ports: Streamlit (7860) + FastAPI (8000)
EXPOSE 7860 8000

# Preload Llama3 model
RUN ollama pull llama3

# Start both FastAPI and Streamlit inside the same container
CMD bash -c "uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
             streamlit run frontend/streamlit_app.py --server.port 7860 --server.address 0.0.0.0"
