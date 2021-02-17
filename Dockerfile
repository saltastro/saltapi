FROM python:3.8-slim

RUN mkdir -p /server/saltapi
WORKDIR /server/saltapi

RUN pip install --upgrade pip

COPY requirements.txt .
COPY . .
RUN pip install -r requirements.txt --extra-index http://pypi.cape.saao.ac.za/simple --trusted-host pypi.cape.saao.ac.za

EXPOSE 5001

CMD ["pytho", "run"]
