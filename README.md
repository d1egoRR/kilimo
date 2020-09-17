# kilimo


python manage.py loaddata fixtures/FieldTerrain.json
python manage.py loaddata fixtures/Rain.json


export DJANGO_SETTINGS_MODULE=rainfalls.settings.dev

`pycodestyle . --exclude=migrations,venv,settings`