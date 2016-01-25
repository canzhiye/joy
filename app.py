from flask import Flask, request
from slacker import Slacker
import os
import pickle

app = Flask(__name__)

tokens = {}

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

@app.route('/auth', methods=['GET'])
def oauth():
    code = request.args.get('code')
    print(os.environ['CLIENT_ID'])
    print(os.environ['CLIENT_SECRET'])
    print(code)
    try:
        oauth_info = Slacker.oauth.access(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'], code)
        print(oauth_info.body)
    except Exception as e: 
        print(e)
    
        team_id = oauth_info.body['team_id']
        bot_access_token = oauth_info.body['bot']['bot_access_token']

        tokens[team_id] = bot_access_token

        with open('tokens.pickle', 'wb') as f:
                pickle.dump(tokens, f)

    return "success!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')