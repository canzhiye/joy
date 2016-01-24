class BaseSentiment:
    name = ''
    _id = ''
    sentiment = {}

    def __init__(self, name, id, s={}):
        self.name = name
        self.sentiment = s
        self._id = id

    def add_sentiment(self, s):
        if self.sentiment != {}:
            for key in self.sentiment.keys():
                if len(self.sentiment[key]) > 9:
                    self.sentiment[key] = self.sentiment[key][1:]
                self.sentiment[key].append(s[key][0]) 
        else:
            self.sentiment = s  

class Channel(BaseSentiment):
    pass

class User(BaseSentiment):
    manager = False

        