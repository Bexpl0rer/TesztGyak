# Számösszegző – Futtatási útmutató és tesztriportok

## 1. Az alkalmazás futtatása

A parancsokat a projekt gyökérkönyvtárában kell kiadni.

**1. Virtuális környezet létrehozása:**

```bash
python -m venv .venv
```

**2. Virtuális környezet aktiválása (Windows Git Bash):**

```bash
source .venv/Scripts/activate
```

PowerShell esetén:

```powershell
.\.venv\Scripts\Activate.ps1
```

**3. Függőségek telepítése:**

```bash
python -m pip install -r requirements.txt
```

**4. Flask-alkalmazás indítása:**

```bash
python app.py
```

A webes felület címe: **http://127.0.0.1:5000/**. A szervert hagyjuk futni a böngészős, Postman- és terheléses tesztek alatt.

Opcionálisan, telepített Waitress esetén a Flask fejlesztői szervere helyett:

```bash
waitress-serve --host=127.0.0.1 --port=5000 --threads=8 app:app
```

## 2. A tesztek futtatása

A tesztparancsokat egy második, aktivált virtuális környezetű terminálban adjuk ki.

### Unit- és API-validációs tesztek

```bash
python -m pytest tests/test_unit.py -v
```

### BDD-tesztek (pytest-bdd)

```bash
python -m pytest tests/test_bdd.py -v
```

Az unit- és BDD-tesztekhez nem szükséges külön futó Flask-szerver.

### Selenium UI-tesztek

Indítsuk el a Flask alkalmazást, és gondoskodjunk a `tests/test_ui.py` beállításának megfelelő böngészőről és WebDriverről. Ezután:

```bash
python -m pytest tests/test_ui.py -v
```

### Összes pytest-teszt

A Selenium UI-tesztekhez az alkalmazásnak futnia kell. Ekkor:

```bash
python -m pytest -v
```

### Postman API-tesztek

1. Indítsuk el az alkalmazást.
2. A Postmanben importáljuk a `postman_collection.json` fájlt.
3. Ellenőrizzük, hogy a kérések a `http://127.0.0.1:5000` címet használják.
4. A **Collection Runner** segítségével, a megadott sorrendben futtassuk a collection összes kérését.
5. Az eredményeket a **Test Results** nézetben tekintsük meg.

### Locust terheléses teszt

Indítsuk el az alkalmazást (például Waitress-szel), majd egy második terminálban:

```bash
python -m locust -f test_load.py --host http://127.0.0.1:5000
```

Nyissuk meg a **http://localhost:8089/** címet. Például **20 felhasználó** és **5 felhasználó/másodperc** beállítással indítsuk el a tesztet, majd a `POST /api/numbers` sorban **legalább 1000 kérés** után állítsuk le. A mérési eredmények a Locust felületén láthatók; a szkript külön riportfájlt nem készít.

*A Locust futtatásához olyan környezet szükséges, ahol a függőségei engedélyezettek.*

## 3. Tesztriportok és eredmények

### pytest-riport

A korábban végrehajtott teljes tesztfuttatás eredménye (**2026. november 19.**):

```text
12 passed in 6.87s
```

| Tesztfájl | Sikeres tesztek | Sikertelen tesztek |
|---|---:|---:|
| `tests/test_unit.py` | 6 | 0 |
| `tests/test_bdd.py` | 4 | 0 |
| `tests/test_ui.py` | 2 | 0 |
| **Összesen** | **12** | **0** |

Az aktuális futtatásról külön **JUnit XML riport** készíthető:

```bash
python -m pytest -v --junitxml=pytest_report.xml
```

A riport a projekt gyökérkönyvtárában `pytest_report.xml` néven jön létre.

### Postman-riport

A collection **5 API-kérést és 10 automatikus ellenőrzést** tartalmaz. A tényleges eredmények a **Collection Runner / Test Results** nézetben láthatók; a sikeres futtatás képernyőképpel dokumentálható. A teljes collection sikerességéről nincs külön igazolt futtatási eredmény.

### Locust-riport

A **Statistics** és **Charts** nézetben ellenőrizhető a kérések száma, a hibák száma, a válaszidő és a másodpercenkénti kérésszám. A beadandóhoz az **1000+ POST-kérést** bemutató képernyőkép használható. Igazolt, éles Locust-mérési eredmény még nem áll rendelkezésre.
