## Get Started

Copy `.streamlit/secrets.example.toml` to `.streamlit/secrets.toml` and fill in your DICT_API_KEY API key.
You can get your free API key from [Merriam-Webster Dictionary API](https://dictionaryapi.com/).

### Docker

Start the container:
```
docker compose up -d
```

Stop the container:
```
docker compose down
```

### Local Development

Prerequisites:
- Python 3.12
- Pipenv

Install dependencies:
```
pipenv install
```

Run the app:
```
pipenv run streamlit run main.py
```


