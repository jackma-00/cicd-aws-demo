FROM public.ecr.aws/lambda/python:3.10

ARG SHA

ENV SHA=${SHA}

COPY ./setup.py .
 
RUN pip install --no-cache-dir --upgrade --target "${LAMBDA_TASK_ROOT}" .

COPY ./src "${LAMBDA_TASK_ROOT}"/src

CMD ["src.lambda_function.lambda_handler"]
