from flask import Flask,request,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin,login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
local_server=True
app = Flask(__name__)
app.secret_key='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:monu@localhost/fms'

login_manager=LoginManager(app)
login_manager.login_view='login'

@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))
db = SQLAlchemy(app)

class users(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String(45))
    lastname=db.Column(db.String(45))
    username=db.Column(db.String(45),unique=True)
    password=db.Column(db.String(200))

class admin(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    firstname=db.Column(db.String(45))
    lastname=db.Column(db.String(45))
    username=db.Column(db.String(45),unique=True)
    password=db.Column(db.String(45))


class feestructure(db.Model):
    slno=db.Column(db.Integer,primary_key=True)
    year=db.Column(db.String(45))
    batch=db.Column(db.String(45))
    cet=db.Column(db.Integer)
    comedk=db.Column(db.Integer)
    snq=db.Column(db.Integer)
    management=db.Column(db.Integer)

class chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(450))
    reply = db.Column(db.String(450))


class conversations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    messages = db.Column(db.String(450))
    reply = db.Column(db.String(450))

class status(db.Model):
    usn = db.Column(db.Integer , primary_key=True , unique=True)
    feepay = db.Column(db.Integer)
    feepaid = db.Column(db.Integer)

class payment(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    fullname = db.Column(db.String(45))
    emailid = db.Column(db.String(45))
    date = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    gender = db.Column(db.String(45))
    pay = db.Column(db.String(45))
    card = db.Column(db.Integer)
    cvc = db.Column(db.Integer)
#db.engine.execute("ALTER TABLE conversations ADD reply varchar(500);")
db.engine.execute("DELETE FROM conversations;")


@app.route('/chatbot', methods=['POST', 'GET'])
def chatbot():
    if request.method == 'POST':
        chat = request.form['bots']
        print(f"i am {chat}")
        query = db.engine.execute(
            f"SELECT * FROM chat where query='{chat}'  ;")
        resu = query.fetchall()
        queries = resu[0][1]
        reply = resu[0][2]
        print(queries)
        print(reply)
        db.engine.execute(
            f"INSERT INTO conversations(messages,reply) VALUES('{queries}','{reply}')  ;")

        query = db.engine.execute(
            f"SELECT * FROM  conversations ;")
        return render_template('chats.html', query=query)
    return render_template('chats.html')

@app.route('/')
def my_form():
    return render_template('register.html')

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        username=request.form.get('username')
        password=request.form.get('password')
        print(firstname,lastname,username,password)
        #user=users.query.filter_by(username=username).first()
        #if user:
            #return render_template('login.html')
        new_user=db.engine.execute(f" INSERT INTO users(firstname,lastname,username,password) VALUES('{firstname}','{lastname}','{username}','{password}')")
        return render_template('login.html')
    else:
        pass
    return render_template ('login.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        user=users.query.filter_by(username=username).first()
        password=users.query.filter_by(password=password).first()
        if user and password :
            login_user(user)
            return render_template('chats.html')
        return render_template('login.html')

#@app.route('/admin',methods=['POST','GET'])
#def admin():
    #if request.method=='POST':
        #firstname=request.form.get('firstname')
        #lastname=request.form.get('lastname')
        #username=request.form.get('username')
        #password=request.form.get('password')
        #print(firstname,lastname,username,password)
        #user=users.query.filter_by(username=username).first()
        #if user:
            #return render_template('login.html')
        #new_user=db.engine.execute(f" INSERT INTO admin(firstname,lastname,username,password) VALUES('{firstname}','{lastname}','{username}','{password}')")
        #return render_template('admin.html')
    #else:
        #pass
    #return render_template ('admin.html')


#@app.route('/adminlogin',methods=['GET','POST'])
#def adminlogin():
#    if request.method=='POST':
#        username=request.form.get('username')
#        password=request.form.get('password')
#        user=admin.query.filter_by(username=username).first()
#        password=admin.query.filter_by(password=password).first()
#        if user and password :
#            login_user(user)
#            return render_template('welcome.html')
#        return render_template('admin.html')



@app.route('/display')
def display():
    query=db.engine.execute('SELECT * FROM feestructure;')
    #res=query.fetchall()
    #print(res)
    return render_template('displayss.html',query=query)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/payment', methods=['GET','POST'])
def payment():
    if request.method=='POST':
        fullname=request.form.get('fullname')
        emailid=request.form.get('emailid')
        date=request.form.get('date')
        month=request.form.get('month')
        year=request.form.get('year')
        gender=request.form.get('gender')
        pay=request.form.get('pay')
        card=request.form.get('card')
        cvc=request.form.get('cvc')
        db.engine.execute(
            f"INSERT INTO payment(fullname,emailid,date,month,year,gender,pay,card,cvc) VALUES('{fullname}','{emailid}','{date}','{month}','{year}','{gender}','{pay}','{card}','{cvc}')  ;")
    return render_template('base.html')


@app.route('/studentinfo', methods=['GET','POST'])
def studentinfo():
    if request.method=='POST':
        firstname=request.form.get('firstname')
        lastname=request.form.get('lastname')
        parentname=request.form.get('parentname')
        date=request.form.get('date')
        month=request.form.get('month')
        year=request.form.get('year')
        gender=request.form.get('gender')
        pay=request.form.get('amount')
        db.engine.execute(
            f"INSERT INTO studentinfo(firstname,lastname,parentname,emailid,date,month,year,gender,amount) VALUES('{firstname}','{lastname}','{parentname}','{emailid}','{date}','{month}','{year}','{gender}','{amount}')  ;")


    return render_template('studentinfo.html')

@app.route('/sucess',  methods=['GET','POST'])
def sucess():
    return render_template('sucess.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=="__main__":
    app.run(debug=True)
