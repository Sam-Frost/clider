"""

******** Line Number Of Different Routes ********

1. /              : 69-71
2. /register      : 78-113
3. /login         : 119-143
4. /logout        : 149-157
5. /mycourses     : 163-203
6. /createcourses : 213-260
7. /createcourse  : 263-297
8. /coursestatus  : 306-354
9. /update_course : 360-425
10. /certificates : 431-464
11. /about        : 470-472

"""


from flask import Flask, flash, render_template, request, redirect, session, send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functools import wraps

from helpers import certificate, name_cleaner, apology, get_username, get_courses_table, remove_spaces

from cs50 import SQL

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#Configuring Flask Application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clider.db")

#Landing onto homepage of the web application
#index route
@app.route("/")
def index():
    return render_template("index.html")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

#Register route for registering user and creating user course and certificates table!
@app.route("/register", methods=["GET", "POST"])
def register():

    #Opens up html form for registering user
    if request.method == "GET":
        return render_template("register.html")

    #Processing User Input and registering user
    else:

        #Getting data from the Form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        #Report Error If Password and Confirmation Message don't match
        if not password == confirmation:
            return apology("Password don't match")

        #Check If User Already Exists
        user_exist = db.execute("SELECT * FROM users WHERE username = ? ", username)
        if user_exist :
            return apology("User Already Exists!")

        #Hash funciton
        hashcode = generate_password_hash(password, method='plain', salt_length="2")

        #Insertion of new user into user table in database
        db.execute("INSERT into users (username, hash) VALUES (?, ?)", username, hashcode)

        # Create table for storings users courses
        table_name = username + "_courses"
        db.execute("CREATE TABLE ? (id INTEGER, coursename varchar(15) NOT NULL, no_of_videos INTEGER NOT NULL, course_status INTEGER NOT NULL, primary key(id))", table_name)

        #User is registered and redirected for being loged in
        return redirect("/login")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    #Opens up html form for logging user in
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("error.html", data = "invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/mycourses")
@login_required
def mycourse():

    #List(values to be added from sql table) of dictionaries to be passed to webpage for priniting
    course_list = []

    #Getting usename from user table
    user_name = get_username()

    #Retrieving all the courses form the course list table
    table_name = get_courses_table(user_name)
    temp_course_list = db.execute("SELECT * FROM ?", table_name)

    for rows in temp_course_list:

        #Temporary dictionary to add to course_list
        temp_dict = {}

        for key, value in rows.items():

            if key == 'id':
                temp_dict['id'] = value

            if key == 'coursename':
                temp_dict['coursename'] = name_cleaner(value)

            if key == 'no_of_videos':
                temp_dict['no_of_videos'] = value

            if key == 'course_status':
                if value == 0 :
                    temp_dict['course_status'] = "Not Finished"
                else :
                    temp_dict['course_status'] = "Finished"

        temp_dict['coursename1'] = temp_dict['coursename']

        course_list.append(temp_dict)

    return render_template("mycourses.html", course_list = course_list)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

course_name = None
no_of_lectures = 0

# Function to redirect the user to page to enter course details
@app.route("/createcourses", methods=["GET", "POST"])
@login_required
def createcourses():

    if request.method == "GET":
        return render_template("createcourses.html")

    else:
        global course_name
        course_name = request.form.get("courseName")

        #Getting username of currently logged in user
        user_name = get_username()

        course_list = get_courses_table(user_name)

        # Create a table for each course
        table_name =  "__" + user_name + "_" + course_name

        # Render Error if a course already exists with the same name
        user_exist = db.execute("SELECT * FROM ? WHERE coursename = ? ", course_list, table_name)
        if user_exist :
            return apology("Course already exists!")

        global no_of_lectures
        no_of_lectures = request.form.get("totalvideos")

        # If the no_of_lectures is not an integer render error
        try:
            no_of_lectures = int(no_of_lectures)
        except ValueError:
            return apology("No. of lectures is not a integer!")

        # If the no_of_lectures is not a positive integer render error
        if no_of_lectures < -1 :
            return apology("No. of lectures cannot be " + str(no_of_lectures))

        # Creating table for user to store the data of the course
        db.execute("CREATE TABLE ? (id INTEGER, name varchar(15) NOT NULL, link varchar(60) NOT NULL, status INTEGER NOT NULL, primary key(id))", table_name)

        # Inserting this table into list of courses tables
        db.execute("INSERT INTO ? ( coursename, no_of_videos, course_status ) VALUES ( ?, ? , 0 )", course_list, table_name, no_of_lectures)

        num = []
        for i in range(1 , no_of_lectures+1):
            num.append(str(i))

        return render_template("createcourse.html", course_name = course_name, no_of_lectures = num)

