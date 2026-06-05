# Library API

Απαλλακτική εργασία για το μάθημα Τεχνολογία Λογισμικού 2025-26.

## Περιγραφή

Το project υλοποιεί ένα απλό REST API για εφαρμογή βιβλιοθήκης με Python και Flask. Κάθε βιβλίο έχει τα πεδία:

- id
- title
- author
- year

Τα δεδομένα αποθηκεύονται σε αρχείο `books.json`.

## Λειτουργίες API

- `GET /books` - επιστρέφει όλα τα βιβλία
- `GET /books/<id>` - επιστρέφει ένα βιβλίο με βάση το id
- `POST /books` - δημιουργεί νέο βιβλίο
- `DELETE /books/<id>` - διαγράφει ένα βιβλίο

## Εκτέλεση τοπικά

```bash
pip install -r requirements.txt
python app.py
```

Η εφαρμογή εκτελείται στο:

```text
http://localhost:5000
```

## Εκτέλεση tests

```bash
pytest --cov=app --cov-report=term-missing
```

## Εκτέλεση με Docker

```bash
docker build -t library-api .
docker run -p 5000:5000 library-api
```

## GitHub Actions

Το αρχείο `.github/workflows/python-tests.yml` εκτελεί αυτόματα τα unit tests κάθε φορά που γίνεται push ή pull request.
