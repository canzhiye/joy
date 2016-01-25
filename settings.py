from slacksocket import SlackSocket
from slacker import Slacker
from watson_developer_cloud import ToneAnalyzerV2Experimental as ToneAnalyzer
import os
import pickle

SLACK_TOKEN = os.environ.get('SLACK_TOKEN')

# with open('tokens.pickle', 'rb') as f:
# 	tokens = pickle.load(f)

IBM_USERNAME = os.environ.get('IBM_USERNAME')
IBM_PASSWORD = os.environ.get('IBM_PASSWORD')

slack_socket = SlackSocket(SLACK_TOKEN, translate=True)
slack = Slacker(SLACK_TOKEN)

tone_analyzer = ToneAnalyzer(username=IBM_USERNAME, password=IBM_PASSWORD)
