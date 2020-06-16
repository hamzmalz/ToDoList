from flask import render_template, request, redirect
from todolist import app, db
from todolist.models import ToDo


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
