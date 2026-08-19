from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import    SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///todo.db'
db  = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(
        db.Integer,
         primary_key= True)
    name = db.Column(
        db.String(80), 
        nullable=False)
    created_at= db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow)
    
    def __repr__(self):
        return f"Todo : {self.name}"

with app.app_context():
    db.create_all()


@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        new_task = Task(name=name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception :
            return "Une erreur s'est produite"
    else:

        tasks = Task.query.order_by(Task.created_at)
    return render_template("index.html",tasks=tasks)



@app.route("/delete/<int:id>/")
def delete(id):
    task= Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect("/")
    except Exception:
        return "Une erreur s'est produite"



@app.route("/update/<int:id>/", methods=["GET","POST"])
def update(id):
    task = Task.query.get_or_404(id)
    if request.method == "POST":
        task.name = request.form["name"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception :
            return "Nous ne pouvons pas mettre a jour la tache"
    else:
        title = "Mise a jour"
        return render_template("update.html", title=title, task=task)

    
@app.route("/about/")
def about():
  return render_template("about.html")
     
if __name__ == "__main__":
     app.run(debug=True)