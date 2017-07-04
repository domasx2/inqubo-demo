FROM python:3.6
RUN mkdir examples
WORKDIR examples
RUN pip install git+https://github.com/domasx2/inqubo.git
ENV PYTHONBUFFERED 1
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh wait-for-it.sh
RUN chmod a+x wait-for-it.sh
COPY *.py ./
