from ppadb.client import Client
from PIL import Image
import numpy as np
import time


adb = Client('127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
	print('no devices attached')
	quit()
	
device = devices[0]

while True:
    image = device.screencap()

    with open(r'C:\Users\Razor\Documents\screen.png','wb') as f:
        f.write(image)
        
    image = Image.open('screen.png')
    image = np.array(image, dtype=np.uint8)

    pixels = [list(i[:3]) for i in image[1800]]

    transitions = []
    ignore = True
    black = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]
        
        if ignore and (r+b+g) != 0:
            continue
            
        ignore = False
        
        if black and (r+b+g) != 0:
            black = not black
            transitions.append(i)
            continue
            
        if not black and (r+b+g) == 0:
            black = not black
            transitions.append(i)
            continue


    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1
    distance = (gap + target/2) * .975
        
    print(distance)
    print(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')
    
    time.sleep(2.5)
    

