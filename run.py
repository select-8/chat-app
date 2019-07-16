#! /Library/Frameworks/Python.framework/Versions/3.7/bin/python3

import os
from datetime import datetime
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "randomstring123"
messages = []

def add_message(username, message):
    """Add messages to the messages list"""
    now = datetime.now().strftime("%H:%M:%S")
    ## messages_dict = {"timestamp": now, "from": username, "message": message}
    # removed dict above an put directly to append. One line of code better than two!
    messages.append({"timestamp": now, "from": username, "message": message})

##### def get_all_messages():
####     """Get all of the messages and seperate using a <br>"""
###     return "<br>".join(messages)

@app.route('/', methods=["GET", "POST"])
def index():
    """ Main page with instructions """

    if request.method == "POST":
        session["username"] = request.form["username"]
    
    if "username" in session:
        ## return redirect(session["username"])
        return redirect(url_for("user", username=session["username"]))

    return render_template("index.html")

# we can add the /chat/ bit once we have used url_for
@app.route('/chat/<username>', methods = ["GET", "POST"])
def user(username):
    """Add and Display chat messages"""
    ## return "<h1>Welcome, {0}</h1>{1}".format(username, messages)

    # if a message has been added we want to add it to the messages list
    if request.method == "POST":
        # if POST, then we will obtain some variables 
        username = session["username"]
        # message object come from our form so we use the request method
        message = request.form["message"]
        # call add_messages function with variables just created to add them to the list
        add_message(username, message)
        # redirect to session username or messages will continue forever
        ## return redirect(session["username"])
        return redirect(url_for("user", username=session["username"]))

    return render_template("chat.html", username = username, chat_messages = messages)

"""we started with this, but can be removed now because we're using a text box"""
# @app.route('/<username>/<message>')
# def send_message(username, message):
#     """Create a new message and redirect to the chat page"""
#     ## return "{0}: {1}".format(username, message)
#     add_message(username, message)
#     return redirect("/" + username)

app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)