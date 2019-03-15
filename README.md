# Object finding in Python with p5.js

A simple object finder implemented as an insecure API for interfacing with p5.js. 
Spot objects in the real world and use the location data to make stuff happen on a p5 canvas!

You'll find both the python API bit and an example p5 sketch that uses it this repo.

The server.py script could be useful for other projects as it serves CGI scripts as well as being CORS-enabled.

## Installation

+ Clone the repo
+ Activate the virtual environment:

    source bin/activate

## Setup with live camera feed

+ Check you have a webcam attached to your computer. For best results,
  - Use a USB webcam attached to a tripod
  - Point it toward a plain, non-reflective background
  - Position some dark objects on the 'canvas' (e.g. toy bricks, beans, etc.)
  - Do this in a well lit room, avoiding direct light so shadows aren't projected
+ Inside the `cgi-bin` folder, open the python interactive shell and import the object finder functions:

    python
    from object_finder import *    
+ Run the following command to check the camera is lined up with the canvas (`q` closes the window): 
    
    test_camera(src=1)
+ Now run the following commands to test the object finder. You may need to adjust the`T_bw` and `T_p` parameters until the red blobs look like they're in the right place. `T_bw` is a value in the range 0-255, while `T_p` is the pixel proximity threshold between two objects. The value you need will depend on your camera resolution and the closeness of the objects.

    img, arr = trigger_capture(src=1, T_bw=60, T_p=30)
    visualise_objects(img, arr)

## Using it like an API

To make the `object_finder` script behave like an API, first adjust the parameters in `call_object_finder.py` to reflect your setup (obviously this is only meant to be served locally!)

Then, from the project root, start the simple CGI/CORS-enabled server:

    python server.py
Test it by making a GET request to `http://localhost:8000/cgi-bin/call_object_finder.py` from a browser.

## Calling the API from p5

Once you have the API bit running, you can write p5 sketches which fetch the object location data with `loadJSON`.

To see an example, open `p5-examples/daisies/index.html` in a browser. Assuming you got everything set up right, you should be able to plant some digital daisies.

Remember you can develop your p5 sketches anywhere in your local file system. They don't have to be located in the object-finder directory.

## Stuck?

Any problems running this code, please feel free to post a comment (but be constructive - this is meant to be fun!)
