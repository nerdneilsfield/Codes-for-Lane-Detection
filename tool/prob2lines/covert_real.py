import numpy as np
import sys
import os
from PIL import Image, ImageDraw
from getLane import  getLine

def processImage(imgName, dataPath, expPath, outputPath, outputImage=False):
    exist = None
    with open(os.path.join(expPath, imgName + ".exist.txt"), 'r') as _file:
        exist = [True if i == '1' else False for i in _file.read().split()]
    coordinates = []
    for i in range(4):
        if exist[i]:
            scorePath = os.path.join(expPath, imgName + "_" + str(i+1) + "_avg.png")
            scoreMap  = np.asarray(Image.open(scorePath))
            coordinate = getLine(scoreMap)
            coordinates.append(coordinate)
        else:
            coordinates.append(np.empty)
    save_name = os.path.join(expPath, imgName + "_lines.txt")
    lanes = []
    point = (0, 0)
    points = []
    with open(save_name, 'w') as _file:
        for i in range(4):
            if exist[i]:
                points = []
                coordinate = coordinates[i]
                for m in range(len(coordinate)):
                    t = coordinate[m]
                    if t > 0:
                        point = (int(t*1640/800)-2, int(590 - m*20-5))
                        # print(point)
                        _file.write("%d %d " %(point[0], point[1]))
                        points.append(point)
                lanes.append(points)
                _file.write('\n')
    if outputImage:
        imgPath = os.path.join(dataPath, imgName + ".jpg")
        img = Image.open(imgPath)
        img = img.resize((1640, 590), Image.BICUBIC)
        drawer = ImageDraw.Draw(img)
        for i in range(len(lanes)):
            color = (255, i * 60, 0)
            drawer.line(lanes[i], width=2, fill=color)
        del drawer
        savePath = os.path.join(outputPath, imgName + "_output.jpg")
        img.save(savePath)

if __name__ == "__main__":
    imageList = []

    if len(sys.argv) != 4:
        exit(12)

    dataPath = sys.argv[2]
    outputPath = sys.argv[3]
    with open(sys.argv[1], 'r') as _file:
        imageList = _file.readlines()

    num = len(imageList)
    for i in range(num):
        imgName = ".".join(imageList[i].split(".")[0:-1])
        processImage(imgName, dataPath, dataPath, outputPath, True)