from flask import Flask, request
from slacker import Slacker

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/auth', methods=['GET'])
def oauth():
    code = request.args.get('code')
    print(code)

    oauth_info = Slacker.oauth.access(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'], code).body
    print(oauth_info)
    return 'successfully authenticated'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
