import tweepy
from datetime import datetime, timedelta
import re
from nltk.tokenize import WordPunctTokenizer
from textblob import TextBlob

##Define TWITTER OAUth access token
ACC_TOKEN = 'YORK TOKEN'
ACC_SECRET = 'YOUR SECRET KEY'
CONS_KEY = 'KEY HERE'
CONS_SECRET = 'KEY HERE TOO'

##authentication function
def authenticateToTwitter(access_token, access_token_secret, consumer_key, consumer_secret):
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	return api

def main():
	score = 0
	api = authenticateToTwitter(ACC_TOKEN, ACC_SECRET, CONS_KEY, CONS_SECRET)
	past_date = getPastDate(2)
	tweets = get_tweets(api, 'Ashesi', past_date, 50)
	for tweet in tweets:
		data = tweet.text.encode('utf-8')
		sanitized_tweet = sanitize_tweets(data)
		new_score = get_sentiment_score(sanitized_tweet)
		score += new_score
		print('Tweet: {}'.format(sanitized_tweet.encode('utf-8')))
		print('Score: {}\n'.format(new_score))
		
	sentiment_classifier = predict_score(score/50)
	print("sentiment score for this text is {0}".format(sentiment_classifier))

def getPastDate(num_days):
	today_date = datetime.today().now()
	yesterday_date = today_date - timedelta(days=num_days)
	today_date = today_date.strftime('%Y-%m-%d')
	yesterday_date = yesterday_date.strftime('%Y-%m-%d')
	return yesterday_date

def get_tweets(twitter_api, keyword, date_value, size_of_tweet):
	search_result = tweepy.Cursor(twitter_api.search, q=keyword, since=date_value, result_type='recent', lang='en').items(size_of_tweet)
	return search_result

def sanitize_tweets(tweet):
	remove_user = re.sub(r'@[A-Za-z0-9]+', '', tweet.decode('utf-8'))
	remove_links = re.sub(r'https?://[A-Za-z0-9./]+', '', remove_user)
	remove_numbers = re.sub(r'[0-9]+', ' ', remove_links)

	##now convert tweet to lowercase and remove white space
	new_tweet = remove_numbers.lower()
	tokenizer = WordPunctTokenizer()
	words = tokenizer.tokenize(new_tweet)
	sanited_tweet = (' '.join(words)).strip()
	return sanited_tweet


def get_sentiment_score(tweet):
	word = TextBlob(tweet)
	return word.sentiment[0]

def predict_score(score):
	if score <= -0.25:
		return 'NEGATIVE'
	elif score <= 0.25:
		return 'NEUTRAL'
	else:
		return 'POSITIVE'

if __name__ == '__main__':
	main()
