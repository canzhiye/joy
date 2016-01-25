import re
from random import randint

def compute_team_morale(people):
    org_score = 0
    supervisor_score = 0
    colleagues_score = 0

    managers = 0
    others = 0

    for name in people:
        
        person = people[name]

        if person.sentiment != {}:
            print(person.sentiment)
            cheerfulness = sum(person.sentiment['cheerfulness']) / len(person.sentiment['cheerfulness'])
            anger = sum(person.sentiment['anger']) / len(person.sentiment['anger'])
            negative = sum(person.sentiment['negative']) / len(person.sentiment['negative'])
            confident = sum(person.sentiment['confident']) / len(person.sentiment['confident'])
            analytical = sum(person.sentiment['analytical']) / len(person.sentiment['analytical'])
            conscientiousness = sum(person.sentiment['conscientiousness']) / len(person.sentiment['conscientiousness'])
            agreeableness = sum(person.sentiment['agreeableness']) / len(person.sentiment['agreeableness'])

            friendliness = cheerfulness # - (anger + negative) / 2

            if friendliness < 0:
                friendliness = 0

            if person.manager:
                managers += 1
                org_score += (confident + conscientiousness + analytical) / 3
                supervisor_score += (friendliness + agreeableness) / 2
            else:
                others += 1
            
            colleagues_score += friendliness

    print('others: ' + str(others))
    print('managers: ' + str(managers))
    print('org_score: ' + str(org_score))
    print('supervisor_score: ' + str(supervisor_score))
    print('colleagues_score: ' + str(colleagues_score))

    if others != 0:
        colleagues_score = colleagues_score / others

    if managers == 0:
        person.morale = colleagues_score
        return score_to_phrase(colleagues_score)
    else:
        org_score = org_score / managers
        supervisor_score = supervisor_score / managers

        morale = (0.75/1.95) * org_score + (0.51/1.95) * supervisor_score + (0.69/1.95) * colleagues_score
        person.morale = morale
        return score_to_phrase(morale)

def compute_person_channel_morale(slack, people, channels, name):
    if name.startswith('<'):
        name = re.sub('[^A-Za-z0-9]+', '', name).upper()

        if name.startswith('U'):
            r = slack.users.info(user=name)
            name = r.body['user']['name']
        elif name.startswith('C'):
            r = slack.channels.info(channel=name)
            name = r.body['channel']['name']
    
    thing = None

    if name in people:
        thing = people[name]
    elif name in channels:
        thing = channels[name]

    if thing != None and thing.sentiment != {}:
        cheerfulness = sum(thing.sentiment['cheerfulness']) / len(thing.sentiment['cheerfulness'])
        thing.morale = cheerfulness
        return score_to_phrase(cheerfulness)
    else:
        return 'hmmm, haven\'t heard enough from ' + name


def score_to_phrase(score):
    very_sad_phrases = ['things aren\'t looking so hot. perhaps a break is in order?', 'oh no! we need more Joy, and less Fear, Disgust, and Anger!']
    sad_phrases = ['we need more Joy, and less Fear, Disgust, and Anger!']
    neutral_phrases = ['as I always like to say, "Think positive!"']
    happy_phrases = ['good vibes, good vibes :simple_smile:']
    very_happy_phrases = ['glad you all are having a great time! :simple_smile: :+1: :100:', 'hear we come, Friendship Island! :simple_smile:']

    phrase = ''
    if score > 0.4:
        i = randint(0, len(very_happy_phrases) - 1)
        phrase = very_happy_phrases[i]
    elif score > 0.3:
        i = randint(0, len(happy_phrases) - 1)
        phrase = happy_phrases[i]
    elif score > 0.2:
        i = randint(0, len(neutral_phrases) - 1)
        phrase = neutral_phrases[i]
    elif score > 0.1:
        i = randint(0, len(sad_phrases) - 1)
        phrase = sad_phrases[i]
    else:
        i = randint(0, len(very_sad_phrases) - 1)
        phrase = very_sad_phrases[i]

    return phrase


