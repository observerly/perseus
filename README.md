# Perseus API

The python FastAPI of stars, galaxies and other astronomical bodies.

## API Development

### Project Requirements

- [Docker](https://www.docker.com/).
- [Docker Compose](https://docs.docker.com/compose/install/).
- [Poetry](https://python-poetry.org/) for Python package and environment management.

### Installing Dependencies

The Perseus project manages Python package dependencies using [Poetry](https://python-poetry.org/). You'll need to follow the instructions for installation there.

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

**N.B.** For development with vscode you will need to run the following command:

```console
$ poetry config virtualenvs.in-project true
```

This will installed the poetry `.venv` in the root of the project and allow vscode to setup the environment correctly for development.

To start development, install all of the dependencies as:

```console
$ poetry install
```

**N.B.** _Ensure that any dependency changes are committed to source control, so everyone has a consistenct package dependecy list._

### Local Development

The Perseus stack can be started with the following `docker` `compose` command:

```console
$ docker compose -f local.yml up --build
```

### Alembic Migrations

The Perseus project utilises the database toolkit SQLAlchemy and the database migration tool Alembic. Alembic is hosted on GitHub at [https://github.com/sqlalchemy/alembic](https://github.com/sqlalchemy/alembic) under the SQLAlchemy organization.

The most recent published version of the Alembic documentation should be at https://alembic.sqlalchemy.org.

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

The process for changes to, or additions of, any models associated with this project is as follows:

- Start an interactive shell session in the api container:

```console
$ docker compose -f local.yml exec api bash
```

- If you created a new model in `.app/models/`, make sure to import it in `.app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

- After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "feat: Added Body model (e.g., Star, Galaxy, Nebulae etc.)"
```

- Make sure to commit to the git repository the files generated in the alembic directory\*.

- After creating the revision, run the migration in the database (this is what will actually change the database schema):

```console
$ alembic upgrade head
```

**N.B.** _All Alembic model "revisions" (changes) should be committed to source control, so everyone has a consistent database schema history._
