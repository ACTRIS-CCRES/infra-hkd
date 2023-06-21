# CCRES API

CCRES API Project

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: GPLv3

## Settings

They are based on the cookiecutter settings  : 

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

Project specific settings are also defined : 
### Grafana settings 

| Environment Variable  | Django Setting        | Description                                                                   |
|-----------------------|-----------------------|-------------------------------------------------------------------------------|
| GRAFANA_URL           | GRAFANA_URL           | Grafana Url                                                                   |
| GRAFANA_AUTH_USERNAME | GRAFANA_AUTH_USERNAME | Grafana username if basic authentification (needs also GRAFANA_AUTH_PASSWORD) |
| GRAFANA_AUTH_PASSWORD | GRAFANA_AUTH_PASSWORD | Grafana password if basic authentification (needs also GRAFANA_AUTH_USERNAME) |
| GRAFANA_AUTH_TOKEN    | GRAFANA_AUTH_TOKEN    | Grafana API Token                                                             | 
               
## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy CCRES API

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

## Deployment

The following details how to deploy this application.
