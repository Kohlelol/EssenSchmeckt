# EssenSchmeckt
Repository für "EssenSchmeckt" von Gruppe 1 aus dem Software-Technik Praktikum 2024/25 der TUC

Voraussetzung: 
- Python Installation min 3.12
- git installiert

Repository Clonen

git clone --branch presenation https://github.com/Kohlelol/EssenSchmeckt.git

Requirements installieren:
pip install -r requirements.txt


OPTIONAL:

in settings.py  
DEBUG=False setzen
IP des Servers zu ALLOWED_HOSTS hinzufügen


SERVER STARTEN:
in den Ordner der Repository wechseln
cd Softwarepraktikum

User erstellen:
py manage.py createsuperuser

Server starten:
py manage.py runserver 0.0.0.0:8000


