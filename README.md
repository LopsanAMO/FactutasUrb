# FactutasUrb

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/cc99ef6ca6c951e33537#?env%5Burbvan__env%5D=W3sia2V5IjoibG9jYWxfdXJsIiwidmFsdWUiOiJodHRwOi8vbG9jYWxob3N0OjgwMDAvIiwiZGVzY3JpcHRpb24iOiIiLCJ0eXBlIjoidGV4dCIsImVuYWJsZWQiOnRydWV9XQ==)

## instalacion del entorno virtual con virtuelenv
```bash
$ pip install virtualenv
````

## Creacion y Activacion del entorno virtual
```bash
$ virtualenv -p python3 venv
$ source venv/bin/activate
````

## Clonar el proyecto
```bash
$ git clone https://github.com/LopsanAMO/FactutasUrb.git
$ cd FactutasUrb
```

# Instalación de las dependencias
```bash
$ pip install -r requirements.txt
```

# Ejecutar el proyecto
```bash
$ python manage.py migrate
$ python manage.py runserver 0.0.0.0:8000
```
