FROM freecad/freecad-container:conda-python-3.10

WORKDIR /app

COPY ./app /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
