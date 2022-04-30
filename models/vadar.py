from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# function to print sentiments
# of the sentence.
def compound_score(sentence):
	# Create a SentimentIntensityAnalyzer object.
	sid_obj = SentimentIntensityAnalyzer()

	# Analyse sentence
	sentiment_dict = sid_obj.polarity_scores(sentence)

	return sentiment_dict['compound']

# Driver code
if __name__ == "__main__" :

	print("\n1st statement :")
	sentence = 'The head of the United Nations says Ukraine has become "an epicentre of unbearable heartache and pain."'

	# function calling
	print(compound_score(sentence))

	print("\n2nd Statement :")
	sentence = "study is going on as usual"
	print(compound_score(sentence))

	print("\n3rd Statement :")
	sentence = "I am very sad today."
	print(compound_score(sentence))

