FROM public.ecr.aws/lambda/python:3.8

# Installing the function's dependencies using file requirements.txt
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
CMD [ "lambda_function.lambda_handler" ]