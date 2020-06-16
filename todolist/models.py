from todolist import db
from datetime import datetime


class ToDo(db.Model):
    __tablename__ = "todo"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.today)  
    
    def __repr__(self):
        return '<Task %r>' % self.id