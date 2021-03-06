# Clider
#### Video Demo:  https://www.youtube.com/watch?v=LLLraUxvr50
#### Description:

Clider is a web application which allows users to create courses by grouping together youtube videos
and provides the user with a certificate upon the completion of the course

#### How the webpage works?
The website is pretty simple! Inorder to use the website the user need to register with the webiste. After registering and logging in
the user then needs to create a course. Enter the name of the course and number of lectures, then enter name and link of each video of the
course. Once then course is created then the course can be access from my courses page. Then as the user progress in the course he can
mark each lecutre as completed. Once all the lectures of a course are completed the course is marked as completed! All the completed
course are listed in the certificates page with a download button. On clicking the download button, the certificate downloads automatically.
The certificate contains the user's name, course name and number of lectures in the course.

###### Technologies

- HTML5 (HTML & CSS, There is no use of javascript)
- Bootstrap (Frontend CSS Framework)
- Python (Flask)
- SQLite3 (For database)

###### Folders/Files

Clider uses the standrd flask folder structures.

1. *flask_session* : This folders stores sessions files. 
2. *static* : This folder contains the style sheets, font files, certificate template and the logo
3. *templates* : This folder contains the HTML templates files
4. *application.py* : This is the main application containing the python code powering the backend
5. *helper.py* : This file contains miscellaneous functions that help application.py
6. *clider.db* : This is the database containg all the users data in form of multiple tables
7. *requirements.txt* : This files enlists the libraries required for the flask application to run
8. *README.md* : This is the file that you are reading right now

**static :**
1. Certificate : This folder contains three files
    -Certificate.png : The certficate.png that users download
    -Clider Certificate Template.jpg : The template file on which the name and other deatils are printed to genereate final certificate
    -Clider Certificate.psd : The photoshop file of certificate for future editing of the certificate template
2. Fonts : This folder contains the font files (.ttf) used in certificate generation. It contains two fonts
    -Roboto
    -Times New Roman
3. Images : This folder contains the clider logo

###### Database
Database consists of one base table called user which always exists. It contains the username and password. When a new user is registered
the user table is updated with his/her details and a new table is created to store the list of courses. Whenever the user creates a new
course a new table is created to store the lectures, there links and there status.

###### Future Improvements
- Add functionality to delete Users
- Add functionality to delete Courses
- Add functionality to delete Videos from particular courses
- Two lectures can't have same name, fix this
- Remove case sesitivity
- Sanitize against SQL attacks
- Run checks on backed to ensure the values returned from users browser are not modified to be illegeal values by user
- Make the UI responsive for mobile devices
- Integrate Logging In with Google Accounts
- Integrate making courses from playlists from YouTube
