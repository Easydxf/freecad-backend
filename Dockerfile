FROM freecad/freecad-container:conda-python-3.10

# Create working directory
WORKDIR /app
COPY . /app

# Install FastAPI + Uvicorn
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn

# Expose the port for FastAPI
EXPOSE 10000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
