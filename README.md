# get-tweets
Simple Python script to get tweet JSON objects from a file containing a list of tweet IDs, one per line.

The input file can be just a single column, or can be a csv/tsv file where one of the columns contains the tweet IDs.

This is mostly useful for cases where you want to receive a Twitter dataset from someone, but they are only allowed to share the IDs with you due to the Twitter API terms of service.

The output file will contain the full JSON object for each tweet, one JSON object per line.

## Setup

`pip install tweepy`

## Usage

```
usage: get_tweets_by_id.py [-h] [--sep SEP] [--col COL] [--verbose]
                           tweet_id_file output_json_file keys_file

positional arguments:
  tweet_id_file      Path to file containing Tweet Ids, one per line.
  output_json_file   Where to create output file.
  keys_file          Path to keys file. (see README or example_keys.txt)

optional arguments:
  -h, --help         show this help message and exit
  --sep SEP, -s SEP  Column separator in tweet_id_file. (default:tab)
  --col COL, -c COL  0-based index of column of tweet_id_file where Tweet Id
                     can be found. (default:0)
  --verbose, -v      turn verbose mode on (prints tweet text to stdout while
                     tweets are being collected
```
