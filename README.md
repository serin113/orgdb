# Org Affiliations Database

This is a backend and frontend application for the management of the online database of science clubs affiliated with the [Philippine Society of Youth Science Clubs](https://www.facebook.com/psysc.inc) (PSYSC).

This is a course requirement for CS191/192 Software Engineering Courses of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman under the guidance of Ma. Rowena C. Solamo for the 1st and 2nd Semester of the academic year 2018-2019.

## Requirements
- Python 3
- MySQL/MariaDB server
- [CherryPy](https://cherrypy.org)
- [Mako](https://www.makotemplates.org)

## Setup
#### `main.py` running in a Heroku dyno with [ClearDB MySQL](https://elements.heroku.com/addons/cleardb)
0. Clone this repo
    1. Run `heroku create` in the `orgdb/` folder
    2. Run `heroku addons:create cleardb:ignite` (change `ignite` to something else if on a different plan)
1. Deploy this Git repo into a Heroku app using `git push heroku master`
2. Run `heroku run python initcredentials.py` in a terminal
3. Input new passwords for the `admin` & `dev` accounts (can be skipped)
4. Run `heroku ps:scale web=1`
5. Run `heroku open`
#### `main.py` and MySQL/MariaDB running locally
0. Install requirements
1. Copy `dbconf.sample` and rename it as `db.conf`, edit server configuration accordingly
2. Run the MySQL/MariaDB server
3. Run `source db.sql;` in an SQL command prompt
4. Run `python initcredentials.py` in a terminal
3. Input new passwords for the `admin` & `dev` accounts (can be skipped)
5. Run `python main.py` in a terminal
6. Open [localhost:8080](http://localhost:8080)

## Website

More information about the application and its development process are available in [orgdb.wordpress.com](https://orgdb.wordpress.com).

## Licenses

This project (Org Affiliations Database) is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE.md file for details.

The [CherryPy library](https://cherrypy.org), used here for the web-serving code, is licensed under the [BSD 3-Clause "New" or "Revised" License](https://github.com/cherrypy/cherrypy/blob/master/LICENSE.md).

The [Mako library](https://www.makotemplates.org), used here for templating HTML pages, is licensed under the [MIT License](https://opensource.org/licenses/MIT).

The [Semantic-UI framework](https://github.com/Semantic-Org/Semantic-UI), used here for its UI elements, is licensed under the [MIT License](https://github.com/Semantic-Org/Semantic-UI/blob/master/LICENSE.md).

The [jQuery library](https://jquery.com/), used to implement various dynamic UI features, is licensed under the [MIT License](https://github.com/jquery/jquery/blob/master/LICENSE.txt).