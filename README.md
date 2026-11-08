# rmatics-back

## Deploying via Ansible

```
ansible-playbook -i 'ansible/hosts' \
--extra-vars "target_server=stage" \
ansible/main.yml
```

## Configuring app

### Settings

Global environment should be passed in different ways depending on boot method:

1. **WSGI** via wsgi.py reads `FLASK_ENV` variable and selects appropriate config class.
2. **flask run** via console or PyCharm configuration reads `FLASK_APP` var, which should point to app with running config module e.g `informatics_front:create_app('informatics_front.config.DevConfig')`  
3. **pytest** automaticaly runs base `informatics_front.config.TestConfig`.

App-specific settings should be provided as env vars along with `FLASK_ENV` and `FLASK_APP`. A complete list of supported ones can be found in `informatics_front/config.py`. 

App should be set as pointer to factory method with appropriate config:

```
FLASK_APP=informatics_front.app_factory:create_app('informatics_front.config.DevConfig')
```

### Database schemas

* `ejudge`;
* `moodle`;
* `pynformatics` — primary.

The test configuration also connects to an `informatics` database, but production has no such schema:
every model names its schema explicitly.

### Database migration

Ensure DB connection string points to primary migration DB. Note `/pynformatics` at the end.

```
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:@localhost/pynformatics
```

Remove any pre-existing tables:

```
drop database refresh_token;
```

We use utf8 character set. Any previously created DB with different charset should be converted:

```
ALTER DATABASE pynformatics CHARACTER SET utf8 COLLATE utf8_unicode_ci;
```

Then update to current schema:

```
flask db upgrade
```

After modifying models:

```
# generate new migrations
flask db migrate


# ensure corresponing pkeys and migrate
flask db upgrade
```

#### Deprecated

1. Convert `moodle.mdl_statements` to InnoDB (refrenced by `contest_instance`):
    ```
    ALTER TABLE moodle.mdl_statements ENGINE = InnoDB;
    ```
    
    Refrenced tables should be the same engine type (InnoDB) as parent;
2. Ensure all FKey refs are described with correspnding types in migrations:
    ```
    from sqlalchemy.dialects.mysql import BIGINT
    ...
    sa.Column('contest_id', BIGINT(display_width=10, unsigned=True), nullable=True), # <-> for
    ```
    or similar. FKey types should be the same type as PKeys e.g. (`bigint(10) unsigned`);
 
## Stack

Python 3.13, Flask 3.1, SQLAlchemy 2.1 with Flask-SQLAlchemy 3.1, marshmallow 4, webargs 8, PyJWT 2, PyMySQL.
Dependencies are in `requirements.in` (direct) and `requirements.txt` (pinned, generated); dev ones in `requirements-dev.*`.

The service does not use MongoDB or Redis. Its database is the production MariaDB 10.3 (schemas `moodle`,
`ejudge`, `pynformatics`); connect with `?charset=utf8` as before.

Run it with gunicorn (see `Dockerfile`):

```
gunicorn --bind 0.0.0.0:12347 --workers 4 informatics_front.wsgi:application
```

## Running tests

### Docker (MariaDB 10.3, like production)

Build and run tests container with provided docker-compose file:

```
docker compose --file docker/docker-compose.yml up --build --abort-on-container-exit --exit-code-from tests
```

If all tests are passed, the Docker process will exit with code 0.

### Quick local run on SQLite

For a fast check without a database server, with the dev requirements installed:

```
SQLALCHEMY_DATABASE_URI=sqlite:// FLASK_ENV=testing JWT_TOKEN_EXP=900 JWT_REFRESH_TOKEN_EXP=14400 \
SERVER_NAME=app.test pytest informatics_front/tests
```

`informatics_front/tests/conftests/sqlite_schemas.py` attaches the three schemas as separate SQLite files.
It is a shortcut, not a substitute for the MariaDB run: foreign keys and `ON DELETE CASCADE` are not enforced.

Tests marked `xfail` fail on `master` as well (stale expectations); each carries its reason.