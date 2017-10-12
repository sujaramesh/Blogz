from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
 
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:refresh@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
 
 
class Blog(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, name, body):
        self.name = name
        self.body = body

blogs = Blog.query.all()
for blog in blogs:
    bn = blog.name
    bb = blog.body

@app.route("/")
def index():

    blogs = Blog.query.all()
    return render_template("main.html",title="Build a Blog!",blogs=blogs,bn=blog.name,bb=blog.body)

@app.route("/view_blog")
def view_blog():  
    name = request.args.get("name")
    blogs = Blog.query.all()
    for blog in blogs:
        if name == blog.name:
            bmsg = blog.body     
            return render_template("view_blog.html",bname=name,bbody=bmsg)


@app.route("/blog")
def view_main():
    return redirect('/')

@app.route("/newpost", methods=["POST","GET"])
def new_post():
    err_name=""
    err_body=""
    if request.method == "POST":
        name = request.form['blogtitle']
        body = request.form['blogbody']
        if len(name) == 0:
            err_name = "Please fill in the title"
        if len(body) == 0:
            err_body = "Please fill in the body"
        if err_name == "" and err_body == "":
            new_blog = Blog(name, body)
            db.session.add(new_blog)
            db.session.commit()
            return render_template("view_blog.html",bname=name,bbody=body)
        else: 
            return render_template("add.html", bname=name, err_name=err_name, bbody=body, err_body=err_body)
    
    return render_template("add.html")

if __name__ == "__main__": 
    app.run()        