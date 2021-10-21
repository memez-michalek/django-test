## Python/Django Developer Test
---
Simple Django project prepared for recruitment process.

Please clone this clean repository into your workspace, do some work and create a pull request.



### Requirements
---
- Python 3.7
- pipenv (https://github.com/pypa/pipenv)




### Project setup
---
##### Environment
Execute in project's root directory:

```
pipenv sync
```

Since now you can switch to virtual environment created by pipenv. To do so run `pipenv shell` command.

Otherwise you would have to add `pipenv run` prefix to every python-related command executed
within project's directory tree (see below).

##### Database setup
Execute in project's root directory:

```
pipenv run python manage.py migrate
pipenv run python manage.py createsuperuser
```

or

```
pipenv shell
./manage.py migrate
./manage.py createsuperuser
```

##### Start the app
Execute in project's root directory:
```
pipenv shell
./manage.py runserver
```



### Other tools
Please run a linter before pushing to the repo. To do so simply execute:
```
pipenv run flake8
```
...add fix any issues.



### Tasks
---
The goal of the exercise is to create a system that tracks various events like clicks, page views, etc. Please complete the following tasks in a given order. Preferably you should prepare a separate commit for every task.

1. Create `analytics.models.Event` model with given fields: 
    * `name` - required non-empty string, maximum length equal to 255 characters,
    * `created_at` - required date of creation, automatically set to "now",
    * `additional_data` - optional text.
2. Add `Event` model to the Django Admin panel.
3. In admin panel: make `Event` model searchable by `name`.
4. Add REST endpoint `POST /api/events` that allows to create an `Event` with given `name` and `additional_data`. Implement any validations, views, forms and serializers needed. It's up to you. **Remember about tests**.
5. Extend existing `User` model (`django.contrib.auth.models.User`) with new field:
    * `api_token` - optional string, maximum length equal to 100, unique.
6. Extend existing `Event` model (`analytics.models.Event`) with new field:
    * `created_by` - required foreign key pointing to `User`
7. Update `POST /api/events` endpoint. From now on it should check the `Authorization` HTTP Header of every incoming request. In case of missing or invalid `Authorization` header it should return an error with HTTP Code `401 Unauthorized`. Valid `Authorization` header looks like this: `Authorization: Bearer API_TOKEN`, where `API_TOKEN` is an existing `api_token` provided for any existing `User` (see point 5). Newly created event's `created_by` field should be set to `User` whose `API_TOKEN` has been provided in the `Authorization` header. **Remember about tests**.
8. In Admin panel: make `Event` searchable by `created_by.username` in addition to `name` implemeted in point 3.

Extending `User` model can be tricky. You are allowed to prepare your own `User` model based on `django.contrib.auth.models.AbstractUser` and override `AUTH_USER_MODEL`. You can also create a separate model for `API Tokens` and link to existing users. It's up to you.

*Optional* things to consider:
1. Djagno REST Framework (https://github.com/encode/django-rest-framework),
2. Move `Authorization: Bearer API_TOKEN` evaluation to middleware.
