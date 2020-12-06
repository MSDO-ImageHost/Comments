# For reference: https://www.docker.com/blog/containerized-python-development-part-1/
# This dockerfile will run the tests.

# set base image (host OS)
FROM python:3.9

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the content
COPY . .

# command to run on container start
CMD [ "python", "./tests.py" ]
