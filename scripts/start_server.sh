#!/bin/bash
source /mnt/RankBotResoources/init_env_variables.sh
nohup python3 -u /mnt/RankBotResoources/DiscordBotApplicationi/main.py > /mnt/RankBotResoources/DiscordBotApplicationi/logs/log.out 2> /mnt/RankBotResoources/DiscordBotApplicationi/logs/log.err &
echo 'server started'