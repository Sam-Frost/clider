from PIL import Image, ImageDraw, ImageFont
from flask import render_template, session
from flask_session import Session
from cs50 import SQL

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///clider.db")

# Returns the username of the user currently logged in
def get_username():
    temp = db.execute("SELECT username FROM users WHERE id = ?", session['user_id'] )
    return temp[0]['username']

# Returns the name of the table storing all the user's courses
def get_courses_table(name):
    return name + "_courses"

# Remove unwatned elements from name for fianlly printing on webpage
def name_cleaner(name):

    i = 0
    clean_name = ""

    for character in name:
        if i == 3:
            clean_name += character

        if character == '_':
            i = i + 1

    return clean_name


# This functions create the certificate
def certificate(name, course_name, number_of_videos):

    # Open the certificate template file
    img = Image.open('./static/Certificate/Clider Certificate Template.jpg')

    # Calling helper for name

    """
    ***** For My Specific Use Case *****

    Font : Bold
    Font Size : 50
    Width : 0 // This is the number number of pixels that needs to be subtracted from the width value
    Height : 215

    """

    helper( img, name, "./static/fonts/Roboto-Bold.ttf", 50, 0, 215 )

    ##############################################################################################################

    # Calling helper for course name

    """
    ***** For My Specific Use Case *****

    Font : Regular
    Font Size : 42
    Width : 0 // This is the number number of pixels that needs to be subtracted from the width value
    Height : 389

    """

    helper( img, course_name, "./static/fonts/Roboto-Regular.ttf", 42, 0, 389 )

    ##############################################################################################################

    # Calling helper for number of videos

    """
    ***** For My Specific Use Case *****

    Font : Bold
    Font Size : 52
    Width : 80 // This is the number number of pixels that needs to be subtracted from the width value
    Height : 530

    """

    helper( img, number_of_videos, "./static/fonts/times new roman bold.ttf", 52, 80, 530 )

    # Saves the final certificate
    img.save( "./static/Certificate/Certificate.png" )


def helper(img, text, my_font, fontsize, subtract_width, my_height):

    # The Width and Height of The Certificate (In Pixels)
    Width, Height = ( 720, 975 )

    # Call draw Method to add text message( 2D graphics ) to the image
    draw = ImageDraw.Draw( img )

    # Custom font style and font size
    font = ImageFont.truetype( my_font, fontsize )

    # Gets the width and height of the text message
    width, height = font.getsize( text )

    # Calculating the width and height for aligin the text to center axis
    W = ( Width - width ) / 2
    H = ( Height - height ) / 2

    # Add user's name to the image
    draw.text( ( W - subtract_width , my_height ), text, font = font, fill = ( 255, 255, 255 ) )


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def remove_spaces(input):
    text = ""
    for character in input:
        if character.isspace() :
            text += "_"
        else:
            text += character

    return text


