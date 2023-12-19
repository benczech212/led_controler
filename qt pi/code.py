import neopixel
import board
from color_tools import *
import math
DEBUG = False  # Set to True to enable debug output
# Example usage:
num_pixels = 50  # Replace with the actual number of pixels in your setup
pin = board.A2



class SmoothPixels:
    def __init__(self, pin,num_pixels,speed=0.1,brightness=1.0,auto_write=False):
        self.pin = pin
        self.num_pixels = num_pixels
        self.brightness = brightness
        self.auto_write = auto_write
        self.neopixels = neopixel.NeoPixel(pin, num_pixels, brightness=brightness, auto_write=auto_write)
        self.speed = speed
    def set_colors(self,colors,show=True):
        if isinstance(colors, list):
            for pixel_id in range(len(colors)):
                current_color = self.neopixels[pixel_id]
                target_color = colors[pixel_id]
                distance = color_distance_rgb(current_color, target_color)
                if distance == 0:
                    continue
                if distance < 0.2:
                    self.neopixels[pixel_id] = target_color
                else:
                    blended_color = lerp_color_hsv(current_color, target_color, self.speed)
                    self.neopixels[pixel_id] = blended_color
            
        elif isinstance(colors, tuple):
            for pixel_id in range(len(self.neopixels)):
                current_color = self.neopixels[pixel_id]
                target_color = colors
                distance = color_distance_rgb(current_color, target_color)
                if distance == 0:
                    continue
                if distance < 0.2:
                    self.neopixels[pixel_id] = target_color
                else:
                    blended_color = lerp_color_hsv(current_color, target_color, self.speed)
                    self.neopixels[pixel_id] = blended_color
        elif isinstance(colors, dict):
            pixel_ids = colors.keys()
            for pixel_id in pixel_ids:
                current_color = self.neopixels[pixel_id]
                target_color = colors[pixel_id]
                distance = color_distance_rgb(current_color, target_color)
                if distance == 0:
                    if DEBUG: print(f"pixel {pixel_id} distance is 0, skipping")
                    continue
                if distance < 0.2:
                    if DEBUG: print(f"setting pixel {pixel_id} to {target_color}")
                    self.neopixels[pixel_id] = target_color
                else:
                    blended_color = lerp_color_hsv(current_color, target_color, self.speed)
                    if DEBUG: print(f"setting pixel {pixel_id} to {blended_color}")
                    self.neopixels[pixel_id] = blended_color
        if show:
            self.show()
    def show(self):
        self.neopixels.show()
speed = 0.1
tick_count = 0
ticks_per_cycle = 4
spread = 255
pixel_step = 3
spixels = SmoothPixels(pin,num_pixels,speed=speed)
color_speed = 1.0

while True:
    hues = [i/num_pixels*spread for i in range(num_pixels)]
    colors = [wheel(hue + tick_count) for hue in hues]
    color_dict = {}
    
    for i in range(spixels.num_pixels):
        pixel_id = (i*pixel_step) % spixels.num_pixels
        color_id = int(tick_count * color_speed + i * 1) % len(colors)
        brightnes = clamp_val(math.sin(tick_count * 0.1 + i * 0.1)*2,0.0,1.0)
        color_dict[pixel_id] = apply_brightness(colors[color_id],brightness=brightnes)
    
    for i in range(ticks_per_cycle):
        tick_count += 1
        spixels.set_colors(color_dict)
        
        



                
