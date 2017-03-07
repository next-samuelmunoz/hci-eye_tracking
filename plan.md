# Eye Tracking RoadMap

## Table of Contents
* [Introduction](#intro)
* [Data generation](#data)
* [Features extraction](#features)
* [Model](#model)
* [Further steps](#further)


## Introduction <a name="intro"></a>
Supervised problem.

### Detected problems

**Constants:**
* Screen size/resolution
* Webcam position
* Webcam picture size/resolution

**Variables:**
* Image of the user


**Outputs**:
* x position in the screen
* y position in the screen



## Data generation <a name="data"></a>
### Game




## Features extraction <a name="features"></a>

### Simplest approach
Steps:
  1. HAAR Cascade to detect face.
  1. Bounding boxes over the eyes.

Features:
  * Left and right eye images.
  * Position in the webcam image of the pupils.

### Facial points
TODO  

**Desired features**
* Pupil locations in the image.
* Images from both eyes.
 * ¿Size?





## Model <a name="model"></a>
TO SEE:
* Regression model (mo max-pooling)
* LeNet
* Siamese Nets
* Concat features

### Topology

### Training

### Tests


## Further steps <a name="further"></a>

### Generalization to other platforms
Fine tunning for fast calibration on platforms where training constants change.

### Interfaces (gaze tracking)
* Client attention:
 * Web pages.
 * Store window.
* Desktop navigation.
 * Libraries:
* Image scrolling
 * Camera + 2 servos.
 * Wow demo.


#### Dataset applications
* Generative models
 * Apple eye paper.
 * Generate eyes on smart mirror following the user.
