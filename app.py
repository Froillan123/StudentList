from flask import Flask, render_template, request, redirect, url_for, session, flash
from dbhelper import *
from flask_session import Session
import os

app = Flask(__name__)

app.config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp/sessions" 
app.config["SESSION_COOKIE_NAME"] = "session_cookie" 
app.config['SECRET_KEY'] = 'Kimperor123'

def userlogin(username: str, password: str) -> bool:
    sql = "SELECT * FROM users WHERE username = ? AND password = ?"
    db = connect('studentinfo.db')
    cursor = db.cursor()
    cursor.row_factory = Row
    cursor.execute(sql, (username, password))
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return len(data) > 0

@app.route('/login', methods=['POST', 'GET'])
def login():
    pagetitle = "User Login"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Both username and password are required", 'error')
            return redirect(url_for('login'))
        if userlogin(username, password):
            session['username'] = username
            flash("User Login successfully!", 'success')  
            return redirect(url_for('student_list'))
        else:
            flash("Invalid username or password", 'error') 
            return redirect(url_for('login')) 
    return render_template('login.html', pagetitle=pagetitle)

@app.route('/students')
def student_list():
    if 'username' in session:
        pagetitle = "Student List"
        print(f"User logged in: {session['username']}")
        return render_template('index.html', data=getall_records('students'), pagetitle=pagetitle, users=get_users())
    else:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info') 
    return redirect(url_for('login'))

@app.route('/')
def index():
    return redirect(url_for('login'))


uploadfolder = 'static/img/'
app.config['SECRET_KEY'] = '!@#$%^'
app.config['UPLOAD_FOLDER'] = uploadfolder

def get_users() -> object:
	return getall_records('students')

def get_user(idno:str) -> object:
	return getone_record('students', idno=idno)

def substringer(s, phrase):
    i = s.find(phrase)
    return s[i + len(phrase):] if i != -1 else ''

@app.route('/register', methods=['POST'])
def register():
    idno = request.form['idno']
    lastname = request.form['lastname']
    firstname = request.form['firstname']
    course = request.form['course']
    level = request.form['level']
    flag = request.form['flag']
    file = request.files['uploadimage']

    if not idno.isdigit():
        flash("ID Number must contain only digits!", 'error')
        return redirect(url_for('student_list'))

    existing_user = getone_record('students', idno=idno)

    if existing_user and flag == '0':  
        flash(f"Student Idno '{idno}' already exists!", 'warning')
        return redirect(url_for('student_list')) 

    imagename = ''
    if file and file.filename != '':
        filename, extension = os.path.splitext(file.filename)
        imagename = os.path.join(uploadfolder, f'{filename}_{idno}{extension}')
        file.save(imagename)

    try:
        ok = False
        if flag == '0': 
            if imagename:
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)

            msg = "Student Registered Successfully!" if ok else "Error Registering User!"
            flash(msg, 'success' if ok else 'error')  

        else:  
            existing_student = getone_record('students', idno=idno)

            if not existing_student:
                flash("Student not found.", 'error')
                return redirect(url_for('student_list'))

            old_image = existing_student[0]['image']

            if (existing_student[0]['lastname'] == lastname and
                existing_student[0]['firstname'] == firstname and
                existing_student[0]['course'] == course and
                existing_student[0]['level'] == level and
                (not imagename or old_image == imagename)):
                flash("No changes were made.", 'info')
            else:
                if imagename and old_image != imagename:
                    if os.path.exists(old_image):
                        os.remove(old_image)  

                if imagename: 
                    ok = update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
                else: 
                    ok = update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)

                msg = "Student Updated Successfully!" if ok else "Error Updating Student!"
                flash(msg, 'success' if ok else 'error')

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')

    return redirect(url_for('student_list'))




@app.route('/delete_user', methods=['POST'])
def delete_user():
    idno: str = request.form['idno']
    print(f"Deleting user with ID: {idno}") 
    imagename: str = get_user(idno)[0]['image']
    print(f"Image path: {imagename}") 
    ok: bool = delete_record('students', idno=idno)
    
    if ok:
        message: str = "User deleted successfully!"
        flash(message, 'delete-success')
    else:
        message: str = "Deleting User: Something went wrong"
        flash(message, 'error')
    
    try:
        if os.path.exists(imagename):
            os.remove(imagename)
            print(f"Deleted image: {imagename}")
    except Exception as e:
        flash(f"Error within '/delete_user': File path error", 'error')
        print(e)
    
    return redirect(url_for('student_list'))



@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True) 