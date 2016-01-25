#!/usr/bin/env python3
from slacksocket import SlackSocket
from slacker import Slacker
from helper import compute_person_channel_morale
import pickle
import schedule
import time

def notify():
    teams = {}

    with open('teams.pickle', 'rb') as f:
        teams = pickle.load(f)
        print(teams.keys())

    for team_key in teams:
        team = teams[team_key]

        SLACK_TOKEN = ''
        with open('tokens.pickle', 'rb') as f:
            tokens = pickle.load(f)
            print(tokens)
            SLACK_TOKEN = tokens[team_key]

        slack_socket = SlackSocket(SLACK_TOKEN, translate=True)
        slack = Slacker(SLACK_TOKEN)

        people = team['people']
        channels = team['channels']

        for key in people:
            person = people[key]
            print(person.name)

            compute_person_channel_morale(slack, people, channels, person.name)
            morale = person.morale
            print(morale)

            if type(morale) is float and morale < 0.15:
                try:
                    res = slack.im.open(person._id)
                    c_id = res.body['channel']['id']
                    msg = slack_socket.send_msg('hey, you seem to be a bit down today. is everything alright?', channel_id=c_id)
                    if msg.sent:
                        print('message sent to: ' + person.name)
                except:
                    pass

schedule.every().day.at("12:30").do(notify)
schedule.every().day.at("14:00").do(notify)

# UNCOMMENT TO TEST
# schedule.every(1).minutes.do(notify)
# notify()

while True:
    schedule.run_pending()
    time.sleep(1)