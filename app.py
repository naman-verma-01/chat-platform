from flask import Flask, render_template, make_response, redirect, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os
from flask_session import Session

app = Flask(__name__)
socketio = SocketIO(app,logger=True)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


	
@app.route("/")
def index():
	if not session.get("name"):
		return redirect("/login")
	
	return render_template('index.html')

	
@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		session["name"] = request.form.get("name")
		session["room"] = request.form.get("room")
		
		return redirect("/")
	return render_template("login.html")
	
	
@socketio.on("message")
def handleMessage(data):
	room = session.get("room")
	socketio.emit("new_message",session.get("name") + " : " + data,to=room)
    
@socketio.on('connect')
def connect():
	room = session.get("room")
	join_room(room)
	socketio.emit("new_message",session.get("name") + " : has joined the chat",to=room)

@socketio.on('disconnect')
def disconnect():
	room = session.get("room")
	leave_room(room)
	socketio.emit("new_message",session.get("name") + " : : has left the chat",to=room)
    
if __name__ == "__main__":
    socketio.run(app, debug=True, host='127.0.0.1', port=5004)
