# Use the Python 3.12.4 image
FROM python:3.12.4-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application
COPY . .

# Set the command to run the app (adjust this depending on how you run your app)
CMD ["python", "manage.py", "runserver"]
