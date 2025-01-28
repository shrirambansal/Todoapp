from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)



    # 
    def __repr__(self):
        return f'{self.title} - {self.desc}'

@app.route('/', methods=['GET', 'POST'])
def index():
    #return 'Hello, World!'
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    #  Add a new todo
    #todo = Todo(title='Todo 1', desc='First todo')

    #   Add the todo to the database
    #db.session.add(todo)

    # Commit the changes
    #db.session.commit()

    # Fetch all todos
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
"""
@app.route('/show')
def show():
    alltodo = Todo.query.all()
    return render_template('show.html', alltodo=alltodo)

"""

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')
    
if __name__ == '__main__':
    app.run(debug=True)

    