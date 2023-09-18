#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-e" or sys.argv[1] == "--encode":
            if len(sys.argv) > 3:
                encode(sys.argv[2], sys.argv[3])
            else:
                if sys.stdin.isatty():
                    message = input(">> ")
                    encode(sys.argv[2], message)
                else:
                    message = ""
                    for line in sys.stdin:
                        message += line
                    encode(sys.argv[2], message)
        elif sys.argv[1] == "-d" or sys.argv[1] == "--decode":
            decode(sys.argv[2])
        else:
            print(f"option '{sys.argv[1]}' not recognized")
            printhelp()
    else:
        printhelp()
        

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
    print()

                
def text_to_bitstring(text):
    bytetext = text.encode()
    bitstring = ""
    for i in bytetext:
        bitchar = bin(i)[2:]
        while len(bitchar) < 8:
            bitchar = '0' + bitchar
        bitstring += bitchar
    return bitstring

def printhelp():
    print("usage: lsb <option> <filename> <message>")
    print("options:")
    print("\t-e, --encode: <filename> <message>")
    print("\t-d, --decode: <filename>")

if __name__ == "__main__":
    main()