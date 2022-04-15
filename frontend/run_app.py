import os
import uvicorn
import dominate
from dominate.tags import *
from dotenv import load_dotenv
from fastapi import Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from idom.server import fastapi
from idom.server.starlette import Options
from pathlib import Path
from requests_oauthlib import OAuth2Session
from starlette.middleware.sessions import SessionMiddleware
from index import page as index_page

# Load in env variables
load_dotenv()

# to be removed and replaced with docker-compose-dev
TIMEFLOW_DEV = os.getenv("TIMEFLOW_DEV")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY")

# OAuth endpoints given in the GitHub API documentation
authorization_base_url = "https://github.com/login/oauth/authorize"
token_url = "https://github.com/login/oauth/access_token"

# Create the fastapi app
app = fastapi.create_development_app()

# Specify location of static files
HERE = Path(__file__).parent
app.mount("/static", StaticFiles(directory=str(HERE)), name="static")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

# Configure app with idom index page
fastapi.configure(app, index_page, Options(redirect_root=False, url_prefix="/_idom"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/", response_class=RedirectResponse)
async def main(request: Request):
    """
    Redirect to login page.
    """
    login_url = f"{str(request.url)}login"
    return login_url


@app.get("/login", response_class=RedirectResponse)
async def login(request: Request):
    """
    Redirect user to GitHub for authentication.
    Future: Implement button that user clicks to cause the redirection.
    """

    github = OAuth2Session(GITHUB_CLIENT_ID, scope=["read:org", "read:user"])

    # Redirect user to GitHub for authorization
    authorization_url, state = github.authorization_url(authorization_base_url)
    request.session["oauth_state"] = state
    return authorization_url


@app.get("/callback", response_class=RedirectResponse)
async def callback(request: Request):
    """
    Fetch token of user and redirect to subdirectory /organizations.
    """
    github = OAuth2Session(GITHUB_CLIENT_ID, state=request.session["oauth_state"])
    authorization_response = str(request.url)

    # Convert authorization_reponse url to return with https
    if TIMEFLOW_DEV != "true":
        authorization_response = str(request.url)[:4] + "s" + str(request.url)[4:]
    token = github.fetch_token(
        token_url,
        client_secret=GITHUB_CLIENT_SECRET,
        authorization_response=authorization_response,
    )
    request.session["oauth_token"] = token
    organizations_url = f"{str(request.base_url)}organizations"
    return organizations_url


@app.get("/organizations", response_class=RedirectResponse)
async def organizations(request: Request):
    """
    Fetch organizations of user and determine role.
    """
    github = OAuth2Session(
        GITHUB_CLIENT_ID,
        token=request.session["oauth_token"],
        state=request.session["oauth_state"],
    )

    github_api = github.get("https://api.github.com/user").json()
    username = github_api["login"]

    # Use dyvenia api with user's username to check if user is in team
    dyvenia_api = github.get(
        f"https://api.github.com/organizations/81221495/team/4777989/members/{username}"
    )

    # Give admin permissions to user if app is ran in dev mode
    if TIMEFLOW_DEV == "true":
        request.session["role"] = "admin"
        return f"{str(request.base_url)}home"

    # User not dyvenia's core team
    if dyvenia_api.status_code == 404:
        return str(request.base_url)
    # User in dyvenia's core team
    elif dyvenia_api.status_code == 204:
        # Check if user is in the GitHub TimeFlow Admin Team
        admin_team = github.get(
            f"https://api.github.com/organizations/81221495/team/5925377/members/{username}"
        )

        if admin_team.status_code == 404:
            request.session["role"] = "user"
        elif admin_team.status_code == 204:
            request.session["role"] = "admin"

        return f"{str(request.base_url)}home"


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """
    Create home page of TimeFlow.
    """
    d = dominate.document(title="TimeFlow", doctype="<!DOCTYPE html>")
    d.head += meta(charset="UTF-8")
    d.head += link(rel="css/styles.css", type="text/css", href="static/css/styles.css")
    d.head += script(type="module", src="static/embedding_script.js")
    d += div(id="idom-app")
    return d.render()


def run():
    """
    Run the app in production or developer mode.
    """

    if os.environ["TIMEFLOW_DEV"] == "true":
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            workers=1,
            access_log=True,
            ssl_keyfile="./127.0.0.1-key.pem",
            ssl_certfile="./127.0.0.1.pem",
        )
    else:
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8001,
            workers=1,
            access_log=True,
        )


run()
