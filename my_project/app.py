from flask import Flask, redirect, url_for, request, session, render_template
import requests

app = Flask(__name__)
app.secret_key = "barryisgay"
# Replace these with your own client ID and client secret
CLIENT_ID = "c1f4309625494c848f3d90c0b3f96813"
CLIENT_SECRET = "7b676d5c061c439389d95257530a0a76"

# This is the URL of your app's homepage
REDIRECT_URI = "http://localhost:5000/callback"

# This is the URL that the user will be redirected to after they grant
# permission to your app
CALLBACK_URI = "http://localhost:5000/home"

@app.route("/")
def homepage():
    return render_template("login.html")

@app.route("/login")
def login():
    # Generate a URL that the user can use to grant permission to your app
    scope = "user-read-private user-read-email"
    url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={scope}"
    return redirect(url)

@app.route("/callback")
def callback():
    # Get the authorization code from the query string
    code = request.args.get("code")

    # Use the authorization code to request an access token
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
    token = response.json()["access_token"]

    # Save the access token in a session cookie
    session["access_token"] = token

    # Redirect the user to the app's homepage
    return redirect(url_for("home"))


@app.route("/home")
def home():
    # Get the access token from the session cookie
    token = session.get("access_token")

    # Use the access token to authenticate the user and make API requests
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    user = response.json()
    return f"Welcome, {user['display_name']}!"

if __name__ == "__main__":
    app.run()
