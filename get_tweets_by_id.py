import argparse
import json
import os
import sys
import time

import tweepy

# take a list of tweet ids, 1 per line, and get full json for each
# save to a new file, created at outfile_path
# keep keys in file that only you have read access to

# get a set of (at most 100) tweets
def get_batch_of_tweets(api, id_list, outfile, i, total, quiet):

    retry = True
    while retry:
        # try to get current set of tweets
        try:
            # make sure to ask for the full 280 characters
            tweets = api.statuses_lookup(id_list, tweet_mode="extended")
            total += len(tweets)
            if not quiet:
                print("Requested",i+1,"tweets so far, got",total)
            # write each json object to the output file
            for tweet in tweets:
                json.dump(tweet._json, outfile)
                outfile.write('\n')
        # wait 15 min if rate limit is hit
        except tweepy.RateLimitError:
            sys.stderr.write("rate limit hit, sleeping 15 min...\n")
            sys.stdout.flush()
            time.sleep(900)
        # if there were no exceptions during the try block
        # stop trying to get these 100 tweets and clear the list
        else:
            retry = False

    return total

def get_all_tweets_by_id(tweet_id_path, outfile_path, auth_path, sep='\t', tweet_col=0, quiet=False):

    # read keys file
    keys = {}
    with open(auth_path) as auth_file:
        for line in auth_file:
            k,v = line.strip().split(':')
            keys[k] = v

    # create Twitter API connection
    auth = tweepy.OAuthHandler(keys["CONSUMER"], keys["CONSUMER_SECRET"])
    auth.set_access_token(keys["OAUTH_TOKEN"], keys["OAUTH_TOKEN_SECRET"])
    api = tweepy.API(auth)

    with open(outfile_path,'w') as outfile, open(tweet_id_path) as tweet_id_file:

        # keep track of sets of 100 ids to get
        id_list = []
        total = 0
        i = 0

        # iterate through list of tweet ids, write to outfile
        for i, line in enumerate(tweet_id_file):

            tweet_id = line.strip().split(sep)[tweet_col]
            id_list.append(tweet_id)

            # wait until we get 100
            if len(id_list) == 100:
                total = get_batch_of_tweets(api, id_list, outfile, i, total, quiet)
                id_list = []

        # make sure to also get the last set of < 100 tweets, if needed
        if id_list:
            total = get_batch_of_tweets(api, id_list, outfile, i, total, quiet)
        print("Final: Requested",i+1,"tweets, got",total)
        print("Done.")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("tweet_id_file",     help="Path to file containing Tweet Ids, one per line.")
    parser.add_argument("output_json_file",  help="Where to create output file.")
    parser.add_argument("keys_file",         help="Path to keys file. (see README or example_keys.txt)")
    parser.add_argument("--sep",'-s',        help="Column separator in tweet_id_file. (default:tab)", default="\t")
    parser.add_argument("--col",'-c',        help="0-based index of column of tweet_id_file where Tweet Id can be found. (default:0)", default=0, type=int)
    parser.add_argument('--quiet','-q', action="store_true", help="Don't print progress messages while collecting tweets.")

    args = parser.parse_args()
    get_all_tweets_by_id(args.tweet_id_file, args.output_json_file, args.keys_file, args.sep, args.col, args.quiet)
