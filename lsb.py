import sys
from PIL import Image
import numpy as np

def main():
    if len(sys.argv) == 3:
        encode(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        decode(sys.argv[1])

def encode(image_path, message):
    image = Image.open(image_path)
    image_array = np.array(image)
    bitstring = text_to_bitstring(message)
    print(f"encoding bitstring: {bitstring}")
    bit_index = 0
    done = True
    for indexx,x in enumerate(image_array):
        for indexy,y in enumerate(x):
            for indexc,channel in enumerate(y):
                if bit_index < len(bitstring):
                    encoded_byte = bin(channel)
                    encoded_byte = encoded_byte[:-1] + bitstring[bit_index]
                    image_array[indexx][indexy][indexc] = int(encoded_byte, 2)
                    bit_index += 1
    out_image = Image.fromarray(image_array)
    out_image.save("out.png")

def decode(image_path):
    image = Image.open(image_path)
    image_array = np.array(image)
    bitstring = ""
    for x in image_array:
        for y in x:
            for channel in y:
                bitstring += bin(channel)[-1]
    text = b''
    for i in range(0,len(bitstring), 8):
        textint = int(bitstring[i: i+8], 2)
        byte = textint.to_bytes(1, byteorder='big')
        try:
            print(byte.decode(), end='')
        except:
            break

                
def text_to_bitstring(text):
    bytetext = text.encode()
    bitstring = ""
    for i in bytetext:
        bitchar = bin(i)[2:]
        while len(bitchar) < 8:
            bitchar = '0' + bitchar
        bitstring += bitchar
    return bitstring

if __name__ == "__main__":
    main()