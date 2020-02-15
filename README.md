# Suministros Puerto Rico

https://suministrospr.com

## Development

```bash
# Install pipenv (https://pipenv.kennethreitz.org/en/latest/install/#installing-pipenv)
$ pip install --user pipenv

# Install project dependencies
$ pipenv install --dev

# Install pre-commit hooks
$ pipenv run pre-commit install

# Copy example environment variables to proper file
$ cp example.env .env

# Run Django database migrations
$ pipenv run python manage.py migrate

# Run local server
$ pipenv run python manage.py runserver_plus
```

### Docker

```bash
$ docker-compose up --build
```

#### Importing data

1. Unarchive [data extract](https://github.com/Code4PuertoRico/suministrospr/issues/8#issuecomment-573977666) to `./data/scraped/*.json`

2. Run the import_data command:

```bash
$ docker-compose exec web python manage.py import_data ./data/scraped
```

### Deployment

```bash
git push heroku master
```

#### Clearing cache

```bash
heroku run python manage.py clear_cache
```

#### Update i18n locale strings

1.  Extract i18n strings with:

```bash
$ docker-compose exec web django-admin makemessages -l en
```

2. Update local strings with the translated text on the files located at `suministrospr/locale`

For example:
```text
#: suministrospr/suministros/templates/suministros/suministro_form.html:36
msgid "Municipio"
msgstr "Municipality""
```
3. Compile strings and generate `.mo` files with:

```bash
docker-compose exec web django-admin compilemessages
```
