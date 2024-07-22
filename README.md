# NewSearchPedia_BE

## How to Start

1. activate venv

```bash
python -m venv venv
source venv/Scripts/activate
```

2. dependency install

```bash
pip install -r requirements.txt
```

3. env 파일 만들기

4. migrate

```bash
python manage.py migrate --settings=newsearchpedia_be.settings.local
```

5. runserver

```bash
python manage.py runserver --settings=newsearchpedia_be.settings.local
```
