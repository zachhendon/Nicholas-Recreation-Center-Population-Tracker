# AWS/python base image
FROM public.ecr.aws/lambda/python:3.9

# Copy files 
COPY . ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Runs the handler function in DataGatherer.py when run
CMD [ "DataGatherer.handler" ] 
