# FSND: Deploy Flask App to Kubernetes Using EKS

## Python 3.9

- Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- Please also install pip3 with Python

## Prerequisites

**Initialize and activate a virtualenv using:**

- MacOS/Linux

```shell
python -m virtualenv env
source env/bin/activate
```

- Windows

```powershell
python -m virtualenv env
.\env\bin\activate.ps1
```

## How to launch application

1. Initialize and activate a virtualenv using (according to previous steps explained in README) and install the dependencies:

- MacOS/Linux

```shell
pip install -r requirements.txt
```

- Windows

```powershell
pip install -r requirements.txt
```

2. Run the development server:

- MacOS/Linux

```shell
export JWT_SECRET='myjwtsecret'
export LOG_LEVEL=DEBUG
export FLASK_APP=app
export FLASK_ENV=development
python3 main.py
```

- Windows with using PowerShell (in case of using 1 installed version of Python use **python**, otherwise use your version of **python3**)

```powershell
$env:JWT_SECRET = 'myjwtsecret'
$env:LOG_LEVEL = 'DEBUG'
$env:FLASK_APP = 'app'
$env:FLASK_ENV = 'development'
python .\main.py
```

## How to test instance

- MacOS/Linux

```shell
export TOKEN=`curl --data '{"email":"abc@xyz.com","password":"mypwd"}' --header "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`
curl --request GET 'http://localhost:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
```

- Windows

```powershell
$env:TOKEN=(Invoke-RestMethod -Uri http://localhost:8080/auth -Method POST -Body (@{"email"="abc@xyz.com";"password"="mypwd";}|ConvertTo-Json) -ContentType "application/json").token
Invoke-RestMethod -Uri http://localhost:8080/contents -Method GET -Headers @{"Authorization"="Bearer $($env:TOKEN)"}
```

## How to launch Dockerized application

- MacOS/Linux

```shell
docker build -t simple-flask .
docker run --name simpleflask --env-file=.env_file -p 8080:8080 simple-flask
```

- Windows

```powershell
docker build -t simple-flask .
docker run --name simpleflask --env-file=.env_file -p 8080:8080 simple-flask
```

## How to test Dockerized application

- MacOS/Linux

```shell
export TOKEN=`curl --data '{"email":"abc@xyz.com","password":"mypwd"}' --header "Content-Type: application/json" -X POST localhost:8080/auth  | jq -r '.token'`
curl --request GET 'http://localhost:8080/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
```

- Windows

```powershell
$env:TOKEN=(Invoke-RestMethod -Uri http://localhost:8080/auth -Method POST -Body (@{"email"="abc@xyz.com";"password"="mypwd";}|ConvertTo-Json) -ContentType "application/json").token
Invoke-RestMethod -Uri http://localhost:8080/contents -Method GET -Headers @{"Authorization"="Bearer $($env:TOKEN)"}
```

## References

- [AWS Documentation](https://docs.aws.amazon.com/)
- [Udacity](https://www.udacity.com/)
- [Stack Overflow](https://stackoverflow.com/)
