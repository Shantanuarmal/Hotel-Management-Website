from flask import Flask,render_template,request,redirect,flash,url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime 
 
 
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db" 
app.config['SQLALCHEMY_Track_MODIFICATIONS'] = False
app.secret_key = 'fhgfkhfguvguyi76gvhf' 
db = SQLAlchemy(app) 
class Room(db.Model):
    sno = db.Column(db.Integer,primary_key=True) 
    checkin= db.Column(db.String(100), nullable=True) 
    checkout= db.Column(db.String(100), nullable=True) 
    adults= db.Column(db.Integer, nullable=True) 
    childs= db.Column(db.Integer, nullable=True) 
    rooms= db.Column(db.Integer, nullable=True) 
 
    # date_created = db.Column(db.DateTime, default=datetime.utcnow) 
    
    def __repr__(self) -> str: 
        return f"[{self.checkin}, {self.checkout},{self.rooms}]"

def getRooms():
    room = 0
    with app.app_context():
        res = Room.query.all()
        for i in res:
            room += i.rooms
    # print("room",room)
        return room
aRoom = max(6-getRooms(),0)

def add_data(checkin,checkout,adults,childs,rooms):
    room= Room(checkin=checkin,checkout=checkout,adults=adults,childs=childs,rooms=rooms)
    with app.app_context():
        db.session.add(room)
        db.session.commit()

def checkRoomDate(datein,dateout,rooms):
    if int(dateout[8:10]) < int(datein[8:10]) or int(dateout[5:7]) < int(datein[5:7]):
        return False
    global aRoom
    with app.app_context():
        res = Room.query.all()
        print(res)
        if int(rooms) <= (6 - getRooms()):
            return True
        else:
                aRoom = 6 - getRooms()
                for i in res:
                        if int(i.checkout[8:10]) < int(datein[8:10]) or int(i.checkout[5:7]) < int(datein[5:7]):
                                aRoom += i.rooms
                                if int(rooms) <= aRoom:
                                        return True
                else: return False
                
                
def getFood():
    return Room.query.all()

@app.route('/action', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        check_in = request.form['check_in']
        rooms = request.form['rooms']
        print(check_in,rooms)
        return render_template('index.html',ava=[check_in,rooms])



@app.route('/', methods=['POST','GET']) 
def hello_world():
    if request.method == 'POST':
        check_in = request.form['check_in']
        checkout = request.form['check_out']
        rooms = request.form['rooms']
        print(check_in,rooms)
        if checkRoomDate(check_in,checkout,rooms):
            return render_template('index.html',ava="rooms are available")
        else:
            return render_template('index.html',ava=f"Oops! only {aRoom} rooms are available")
            
    return render_template('index.html',ava="") 

@app.route('/food') 
def food(): 
    foods = Room.query.all()
    return render_template('food.html',food=foods) 
    # return 'Hello, world!' 
 
@app.route('/reset') 
def products():
    with app.app_context():
        db.drop_all()
        db.create_all() 
    return redirect("http://localhost:8000") 

@app.route('/register-room', methods=['GET', 'POST'])
def register_room():
    if request.method == 'POST':
        checkin = request.form['check_in']
        checkout = request.form['check_out']
        adults = request.form['adults']
        childs = request.form['childs']
        rooms = request.form['rooms']
        if checkRoomDate(checkin, checkout,rooms):
            print("yes")
            room = Room(checkin=checkin, checkout=checkout, adults=int(adults), childs=int(childs), rooms=int(rooms))
            db.session.add(room)
            db.session.commit()
            return render_template('index.html',ava="room Booked!")
        else:
            flash('There are no rooms available for the selected check-in date and number of rooms. Please try again with a different date or fewer rooms.')
            return render_template('index.html',ava=f"Opps! only {aRoom} rooms are available") 


with app.app_context():
    db.create_all()

if __name__ == '__main__': 
    app.run(debug=True, port=8000)