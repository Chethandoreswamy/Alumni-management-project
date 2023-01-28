from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from datetime import datetime
import json


# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='kusumachandashwini'

login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:1234567890@localhost/ams'
db=SQLAlchemy(app)



class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))
    # role=db.Column(db.String(20))

class Club(db.Model):
    cid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    president=db.Column(db.String(20))
    number_of_members=db.Column(db.Integer)
    desi=db.Column(db.String(100))

class event(db.Model):
    eid=db.Column(db.Integer,primary_key=True)
    EventName=db.Column(db.String(20))
    date_of_conduct=db.Column(db.DateTime(),default=datetime.utcnow)
    eventc=db.Column(db.String(20))
    headline=db.Column(db.String(100))

class student(db.Model):
    rollno=db.Column(db.String(20),primary_key=True,unique=True)
    sname=db.Column(db.String(50))
    sem=db.Column(db.Integer())
    gender=db.Column(db.String(50))
    branch=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    number=db.Column(db.String(50),unique=True)
    address=db.Column(db.String(150))
    approve=db.Column(db.Integer(),default=0)

class alumni(UserMixin,db.Model):
    name=db.Column(db.String(30),primary_key=True)
    email=db.Column(db.String(30),primary_key=True)
    designation=db.Column(db.String(100))
    linkdin=db.Column(db.String(50))
    company=db.Column(db.String(100))
    about=db.Column(db.String(100))
    approve=db.Column(db.Integer(),default=0)


class event_participation(db.Model):
    eid=db.Column(db.Integer(),db.ForeignKey(event.eid),primary_key=True)
    rollno=db.Column(db.String(20),db.ForeignKey(student.rollno),primary_key=True)
    name=db.Column(db.String(30),db.ForeignKey(alumni.name))

class club_participation(db.Model):
    cid=db.Column(db.Integer(),db.ForeignKey(Club.cid),primary_key=True)
    rollno=db.Column(db.String(20),db.ForeignKey(student.rollno),primary_key=True)
   




#  @app.route('/')
# def index(): 
#     return render_template('index.html')

# newly added admin login
# @app.route('/logindmin',methods=['POST','GET'])
# def loginadmin():
#     if request.method == "POST":
#         email=request.form.get('email')
#         password=request.form.get('password')
#         user=User.query.filter_by(email=email,rloe="As admin").first()

#         if user and check_password_hash(user.password,password):
#             login_user(user)
#             flash("Login Success","primary")
#             return redirect(url_for('index'))
#         else:
#             flash("invalid credentials","danger")
#             return render_template('loginadmin1.html')    
#     return render_template('loginadmin1.html')

@app.route('/',methods=['POST','GET'])
def index(): 
    if request.method=="POST":
        user1=request.form.get('name1')
        id=alumni.query.filter_by(name=user1).first()
        return render_template('index1.html',bio=id)
    return render_template('index1.html')

@app.route('/alumnis')
def alumnis(): 
    return render_template('alumnis.html')

@app.route('/clubs1')
def clubs1(): 
    return render_template('clubs1.html')

@app.route('/events')
def events():
    data=db.engine.execute(f"SELECT * FROM `event` order by eid DESC")
    return render_template('Events.html',data=data)


@app.route('/addevents',methods=['POST','GET'])
# decorator 
@login_required
# # @admin_required
# @roles_required
def addevent():
    query=db.engine.execute(f"SELECT * FROM `club`") 
    if request.method=="POST":
        eventc=request.form.get('event-c')
        eventname=request.form.get('eventname')
        date=request.form.get('date-event')
        headline=request.form.get('headline')
        atte=event(EventName=eventname,date_of_conduct=date,eventc=eventc,headline=headline)
        db.session.add(atte)
        db.session.commit()
        flash("Events added","warning")
    return render_template('addevents.html',query=query)

