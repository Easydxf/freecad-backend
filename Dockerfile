# Base image with FreeCAD already set up
FROM ghcr.io/freecad/freecad:latest

# Set working directory
WORKDIR /app

# Copy your code
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the FastAPI app
EXPOSE 10000

# Run your FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
