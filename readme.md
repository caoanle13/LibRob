# How to setup LibRob

### Table of contents
* Connecting and setting up the Raspberry Pi
* Launching LibRob
* (Optional) Troubleshooting router connection

---

## Connecting and setting up the Raspberry Pi

The first step is to connect to the Raspberry Pi from your Laptop and check whether everything is connected properly to the Pi.
Follow the following instructions:

1. Check that the Pi and router are powered by the batteries, that the Lidar, robot, microphone and controller are connected by USB to the Pi and that the router is connected to the Pi by ethernet.
2. Connect to the **LibRob** Wi-Fi on your Laptop (**if you can't find it go to the Troubleshooting part**)
3. Open a terminal window
4. Type `ssh ubuntu@ros-pi.lan` to connect to the Pi
5. **Password: ubuntu**

---

## Launching the robot

The next will be to run the relevant launch files in order to start the Operation of LibRob.
Follow these instructions:

1. Turn on the robot
2. Go to terminal
3. Type `cd catkin_ws/src/` to go the GitLab repo
4. You can type `git pull` if you're not sure whether you have the latest version
5. Type `tmux` to open a virtual terminal (so you don't close all the processes if there is a connection failure, if it does fail use `tmux a` to "reattach" your virtual terminal)
6. run `roslaunch librob start_Pi.launch` on the Pi
7. run `roslaunch librob start_laptop.launch` on the Lenovo laptop
8. Adjust the initial position of the robot on **rviz**

_Note_: If the launch files mention an error with the USB ports you'll have to swap the USB ports on the `rplidar.launch` and `teleop.launch` files.
The rplidar will either use USB0 or USB2 and the teleop will be USB0 or USB1

---

## Troubleshooting the router connection

The router might run into issues when it tries to set up our LAN in the library. If that's the case, you won't have internet access through LibRob or you won't see the librob Wi-Fi option.
If this happens, try this:

1. If you don't see the LibRob WiFi connect to the router using an ethernet cable (not necessary if you can connect but can't access Pi or internet)
2. Go to your favourite browser and type `192.168.2.1` in the search bar
3. Connect using **username: root, Password: root** credentials
4. Go to `Network/wireless/overview`
5. Click the scan button on the first item of the list
6. Find the channel number of the strongest `Imperial-WPA` signal
7. Go back to overview and edit the **librob client** to the right channel number 
