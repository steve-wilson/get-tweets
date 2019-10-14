import argparse
import json
import os
import sys
import time

import tweepy

# take a list of tweet ids, 1 per line, and get full json for each
# save to a new file, created at outfile_path
# keep keys in file that only you have read access to

def get_all_tweets_by_id(tweet_id_path, outfile_path, auth_path, sep='\t', tweet_col=0, verbose=False):

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

    # iterate through list of tweet ids, write to outfile
    with open(outfile_path,'w') as outfile, open(tweet_id_path) as tweet_id_file:
        for line in tweet_id_file:
            tweet_id = line.strip().split(sep)[tweet_col]

            try:
                tweet = api.get_status(tweet_id, tweet_mode="extended")
                if verbose:
                    print(tweet.full_text)
                json.dump(tweet._json, outfile)
                outfile.write('\n')

            except tweepy.RateLimitError:
                sys.stderr.write("rate limit hit, sleeping 15 min...\n")
                sys.stdout.flush()
                time.sleep(900)
                try:
                    tweet = api.get_status(tweet_id, tweet_mode="extended")
                    if verbose:
                        print(tweet.full_text)
                    json.dump(tweet._json, outfile)
                    outfile.write('\n')
                except tweepy.TweepError as err:
                    sys.stderr.write("Error getting tweet: {0}\n".format(err))
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except:
                    sys.stderr.write("Unexpected error: " + str(sys.exc_info()[0]) + '\n')

            except tweepy.TweepError as err:
                sys.stderr.write("Error getting tweet: {0}\n".format(err))
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                sys.stderr.write("Unexpected error: "  + str(sys.exc_info()[0]) + '\n')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("tweet_id_file",     help="Path to file containing Tweet Ids, one per line.")
    parser.add_argument("output_json_file",  help="Where to create output file.")
    parser.add_argument("keys_file",         help="Path to keys file. (see README or example_keys.txt)")
    parser.add_argument("--sep",'-s',        help="Column separator in tweet_id_file. (default:tab)", default="\t")
    parser.add_argument("--col",'-c',        help="0-based index of column of tweet_id_file where Tweet Id can be found. (default:0)", default=0, type=int)
    parser.add_argument("--verbose",'-v', action="store_true", help="turn verbose mode on (prints tweet text to stdout while tweets are being collected")

    args = parser.parse_args()
    get_all_tweets_by_id(args.tweet_id_file, args.output_json_file, args.keys_file, args.sep, args.col, args.verbose)
