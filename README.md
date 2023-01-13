# Skripsi Agnes
Agnes Carolina
825190023


## Instalation
1. Install requirement
``` bash
    pip install -r requirements.txt
```

2. Run Migration
``` python

    from app import app, db
    with app.app_context():
        db.create_all()

```
3. Configure config in app/__init__.py

4. Run Server
``` bash
    python run.py
```

Good Luck Agnes !!! :)
