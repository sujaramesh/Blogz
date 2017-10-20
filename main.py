from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:refresh@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "super secret key"
 
 
class Blog(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username,password):
        self.username = username
        self.password = password

@app.route("/")
def index():

    users = User.query.all()
    for usr in users:
        uname = usr.username
        print("uname:",uname)

    return render_template("index.html",uname=usr.username,users=users)

@app.route("/home")
def home():
    return redirect("/")

@app.route("/newpost",methods=["POST","GET"])
def newpost():

    if 'user' in session:
        err_name=""
        if request.method == "POST":
            name = request.form['blogtitle']
            body = request.form['blogbody']
            if len(name) == 0 or len(body) == 0:
                err_name = "we need both a title and a body"
            if err_name == "" :
                usr = User.query.filter_by(username=session['user']).first()
                print("usr",usr)
                
                new_blog = Blog(name,body,usr)
                db.session.add(new_blog)
                db.session.commit()
                blog = Blog.query.order_by('-id').first()
                bid = blog.id
                bname = blog.name
                bbody = blog.body
                return redirect("/view_blog?id={0}".format(blog.id))
            else: 
                return render_template("add.html", bname=name, err_name=err_name, bbody=body)
    
        return render_template("add.html")
    else:
        return redirect("/login")
        
#    return redirect("/login")

#     allowed_routes = ['newpost']
#     if request.endpoint in allowed_routes:  
        
#         redirect('/login') 
# #    if request.endpoint in allowed_routes:
 #       return "<h1>hiiiiii<h1>"
    
#        redirect('/login')
#    if user and user.password == password:
#    else:
# def new_post():
#     redirect("/login")
#     render_template("add.html")
#        render_template("add.html")
#     err_name=""
#     if request.method == "POST":
#         name = request.form['blogtitle']
#         body = request.form['blogbody']
#         if len(name) == 0 or len(body) == 0:
#             err_name = "we need both a title and a body"
#         if err_name == "" :
#             new_blog = Blog(name, body)
#             db.session.add(new_blog)
#             db.session.commit()
#             blog = Blog.query.order_by('-id').first()
#             bid = blog.id
#             bname = blog.name
#             bbody = blog.body
#             return redirect("/view_blog?id={0}".format(blog.id))
#         else: 
#             return render_template("add.html", bname=name, err_name=err_name, bbody=body)
    
#     return render_template("add.html")

# #    return render_template("add.html", bname=name, err_name=err_name, bbody=body, err_body=err_body)

@app.route("/allpost")
def all_post():
    blogs = Blog.query.all()
    for blog in blogs:
        boid = blog.owner_id
        bname = blog.name
        bbody = blog.body
        usr = User.query.filter_by(id=boid).first()    
    return render_template("view_allblog.html",bid=boid,bname=bname,bbody=bbody,uname=usr.username)

@app.route("/blog")
def view_all_blog():
    
    blg_usr = request.args.get('user')
    usr = User.query.filter_by(username=blg_usr).first()

    existing_blog = Blog.query.filter_by(owner_id=usr.id).first()
    if existing_blog:
        blogs = Blog.query.filter_by(owner_id=usr.id).all()
        print ("blogs:", blogs)
        for blog in blogs:
            bid = blog.id
            bname = blog.name
            bbody = blog.body

 #   return redirect("/view_blog?id={0}".format(bid))    
    
        return render_template("view_allblog.html",bid=bid,bname=bname,bbody=bbody,uname=blg_usr)
    else:
        return render_template("view_empty.html")

@app.route("/view_blog")
def view_blog(): 
    
    bid = request.args.get("id")
    blogs = Blog.query.filter_by(owner_id=bid).all()
    for blog in blogs:
        bid = blog.id
        bname = blog.name
        bbody = blog.body

    usr = User.query.get(bid)    

    return render_template("singleUser.html",bname=blog.name,bbody=blog.body,uname=usr.username)

# @app.before_request
# def require_login():
#     allowed_routes = ['login', 'signup']
#     if request.endpoint not in allowed_routes and 'user' not in session:
#         return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    err_usr=""
    err_pwd=""
    if request.method == 'POST':
        usrname = request.form['uname']
        password = request.form['password']
        user = User.query.filter_by(username=usrname).first()
        if not user or len(usrname) == 0:
            err_usr = "Invalid username"
#            flash("Invalid username","error")
        if len(password) == 0 or password != user.password :
            err_pwd = "Invalid password"
#            flash("Invalid password","error")
        if err_usr=="" and err_pwd=="":
            session['user'] = usrname
#            return(session['user'])
            flash("Logged in")
            return redirect("/newpost")

        else:
            return render_template('login.html',uname=usrname,err_usr=err_usr,err_pwd=err_pwd)
    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def register():
    err_vefy=""
    if request.method == 'POST':
        usrname = request.form['uname']
        password = request.form['password']
        verify = request.form['verify']

        if password != verify:
            err_vefy = "Passwords don't match"
            return render_template('signup.html',uname=usrname,err_vefy=err_vefy) 

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=usrname).first()
        if not existing_user:
            new_user = User(usrname, password)
            db.session.add(new_user)
            db.session.commit()
            session['user'] = usrname
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate user</h1>"

    return render_template('signup.html')

@app.route('/logout')
def logout():
    # if user in session:
    #     del session['user']
    #     return redirect('/allpost')
    # else:
    return redirect('/allpost')

if __name__ == "__main__": 
    app.debug = True
    app.run()       