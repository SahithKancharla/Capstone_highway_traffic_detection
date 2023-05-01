# Capstone_highway_traffic_detection
![image](/frontend/highway_integrated_frontend/src/images/99018_1559_03-26-23.png)

### How to Run ###
1. Run the vdot webscraper in 'Capstone_highway_traffic_detection/highway_integrated/src/webscraper/pipeline.py'
```
python Capstone_highway_traffic_detection/highway_integrated/src/webscraper/vdot511webscraper.py
```
Please ntoe that there is a manual fix required for the webscraper, please see below
2. Run the pipeline script
```
python Capstone_highway_traffic_detection/highway_integrated/src/webscraper/pipeline.py
```
3. Run the front end
```
Sahith add here
```

### How to fix VDOT Webscraper ###
The script will login, then prompt the user for input. Do not press enter in the python kernel (typing text will have no effect) until you have completed the following steps:

1. Wait for the visual map of Virginia to appear
2. Click on any camera, then favorite and unfavorite the camera by clicking the gray star so it becomes yellow then gray again.
3. Press enter on the python kernel

The webscraper will now run, and place the files in a subfolder for the pipeline and front end to handle.
