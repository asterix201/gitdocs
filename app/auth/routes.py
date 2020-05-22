from flask import render_template, flash, redirect, url_for, \
    request, current_app, session, make_response, g
import requests_oauthlib
from . import auth_bp
from requests.auth import HTTPBasicAuth


# @auth_bp.before_request
# def before_request():
#     g.is_authenticated = False
#     if is_logged_in():
#         g.is_authenticated = True


@auth_bp.route("/login")
def login():
    return render_template('login.html', title='Login')


@auth_bp.route('/decathlon_login')
def decathlon_login():
    decathlon = requests_oauthlib.OAuth2Session(
        client_id=current_app.config['DECATHLON_CLIENT_ID'],
        redirect_uri=current_app.config['DECATHLON_REDIRECT_URI'],
        state=current_app.config['SECRET_KEY'],
        scope=current_app.config['DECATHLON_SCOPE'],
    )
    authorization_url, _ = decathlon.authorization_url(
        current_app.config['DECATHLON_AUTHORIZATION_URL']
    )

    session['AUTH_STATE_KEY'] = current_app.config['SECRET_KEY']
    session.permanent = True

    return redirect(authorization_url)


@auth_bp.route('/callback')
def callback():
    req_state = request.args.get('state', default=None, type=None)

    if req_state != session['AUTH_STATE_KEY']:
        response = make_response('Invalid state parameter', 401)
        return response

    decathlon = requests_oauthlib.OAuth2Session(
        client_id=current_app.config['DECATHLON_CLIENT_ID'],
        redirect_uri=current_app.config['DECATHLON_REDIRECT_URI'],
        scope=current_app.config['DECATHLON_SCOPE']
    )
    auth = HTTPBasicAuth(
        current_app.config['DECATHLON_CLIENT_ID'],
        current_app.config['DECATHLON_CLIENT_SECRET']
    )
    authorization_response = request.url
    oauth2_token = decathlon.fetch_token(
        current_app.config['DECATHLON_ACCESS_TOKEN_URL'],
        authorization_response=authorization_response,
        auth=auth,
        scope=current_app.config['DECATHLON_SCOPE']
    )
    session['AUTH_TOKEN'] = oauth2_token

    # info = decathlon.token
    # return f"""
    #     {info}
    #     <a href="/">Home</a>
    #     """
    return redirect(url_for('main_bp.index'))


@auth_bp.route('/logout')
def logout():
    session.pop('AUTH_TOKEN', None)
    session.pop('AUTH_STATE_KEY', None)
    flash('You are logged out.')

    return redirect(url_for('main_bp.index'), code=302)
