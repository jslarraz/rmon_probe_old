#!/bin/bash

# Stop anything related to the agent
pkill -f python

# Reset the database to default
mysql rmon --execute "DELETE from td_filterEntry; DELETE from td_channelEntry;"

# Start the agent
python /etc/rmon/start.py &> /dev/null &