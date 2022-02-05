# Discord-Epilepsy-Detector
# Warning: The below demonstration may be seizure inducing
https://user-images.githubusercontent.com/69024184/152601424-4fd903c7-7dad-429d-bb3a-1f0ac9a7f8b6.mp4

## Setup
1. Open the command prompt and download the required packages with `pip install opencv-python, numpy, discord.py, beautifulsoup4`
2. Add in your discord bot token by replacing [`TOKEN`](https://github.com/gosqib/Discord-Epilepsy-Detector/blob/005aa6560aaead126c785dfb7ccd882532a6d1e8/src/discordbot.py#L78)'s value of `[ADD_YOUR_TOKEN_HERE]` (delete brackets too)

Now you can run `discordbot.py` in `src` and the bot will start working in all servers.

## Features

No commands, just a discord `on_message` event handler. Whenever a message is sent in any server, the program will first check if there're any attachments. If there is, check if the first attachment is a `.mp4` file, if so; perform the flashing-light-checking algorithm on it. If the previous requirements weren't satisfied, check if the message is a discord `/tenor` message and pending a `True`, perform the flashing-light-algorithm on the `/tenor` message.  

## Main Strategy
### Epilepsy checking algorithm
<ins>Preliminary steps</ins>
1. Read all frames

<ins>Main analysis</ins>
1. Skip every second frame (the differences in every frame is negligible and causes inconsistencies)
2. Grayscale every image (so it's easier to check frame's pixel averages to determine big differences)
3. Split each frame into eight equal parts ![image](https://user-images.githubusercontent.com/69024184/152646909-5d912253-120e-44bb-a797-afa75dd6c477.png) (breaking the image into smaller parts allow smaller portions of the image that could be an seizure trigger to be noticed in the difference-checking-process. If the entire image was checked for a pixel change, and only 50% of the image was a potential trigger, it may possibly miss the changes)
4. Loop through the frames
5. Store the pixel averages of the eight portions
6. On the next frame, check if there's a massive difference in any of the last ten results obtained through step `5.`. If there is, increase the trigger counter
7. After the loop, depending on the count of triggers being above seven or not, `True` or `False` will be returned respectively

<ins>If video is a gif</ins>
1. Lower the requirements of number of dangerous frames required to conclude a potential seizure trigger found and the difference required to sound the alarm (gifs are shorter so less quantities of danger are required)
3. Set the data to be analyzed by the algorithm as every frame in the video (when the length of the video is short, every frame counts)
4. Perform the <ins>Main analysis</ins> on this adjusted data set (Skipping its first - `1.` step)

<ins>Ending</ins>
1. If hard flashing lights was detected, add reactions to the discord message as a warning

## Time Complexity
`O((WL)^ASDASD)` where `W` is the width of the image and `L` is height of the image.
<br>
###### Contributing factors
1. (WL) -> storing all frames
2. aidqwueo

## What I learned & Problems
Working with videos, generator details, structure organization
