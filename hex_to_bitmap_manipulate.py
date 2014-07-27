# http://www.reddit.com/r/dailyprogrammer/comments/2ao99p/7142014_challenge_171_easy_hex_to_8x8_bitmap/

#FF 81 BD A5 A5 BD 81 FF
#AA 55 AA 55 AA 55 AA 55
#3E 7F FC F8 F8 FC 7F 3E
#93 93 93 F3 F3 93 93 93

from string import maketrans

def hex_to_bitmap(hex_string):
    output = ""
    for i in hex_string.split(" "):
        for bit in range(8):
            output += "x" if (int(i, 16) << bit) & (1 << 7) else " "
        output += "\n"
    return output[:-1]

def zoomIn(image, factor):
    output = ""
    for row in image.split('\n'):
        line = ''.join([char*factor for char in row])
        output += (line+'\n')*factor
    return output[:-1]

# [::2] - return all elements stride 2, so every other element
def zoomOut(image, factor):
    return '\n'.join(row[::factor] for row in image.split('\n')[::factor])

def zoom(image, direction, factor):
    if direction == 'IN':
        return zoomIn(image, factor)
    elif direction == 'OUT':
        return zoomOut(image, factor)

def rotate(image, direction):
    output = ""
    rows = [row for row in image.split('\n')]
    rowLen = len(rows)
    for i in range(rowLen):
        line = ""
        if direction == 'CW':
            for row in reversed(rows):
                line += row[i]
        if direction == 'CCW':
            for row in rows:
                line += row[rowLen-i-1]
        output += line+'\n'
    return output[:-1]

def invert(image):
    return image.translate(maketrans('x ', ' x'))

def input_and_call(image):
    command = raw_input("Enter command (x to quit): ")
    commands = command.split(' ')
    if commands[0] == 'x':
        return False
    elif commands[0] == 'zoom':
        return zoom(image, commands[1], int(commands[2]))
    elif commands[0] == 'invert':
        return invert(image)
    elif commands[0] == 'rotate':
        return rotate(image, commands[1])
    else:
        return image

def main():
    hex_input = raw_input("Enter Hex Numbers: ")
    image = hex_to_bitmap(hex_input)
    while(image):
        print image
        image = input_and_call(image)

main()
