from settings import slack_socket, slack, tone_analyzer
import json
from models import User, Channel
import pickle
from helper import compute_team_morale, compute_person_channel_morale
import os

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

def start():
    for event in slack_socket.events():
        res = json.loads(event.json)
        if res['type'] == 'message' and 'user' in res and res['user'] != 'joy':
            print(res)

            message = res['text']
            user = res['user']
            channel = res['channel']
            timestamp = res['ts']

            if '@U0K36FLRZ' in message:
                if 'get morale' in message.lower():
                    t = message.lower().split('get morale ')
                    person = ''
                    if len(t) > 1:
                        person = t[1]
                        # print(person)
                        slack_socket.send_msg(str(compute_person_channel_morale(people, channels, person)), channel_name=channel)
                    else:
                        slack_socket.send_msg(str(compute_team_morale(people)), channel_name=channel)
                elif 'get happiness' in message.lower():
                    pass
                continue

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

            # print('cheerfulness: ' + str(cheerfulness))
            # print('negative: ' + str(negative))
            # print('anger: ' + str(anger))
            # print('analytical: ' + str(analytical))
            # print('confident: ' + str(confident))
            # print('tentative: ' + str(tentative))
            # print('openness: ' + str(openness))
            # print('agreeableness: ' + str(agreeableness))
            # print('conscientiousness: ' + str(conscientiousness))

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

            # org = (0.75/2.54) * (confident + conscientiousness + analytical)
            # morale = 
            # if user in people:
            #     people[user] = collect(people[user], sentiment)
            # else:
            #     people[user] = sentiment
            if channel in channels:
                channels[channel].add_sentiment(sentiment)

            if user in people:
                people[user].add_sentiment(sentiment)

            with open('people.pickle', 'wb') as f:
                pickle.dump(people, f)

            with open('channels.pickle', 'wb') as f:
                pickle.dump(channels, f)

            # channels[channel] = collect(channels[channel], sentiment)

            # print(people[user])
            # print(channels[channel].sentiment)
            # print('   ')


start()

