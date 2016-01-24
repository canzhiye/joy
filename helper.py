import re
from settings import slack

def compute_team_morale(people):
    org_score = 0
    supervisor_score = 0
    colleagues_score = 0

    managers = 0
    others = 0

    for name in people:
        
        person = people[name]

        if person.sentiment != {}:
            # print(person.sentiment['cheerfulness'])
            cheerfulness = sum(person.sentiment['cheerfulness']) / 10
            anger = sum(person.sentiment['anger']) / 10
            negative = sum(person.sentiment['negative']) / 10
            confident = sum(person.sentiment['confident']) / 10
            analytical = sum(person.sentiment['analytical']) / 10
            conscientiousness = sum(person.sentiment['conscientiousness']) / 10
            agreeableness = sum(person.sentiment['agreeableness']) / 10

            friendliness = cheerfulness - (anger + negative) / 2

            if friendliness < 0:
                friendliness = 0

            if person.manager:
                managers += 1
                org_score += (confident + conscientiousness + analytical) / 3
                supervisor_score += (friendliness + agreeableness) / 2
            else:
                others += 1
            
            colleagues_score += friendliness

    if others != 0:
        colleagues_score = colleagues_score / others

    if managers == 0:
        # print(colleagues_score)
        return colleagues_score
    else:
        org_score = org_score / managers
        supervisor_score = supervisor_score / managers

        morale = (0.75/1.95) * org_score + (0.51/1.95) * supervisor_score + (0.69/1.95) * colleagues_score
        # print(morale)
        return morale

def compute_person_channel_morale(people, channels, name):
    if name.startswith('<'):
        name = re.sub('[^A-Za-z0-9]+', '', name).upper()
        print(name)

        if name.startswith('U'):
            r = slack.users.info(user=name)
            name = r.body['user']['name']
        elif name.startswith('C'):
            r = slack.channels.info(channel=name)
            name = r.body['channel']['name']
    
    thing = None

    if name in people:
        print(name)
        thing = people[name]
        print(thing)
    elif name in channels:
        thing = channels[name]

    if thing != None and thing.sentiment != {}:
        cheerfulness = sum(thing.sentiment['cheerfulness']) / 10
        return cheerfulness
    else:
        return 'hmmm, haven\'t heard enough from ' + name