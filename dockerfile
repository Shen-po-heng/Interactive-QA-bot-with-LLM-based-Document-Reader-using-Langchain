# Use the official Python 3.10 base image
FROM python:3.10-slim

# Set environment variables to avoid Python buffering and set working directory
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . /app/

# Expose the port that the Gradio app will run on
EXPOSE 7860

# Command to run the Gradio app when the container starts
CMD ["python", "app.py"]
