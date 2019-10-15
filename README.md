# get-tweets

Simple Python (v3.7+) script to get tweet JSON objects from a file containing a list of tweet IDs, one per line.

**Input**: a single column plain text file, or a csv/tsv file where one of the columns contains the tweet IDs.

**Output**: A file containing the full JSON object for each tweet, one JSON object per line.

**Purpose**: For cases where you want to receive a Twitter dataset from someone, but they are only allowed to share the IDs with you due to the Twitter API terms of service.

## Setup

### Install tweepy
Run `pip install tweepy`

### Get your API keys
Learn about the Twitter API, including how to apply for your own keys, [here](https://developer.twitter.com/).

Put them in a file of your choosing, but the format should match the `example_keys.txt` file included in this repo.

_Note: Don't push the file containing your keys to a public repository! These should be kept private._

## Usage

```
usage: get_tweets_by_id.py [-h] [--sep SEP] [--col COL] [--quiet]
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
  --quiet, -q        Don't print progress messages while collecting tweets.
```

### Example

Your tweet IDs are in a file called `tweet_ids.txt`, with one ID per line. You have added your keys to a file called my_keys.txt in the same format as the `example_keys.txt` file. Then you can run:

`python get_tweets_by_id.py tweet_ids.txt my_tweets.json my_keys.txt`

and a file called `tweet_ids.txt` will be created containing the json objects for each available tweet in your `tweet_ids.txt` file.

## FAQ

_I have `N` tweet IDs, why am I only getting `<N` tweets?_

You will only be able to retrieve tweets that are still publicly available on Twitter. This means no deleted tweets, tweets by users that have been banned, or tweets from users who have switched their accounts to private. These things are all fairly common, so it is likely that you won't be able to get every tweet, and it becomes more likely over time.
