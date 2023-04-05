#!/usr/bin/python3

import os.path
import re
from PIL import Image, ImageDraw, ImageFont


def detectImages():
    images=[]
    for f in os.listdir("sampleimages/"):
        if (f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png')):
            images.append(f)
    return images

def main():

    if not os.path.isfile("unicodescale.txt"):
        print("Could not find scale file.")
        return
    
    images=detectImages()
    print("Located the following images:")
    for i in range(len(images)):
        print(f'\t({i+1}) {images[i]}')
    
    print(f'\t({len(images)+1}) Custom File Path')
    print(f'\t({len(images)+2}) Quit')

    answer=None
    imageFile=None
    while not answer:
        answer=int(input("Please make a selection: "))
        if not answer in range(1,len(images)+3):
            answer=None
            print(f"Invalid Option")
            continue

        if answer==len(images)+2:
            return
        elif answer==len(images)+1:
            valid=False
            while(not valid):
                imageFile=input("Enter the name of the image file: ")
                valid=os.path.isfile(imageFile)
        else:
            imageFile=images[i-1]

    #TODO are lists not ordered?
    

    print(f"Using {imageFile}")
    return

        #answer=1

    
    #imageFile="planet.png"
    #imageFile="eggs.jpeg"

    w=0
    h=0
    valid = False
    while (not valid):
        w=input("Enter desired character width: ")
        valid = w.isdigit()

    # valid = False
    # while (not valid):
    #     h=input("Enter desired character height: ")
    #     valid = h.isdigit()

    w=int(w)
    h=int(h)




    font_file=''
    scale=[]
    with open("unicodescale.txt","r") as f:
        font_file = next(f).replace('\n','')
        if not os.path.isfile(font_file):
            print(f"Could not locate font at {font_file} to calculate aspect ratio")
            return
        print(f"Font is {font_file}")
        for line in f:
            spt=line.replace('\n','').split(',')
            character = chr(int(spt[0]))
            gv = float(spt[1])
            scale.append((character,gv))

    font=ImageFont.truetype(font_file,size=100)
    bbox=font.getbbox(chr(9608))
    character_height=abs(bbox[3]-bbox[2])

    with Image.open(imageFile).convert('L') as img:
        imgW, imgH = img.size
        # tileW=imgW/w
        # tileH=imgH/h
        
        #Calculate the height of the image as if characters are 1x1
        sqh=(w/imgW)*imgH #The square height
        h=int(sqh*0.5)

        if h<=0:
            h=1

        

        if (h>imgH or w>imgW):
            print(f"Error: Bad dimensions {w}x{h}. Max dimensions are {imgW}x{imgH}")
            return
        else:
            print(f'Dimensions set to {w}x{h}')

        tiles=[[0] * w for i in range(h)]
        count=[[0] * w for i in range(h)]
        averaged=[[0] * w for i in range(h)]
        characters=[[' '] * w for i in range(h)]
        inverted=[[' '] * w for i in range(h)]

        for i in range(imgH):
            r=int((i/imgH)*(h))
            for j in range(imgW):
                c=int((j/imgW)*(w))
                p=img.getpixel((j,i))
                tp= p+tiles[r][c]
                tiles[r][c]=tp
                count[r][c]+=1

        for r in range(len(tiles)):
            for c in range(len(tiles[r])):
                if (count[r][c]==0):
                    averaged[r][c]=255
                else:
                    averaged[r][c]=tiles[r][c]/count[r][c]

        for r in range(len(tiles)):
            for c in range(len(tiles[r])):
                gv = averaged[r][c]
                for s in range(len(scale)):
                    if gv<scale[s][1]:
                        characters[r][c]=scale[s][0]
                        inverted[r][c]=scale[len(scale)-s][0]
                        break

        for r in characters:
            for c in r:
                print(c,end='')
            print()

        answer=''
        while answer!='q':
            print("\nquit(q), fileOut(f), invert(i)")
            answer=input("What would you like to do next?: ")

            if answer=='i':
                for r in inverted:
                    for c in r:
                        print(c,end='')
                    print()
            
            elif answer=='f':
                print("\nFile Out Options:")
                print("\tc - Cancel")
                print("\tn - Normal: \tWrite the original")
                print("\td - Digit: \tWrite the integer representation of the unicode characters line by line (\\n included)")
                print("\ti - Inverted: \tWrite the inverted characters")
                print("\tf - Inverted Digit: \tWrite the integer representation of the unicode characters line by line (\\n included)")
                answer=input("Enter your selection: ")
                if answer not in ['n','l','d','i','u','f']:
                    continue
                
                newfile=None
                while not newfile:
                    newfile=input("Enter a filename: ")
                    if os.path.isfile(newfile):
                        print("Error: File Exists")
                        newfile=None

                with open(newfile,"w") as f:
                    if answer=='n':
                        for r in characters:
                            for c in r:
                                f.write(c)
                            f.write('\n')
                        print(f'Wrote {newfile}')
                    elif answer=='d':
                        for r in characters:
                            for c in r:
                                f.write((str(ord(c))+'\n'))
                            f.write(str(ord('\n')))
                        print(f'Wrote {newfile}')
                    elif answer=='i':
                        for r in inverted:
                            for c in r:
                                f.write(c)
                            f.write('\n')
                        print(f'Wrote {newfile}')
                    elif answer=='f':
                        for r in inverted:
                            for c in r:
                                f.write((str(ord(c))+'\n'))
                            f.write(str(ord('\n')))
                        print(f'Wrote {newfile}')
                answer=''


if __name__=="__main__":
    main()