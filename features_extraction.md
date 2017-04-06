# Features Extraction

In order to train a machine learning model, the raw dataset of photographs of people looking at different positions in the screen has to be processed to extract meaningful features

## Table of contents
* [Microsoft Cognitive features](#msc_features)
* [Features01](#features01)


## Microsoft Cognitive features <a name="msc_features"></a>
The program `eye_tracking/features_cognitive.py` takes the images from the raw dataset and generates a directory with the same structure and json files of detected features. A Json file per picture.

* Microsoft Cognitive Face API ([demo](https://www.microsoft.com/cognitive-services/en-us/face-api)).
* Free tier allows 20 calls/minute. 30,000 per month ([pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/face-api/)).
* Landmarks include 5 points for each eye ([details](https://www.microsoft.com/cognitive-services/en-us/face-api/documentation/face-api-how-to-topics/HowtoDetectFacesinImage#step3)).

```
python face-detect-ms-cognitive.py
```

### Validate responses
Remove wrong files
```
grep -l -r -v faceR $OUTPUT_PATH > files_to_remove.txt
cat files_to_remove.txt | xargs rm -f
rm files_to_remote.txt
```
Count number of faces
```
grep -or faceR $OUTPUT_PATH | uniq --count | grep -v "1\s"
```
Check eye landmarks for biggest faces
```
python check-face-features.py
```


## Features01 <a name="features01"></a>

### Description of the dataset
#### features.csv
Columns obtained in this iteration:
* face_x, face_y, face_width, face_height
  * These four columns define the bounding box for theface.
* eye_right_x, eye_right_y, eye_right_width, eye_right_height
  * These four columns define the bounding box for the right eye.
* eye_left_x, eye_left_y, eye_left_width, eye_left_height
  * These four columns define the bounding box for the right eye.
* eye_left_image
  * Relative path for to the left eye image
* eye_right_image
  * Relative path for to the right eye image

Columns from the raw dataset:
* screen_width, screen_height
  * size of the screen
* screen_diagonal
  * Size in inches of the screen diagonal.
* timestamp
  * Time when the picture was taken
* camera_position
  * Position of the webcam relative to the screen.
* game_id
  * Unique identifier for the game.
* score
  * User score in the datum. The close the mouse was to the target (10-5).
* y,x
  * Where the target was shown and the user should be looking in the picture.
* glasses
  * Wether the user wears or not glasses.

#### Images
Inside the folder, there 2 images per datum (raw dataset picture).
* Filename is md5(path to the raw image)\_eye_<left/right>.jpg
* Size is 20x30 pixels.
* This image is linked once from `features.csv`.


### Extraction with Microsoft Cognitive
The program `eye_tracking/features01_cognitive.py` takes the raw dataset images and the features from MS Cognitive and generates a suitable dataset in the specified directory.


### Extraction with OpenCV
