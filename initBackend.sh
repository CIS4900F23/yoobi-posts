#!/usr/bin/env bash

# This script starts our flask app and populates our db. The script also forks a child process that will continue to pull new tweets and reddit posts every 2 hours and update our database sentiment plot by saving it to a JSON file so that it can be accessed from elsewhere.

#populate db at startup
startup()
{
    # python3 dbUpdateSentimentPlot.py
    python3 dbPopulateTwitter.py
    python3 dbPopulateReddit.py
    python3 dbUpdateSentimentPlot.py
}

#fork new child processes for startup and update_db functions
# startup &
# update_db &
startup &

#start flask app in parent process
python3 app.py
