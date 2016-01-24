from settings import slack, slack_socket
from helper import compute_person_channel_morale
import pickle

people = {}
channels = {}
with open('people.pickle', 'rb') as f:
    people = pickle.load(f)

with open('channels.pickle', 'rb') as f:
    channels = pickle.load(f)

for key in people:
    person = people[key]

    morale = compute_person_channel_morale(people, channels, person.name)

    if type(morale) is float and morale < 0.5:
        try:
            res = slack.im.open(person._id)
            c_id = res.body['channel']['id']
            msg = slack_socket.send_msg('hey, you seem to be a bit down today. is everything alright?', channel_id=c_id)
        except:
            pass