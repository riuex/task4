import numpy as np
import os
from optparse import OptionParser
import openslide
from openslide import open_slide,OpenSlide
from openslide.deepzoom import DeepZoomGenerator
#this package is need to read SVSfiles.
from multiprocessing.pool import Pool
import multiprocessing as multi
#this package is need to make multitask possible
from PIL import Image
import argparse
import time
"""
def conv3(image_path,save_folder,pixels,overlap,limit_bounds,coreN,border):
    image = open_slide(image_path)
    file_name = image_path.split("/")[1]
    file_name = file_name.split(".")[0]
    save_name = save_folder +"/" + file_name
    simage = DeepZoomGenerator(image,pixels,overlap,limit_bounds)
    level = simage.level_count - 1
    Xmax,Ymax = simage.level_tiles[level]
    Xmax,Ymax = Xmax - 1,Ymax - 1
    conunter = 0
    Yrange = range(Ymax)
    Xrange = range(Xmax)
    #for j in Xrange:
    p = Pool(coreN)
    p.map(conv3p,Xrange)
    p.close()
    print("mission completed!! Good bye!!!!")

def conv3p(i):
    for i in range(Ymax):
        address = (j,i)
        tile = simage.get_tile(level,address)
        gray = tile.convert("L")
        bw = gray.point(lambda x: 0 if x<220 else 1,"1")
        avgBkg = np.average(bw)
        if avgBkg <= (border/100) :
            image_name = save_name + "_" + str(i) + "_" + str(j) + ".jpg"
            print(save_name+ "_(" + str(i) +"/" + str(Ymax) + ")_(" + str(j) + "/" +str(Xmax) + ").jpg")
            tile.save(image_name)
            conunter += 1
        else :
            pass
        #print("-------Y length{" +str(i) + "}was completed!!!-----------")
        print("Number of tiles : " + str(conunter) + "/" + str(Xmax*Ymax))
"""

def conv4(image_path,save_folder,pixels,overlap,limit_bounds,coreN,border):
    image = open_slide(image_path)
    file_name = image_path.split("/")[1]
    file_name = file_name.split(".")[0]
    save_name = save_folder +"/" + file_name
    simage = DeepZoomGenerator(image,pixels,overlap,limit_bounds)
    level = simage.level_count - 1
    Xmax,Ymax = simage.level_tiles[level]
    Xmax,Ymax = Xmax - 1,Ymax - 1
    conunter = 0
    p = Pool(coreN)
    for j in range(Ymax):
        dataList = [(image_path,pixels,overlap,limit_bounds,i,j,Xmax,Ymax,level,border,save_name,conunter) for i in range(Xmax)]
        print("\n processing" + str(j) + "\n")
        p.map(conv4q,dataList)
    print("mission completed!! Good bye!!!!")
        #print("Number of tiles : " + str(conunter) + "/" + str(Xmax*Ymax))


def conv4q(dataList):
    conv4p(*dataList)

def conv4p(image_path,pixels,overlap,limit_bounds,x,y,Xmax,Ymax,level,border,save_name,counter):
    image = open_slide(image_path)
    simage = DeepZoomGenerator(image,pixels,overlap,limit_bounds)
    address = (x,y)
    tile = simage.get_tile(level,address)
    gray = tile.convert("L")
    bw = gray.point(lambda x: 0 if x<220 else 1,"1")
    avgBkg = np.average(bw)
    if avgBkg <= (border/100) :
        image_name = save_name + "_" + str(y) + "_" + str(x) + ".jpg"
        print(save_name+ "_(" + str(y) +"/" + str(Ymax) + ")_(" + str(x) + "/" +str(Xmax) + ").jpg")
        tile.save(image_name)
        #conunter += 1
    else :
        pass
#print("-------Y length{" +str(i) + "}was completed!!!-----------")


def conv3pro(image_path,save_folder,pixels,overlap,limit_bounds,coreN,border):
    image = open_slide(image_path)
    file_name = image_path.split("/")[1]
    file_name = file_name.split(".")[0]
    save_name = save_folder +"/" + file_name
    simage = DeepZoomGenerator(image,pixels,overlap,limit_bounds)
    level = simage.level_count - 1
    Xmax,Ymax = simage.level_tiles[level]
    Xmax,Ymax = Xmax - 1,Ymax - 1
    conunter = 0
    for i in range(Ymax):
        for j in range(Xmax):
            address = (j,i)
            tile = simage.get_tile(level,address)
            gray = tile.convert("L")
            bw = gray.point(lambda x: 0 if x<220 else 1,"1")
            avgBkg = np.average(bw)
            if avgBkg <= (border/100) :
                image_name = save_name + "_" + str(i) + "_" + str(j) + ".jpg"
                print(save_name+ "_(" + str(i) +"/" + str(Ymax) + ")_(" + str(j) + "/" +str(Xmax) + ").jpg")
                tile.save(image_name)
                conunter += 1
            else :
                pass
        #print("-------Y length{" +str(i) + "}was completed!!!-----------")
    print("Number of tiles : " + str(conunter) + "/" + str(Xmax*Ymax))
    print("mission completed!! Good bye!!!!")



