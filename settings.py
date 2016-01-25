from watson_developer_cloud import ToneAnalyzerV2Experimental as ToneAnalyzer
import os

IBM_USERNAME = os.environ.get('IBM_USERNAME')
IBM_PASSWORD = os.environ.get('IBM_PASSWORD')

tone_analyzer = ToneAnalyzer(username=IBM_USERNAME, password=IBM_PASSWORD)