# Function to actually create course and store data in the database
@app.route("/createcourse", methods=["GET", "POST"])
def createcourse():
    if request.method == "POST":

        global course_name
        global no_of_lectures

        #initializing empty list to store the dictionares
        temp = []

        # Loop to get store the data of all the videos in a list of dictionaries
        for i in range(1 , no_of_lectures+1):
            temp_name = str(i) + ".name"
            name = request.form.get(temp_name)

            temp_url = str(i) + ".url"
            address = request.form.get(temp_url)

            temp_dict = {name: address}
            temp.append(temp_dict)

        # Getting username from the users tables for creating new table
        name = get_username()
        table_name = "__" + name + "_" + course_name

        # Storing the data of videos in table
        for item in temp:
            for name, link in item.items():
                db.execute("INSERT INTO ? ( name, link, status ) VALUES( ? , ? , 0 )", table_name, name, link)

        course_name = None
        no_of_lectures = 0

        # return render_template("coursecreated.html")
        return redirect("/mycourses")


#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

current_course = None

@app.route("/course_status", methods=["GET", "POST"])
@login_required
def course_status():

    if request.method == "GET":

        temp = request.args.get("coursename")
        print(temp)
        name = get_username()

        course_name = "__" + name + "_" + temp

        global current_course
        current_course =  course_name

        lectures = []

        course_list = db.execute("SELECT * FROM ?", course_name)

        for rows in course_list:

            #Temporary dictionary to add to course_list
            temp_dict = {}

            for key, value in rows.items():

                if key == 'id':
                    temp_dict['id'] = value

                if key == 'name':
                    temp_dict['name'] = value

                if key == 'link':
                    temp_dict['link'] = value

                if key == 'status':
                    if value == 0 :
                        temp_dict['status'] = "Not Finished"
                    else :
                        temp_dict['status'] = "Finished"

            lectures.append(temp_dict)

        print(lectures)

        return render_template("coursestatus.html", lectures = lectures , coursename = name_cleaner(current_course))

    else :

        return redirect("/mycourses")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/update_course", methods = [ "GET", "POST" ])
@login_required
def update_course():

    if request.method == "GET":

        global current_course

        lectures = []

        course_list = db.execute("SELECT * FROM ?", current_course)

        for rows in course_list:

            #Temporary dictionary to add to course_list
            temp_dict = {}

            for key, value in rows.items():

                if key == 'name':
                    temp_dict['name'] = value

                if key == 'status':
                    if value == 0 :
                        temp_dict['status'] = "Not Finished"
                    else :
                        temp_dict['status'] = "Finished"

            lectures.append(temp_dict)

        return render_template("updatecourse.html", lectures = lectures, coursename = name_cleaner(current_course))

    else :

        course_list = db.execute("SELECT * FROM ?", current_course)

        for item in course_list:

            temp = {}
            name = item [ 'name' ]
            temp[name] = request.form.get( name )

            db.execute("UPDATE ? SET status = ? WHERE name = ?", current_course, temp[name], name)

        course_list = db.execute("SELECT * FROM ?", current_course)

        flag = True

        name = get_username()
        tableName = get_courses_table(name)

        for item in course_list:

            if item['status'] == 0:
                flag = False
                break

        if flag:
            db.execute("UPDATE ? SET course_status = 1 WHERE coursename = ?", tableName , current_course)

        else :
            db.execute("UPDATE ? SET course_status = 0 WHERE coursename = ?", tableName , current_course)



        return redirect("/mycourses")

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/certificates", methods = ["GET", "POST"])
@login_required
def certificates():

    if request.method  == "GET":

        name = get_username()

        table_name = get_courses_table(name)

        courses = db.execute("SELECT coursename FROM ? WHERE course_status = 1", table_name)

        for item in courses:
            item['coursename'] = name_cleaner( item['coursename'] )

        return render_template("certificates.html", courses = courses)

    else :

        name = get_username()

        course_name = "__" + name + "_" + request.form.get("coursename")

        table_name = get_courses_table(name)
        videos = db.execute("SELECT no_of_videos FROM ? WHERE coursename = ?", table_name, course_name)

        number_of_videos = str(videos[0]['no_of_videos'])

        course_name = name_cleaner( course_name )

        certificate(name, course_name, number_of_videos)

        path = "./static/Certificate/Certificate.png"
        return send_file(path, as_attachment=True)

#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#
#-----------------------------------------------------------------------#

@app.route("/about")
def about():
    return render_template("about.html")
