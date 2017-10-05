from timeit import default_timer
from collections import Counter


def readFiles(dictFileName, rawFileName):
    with open(dictFileName, "r") as f:
        dict = f.read().split("\n")
        while '' in dict:
            dict.remove('')
    with open(rawFileName, "r") as f:
        raw = f.read().split("\n")
        while '' in raw:
            raw.remove('')

    return dict, raw
    # print(dict)
def MIN(a, b, c):
    if a < b and a < c:
        return a
    elif(b<c):
        return b
    return c

def LevenshteinDistance(source, target):
    distance = 0
    n = len(target)
    m = len(source)

    distanceMatrix = [[0] * (m+1) for i in range(n+1)]
    for i in range(1,n+1):
        distanceMatrix[i][0] = distanceMatrix[i-1][0] + 1
    for j in range(1, m+1):
        distanceMatrix[0][j] = distanceMatrix[0][j-1] + 1
    for i in range(1, n+1):
        for j in range(1, m+1):
            if source[j-1] == target[i-1]:
                sub_cost = 0
            else:
                sub_cost = 1
            distanceMatrix[i][j] = MIN(distanceMatrix[i-1][j]+1, distanceMatrix[i][j-1]+1, distanceMatrix[i-1][j-1]+ sub_cost)
    # print(distanceMatrix)

    return distanceMatrix[n][m]

def LevenshteinDistanceImproved(source, target, currentDistance):
    n =  len(target)
    m = len(source)
    v0 = [0]*(n+1)
    # print(len(v_list),n)
    # v0 = v_list[n]
    v1 = [0]*(n+1)
    for i in range(0,n+1):
        v0[i] = i

    # print(v0)
    min = 50
    for i in range(0,m):
        # v1 = [0] * (n + 1)
        v1[0] = i +1
        min = i + 1
        for j in range(0,n):
            if source[i] == target[j]:
                sub_cost = 0
            else:
                sub_cost = 1

            v1[j+1] = MIN(v1[j] + 1, v0[j+1] +1, v0[j] + sub_cost)
            if v1[j+1] < min:
                min = v1[j+1]
        if currentDistance <= min:
            return currentDistance
        v2 = v0
        v0 = v1
        v1 = v2
        # print(v0)
    return v0[n]

def writeOutput(dict, raw, outputFileName):
    count = 0
    start = default_timer()

    with open(outputFileName, "w") as f:
        for source in raw:
            if source not in dict:
                spelledWord = ""
                minDistance = 100

                #initialize variables here save time


                for target in dict:
                    distance = LevenshteinDistanceImproved(source, target, minDistance)
                    # distance = LevenshteinDistance(source, target)
                    if distance < minDistance:
                        spelledWord = target
                        minDistance = distance
                        if minDistance == 1:
                            break
                f.write(spelledWord + " "+ str(minDistance)+"\n")
            else:
                f.write(source + " 0\n")

            count +=1
            if count % 5 == 0:
                print(count)
                end = default_timer()
                print("Running time: ", (end - start)/60)

def task1():
    # start = default_timer()
    print("Running...")
    dictData, rawData = readFiles("dictionary.txt", "raw.txt")
    # print(Counter(rawData).most_common())
    writeOutput(dictData, rawData, "output1.txt")
    # end = default_timer()
    # print("Running time: ", (end - start))

task1()
# print(LevenshteinDistanceImproved("intention", "execution"))

