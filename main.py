import openai
import tweepy
import os
import datetime

# Set up OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]
# Set up Twitter API keys and access tokens
consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
access_token = os.environ["TWITTER_ACCESS_TOKEN"]
access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
# Authenticate with Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def generate_riddle():
    prompt = f"Give me a riddle in one short sentence about a movie scene from a popular movie. Don't mention any actor names. Try to make the riddle accurate and true to the movie. Also try to make the riddle clever."
    completion = openai.ChatCompletion.create(
    model="gpt-4-0314",
    messages=[
        {"role": "user", "content": f"{prompt}"}
    ]
    )
    return(completion.choices[0].message.content)

def validate_riddle(riddle):
    prompt = f"""
    What movie is this riddle about?

    [Riddle: {riddle}]

    Are you sure? Did all those things actually happen in the movie? Answer simply with "Yes" if you are 100% confident in your answer. Answer "No" if you are not. Please only answer with a "Yes" or a "No".
    """
    completion = openai.ChatCompletion.create(
    model="gpt-4-0314",
    messages=[
        {"role": "user", "content": f"{prompt}"}
    ]
    )
    print(completion.choices[0].message.content)
    return(completion.choices[0].message.content)

def build_tweet(riddle):
    tweet = f"""🎥 The Scene: {riddle}

🎬 ReelRiddle time! Can you guess the movie from this iconic scene? 🕵️‍♂️ Drop your answer in the comments! 🍿 #Riddle
    """
    return tweet

def post_tweet(tweet):
    try:
        client.create_tweet(text=tweet)
        #print(f"Tweet posted: {tweet}")
    except tweepy.TweepError as e:
        print(f"Error posting tweet: {e}")
if __name__ == "__main__":
    riddle = generate_riddle()
    if validate_riddle(riddle) == "Yes":
        tweet = build_tweet(riddle)
        post_tweet(tweet)