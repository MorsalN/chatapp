#creating a new flask app called chatapp

from flask import Flask, render_template, request, Response, make_response, jsonify, json
from flask import redirect, url_for 
import requests
import os
import re
import html
import sqlite3 #used to create the Connection object that represent the database
import datetime

#once we import Flask, we need to create an instance of the Flask class for our web app. That’s what line 3 does. __name__ is a special variable that gets as value the string "__main__" when you’re executing the script.
app = Flask(__name__) 

#To use the module, you must first create a Connection object that represents the database. Here the data will be stored in the chatapp.db file:
connection = sqlite3.connect('data/chatapp.db')
c = connection.cursor()

#creating a table that has:id, message, date posted, sender id, receiver id and some foreign keys that relate to the User table below it 
c.execute('''CREATE TABLE IF NOT EXISTS message 
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, message VARCHAR(300) NOT NULL, date_posted default CURRENT_DATE, sender_id INTEGER, receiver_id INTEGER, FOREIGN KEY(sender_id) REFERENCES users(id), FOREIGN KEY(receiver_id) REFERENCES users(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS users
			 (id INTEGER PRIMARY KEY AUTOINCREMENT, username text NOT NULL, password VARCHAR(12) NOT NULL, fname text, lname text, birthday date)''')

#creating our own users as a test down below 
# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("jassycodes", "polygloter03", "Jasmine"))
# c.execute("INSERT INTO users(username, password, fname) VALUES(?,?,?);", ("morsal11", "polygloter11", "Morsal"))

# Save (commit) the changes
connection.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
connection.close()


#this is the homepage route that will connect to an index.html page
@app.route("/")
def homepage():
	return render_template('index.html')


@app.route("/sample") #creating a route for localhost:5000/sample
def sample(): #creating a function called sample
	return render_template('samplechat.html') #connection to html - Flask will look for templates in the templates folder. 

@app.route("/sendmessage", methods=['POST']) #The browser tells the server that it wants to POST some new information to that URL (/sendmessage)
#and that the server must ensure the data is stored and only stored once. This is how HTML forms usually transmit data to the server.
def send(): #creating a function called "send"
	sender = request.form.get('sender')
	receiver = request.form.get('receiver')	
	a_message = request.form.get('message')

	print(sender)
	print(receiver)


	connection = sqlite3.connect('data/chatapp.db')
	c = connection.cursor()

	sender_id = 0
	receiver_id = 0
<<<<<<< HEAD
	senderFound = False #
	receiverFound = False #
=======
	senderFound = False
	receiverFound = False
	sender_name = ""
	receiver_name = ""
>>>>>>> c35c11925263998fea09d52f659444acaf6927f0

	#query for checking if username SENDER exists in the database
	c.execute("SELECT id FROM users WHERE username='{}'".format(sender))

	if c.fetchall() is not None:
		c.execute("SELECT id FROM users WHERE username='{}'".format(sender))
		sender_id = c.fetchone()[0]
		print(sender_id)
		senderFound = True
		c.execute("SELECT fname FROM users WHERE username='{}'".format(sender))
		sender_name = c.fetchone()[0]
	else:
		print("Empty")

	#query for checking if username RECEIVER exists in the database
	c.execute("SELECT id FROM users WHERE username='{}'".format(receiver))
	
	if c.fetchall() is not None:
		c.execute("SELECT id FROM users WHERE username='{}'".format(receiver))
		receiver_id = c.fetchone()[0]
		print(receiver_id)
		receiverFound = True
		c.execute("SELECT fname FROM users WHERE username='{}'".format(receiver))
		receiver_name = c.fetchone()[0]
	else:
		print("Empty")

	if senderFound == True and receiverFound == True:
		c.execute("INSERT INTO message(message, sender_id, receiver_id) VALUES(?,?,?);", (a_message, sender_id, receiver_id))
	else:
		print("either receiver or sender not found in the database")



	connection.commit()
	connection.close()



	# print(a_message)
	return json.dumps({'status':'OK','a_message':a_message, 'sender': sender_name, 'receiver': receiver_name });

# @app.route('/signUpUser', methods=['POST'])
# def signUpUser():
#     user =  request.form['username'];
#     password = request.form['password'];
#     return json.dumps({'status':'OK','user':user,'pass':password});


@app.route("/randomstring")
def rndmstring():
	return "this is a randomstring";


@app.route("/hackernews", methods=['GET'])
def hacker():
	response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
	top_ten_ids = response.json()[:10]
	print("hello test hackernews")
	print(top_ten_ids)

	top10_titles = []
	stories = []

	for top_id in top_ten_ids:
		response_url = 'https://hacker-news.firebaseio.com/v0/item/{}.json?print=pretty'.format(top_id)
		response = requests.get(response_url)
		stories.append(response.json()) 

	for story in stories:
		top10_titles.append(story['title'])

		top10_titles.sort()

	return jsonify(top10_titles)

@app.route("/random_string")
def rndm_string():
	return "another random string"


if __name__ == '__main__':
   app.run()

	


