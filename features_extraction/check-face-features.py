#!/usr/bin/env python

########### Python 2.7 #############
import json
import ConfigParser
import os


config = ConfigParser.RawConfigParser()
config.read('config.cfg')

INPUT_PATH = config.get('general', 'OUTPUT_PATH')
OUTPUT_PATH = INPUT_PATH.replace("HCI-ET-cognitive_dataset", "HCI-ET-cognitive_dataset_fixed")


def get_area(face):
    width = face['width']
    height = face['height']
    return width*height

def check_biggest_face(filename):
    with open(filename) as data:
        myarray = json.load(data)
    mylist = map(lambda x: get_area(x['faceRectangle']), myarray)
    maxindex = mylist.index(max(mylist))
    if (maxindex is not 0):
        print "%i: %s" %(maxindex, mylist)

    # Check eye landmarks for the biggest face
    landmarks = myarray[maxindex]["faceLandmarks"]
    targetLandmarks = ["pupilLeft","eyeLeftInner", "eyeLeftBottom", "eyeLeftOuter", "eyeLeftTop"]
    targetLandmarks.extend([k.replace("Left", "Right") for k in targetLandmarks])
    if not all (k in landmarks for k in targetLandmarks):
        raise(Exception("Missing landmark in %s" %filename))

    return myarray[maxindex]


# Loop for checking faces for all files
def check_faces(input_dir, output_dir, max_images=5000):
    count = 0
    for my_sub_dir in os.listdir(input_dir):

        my_input_dir = input_dir + my_sub_dir
        print my_input_dir
        dest_dir = output_dir + my_sub_dir
        for filename in os.listdir(my_input_dir):
            count=count+1
            if count % 100 == 0:
                print "%i images processed" %count

            # Check if the file has been already processed
            if os.path.exists(os.path.join(dest_dir,filename.replace("json", "fix.json"))):
                continue
            myjson = check_biggest_face(os.path.join(my_input_dir, filename))

            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

            if (myjson):
                with open(os.path.join(dest_dir, filename.replace("json", "fix.json")), "w+") as f_out:
                    json.dump(myjson, f_out)

            if count >= max_images:
                return


check_faces(INPUT_PATH, OUTPUT_PATH)




####################################
