FROM python:latest
RUN pip install neo4j
COPY tp2.py ./
CMD ["python", "-u", "tp2.py"]