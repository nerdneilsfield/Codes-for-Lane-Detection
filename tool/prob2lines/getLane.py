import numpy as np

def getLine(score):
    # print(score)
    thr = 0.3
    coordinate = np.zeros((18, 1))
    for i in range(18):
        lineId = int(288-i*20/590*288) -1
        line = score[lineId]
        maximum = np.max(line)
        id = np.where(line == maximum)[0][0]
        # print(id)
        value = line[id]
        # print(value)
        if value / 255.0 > thr:
            coordinate[i] = id
    if sum([i for i in coordinate if i > 0])<2:
        coordinate = np.zeros((18, 1))
    # print(coordinate)
    return coordinate