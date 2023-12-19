
# Function to generate a color wheel
def wheel(pos):
    pos = int(pos)
    pos &= 255
    
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)
        
def hsv_to_rgb(h, s, v):

    h = overflow_val(h, 0, 360)
    s = overflow_val(s, 0, 1)
    v = overflow_val(v, 0, 1)
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)

def rgb_to_hsv(r, g, b):
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    delta = cmax - cmin

    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * ((b - r) / delta + 2)
    elif cmax == b:
        h = 60 * ((r - g) / delta + 4)

    s = 0 if cmax == 0 else delta / cmax
    v = cmax

    return h, s, v

def lerp(start, end, t):
    return start * (1 - t) + end * t

def lerp_color(color1, color2, t):
    color = [int(lerp(color1[i], color2[i], t)) for i in range(len(color1))]
    return color

def lerp_color_hsv(rgb_color1, rgb_color2, t):
    # Convert RGB to HSV
    hsv_color1 = list(rgb_to_hsv(*rgb_color1))
    hsv_color2 = list(rgb_to_hsv(*rgb_color2))
    h_dist = abs(hsv_color2[0] - hsv_color1[0])
    if h_dist > 180:
        hsv_color2[0] -= 360

    lerped_vals = [lerp(hsv_color1[n], hsv_color2[n], t) for n in range(len(rgb_color1))]
    # Convert back to RGB
    # print(lerped_vals)
    lerped_rgb = hsv_to_rgb(*lerped_vals)

    return lerped_rgb
def clamp_val(val, min_val, max_val):
    return max(min(val, max_val), min_val)
def overflow_val(val, min_val, max_val):
    range_val = max_val - min_val
    if val < min_val:
        return max_val - (min_val - val) % range_val
    elif val > max_val:
        return min_val + (val - max_val) % range_val
    else:
        return val
def apply_brightness(color, brightness):
        # Assuming color is in RGB format
        adjusted_color = tuple(int(c * brightness) for c in color)
        return adjusted_color
def validate_color(color):
    for c in color:
        if c < 0 or c > 255:
            raise ValueError(f"Invalid color value: {c}")
    return True
def color_distance_rgb(color1, color2):
    deltas = [abs(color1[i] - color2[i])/255 for i in range(len(color1))]
    return (sum(deltas) / len(deltas))