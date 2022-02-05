# Discord-Epilepsy-Detector
# Warning: The below demonstration may be seizure inducing
https://user-images.githubusercontent.com/69024184/152601424-4fd903c7-7dad-429d-bb3a-1f0ac9a7f8b6.mp4

## Setup
1. Open the command prompt and download the required packages with `pip install opencv-python, numpy, discord.py, beautifulsoup4`
2. Add in your discord bot token by replacing [`TOKEN`](https://github.com/gosqib/Discord-Epilepsy-Detector/blob/005aa6560aaead126c785dfb7ccd882532a6d1e8/src/discordbot.py#L78)'s value of `[ADD_YOUR_TOKEN_HERE]` (delete brackets too)
<br>
Now you can run `discordbot.py` in `src` and the bot will start working in all servers.

## Features

No commands, just a discord `on_message` event handler. Whenever a message is sent in any server, the program will first check if there're any attachments. If there is, check if the first attachment is a `.mp4` file, if so; it would perform the epilepsy checking algorithm on it. If the previous requirements weren't satisfied, check if the message is a discord `/tenor` message and if so, perform the epilepsy algorithm on the `/tenor` message.  

## Implementation
...

## Time Complexity


## What I learned & Problems
Working with videos, generator details, structure organization
