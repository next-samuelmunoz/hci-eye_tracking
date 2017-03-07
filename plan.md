# Eye Tracking RoadMap

## Introduction
Supervised problem.

### Detected problems

**Constants:**
* Screen size
* Screen resolution
* Webcam position
* Webcam resolution

**Variables:**
* Image of the user


**Outputs**:
* x position in the screen
* y position in the screen




## 1 Features extraction
1. Detect face. HAAR Cascade.
1. Detect pupils. Extract eyes images.

**Desired features**
* Pupil locations in the image.
* Images from both eyes.
 * ¿Size?


## 2 Data generation
Game


## 3 Model

### Topology

### Training

### Tests


## 4 Further steps

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
