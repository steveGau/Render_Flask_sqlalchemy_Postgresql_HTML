# write a python flask app 
# 1. using flask_sqlalchemy to create postgresql a table with key first name, last name and email of a student
# 2. load a index.html when start the app, using a function with name Index
# 3. index.html can get input of the first name, last name and email and save and add the inputs to the table, using a function with name add_student
# 4. index.html can list all the student's first name, last name and email in the table
# 5. a delete key for each student to delete the record from table and update the database, using a function with name delete_student and update_student
# 6. a edit key for each student to edit the record from table and update the database, using a function with name edit_student and update_student
#
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import gunicorn
#
app = Flask(__name__)
with app.app_context():
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/db_name'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3050Pony$@localhost/students'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:3050Pony$@localhost/mydatabase'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stevegau:pCdaBZ1ehnzaSkF4sQFYgPRWQSWoVl6x@dpg-cfc9gbun6mpiero1lsbg-a.ohio-postgres.render.com:1000/students_0h01'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://stevegau:pCdaBZ1ehnzaSkF4sQFYgPRWQSWoVl6x@dpg-cfc9gbun6mpiero1lsbg-a/students_0h01'
#
    db = SQLAlchemy(app)
#
    # define a table: Students
    class Students(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        fname = db.Column(db.String(20), nullable=False)
        lname = db.Column(db.String(20), nullable=False)
        email = db.Column(db.String(50), nullable=False)

    # Create a table: Students
    db.create_all()
#
    # start index.html and put data from query table all
    @app.route("/")
    def Index():
        all_data = Students.query.all()
        all_data_list = [(row.id, row.fname, row.lname, row.email) for row in all_data]
        return render_template("index.html", list_users=all_data_list)
#
    # add data to table through the GUI in function Index() then to index.html
    # <form action="{{url_for('add_student')}}" method="POST">
    @app.route('/add_student', methods=['POST'])
    def add_student():
        if request.method == 'POST':
            fname = request.form.get("fname")
            lname = request.form.get("lname")
            email = request.form.get("email")
            student = Students(fname=fname, lname=lname, email=email)
            db.session.add(student)
            db.session.commit()
            return redirect(url_for('Index'))
#
    # edit the table data through the GUI in index.html then to GUI in edit.html
    # <a href="/edit/{{row[0]}}" class="btn btn-secondary btn-sm">edit</a> (index.html)
    @app.route('/edit/<id>', methods=['POST', 'GET'])
    def edit_student(id):
        student = Students.query.get(id)
        return render_template('edit.html', student=student)
#
    # update the edited table data through the GUI in edit.html and back to function Index() then to index.html
    # <form action="/update/{{student.id}}" method="POST"> (edit.html)
    @app.route('/update/<id>', methods=['POST'])
    def update_student(id):
        if request.method == 'POST':
            student = Students.query.get(id)
            student.fname = request.form.get("fname")
            student.lname = request.form.get("lname")
            student.email = request.form.get("email")
            db.session.commit()
            print(student)
            return redirect(url_for('Index'))
#
    # detele the table data through the GUI in index.html then to GUI in edit.html and back to function Index() then to index.html
    # <a href="/delete/{{row[0]}}" class="btn btn-danger btn-delete btn-sm">delete</a> (index.html)
    # btn-delete call a script in layout.html: const btnDelete= document.querySelectorAll('.btn-delete');
    # @app.route('/delete/<id>', methods=['POST', 'GET'])
    @app.route('/delete/<string:id>', methods=['POST', 'GET'])
    def delete_student(id):
        student = Students.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('Index'))
#
    if __name__ == "__main__":
        app.run()
