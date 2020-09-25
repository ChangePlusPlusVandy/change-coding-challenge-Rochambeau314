
import json
import random
import re
from requests_oauthlib import OAuth1Session



"""
When user starts program, load the first 3200 tweets by Elon and Kanye, 
filtered to not include any links or tags to other twitter users
Randomly choose a tweet by Elon or Kanye to give to the user
Prompt the user to guess
Let the user know if they were correct
Repeat steps 2-4
Show the user their game statistics
"""

"""
randomly selects whether the tweet will come from Elon Musk or Kanye West
"""
def elon_or_kanye():
    renaissance_man = random.randint(0, 1)
    if renaissance_man == 1:
        return "Kanye West"
    else:
        return "Elon Musk"

"""
Generates an API request
"""
def twitter_API(person):
    consumer_key = '8XFYuKXJlPeiwdRqz8OEgSXJW'  # API key
    consumer_secret = 'kzA7YaruvE40iGOUqm39iSOLzn81RZ4BHritYwsQcixbFnGedm'  # API secret key

    # Get request token
    request_token_url = "https://api.twitter.com/oauth/request_token"
    oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
    fetch_response = oauth.fetch_request_token(request_token_url)
    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')
    print("Got OAuth token: %s" % resource_owner_key)

    # # Get authorization
    base_authorization_url = 'https://api.twitter.com/oauth/authorize'
    authorization_url = oauth.authorization_url(base_authorization_url)
    print('Please go here and authorize: %s' % authorization_url)
    verifier = input('Paste the PIN here: ')

    # # Get the access token
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
    oauth_tokens = oauth.fetch_access_token(access_token_url)

    access_token = oauth_tokens['oauth_token']
    access_token_secret = oauth_tokens['oauth_token_secret']

    # Make the request
    oauth = OAuth1Session(consumer_key,
                          client_secret=consumer_secret,
                          resource_owner_key=access_token,
                          resource_owner_secret=access_token_secret)

    if person == "Kanye West":
        response = oauth.get(
            "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=kanyewest&count=3200&exclude_replies=True&include_rts=False&tweet_mode=extended")
    if person == "Elon Musk":
        response = oauth.get(
            "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=elonmusk&count=3200&exclude_replies=True&include_rts=False&tweet_mode=extended")

    return response

"""
pulls the text out of each tweet, and stores them in a list
"""
def tweet_text(response):
    text = []
    json_object = json.loads(response.text)
    num = len(json_object)
    count = 0

    while count < num:
        text.append(json_object[count]["full_text"])
        count += 1
    return text

"""
randomly selects a tweet from Elon Musk
"""
def elon_tweet():
    elon = twitter_API("Elon Musk")
    wisdom_of_elon = tweet_text(elon)
    index = random.randint(0, len(wisdom_of_elon)-1)
    elon_nugget = wisdom_of_elon[index - 1]
    elon_nugget = re.sub('http://\S+|https://\S+', '', elon_nugget)
    if elon_nugget =="":
        rand_tweet("Elon Musk")
    print(elon_nugget)
    return elon_nugget

"""
randomly selects a tweet from Kanye West
"""
def kanye_tweet():
    kanye = twitter_API("Kanye West")
    wisdom_of_kanye = tweet_text(kanye)
    index = random.randint(0, len(wisdom_of_kanye)-1)
    kanye_nugget = wisdom_of_kanye[index-1]
    kanye_nugget = re.sub('http://\S+|https://\S+', '', kanye_nugget)
    if kanye_nugget =="":
        rand_tweet("Kanye West")
    print(kanye_nugget)
    return kanye_nugget

"""
selects either Kanye West or Elon Musk
"""
def rand_tweet(modern_day_prometheus):
    if modern_day_prometheus == "Kanye West":
        kanye_tweet()
    else:
        elon_tweet()


"""
asks the user for their guess, ensuring that the user spelled the names correctly
"""
def ask():
    answer = False
    while answer == False:
        guess = str(input("Who is the architect of this tweet? Kanye West or Elon Musk? "))
        if guess != "Kanye West" and guess != "Elon Musk":
            print("Be sure to type in a full name!")
            ask()
        answer = True

    return guess

"""
checks whether or not the user's guess is correct 
"""
def check(guess, answer):
    if guess == answer:
        return True
    else:
        return False

"""
asks the user to guess whether or not a tweet came from Elon or Kanye, and tracks the statistics of the game
"""
def game():
    boolean_game = 'Y'
    win = 0
    loss = 0

    while boolean_game == 'Y':
        future_president = elon_or_kanye()
        rand_tweet(future_president)
        normie_guess = ask()
        normie_result = check(normie_guess, future_president)

        if normie_result:
            print("Correct!")
            win += 1
        else:
            loss += 1
            print("Incorrect")
        boolean_game = str(input('play again? (Y or N) '))

    total = win + loss
    print("Wins:", win)
    print("Losses:", loss)
    print("Accuracy:", (win/total)*100, "%")
    print("Sample Size: ", total)

if __name__ == '__main__':
    game()