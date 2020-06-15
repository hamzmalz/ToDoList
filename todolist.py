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
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.today) 
    
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
            return "Your task could not be added!!"
    else:
        tasks = ToDo.query.order_by(ToDo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/done/<int:id>')
def done(id):
    task_completed = ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_completed)
        db.session.commit()
        return redirect('/')
    except:
        return "Task could not be marked as complete!!"


@app.template_filter('dt')
def _jinja2_filter_datetime(date):
    return date.strftime(('%I:%M %p'))


if __name__ == "__main__":
    app.run(debug=True)