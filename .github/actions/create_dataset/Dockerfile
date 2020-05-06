FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY .github/actions/create_dataset/create.py ./

CMD [ "python", "./create.py" ]