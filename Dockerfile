# use official python as parent img
FROM python:3.12

# set the working directory in the container
WORKDIR /usr/src/app

# copy the current directory contents into the container
COPY . .

# check if we are running in container, if not use default path
ENV RUNNING_IN_CONTAINER=true 
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app/src"
ENV NAME World

# install any needed packages specified in setup.py
RUN pip install --no-cache-dir -e .

# run the package
CMD ["swpackage"]
