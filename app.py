from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
from dbhelper import *

app = Flask(__name__)

app.config
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp/sessions" 
app.config["SESSION_COOKIE_NAME"] = "session_cookie" 
app.config['SECRET_KEY'] = 'Kimperor123'
uploadfolder = 'static/img/'
app.config['UPLOAD_FOLDER'] = uploadfolder


def get_users() -> object:
	return getall_records('students')

def get_user(idno:str) -> object:
	return getone_record('students', idno=idno)

def substringer(s, phrase):
    i = s.find(phrase)
    return s[i + len(phrase):] if i != -1 else ''


@app.route('/login', methods=['POST', 'GET'])
def login():
    pagetitle = "User Login"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash("Username and Password are required", 'error')
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

@app.route('/check_student_exists')
def check_student_exists():
    idno = request.args.get('idno')
    existing_user = get_user(idno=idno)
    if existing_user:
        return jsonify({"exists": True})
    else:
        return jsonify({"exists": False})

@app.route('/register', methods=['POST'])
def register():
    try:
        idno = request.form['idno']
        lastname = request.form['lastname']
        firstname = request.form['firstname']
        course = request.form['course']
        level = request.form['level']
        flag = request.form.get('flag', '0')
        image_file = request.files.get('image_data')  
        imagename = ''

        if not idno.isdigit():
            flash("ID Number must contain only digits!", 'error')
            return redirect(url_for('student_list'))
        
        if image_file:
            filename = f'{idno}.png' 
            imagename = os.path.join(uploadfolder, filename)
            try:
                image_file.save(imagename)
            except Exception as e:
                flash(f"Error saving image: {str(e)}", 'error')
                return redirect(url_for('student_list'))
        
        if flag == '0':
            existing_user = get_user(idno=idno)
            if existing_user:
                flash(f"Student {idno} already exists!", 'warning')
                return redirect(url_for('student_list'))  
            ok = False
            if imagename:
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
            else:
                ok = add_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level)
            
            msg = "Student Registered Successfully!" if ok else "Error Registering User!"
            flash(msg, 'success' if ok else 'error')
        else:
            existing_user = getone_record('students', idno=idno)
            
            if existing_user:
                old_image = existing_user[0]['image']
                if not imagename:
                    imagename = old_image 
                else:
                    if old_image != imagename and os.path.exists(old_image):
                        try:
                            os.remove(old_image)
                        except Exception as e:
                            flash(f"Error removing old image: {str(e)}", 'error')
                            return redirect(url_for('student_list'))
                ok = update_record('students', idno=idno, lastname=lastname, firstname=firstname, course=course, level=level, image=imagename)
                msg = "Student Updated Successfully!" if ok else "Error Updating Student!"
                flash(msg, 'success' if ok else 'error')
            else:
                flash("Student not found, unable to update.", 'error')

    except Exception as e:
        flash(f"Error: {str(e)}", 'error')

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
        flash(f"Error within '/delete_user': File path error", 'error')
    
    return redirect(url_for('student_list'))



@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True) 