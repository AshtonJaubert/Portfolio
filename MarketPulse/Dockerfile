# Use AWS Lambda base image for Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# 1. Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# 2. Install packages
# We assume the base image has pip installed
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# 3. Download NLTK data inside the container build
RUN python3 -m nltk.downloader -d ${LAMBDA_TASK_ROOT}/nltk_data vader_lexicon

# 4. Copy app code
COPY main.py ${LAMBDA_TASK_ROOT}

# 5. Set the CMD to your handler
CMD [ "main.handler" ]