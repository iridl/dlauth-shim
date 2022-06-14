from flask import Flask, session, redirect, url_for, escape, request
from simplepam import authenticate
import urllib


app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        redirect_url = request.form['redirect']
        if authenticate(str(username), str(password)):
            session['username'] = request.form['username']
            return redirect(redirect_url)
        else:
            return 'Invalid username/password'

    assert request.method == 'GET'
    redirect_url = urllib.parse.unquote_plus(request.args.get('redirect'))
    return f'''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
            <input name="redirect" type="text" value="{redirect_url}" hidden="">
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'shh'

if __name__ == '__main__':
    app.run(debug='True', port=5001)