def conv2():
    try :
        UNIT_X,UNIT_Y = wpixels,hpixels
        fname,f_input,f_output = data
        save_name = fname.split("/")[1]
        save_name = save_name.split(".")[0]
        print("processing : " + fname)
        simage = OpenSlide(fname)
        w,h = simage.dimensions
        w_rep,h_rep = int(w//UNIT_X)+1,int(h//UNIT_Y)+1
        w_end,h_end = w%UNIT_X,h%UNIT_Y
        w_size,h_size = UNIT_X,UNIT_Y
        w_start,h_start = 0,0
        print("function is ready!!")
        for i in range(h_rep):
            if i == h_rep - 1:
                h_size = h_end
            for j in range(w_rep):
                if j == w_rep - 1:
                    w_size = w_end
                img = simage.read_region((w_start,h_start),0,(w_size,h_size))
                img = img.convert("RGB")
                img_name = f_output+ "/" + save_name + "_" + str(i) + "_" + str(j) + ".jpg"
                img.save(img_name)
                """
                ggray = img.point()
                print(ggray)
                """
                print("saving image:" + f_output + "/" + save_name + "_(" + str(i) + "/" + str(h_rep-1) + ")_(" + str(j) + "/" + str(w_rep-1) + ").jpg")
                w_start += UNIT_X
            w_size = UNIT_X
            h_start += UNIT_Y
            w_start = 0
    except:
        print("Couldn't run! Something wrong in :" + fname)


#to make process of sepalating Unit
def conv(data,wpixels,hpixels):
    try:
        UNIT_X,UNIT_Y = wpixels,hpixels
        #print(insert)
        fname,f_input,f_output = data
        save_name = fname.split("/")[1]
        save_name = save_name.split(".")[0]
        print("processing : " + fname)
        simage = open_slide(fname)
        w,h = simage.dimensions
        w_rep,h_rep = int(w//UNIT_X)+1,int(h//UNIT_Y)+1
        w_end,h_end = w%UNIT_X,h%UNIT_Y
        w_size,h_size = UNIT_X,UNIT_Y
        w_start,h_start = 0,0
        print("function is ready!!")
        for i in range(h_rep):
            if i == h_rep - 1:
                h_size = h_end
            for j in range(w_rep):
                if j == w_rep - 1:
                    w_size = w_end
                img = simage.read_region((w_start,h_start),0,(w_size,h_size))
                img = img.convert("RGB")
                img_name = f_output+ "/" + save_name + "_" + str(i) + "_" + str(j) + ".jpg"
                img.save(img_name)
                """
                ggray = img.point()
                print(ggray)
                """
                print("saving image:" + f_output + "/" + save_name + "_(" + str(i) + "/" + str(h_rep-1) + ")_(" + str(j) + "/" + str(w_rep-1) + ").jpg")
                w_start += UNIT_X
            w_size = UNIT_X
            h_start += UNIT_Y
            w_start = 0
    except:
        print("Couldn't run! Something wrong in :" + fname)


if __name__ == "__main__":
    #Read the command line.
    parser = argparse.ArgumentParser(description='This script is ...',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--input", "-i", default="input",
                        help="The Directory name where the input image is saved. default='./input'")
    parser.add_argument("--filename","-f",default="test.svs",
                        help = "you should input the file name")
    parser.add_argument("--output", "-o", default="output",
                        help="Directory name where the converted image is saved. default='./output'")
    parser.add_argument("--multi", "-m", type=int, default=2,
                        help="Number of CPU cores to use for conversion. default=2")
    parser.add_argument("--widepixel","-w",type = int,default=512,
                        help = "Input the number of pixels")
    parser.add_argument("--heightpixel","-e",type = int,default=512,
                        help = "Input the number of height pixels")
    parser.add_argument("--border","-b", type=int ,default = 50,
                        help ="please input the border of background")
    parser.add_argument("--function","-fu",type = str,default = "conv3pro",
                        help = "Please select method of tiling")
    args = parser.parse_args()
    # "args" is object which contains all of parameter which user definded on command line
    #  this is opneslide reader of the testslide which the format is svs
    #f_lst = [f for f in os.listdir(args.input) if ".svs" in f]
    image_path = args.input + "/" + args.filename
    f_list = [image_path,args.input,args.output]
    widepixels = args.widepixel
    heightpixels = args.heightpixel
    function = args.function
    print("----------program start----------")
    starttime = time.time()
    #Set multi processing and run.
    #try:
    if function == "conv3pro":
        conv3pro(image_path,args.output,widepixels,1,False,args.multi,args.border)
    elif function == "conv3":
        conv3(image_path,args.output,widepixels,1,False,args.multi,args.border)
    elif function == "conv4":
        conv4(image_path,args.output,widepixels,1,False,args.multi,args.border)
    else :
        print("we couldn't recognize this function.")

    endtime = time.time()
    usedtime = round(endtime - starttime,2)

    print("You need " + str(usedtime) + "seconds")
    #testjpg = slide.read_region((0,0),0,slide.dimensions)
    #except:
    #print("WARNING!!!----------This command was failed-----------")
