from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class ToDo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def add_task():
    if request.method == 'POST':
        task_created = request.form['content']
        new_task = ToDo(content=task_created)
        print(task_created)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error adding your task!"
    else:
        tasks = ToDo.query.order_by(ToDo.date).all()
        return render_template('index.html', tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)