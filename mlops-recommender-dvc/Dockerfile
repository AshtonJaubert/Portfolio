# Dockerfile

# 1. Use a standard Python 3.11 slim image as the base
FROM python:3.11-slim

# 2. Set environment variables to prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the requirements file and install dependencies
COPY requirements.txt .

# 4a. INSTALL BUILD DEPENDENCIES (THIS IS THE NEW STEP)
# This step installs the necessary compiler and development headers for libraries like scikit-surprise
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 4b. Install Python Libraries
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install fastapi uvicorn[standard]

# 5. Copy the application code (app.py) and the trained model file
COPY app.py ./
COPY models/recommender.pkl models/recommender.pkl

# 6. Define the command to run the application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]