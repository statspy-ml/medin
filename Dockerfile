# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install fastapi[all] openai nltk python-dotenv uvicorn google-cloud-bigquery jinja2 aiofiles python-multipart
    

RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt')"
   

# Make port 80 available to the world outside this container
EXPOSE 80

# Run uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

