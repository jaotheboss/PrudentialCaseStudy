# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY /data/. ./data/.
COPY /requirements.txt ./requirements.txt
COPY /utils.py ./utils.py
COPY /app.py ./app.py

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
