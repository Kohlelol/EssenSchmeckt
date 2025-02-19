# EssenSchmeckt
Repository für "EssenSchmeckt" von Gruppe 1 aus dem Software-Technik Praktikum 2024/25 der TUC
---
---
Voraussetzung: 
- Betriebssystem: Windows 10 oder 11
- Python Installation min 3.12
- git installiert

---

Repository Clonen:
git clone https://github.com/Kohlelol/EssenSchmeckt.git

---
Requirements installieren:
pip install -r requirements.txt

---
OPTIONAL:

in settings.py  
DEBUG=False setzen
IP des Servers zu ALLOWED_HOSTS hinzufügen, dann kann py manage.py runserver 0.0.0.0:8000 verwendet werden

---

SERVER STARTEN:
in den Ordner der Repository wechseln
cd Softwarepraktikum

---

Superuser erstellen:
py manage.py createsuperuser
-> Anweisungen in der Konsole befolgen

---

Server starten:
py manage.py runserver

---

Der Server ist erreichbar über
- 127.0.0.1:8000
- oder, wenn die IP in ALLOWED_HOSTS eingetragen wurde, die IP des PCs auf dem der Server läuft. Beachten: Chrome mit Flag --unsafely-treat-insecure-origin-as-secure=http://{IP}:8000


