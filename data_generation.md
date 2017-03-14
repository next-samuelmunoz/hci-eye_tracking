# Dataset Generation

In order to generate a dataset of people looking at some specific point in the screen, a game has been developed.

## Table of contents
* [Game stages](#stages)
* [Dataset](#dataset)
* [Installation](#installation)
* [Configuration](#configuration)
* [Troubleshooting](#troubleshooting)


## Game stages <a name="stages"></a>
The `dataset_game.py` file contains this game with the following stages:

### Glasses
The user is asked if they wear glasses.

### Webcam
The user is asked to center themselselves in the webcam.

### Game
The actual game starts. There is a time limit of 1 minute and the user has to hit some bulleye targets. The user can fail to hit a target up to 5 times and they have to face inconvenients such as drag and relocation of the mouse.

Each time the user hits a target, a photo is added to the dataset.


### Results
When the game is ended, some stats are shown, such as:
* Number of hits
* Number of hits per second
* Average precision 5-10
* Total score


## Dataset <a name="dataset"></a>

### Directories
Everytime a game is played, a directory is added to `data/raw`, the name of the directory contains the following information separated by underscores "_ ".
* Game identifier, uuid.
* Screen width, pixels.
* Screen height, pixels.
* Screen diagonal, inches.
* Webcam position.
* Whether the user wears glasses.

### Files
Inside the game associated directory lay corresponding images. The name of the image contains the following information separated by underscores "_ ".
* Timestamp epoch, seconds.
* X position of the target, pixels.
* Y position of the target, pixels.
* Score. Where the user hit the target (5-10)


## Installation <a name="installation"></a>
1. Clone the project.
1. Create a Python virtual environment.
1. `pip install -r requirements/requirements-dataset.txt`


## Configuration <a name="configuration"></a>
Copy the file `config.py` into `config_local.py` and edit what you need.
Some constants you may want to alter are:
* SCREEN_WIDTH and SCREEN_HEIGHT: to set the screen dimensions
* CAM_DEVICE, CAM_WIDTH and CAM_HEIGHT: to configure the webcam.
* TIME_GAME: to set how long a game is.



## Troubleshooting <a name="troubleshooting"></a>
### I can't install v4l2capture
The `v4l2capture` python package requires the v4l libraries.
```bash
apt-get install libv4l-dev
```

### Where is my webcam device?
Execute  one of the webcam modules. They should output the detected webcam devices.

```bash
$ python utils/webcam_v4l2.py
Detected webcams:
 /dev/video0
```
```bash
$ python utils/webcam_v4l2.py
/dev/video0
   driver:       uvcvideo
   card:         HP HD Camera
   bus info:     usb-0000:00:14.0-9
   capabilities: readwrite, streaming, video_capture
```

### I can't use the webcam
If you don't get a device in the previous step, add your user to the `video` group.
```bash
 usermod -a -G video <user>
 ```
