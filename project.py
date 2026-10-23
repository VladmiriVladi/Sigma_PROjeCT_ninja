'''
Toulouse Business School MSc AIBA
Course: Python for Data Science -- PROJECT
Author: CRISAN Mihnea - TBS Master 2
'''

import matplotlib.pyplot as plt
import pandas as pd


def main():
    print("Starting the project...")

    tweets = pd.read_csv("tweets.csv")
    tweets = tweets[["created_at", "lang", "text"]]
    print("\nFirst 5 tweets:")
    print(tweets.head())

    n_tweets = len(tweets)
    max_length = 140
    candidates = ["trump", "clinton", "sanders", "cruz"]
    print("\nNumber of tweets in the dataset:", n_tweets)
    print("Candidates we are looking for:", candidates)

    # for each tweet: length, retweet or not, and which candidates are mentioned
    for index, row in tweets.iterrows():
        text = row["text"].lower()
        tweets.loc[index, "length"] = len(row["text"])
        tweets.loc[index, "is_retweet"] = row["text"].startswith("RT @")
        for candidate in candidates:
            tweets.loc[index, candidate] = candidate in text

    print("\nDataFrame with the new columns:")
    print(tweets[["length", "is_retweet"] + candidates].head(10))

    long_tweets = tweets[tweets["length"] >= max_length - 5]
    print("\nTweets with at least", max_length - 5, "characters:",
          len(long_tweets))
    print(long_tweets[["text", "length"]])

    # original tweets (not retweets) that mention Trump
    original_trump = tweets[(~tweets["is_retweet"].astype(bool))
                            & (tweets["trump"].astype(bool))]
    print("\nOriginal tweets (not retweets) mentioning Trump:",
          len(original_trump))
    print(original_trump[["text"]])

    mentions = {c: int(tweets[c].astype(bool).sum()) for c in candidates}
    print("\nMentions per candidate:", mentions)
    retweet_share = tweets["is_retweet"].astype(bool).mean() * 100
    print("Share of retweets: {:.0f}%".format(retweet_share))
    print("Average tweet length: {:.0f} characters".format(
        tweets["length"].mean()))

    # histogram of tweet lengths, red line = 140 character limit
    plt.hist(tweets["length"], bins=10, edgecolor="black")
    plt.axvline(max_length, color="red", linestyle="--",
                label="140-character limit")
    plt.xlabel("Tweet length (number of characters)")
    plt.ylabel("Number of tweets")
    plt.title("Distribution of tweet lengths (US primaries, March 2016)")
    plt.legend()
    plt.show()

    print("... project ended.")


if __name__ == '__main__':
    main()


"""
INTERPRETATION
---
- Trump dominates the conversation: he appears in about 70 of the 91
  tweets (~77%), far ahead of Cruz (14), Clinton (9) and Sanders (6).
  In March 2016, even with several candidates still in the race, the
  online attention was concentrated on a single person.
- About 63% of the tweets are retweets. People mostly relay content
  (from media accounts or other users) rather than write their own,
  so a few original accounts drive most of what circulates.
- The histogram shows that many tweets sit close to the 140-character
  limit: users (and media headlines that get retweeted) tend to use all
  the space available. Retweets are often cut at 140 characters
  because the "RT @username:" prefix takes up space.
- Limits: 91 tweets collected in a few seconds is a very small sample,
  and a simple keyword search counts any mention of "trump" whether it
  is positive or negative. Conclusions should be confirmed on a much
  larger dataset collected over several days.

REAL-WORLD USE CASE
---
This is the basis of social media monitoring ("social listening"),
which is used by campaign teams, brands and journalists:
- A political campaign tracks how often its candidate is mentioned
  compared to rivals, day by day, to measure the effect of a debate,
  a speech or a scandal.
- A company does exactly the same with its brand name and its
  competitors' names (e.g. "nike" vs "adidas") to measure its
  "share of voice" online, and detect a bad-buzz early when mentions
  suddenly spike.
- Separating retweets from original tweets helps identify the
  influencers whose content gets relayed the most, which is useful
  for targeting partnerships or spotting disinformation campaigns.
The next step would be to add sentiment analysis (is the tweet
positive or negative?) and to plot the number of mentions over time.
"""
