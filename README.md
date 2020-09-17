# kilimo API

## Índice ##

1. Instalación
2. Ejecutar
3. IMportar datos desde fixtures
4. Ejecutar Tests
5. Code Style
6. Ejemplos de la API


### 1. Instalación ###

- **Crear el virtualenv y activarlo:** `python3 -m venv myvirtual`
- **Clonar el Proyecto.**
- **Instalar las dependencias dev:** `pip install -r requirements/dev.txt`
- **Setear variable de entorno:** `export DJANGO_SETTINGS_MODULE=rainfalls.settings.dev`
- **Migrate:** `python manage.py migrate`
- **Crear superuser:** `python manage.py createsuperuser`


### 2. Ejecutar ###

- **Activar el virtualvenv:** `/path/to/virtualvenv/activate`
- **Setear variable de entorno:** `export DJANGO_SETTINGS_MODULE=rainfalls.settings.dev`
- **Ejecutar el servidor:** `python manage.py runserver`
- **Ir al navegador:** `http://localhost:8000`, `http://localhost:8000/admin`
- **Swagger:** `http://localhost:8000/swagger`


### 3. Importar datos desde fixtures ###

- **Setear variable de entorno:** `export DJANGO_SETTINGS_MODULE=rainfalls.settings.dev`
- **FieldTerrain (Campos)**: `python manage.py loaddata fixtures/FieldTerrain.json`
- **Rains**: `python manage.py loaddata fixtures/Rain.json`


### 4. Ejecutar Tests ###

- Ejecutar: `pytest`
- Coverage: `pytest --cov`


### 5. Code Style ###

**Para verificar que el código cumpla con PEP8 se puede ejecutar pycodestile.**
**Para esto hay que posicionarse en la raíz del proyecto y ejecutar lo siguiente:**

`pycodestyle .`

**Para este chequeo podemos excluir archivos y directorios:**

`pycodestyle . --exclude=migrations,venv,settings`


### 6. Ejemplos de la API ###

**Solo se muestran algunos ejemplos. El resto de los endpoints se puede consultar con swagger**
`http://localhost:8000/swagger`

- **Listado de lluvias por campos:**

`GET /api/app/v1/fieldterrains/<uuid:uuid>/rains`

Devuelve:

```json
[
    {
        "id": 1,
        "uuid": "4e774f60-dd93-4669-b001-44fd11d37f04",
        "rain_date": "2020-09-15",
        "milimeters": "55.00",
        "created_at": "2020-09-16",
        "fieldterrain": 1
    },
    {
        "id": 2,
        "uuid": "fe627bda-3c50-4049-9ff9-6570c76545dc",
        "rain_date": "2020-09-14",
        "milimeters": "130.00",
        "created_at": "2020-09-16",
        "fieldterrain": 1
    },
    ...
]
```

- **Listado de campos con acumulación de lluvia mayor a x milímetros:**

`GET /api/app/v1/fieldterrains/cumulative-rain-greater-than/<int:milimeters>`

Devuelve:

```json
[
    {
        "id": 3,
        "average_rain": null,
        "uuid": "8a8ad76b-361d-47cc-b5b8-f5dc779210a1",
        "name": "Campo 3",
        "hectares": 1800,
        "latitude": 0.0,
        "longitude": 0.0
    }
    ...
]
```


- **Listado de campos con promedio de lluvia en los últimos x días:**

`GET /api/app/v1/fieldterrains/average-rain/<int:days>`

Devuelve:

```json
[
    {
        "id": 1,
        "average_rain": 87.26,
        "uuid": "45a508df-c424-4d79-8d5e-742ce81bb68c",
        "name": "Campo 1",
        "hectares": 5500,
        "latitude": 0.0,
        "longitude": 0.0
    },
    ...
]
```
