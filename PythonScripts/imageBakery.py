from PIL import Image
import numpy as np
import json
import os

def is_null_pixel(ls:np.ndarray):
    if bool(np.add.reduce(ls==0)==len(ls)):
        return 1
    else:
        return 0

def getHitboxGrid(ls:np.ndarray[np.ndarray[np.ndarray]]):
    return list(map(lambda x:list(map(is_null_pixel,x)),ls))



resourcePath = "\\".join(os.path.abspath(__file__).split("\\")[:-2]+["resources"])
resourcePath.replace("\\","/")
ImgPath = resourcePath+"/images"


def getHitboxFile(file):
    return file.path.replace("\\","/").replace("/images/","/hitboxes/").split(".")[0]+".json"



def getFileGenerator(path):
    if not os.path.exists(path.replace("/images","/hitboxes")):
        os.mkdir(path.replace("/images","/hitboxes"))
    for file in os.scandir(path):
        
        if not file.is_dir():
            
            yield file
        else:

            for subFile in getFileGenerator((file.path).replace("\\","/")):
                yield subFile

for file in getFileGenerator(ImgPath):
    with open(getHitboxFile(file),"w") as opened:
        I = Image.open(file.path)
        opened.write(json.dumps(getHitboxGrid(np.asarray(I))))
        I.close()


