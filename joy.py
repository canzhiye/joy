from slacksocket import SlackSocket
from slacker import Slacker
from settings import tone_analyzer
import json
from models import User, Channel
import pickle
from helper import compute_team_morale, compute_person_channel_morale
import os

def start_joy(team_id, bot_id):
    SLACK_TOKEN = ''
    with open('tokens.pickle', 'rb') as f:
        tokens = pickle.load(f)
        SLACK_TOKEN = tokens[team_id]

    slack_socket = SlackSocket(SLACK_TOKEN, translate=True)
    slack = Slacker(SLACK_TOKEN)

    response = slack.channels.list()
    channels = {}
    for c in [u for u in response.body['channels']]:
        name = c['name']
        user_id = c['id']

        channels[name] = Channel(name, user_id)

    response = slack.users.list()
    people = {}
    for p in [u for u in response.body['members']]:
        name = p['name']
        user_id = p['id']

        person = User(name, user_id)
        if 'is_admin' in p:
            person.manager = p['is_admin']
        else:
            person.manager = False

        people[name] = person

    print('starting joy on ' + team_id)

    for event in slack_socket.events():
        res = json.loads(event.json)

        if 'team' in res and res['team'] == team_id and res['type'] == 'message' and 'user' in res and res['user'] != 'joy':
            print(res)
            team_id = res['team']
            message = res['text']
            user = res['user']
            channel = res['channel']
            timestamp = res['ts']

            BOT = 'NO BOT'
            if bot_id in message:
                BOT = 'YES BOT'

                if 'get morale' in message.lower():
                    t = message.lower().split('get morale ')
                    person = ''
                    if len(t) > 1:
                        person = t[1]
                        # print(person)
                        slack_socket.send_msg(str(compute_person_channel_morale(slack, people, channels, person)), channel_name=channel)
                    else:
                        slack_socket.send_msg(str(compute_team_morale(people)), channel_name=channel)
                continue

            print(BOT)
            res = tone_analyzer.tone(text=message)
            emotional_tone = res['children'][0]
            writing_tone = res['children'][1]
            social_tone = res['children'][2]

            cheerfulness = float(emotional_tone['children'][0]['normalized_score'])
            negative = float(emotional_tone['children'][1]['normalized_score'])
            anger = float(emotional_tone['children'][2]['normalized_score'])

            analytical = float(writing_tone['children'][0]['normalized_score'])
            confident = float(writing_tone['children'][1]['normalized_score'])
            tentative = float(writing_tone['children'][2]['normalized_score'])
           
            openness = float(social_tone['children'][0]['normalized_score'])
            agreeableness = float(social_tone['children'][1]['normalized_score'])
            conscientiousness = float(social_tone['children'][2]['normalized_score'])

            sentiment = {
                'cheerfulness' : [cheerfulness],
                'negative' : [negative],
                'anger' : [anger],
                'analytical' : [analytical],
                'confident' : [confident],
                'tentative' : [tentative],
                'openness' : [openness],
                'agreeableness' : [agreeableness],
                'conscientiousness' : [conscientiousness]         
            }

            
            teams = {}
            try:
                with open('teams.pickle', 'rb') as f:
                    teams = pickle.load(f)
                    # print('load current teams: ' + str(teams.keys()))
            except:
                pass

            if team_id in teams:
                if channel in channels:
                    teams[team_id]['channels'][channel].add_sentiment(sentiment)
                    channels = teams[team_id]['channels']

                if user in people:
                    teams[team_id]['people'][user].add_sentiment(sentiment)
                    people = teams[team_id]['people']
            else:
                d = {'channels' : channels, 'people' : people}
                teams[team_id] = d

            # print('saving ' + team_id)
            # print('current teams: ' + str(teams.keys()))

            with open('teams.pickle', 'wb') as f:
                pickle.dump(teams, f)

