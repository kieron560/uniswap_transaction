FROM python:3.12

# Set working directory in the container
WORKDIR /app

# Copy requirements.txt file to install dependencies
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . /app/

# Expose the port that the app will run on
EXPOSE 5000

# Command to run Gunicorn with 4 workers
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]