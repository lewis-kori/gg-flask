#Gigi Motors

Flask based web application for gigi motors online system.

###Dev Setup
TODO: Sort out dependencies and reduce unnecessary installs. E.g psycopg2, cryptography.

To set up a local server, create a database and configure it's location in the `config.py` 
file. 
You can then run:

`python gg.py db init` to initialize the database

`python gg.py db migrate` to run migrations

`python gg.py db upgrade` to upgrade

`python gg.py setup_dev` to set up some dummy data and admin(configurable in `config.py`)

`python gg.py runserver` to start the local server
