from app import add_data,app,db,getRooms,Room

checkin=["2023-03-23","2023-03-24","2023-03-26","2023-03-26","2023-04-28","2023-04-29"]
checkout=["2023-03-25","2023-03-26","2023-03-28","2023-03-29","2023-04-29","2023-05-30"]
adults=[4,1,2,2,1,7]
childs=[1,1,3,3,2,4]
rooms=[4,2,3,2,5,4]

def checkRoomDate(datein,rooms):
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
                                if rooms <= aRoom:
                                      return True
                        print("currently rooms are",aRoom)
                else: return False

with app.app_context():
        db.drop_all()
        db.create_all()
        for i in range(len(checkin)):
                if checkRoomDate(checkin[i],rooms[i]):
                        print("Room Booked")
                        add_data(checkin[i],checkout[i],adults[i],childs[i],rooms[i])
                else:
                        print("not available")
                        
                        
                        
with app.app_context():
        db.drop_all()
        db.create_all()
        