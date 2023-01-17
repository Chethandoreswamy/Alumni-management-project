from flask import Flask,render_template, request,redirect,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
 
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234567890'
app.config['MYSQL_DB'] = 'alumni'
 
mysql = MySQL(app)

@app.route('/')
def homepage():
    return render_template('index.html') 

@app.route('/signup as student', methods = ['POST', 'GET'])
def signup(): 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email_id']
        password = request.form['password']
        Repassword = request.form['Repassword']
        cursor = mysql.connection.cursor()
        if password!=Repassword:
            return "<h1> passwords are not matching</h>"
        cursor.execute("INSERT INTO student_registration (Sname,Email_id,Password) VALUES (%s, %s, %s)",(name,email,password))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('Main'))
    return render_template('stureg.html')

@app.route('/main home')
def Main():
    return render_template('main.html')

# to add events
@app.route('/adminEvents', methods=['POST','GET'])
def adminEvent():
    if request.method=='POST':
        Ename=request.form['Ename']
        ClubName=request.form['ClubName']
        Guest=request.form['Guest']
        Contents=request.form['Contents']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO Events (Ename,ClubName,Guest,Contents) VALUES (%s, %s, %s,%s)",(Ename,ClubName,Guest,Contents))
        mysql.connection.commit()
        cursor.close()
        # return redirect(url_for('#adding events'))      
    return render_template('EventsRegister.html')  

# admin login
@app.route('/adminLogin', methods=['POST','GET'])
def adminLogin():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        if password!='1234567890':
            return "<h1>Enter correct password</h1>"
        return redirect(url_for('adminMain'))
    return render_template('admni_log.html')

@app.route('/adminMain')
def adminMain():
    return render_template('admin_main.html')

# to add club
@app.route('/adminClub',methods=['POST','GET'])
def adminClub():
    if request.method=='POST':
        ClubName=request.form['ClubName']
        Description=request.form['Description']
        President=request.form['President']
        number=request.form['number']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO club (ClubName,Details,President,no_of_members) VALUES (%s, %s, %s,%s)",(ClubName,Description,President,number))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('Main'))

    return render_template('club_add.html',)



@app.route("/signupA", methods = ['POST', 'GET'])
def signupA(): 
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['Email_id']
        password = request.form['password']
        org = request.form['organization']
        desi = request.form['desi']
        cursor = mysql.connection.cursor()
        # if password!=Repassword:
        #     return "<h1> passwords are not matching</h1>"
        cursor.execute("INSERT INTO alumni (name,email,password,desi,organization) VALUES (%s, %s, %s,%s,%s)",(name,email,password,desi,org))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('Main'))
    return render_template('alureg.html')


# to display event
@app.route('/events',methods=['POST','GET'])
def Events():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Events")
    # mysql.connection.commit()
    result=cursor.fetchall()
    cursor.close()
    return render_template('Events.html',data=result)



if __name__=="__main__": 
    app.run(debug=True)