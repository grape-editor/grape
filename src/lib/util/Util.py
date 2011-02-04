

    
def rgb_to_hex(rgb):
    import struct    
    r = rgb[0] * 255
    g = rgb[1] * 255
    b = rgb[2] * 255
    
    rgb = (r, g, b)      
    hex = struct.pack('BBB',*rgb).encode('hex')
    print hex
    return hex

def hex_to_rgb(hex):
    import struct
    
    rgb = struct.unpack('BBB', hex.decode('hex'))
    return rgb
    