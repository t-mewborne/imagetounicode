#!/usr/bin/python3

from PIL import Image, ImageDraw, ImageFont
import unicodedata
import random

def calcGreyValue(character,font_path,font_size):
    # Set up a PIL Image object with a white background
    background_color = (255, 255, 255)
    image_width = font_size*2
    image_height = font_size*2
    image = Image.new("RGB", (image_width, image_height), background_color)

    # Draw the character in the center of the image
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, font_size)
    
    draw.text((50, 50), character, font=font, fill=(0, 0, 0))

    # Convert the image to grayscale and compute the mean grey value
    grey_image = image.convert("L")
    mean_grey_value = sum(grey_image.getdata()) / len(grey_image.getdata())
    
    #image.save("o.jpg")
    #print("Mean grey value:", mean_grey_value)
    return (mean_grey_value)

def main():
    # Set up a font and size
    font_path = "/Library/Fonts/SF-Mono-Medium.otf"
    font_size = 100
    print("Font is set to", font_path, "with size",font_size)
    character = chr(9995)
    calcGreyValue(character,font_path,font_size)

    characterSet=[' ']

    for i in range(33,15000):
        if (chr(i).isprintable()):
            characterSet.append(chr(i))

    calculated=[(chr(32),255)]

    for c in characterSet:
        gv=calcGreyValue(c,font_path,font_size)
        if gv!=255:
            calculated.append((c,gv))

    calculated_sorted=sorted(calculated,key=lambda x:x[1])

    adjustedValues=[]
    for i in range(len(calculated_sorted)):
        x=(i/len(calculated_sorted))*255
        adjustedValues.append((calculated_sorted[i][0],x))

    filtered_values=[]
    prev_value=None
    for cs in adjustedValues:
        if prev_value is None or abs(cs[1]-prev_value)>=0.001:
            filtered_values.append(cs)
            prev_value=cs[1]

    print("Created a character set of",len(filtered_values),"characters.")

    with open("unicodescale.txt", "w") as f:
        f.write((font_path+"\n"))
        for fv in filtered_values:
            f.write((str(ord(fv[0]))+','+str(fv[1])+'\n'))

    print("File saved")

if __name__=="__main__":
    main()