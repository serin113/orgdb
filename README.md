# Org Affiliations Database

This is a backend and frontend application for the management of the online database of science clubs affiliated with the [Philippine Society of Youth Science Clubs](https://www.facebook.com/psysc.inc) (PSYSC).

This is a course requirement for CS191/192 Software Engineering Courses of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman under the guidance of Ma. Rowena C. Solamo for the 1st and 2nd Semester of the academic year 2018-2019.

## Requirements
- Python 3
- MySQL/MariaDB server
- [CherryPy](https://cherrypy.org)
- [Mako](https://www.makotemplates.org)

## Installation & Configuration
#### `main.py` running in a Heroku dyno with [ClearDB MySQL](https://elements.heroku.com/addons/cleardb)
1. Clone this repo
    1. Run `heroku create` in the `orgdb/` folder
    2. Run `heroku addons:create cleardb:ignite` (change `ignite` to something else if on a different plan)
2. Deploy this Git repo into a Heroku app using `git push heroku master`
3. Run `heroku run python importdb.py` in a terminal, ignore the `[Command skipped]` messages
4. Run `heroku run python initcredentials.py` in a terminal
5. Input new passwords for the `admin` & `dev` accounts (can be skipped by pressing Enter)
6. Run `heroku ps:scale web=1`
7. Run `heroku open`
#### `main.py` and MySQL/MariaDB running locally (*not* for deployment)
1. Install requirements: `pip install -r requirements.txt`
2. Copy `dbconf.sample` and rename it as `db.conf`
3. Edit `db.conf` according to the MySQL/MariaDB settings
3. Run the MySQL/MariaDB server
4. Run `source db.sql;` in an SQL command prompt
5. Run `python initcredentials.py` in a terminal
6. Input new passwords for the `admin` & `dev` accounts (can be skipped)
7. Run `python main.py` in a terminal
8. Open [https://localhost:8080](https://localhost:8080) in a browser

## Website

More information about the application and its development process are available in [orgdb.wordpress.com](https://orgdb.wordpress.com).

## Licenses

This project (Org Affiliations Database) is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE.md file for details.

The [CherryPy library](https://cherrypy.org), used here for the web-serving code, is licensed under the [BSD 3-Clause "New" or "Revised" License](https://github.com/cherrypy/cherrypy/blob/master/LICENSE.md).

The [Mako library](https://www.makotemplates.org), used here for templating HTML pages, is licensed under the [MIT License](https://opensource.org/licenses/MIT).

The [Semantic-UI framework](https://github.com/Semantic-Org/Semantic-UI), used here for its UI elements, is licensed under the [MIT License](https://github.com/Semantic-Org/Semantic-UI/blob/master/LICENSE.md).

The [jQuery library](https://jquery.com/), used to implement various dynamic UI features, is licensed under the [MIT License](https://github.com/jquery/jquery/blob/master/LICENSE.txt).