@app.route('/addstudent',methods=['POST','GET'])
def addstudent():
    if request.method=="POST":
        rollno=request.form.get('rollno')
        sname=request.form.get('sname')
        sem=request.form.get('sem')
        gender=request.form.get('gender')
        branch=request.form.get('branch')
        email=request.form.get('email')
        num=request.form.get('num')
        address=request.form.get('address')
        query=db.engine.execute(f"INSERT INTO `student` (`rollno`,`sname`,`sem`,`gender`,`branch`,`email`,`number`,`address`) VALUES ('{rollno}','{sname}','{sem}','{gender}','{branch}','{email}','{num}','{address}')")
        flash("registered Confirmed","info")


    return render_template('student.html')

@app.route('/addalumni',methods=['POST','GET'])
def addalumni():
    if request.method=="POST":
        name=request.form.get('sname')
        desi=request.form.get('desi')
        linkdin=request.form.get('link')
        company=request.form.get('company')
        about=request.form.get('about')
        email=request.form.get('email')
        # num=request.form.get('num')
        # address=request.form.get('address')
        query=db.engine.execute(f"INSERT INTO `alumni` (`name`,`designation`,`linkdin`,`company`,`email`,`about`) VALUES ('{name}','{desi}','{linkdin}','{company}','{email}','{about}')")
        flash("registered Confirmed","info")


    return render_template('alumnidetails.html')

@app.route('/club',methods=['POST','GET']) 
@login_required
def addclub():
    if request.method=="POST":
        name=request.form.get('club')
        president=request.form.get('p')
        number=request.form.get('number_of')
        desi=request.form.get('desi')
        # atte=club(name=name,president=president,number_of_members=number,desi=desi)
        db.engine.execute(f"INSERT INTO `club` (`name`,`president`,`number_of_members`,`desi`) VALUES ('{name}','{president}','{number}','{desi}')")
        flash("club  Succes Please Login","success")
    return render_template('clubs.html')


@app.route('/studentdetails', methods=['POST','GET'])
@login_required
def signup_details():
    querys= db.engine.execute("SELECT * FROM student where approve=0")
    querya = db.engine.execute("SELECT * FROM alumni where approve=0")
    
    return render_template('studentdetails.html',query=querys,data=querya)
    
     


@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        user1=request.form.get('roll')
        id=student.query.filter_by(rollno=user1).first()
        # email=Attendence.query.filter_by(email=email).first()
        # role=Attendence.query.filter_by(role=role).first()
        return render_template('searchstudent.html',bio=id)
        
    return render_template('searchstudent.html')
        

# @app.route('/searchclub',methods=['POST','GET'])
# def searchc():
#     if request.method=="POST":
#         event=request.form.get('name1')
#         id=event.query.filter_by(EventName=event).first()
#         # email=Attendence.query.filter_by(email=email).first()
#         # role=Attendence.query.filter_by(role=role).first()
#         return render_template('clubs1.html',bio=id)

#     return render_template('clubs1.html')

# @app.route('/searchevent',methods=['POST','GET'])
# def searche():
#     if request.method=="POST":
#         user1=request.form.get('name1')
#         id=User.query.filter_by(username=user1).first()
#         # email=Attendence.query.filter_by(email=email).first()
#         # role=Attendence.query.filter_by(role=role).first()
#         return render_template('Events.html',bio=id)
        
#     return render_template('Events.html')
   

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        # role=request.form.get('role')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login","success")
        return render_template('loginc.html')

          

    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return redirect(url_for('index'))
        else:
            flash("invalid credentials","danger")
            return render_template('loginc.html')    
    return render_template('loginc.html')


@app.route("/approve/<rollno>",methods=['POST','GET'])
@login_required
def delete(rollno):
    db.engine.execute(f"UPDATE `student` SET `approve`=1 WHERE `student`.`rollno`='{rollno}' ")
    flash("approved Successful","warning")
    return redirect('/studentdetails')


@app.route("/approvefor/<name>",methods=['POST','GET'])
@login_required
def approvefor(name):
    db.engine.execute(f"UPDATE `alumni` SET `approve`=1 where `alumni`.`name`='{name}' ")
    flash("approved sucessful")
    return redirect('/studentdetails')

@app.route("/participate/<rollno> <eid>",methods=['POST','GET'])
def participates():
    db.engine.execute(f"INSERT INTO event_participation (eid,rollno) values({eid},'{rollno}' ")
    flash("registered sucessful")
    return redirect('/events')

@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'

app.run(debug=True)    