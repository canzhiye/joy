from flask import Flask, request, redirect
from slacker import Slacker
import os
import pickle
from joy import start_joy

app = Flask(__name__)

tokens = {}

@app.route("/")
def hello():
    return redirect('http://canzhiye.com')

@app.route('/auth', methods=['GET'])
def oauth():
    code = request.args.get('code')
    print(os.environ['CLIENT_ID'])
    print(os.environ['CLIENT_SECRET'])
    print(code)
    try:
        oauth_info = Slacker.oauth.access(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'], code)
        print(oauth_info.body)

        team_id = oauth_info.body['team_id']
        bot_access_token = oauth_info.body['bot']['bot_access_token']
        bot_id = oauth_info.body['bot']['bot_user_id']

        try:
            with open('tokens.pickle', 'rb') as f:
                tokens = pickle.load(f)
        except:
            pass

        tokens[team_id] = (bot_access_token, bot_id)

        with open('tokens.pickle', 'wb') as f:
            pickle.dump(tokens, f)

        return redirect(oauth_info.body['incoming_webhook']['configuration_url'])
    except Exception as e: 
        print(e)
        return e

if __name__ == "__main__":
    app.run(host='0.0.0.0')
