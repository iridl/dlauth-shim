import datetime
from flask import Flask, session, redirect, url_for, escape, request
import urllib


app = Flask(__name__)
app.secret_key = 'shh'
app.config.update(
    SESSION_COOKIE_NAME="__dlauth_id",
    PERMANENT_SESSION_LIFETIME=datetime.timedelta(days=1),
    #SESSION_COOKIE_SECURE=True, # only send over https
    SESSION_COOKIE_HTTPONLY=False,
)



@app.route('/api/check') # ?ssid=abcde
def index():
    ssid = request.args.get('ssid')
    ssid_serializer = app.session_interface.get_signing_serializer(app)
    ssid_contents = ssid_serializer.loads(ssid) # todo max-age
    print(ssid_contents)
    if 'username' in ssid_contents:
        response = dict(errcode=0, code=200, errstr="", redirect=None)
    else:
        response = dict(
            errcode=2,
            code=200,
            errstr="missing credential",
            redirect=ingrid_url_for('login')
        )
    print(response)
    return response


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        redirect_url = request.form['redirect']
        if authenticate(username, password):
            print('AUTHENICATION SUCESSFUL')
            session['username'] = username
            session.permanent = True
            for k, v in session.items():
                print(k, v)
            return redirect(redirect_url)
        else:
            print('AUTH FAILED')
            return redirect(ingrid_url_for('login', redirect=redirect_url))
 
    assert request.method == 'GET'
    redirect_url = urllib.parse.unquote_plus(request.args.get('redirect', ''))
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
    return redirect(ingrid_url_for('index'))


@app.route('/key')
def api_credential():
    if 'username' in session:
        key = request.cookies[app.config['SESSION_COOKIE_NAME']]
        return(key)
    return redirect(ingrid_url_for('login', redirect=ingrid_url_for('api_credential')))


def ingrid_url_for(method, **kwargs):
    '''Like flask.url_for but ensures that the '?' that starts the
querystring is present, because Ingrid never adds one.'''
    url = url_for(method, **kwargs)
    if len(kwargs) == 0:
        url += '?'
    return url


def authenticate(user, password):
    if user == 'aaron' and password == 'thepass':
        return True
    return False


if __name__ == '__main__':
    app.run(debug='True', port=5001)
