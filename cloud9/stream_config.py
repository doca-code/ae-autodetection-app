# Twitter Authentication: update with your own credentials
APP_KEY ='d05YTsI9Yxtz2pMHHuqmrGCvN'
APP_SECRET = 'cRaxm4DK4ZDpBpYDShZF5XJMPJTFaflpxJRZMwhVC5KGEjF71E'
OAUTH_TOKEN = '204861017-s4FR4c6RTW3RJYfzDKbFCl7kek159z2gPXK2waED'
OAUTH_TOKEN_SECRET = 'NeHIpqnGcN11M46PrSLcmtxKlZCpLm6yETuS3JOB19KDw'
bearer_token='AAAAAAAAAAAAAAAAAAAAAAIi0AEAAAAAVFOWFRcGMFgK6%2F12WKhFrLVk9Ww%3DgbKNBAKiDYuhTzEkqyWev3tiefMJ48bQ7REjBEUfzg1C2QFhyo' 

# Twitter Rules List (stream filters), see Twitter docs for details
# Note that these rules are overwritten each time the script is run!
sample_rules = [
    { 'value': 'prozac OR fluoxetine OR cymbalta OR celexa OR citalopram OR amoxil OR amoxicillin OR moxatag OR lexapro OR escitalopram lang:en -is:retweet', "tag": "newest"},]

# List of drug brand names to be extract from raw tweets.
drug_names = [['prozac', 'fluoxetine'], ['celexa', 'citalopram'], 
              ['cymbalta', 'duloxetine'], ['lexapro', 'escitalopram'], 
              ['moxatag', 'amoxicillin','amoxil']]  # [[brand name, name variant 1, name variant 2, ...], ...]

# DynamoDB Information
region_name ='us-east-1'
aws_access_key_id = '' # update with your own credentials
aws_secret_access_key = '' #update with your own credentials 
table_name = 'ae_tweets_ddb'
