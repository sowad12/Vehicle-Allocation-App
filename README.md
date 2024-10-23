
## Table of Contents
- [Requirements](#Requirements)
- [Installation](#Installation)
- [Docker_Pull](#Docker_Pull)
- [Deploy and maintain this project](#Short_brief)

# Requirements
Python 3.12 and Later
Mongodb 
# Installation
```bash
#Navigate to the project directory
cd exsited-python

# Install virtualenv
pip install virtualenv

# Create Virtual Environment
python -m venv venv

# Active virtual Environment from windows
venv\Scripts\activate

# Upgrade the pip
python -m pip install --upgrade pip

# Install all modules
pip install -r requirments.txt

uvicorn main:app --reload    


```
# Docker_Pull
docker pull sowad/allocation:v1
docker run -d -p 8000:8000 sowad/allocation:v1

# Short_brief
To deploy this FastAPI project, I would push the Docker images to a container registry like Docker Hub and use a cloud platform such as AWS or Google Cloud for orchestration. For maintenance, I would implement monitoring tools to track application performance, schedule regular backups of the Redis database, and ensure that dependencies are updated periodically to maintain security and stability.


