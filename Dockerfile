FROM python:latest
RUN pip install neo4j
COPY tp2mt.py ./
CMD ["python", "-u", "tp2mt.py"]