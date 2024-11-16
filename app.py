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
        print(f"User logged in: {session['username']}")  # Debugging line to see session value
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
    idno: str = request.form['idno']
    lastname: str = request.form['lastname']
    firstname: str = request.form['firstname']
    course: str = request.form['course']
    level: str = request.form['level']
    flag: str = request.form['flag']
    file: object = request.files['uploadimage']

    if not idno.isdigit():
        flash("ID Number must contain only digits!", 'error')
        return redirect(url_for('student_list'))  # Change this line

    existing_user = get_user(idno)
    
    if existing_user and flag == '0':  
        flash(f"User ID '{idno}' already exists!", 'warning')
        return redirect(url_for('student_list'))  # Change this line

    imagename = ''
    if file.filename != '':
        filename, extension = os.path.splitext(file.filename)
        imagename = os.path.join(uploadfolder, f'{filename}{idno}{extension}')
    
    try:
        ok: bool = False
        if flag == '0':  
            if file.filename != '':
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
            
            msg: str = "New User Registered!" if ok else "Error Registering User!"
            flash(msg, 'success' if ok else 'error')  
            
        else:
            if file.filename != '':
                ok = update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
            
            msg: str = "User Updated Successfully!" if ok else "Error Updating User!"
            flash(msg, 'success' if ok else 'error') 
        
        if file.filename != '' and ok:
            file.save(imagename)
    except Exception as e:
        flash(f"File Saving Error: {e}", 'error') 
    return redirect(url_for('student_list')) 



@app.route('/delete_user', methods=['POST'])
def delete_user():
    idno: str = request.form['idno']
    imagename: str = get_user(idno)[0]['image']
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
    except Exception as e:
        flash(f"Error within '/delete_user': File path error", 'error')  # Red for file errors
        print(e)
    
    return redirect('index')


@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True) 