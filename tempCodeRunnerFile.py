@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info') 
    return redirect(url_for('login'))