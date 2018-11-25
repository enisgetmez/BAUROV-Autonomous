# BAUROV-Autonomous
BAUROV autonomous with opencv and pymavlink

# Raspberry Pi Instructions
Always good practice to update everything before you install stuff:

```sudo apt-get update```

```sudo apt-get upgrade```

Install opencv and dependencies

```sudo apt install python-numpy python-opencv libopencv-dev```

```apt install python python-pip python-future```

Install gstreamer and plugins

```sudo apt install python-gst-1.0 gstreamer1.0-plugins-good \ gstreamer1.0-plugins-bad gstreamer1.0-libav \ gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0```

Install mavproxy module and everything else needed

```pip install mavproxy```

# How to using converter.py for ColorTracking


command : 

`python converter.py R G B `

Example :

`python converter.py 131 6 24 `
