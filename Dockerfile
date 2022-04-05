FROM python:3.9.12

# WORKDIR /the/workdir/path # Tells Docker that this is where all the commands are going to run from 
WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . . 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]