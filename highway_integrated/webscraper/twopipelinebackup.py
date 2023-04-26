import os
import json
import datetime
from ultralytics import YOLO
import shutil



def get_yolov8(model, source):
    # model = YOLO('yolov8n.pt')
    results = model.predict(source=source, conf=0.25, save=True, show_labels=False, show_conf=False)
    return results





#Helper function to find the location of the latest image for a given key
def get_img(key, date=None):
    #By default look in the directory based on todays date.
    #Requires that the webscraper was ran today.
    if date is None:
        date = datetime.datetime.now().strftime("%m-%d-%y")
    screenshots_dir = f"Screenshots {date}"
    
    if not os.path.exists(screenshots_dir):
        return f"Directory not found: {screenshots_dir}"
    
    #Look for possible match based on the ID of the camera
    files = [f for f in os.listdir(screenshots_dir) if f.startswith(key)]
    if not files:
        return f"No files found that start with {key} in {screenshots_dir}"
    
    #Filter down so we get only the most recent timestamp in case multiple exist
    files_with_timestamps = []
    for f in files:
        parts = f.split()
        if len(parts) < 2:
            continue
        if not parts[1].count(":") == 1:
            continue
        try:
            timestamp = datetime.datetime.strptime(parts[1], "%H:%M")
            files_with_timestamps.append((f, timestamp))
        except ValueError:
            pass
    
    if not files_with_timestamps:
        return f"No files found with timestamps in {screenshots_dir}"
    
    latest_file = max(files_with_timestamps, key=lambda x: x[1])[0]
    return os.path.relpath(os.path.join(screenshots_dir, latest_file), start=os.getcwd())



#Helper function that will load in the lat long we manually added to the camera_locations.json
def load_camera_locations():
    with open('camera_locations.json') as f:
        camera_locations = json.load(f)
        #Create a dictionary of each key value pair {string id: [lat, long]}
        camera_locations_dict = {}
        for key, value in camera_locations.items():
            camera_locations_dict[key] = value
        return camera_locations_dict

def generate_locations():
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
                id = i
                value = value
                url = url
                camera_id = key
                lat = 0 #Needs to be changed
                long = 0
                img = get_img(key, date='04-10-23')
                item = {
                    'id': id,
                    'name': value,
                    'camera_id': camera_id,
                    'lat': lat,
                    'long': long,
                    'img': img,
                    'url': url,
                }
                data.append(item)
                i += 1
                
            #Call json.dump to write to the file
            f.write(json.dumps(data, indent=4))

if __name__ == '__main__':
    shutil.rmtree('runs', ignore_errors=True)
    model = YOLO('yolov8n.pt')
    get_yolov8(model, '/Users/maxbabka/Programs/VDOT WebScraping/webscraper/Screenshots 04-24-23/85434 17:32 04-24-23.png')
    get_yolov8(model, '/Users/maxbabka/Programs/VDOT WebScraping/webscraper/Screenshots 04-24-23/85701 17:32 04-24-23.png')
    # generate_locations()

    #Delete the /runs/ folder and subfolders if it exists
    


