# Discord-Epilepsy-Detector
# Warning: The below demonstration may be seizure inducing
https://user-images.githubusercontent.com/69024184/152601424-4fd903c7-7dad-429d-bb3a-1f0ac9a7f8b6.mp4

## Setup
1. Open the command prompt and download the required packages with `pip install opencv-python, numpy, discord.py, beautifulsoup4`
2. Add in your discord bot token by replacing [`TOKEN`](https://github.com/gosqib/Discord-Epilepsy-Detector/blob/005aa6560aaead126c785dfb7ccd882532a6d1e8/src/discordbot.py#L78)'s value of `[ADD_YOUR_TOKEN_HERE]` (delete brackets too)

Now you can run `discordbot.py` in `src` and the bot will start working in all servers.

## Features

No commands, just a discord `on_message` event handler. Whenever a message is sent in any server, the program will first check if there're any attachments. If there is, check if the first attachment is a `.mp4` file, if so; perform the epilepsy checking algorithm on it. If the previous requirements weren't satisfied, check if the message is a discord `/tenor` message and pending a `True`, perform the epilepsy algorithm on the `/tenor` message.  

## Main Strategy
### Epilepsy checking algorithm
<ins>Preliminary steps</ins>
1. Read all frames

<ins>Main analysis</ins>
1. Skip every second frame &nbsp(the differences in every frame is negligible and causes inconsistencies)
2. Grayscale every image &nbsp(so it's easier to check frame's pixel averages to determine big differences)
3. 

<ins>If video is a gif</ins>
1. Lower the requirements of number of dangerous frames required to conclude an epilepsy trigger found and the difference required to sound the alarm (gifs are shorter so less quantities of danger are required)
3. Set the data to be analyzed by the algorithm as every frame in the video (when the length of the video is short, every frame counts)
4. askldjasdklj

## Time Complexity


## What I learned & Problems
Working with videos, generator details, structure organization
