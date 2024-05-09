# README #

## Vendor Management Backend API Service ##

REST-ful web service developed in Python-Django

### Pre-requisites ###

- Python 3.10 or higher

### How do I get set up? ###

Install Python with supporting libraries and package manager.

```bash
# Install python with its package manager 'pipenv'.
$ sudo apt install python3 python3-pip
$ sudo python3 -m pip install pipenv
$ sudo apt install python3-dev libpq-dev
```

Clone and build

```bash
# Clone from git repository and move to cloned directory.
$ cd <your workspace>
$ git clone git@github.com:pallav-m/Django-assignment.git
$ cd Django-assignment
```

### How do I build? ###

#### Build and run manually ####

```bash
# Create virtual environment.
$ python3 -m pipenv --python=`which python3` shell

# Install python dependencies from Pipfile in virtual environment.
$ python3 -m pipenv --python=`which python3` install

# Start the server using default wsgi server (for development only)
$ `python3 -m pipenv --venv`/bin/python3 manage.py runserver
```

### For API documentation, visit: http://localhost:8000/swagger ###
To test the APIs using swagger, follow these steps:

- Add a superuser in django with this command in the terminal and provide user details

    ```bash
    $ `python3 -m pipenv --venv`/bin/python3 manage.py createsuperuser
    ```
- Start the dev server using the command

    ```bash
    $ `python3 -m pipenv --venv`/bin/python3 manage.py runserver
    ```
- Visit the django admin panel using the url http://localhost:8000/admin and use the superuser's credentials to login
- Open Tokens and create a new token using the UI
- Copy the newly created token 
- Now, visit the swagger URL and add this token to the Authorize the APIs in this format, eg:

    ```bash
    Token jh5lk3j4lk43j5bk346blk3j5b6l
    ```
- The APIs can be now tested using the swagger.

### How do I run unittest cases? ###

```bash
# Execute all test files.
$ `python3 -m pipenv --venv`/bin/python3 manage.py test
```

### Who do I talk to? ###

- pallavmishra314@gmail.com
