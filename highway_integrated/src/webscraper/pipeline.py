#Written by Max Babka
#This file stitches together the images from the webscraper, the YOLOv8 model, and makes a file for the front end.

import os
import json
import datetime
from ultralytics import YOLO
import shutil

#Helper function to parse a run and find the number of vehicles and people detected
def get_detections(key):    
    file = [f for f in os.listdir('runs/detect/predict/labels') if f.startswith(str(key))]
    if not file:
        return 0, 0        

    #Open it and return the number of vehicles and people detected
    with open(os.path.join('runs/detect/predict/labels', file[0])) as f:
        vehicles = sum(1 for line in f if line.startswith('7') or line.startswith('2'))
        people = sum(1 for line in f if line.startswith('0'))
        return vehicles, people


#Helper function to find the location of the latest image for a given key
def get_img(key, date=None):
    #By default look in the directory based on todays date.
    #Requires that the webscraper was ran today.
    if date is None:
        date = datetime.datetime.now().strftime("%m-%d-%y")
    screenshots_dir = f"Screenshots {date}"
    
    if not os.path.exists(screenshots_dir):
        return False
    
    #Look for possible match based on the ID of the camera
    files = [f for f in os.listdir(screenshots_dir) if f.startswith(key)]
    if not files:
        return False
    
    #Filter down so we get only the most recent timestamp in case multiple exist
    files_with_timestamps = []
    for f in files:
        parts = f.split()
        if len(parts) < 2:
            continue
        if not parts[1].count(":") == 1:
            continue
        timestamp = datetime.datetime.strptime(parts[1], "%H:%M")
        files_with_timestamps.append((f, timestamp))
    
    if not files_with_timestamps:
        return False
    
    latest_file = max(files_with_timestamps, key=lambda x: x[1])[0]
    path = os.path.abspath(screenshots_dir + "/" + latest_file)
    return path


#Similar to above, but used to find the location of the image that has been processed by YOLOv8
def get_box_img(key, date=None):
    #Look for possible match based on the ID of the camera
    file = [f for f in os.listdir('runs/detect/predict') if f.startswith(key)]
    if not file:
        return f"No files found that start with {key} in {'runs/detect/predict/'}"
    return os.path.abspath('runs/detect/predict/' + file[0])
    # return os.path.relpath(os.path.join('runs/detect/predict', file), start=os.getcwd())


#Helper function that will load in the lat long we manually added to the camera_locations.json
def load_camera_locations():
    with open('camera_locations.json') as f:
        camera_locations = json.load(f)
        #Create a dictionary of each key value pair {string id: [lat, long]}
        camera_locations_dict = {}
        for key, value in camera_locations.items():
            camera_locations_dict[key] = value
        return camera_locations_dict

#Main driver file that will create the locations.json file to update the front end.
def generate_locations(model):
    #Open camera_dict.json and read data in the key value pairw {string id: string name}
    #load_camera_locations_dict = load_camera_locations() #Uncomment when support for this is added

    with open('camera_dict.json') as f:
        camera_dict = json.load(f)
        # for key, value in camera_dict.items():
            # print(key, value)

        #Open locations.json, replace the old one if it exists
        with open('locations.json', 'w') as f:
            data = [] #What we will populate the file with

            url = 'https://images2.imgbox.com/45/e0/ENTfENPd_o.png'
            i = 0
                        

            for key, value in camera_dict.items():
                if not get_img(key):
                    continue
                print('Working on Camera ID: ', key)
                # break
                model.predict(source=get_img(key), conf=0.25, save=True, show_labels=False, show_conf=False, save_txt=True)
                id = i
                value = value
                url = url
                camera_id = key
                vehicles, people = get_detections(key)
                lat = 0 #Needs to be changed
                long = 0
                img = get_box_img(key)
                item = {
                    'id': id,
                    'name': value,
                    'camera_id': camera_id,
                    'lat': lat,
                    'long': long,
                    'img': img,
                    'url': url,
                    'vehicles_detected': vehicles,
                    'people_detected': people
                } 
                data.append(item)
                i += 1
                
            #Call json.dump to write to the file
            f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    shutil.rmtree('runs', ignore_errors=True) #Clean up from previous runs
    model = YOLO('yolov8n.pt') #This model can be swapped out if trained on a different dataset
    generate_locations(model)


