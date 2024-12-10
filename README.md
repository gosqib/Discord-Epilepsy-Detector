# Discord-Epilepsy-Detector
# Warning: The below demonstration
# Also, the gif checker does NOT work with message that don't start with `https://tenor.com/`
Ex. `qwehttps://tenor.com/ZJXy.gif`
<br>

https://user-images.githubusercontent.com/69024184/152660005-15f88d20-89f4-43ff-b000-a869df4cdc79.mp4


## Setup
1. Open the command prompt and download the required packages with `pip install opencv-python, numpy, discord.py, beautifulsoup4`
2. Add in your discord bot token by replacing [`TOKEN`](https://github.com/gosqib/Discord-Epilepsy-Detector/blob/master/src/discordbot.py#L86)'s value of `[ADD_YOUR_TOKEN_HERE]` (delete brackets too)

Now you can run `discordbot.py` in `src` and the bot will start working in all servers.

## Features

No commands, just a discord `on_message` event handler. Whenever a message is sent in any server, the program will first check if there're any attachments. If there is, check if the first attachment is a `.mp4` file, if so; perform the flashing-light-checking algorithm on it. If the previous requirements weren't satisfied, check if the message is a discord `/tenor` message and pending a `True`, perform the flashing-light-algorithm on the `/tenor` message.  

## Epilepsy checking
<ins>Preliminary steps</ins>
1. Read all frames

#### Main analysis
1. Skip every second frame (the differences in every frame is negligible and causes inconsistencies)
2. Grayscale every image (so it's easier to check frame's pixel averages to determine big differences)
3. Split each frame into eight equal parts ![image](https://user-images.githubusercontent.com/69024184/152646909-5d912253-120e-44bb-a797-afa75dd6c477.png) (breaking the image into smaller parts allow smaller portions of the image that could be an seizure trigger to be noticed in the difference-checking-process. If the entire image was checked for a pixel change, and only 50% of the image was a potential trigger, it may possibly miss the changes)
4. Loop through the frames
5. Store the pixel averages of the eight portions
6. On the next frame, check if there's a massive difference in any of the last ten results obtained through step `5.`. If there is, increase the trigger counter
7. After the loop, depending on the count of triggers being above seven or not, `True` or `False` will be returned respectively

#### If video is a gif
1. Lower the requirements of number of dangerous frames required to conclude a potential seizure trigger found and the difference required to sound the alarm (gifs are shorter so less quantities of danger are required)
3. Set the data to be analyzed by the algorithm as every frame in the video (when the length of the video is short, every frame counts)
4. Perform the <ins>Main analysis</ins> on this adjusted data set (Skipping its first - `1.` step)

#### Ending
1. If hard flashing lights was detected, add reactions to the discord message as a warning

## Time Complexity (Assuming .mp4 file received)
`O(N^2)` where `N` is the number of total pixels in all frames of the video (can also be viewed as the duration of the video)
<br>
#### Contributing factor
##### Small details will be neglected
-> `(Looping through every frame) * [(loop through frame to find mean pixel val) + (check if last ten frame's pixel value) + (add current frame data to storage) + (remove first data item in storage of portion if capacity reaches ten)]`
<br>
-> `F * [F_p + 10 + 1 + 10]` where `F` is the number of frames of the video and `F_p` is the number of pixels in a frame. The value of `F_p` is `1/N`
<br>
-> `F * (1/N + 21)`
<br>
<br>
The value of `F` is `N/F_p` and `F_p` is `1/N`; `F = N/(1/N)` = [`N^2`]
<br>
-> `N^2/N + 21N^2`
<br>
<br>

