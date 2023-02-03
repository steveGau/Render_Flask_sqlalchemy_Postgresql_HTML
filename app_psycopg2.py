#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import gunicorn

# write a python flask app 
# 1. using flask_sqlalchemy to create postgresql a table with key first name, last name and email of a student
# 2. load a index.html when start the app, using a function with name Index
# 3. index.html can get input of the first name, last name and email and save and add the inputs to the table, using a function with name add_student
# 4. index.html can list all the student's first name, last name and email in the table
# 5. a delete key for each student to delete the record from table and update the database, using a function with name delete_student and update_student
# 6. a edit key for each student to edit the record from table and update the database, using a function with name edit_student and update_student
#
app = Flask(__name__)

 
DB_HOST = "localhost"
DB_NAME = "students"
DB_USER = "postgres"
DB_PASS = "3050Pony$"
 
con = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
 
# display student table data, call index.html
@app.route('/')
def Index():
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM students"
    cur.execute(s) # Execute the SQL
    list_users = cur.fetchall()
    return render_template('index.html', list_users = list_users)

# get student names and email for index.html when click save in <form action="{{url_for('add_student')}}" method="POST">
@app.route('/add_student', methods=['POST'])
def add_student():
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur.execute("INSERT INTO students (fname, lname, email) VALUES (%s,%s,%s)", (fname, lname, email))
        con.commit()
        flash('Student Added successfully')
        return redirect(url_for('Index'))

# edit student record in index.html when click edit and call edit.html with student record
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def edit_student(id):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM students WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', student = data[0])

# update student record when click update in edit.html: <form action="/update/{{student.id}}" method="POST">
@app.route('/update/<id>', methods=['POST'])
def update_student(id):
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE students
            SET fname = %s,
                lname = %s,
                email = %s
            WHERE id = %s
        """, (fname, lname, email, id))
        flash('Student Updated Successfully')
        con.commit()
        return redirect(url_for('Index'))

# dekete a record when click delete in index.html
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_student(id):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    con.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    app.run(debug=True)