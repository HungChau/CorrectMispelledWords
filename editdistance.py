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

def LevenshteinDistance(source, target, currentDistance):
    n = len(target)
    m = len(source)

    distanceMatrix = [[0] * (m+1) for i in range(n+1)]
    for i in range(1,n+1):
        distanceMatrix[i][0] = i
    for j in range(1, m+1):
        distanceMatrix[0][j] = j
    min = 50
    for j in range(1, m + 1):
        min = j
        for i in range(1, n + 1):
            if source[j-1] == target[i-1]:
                sub_cost = 0
            else:
                sub_cost = 1
            distanceMatrix[i][j] = MIN(distanceMatrix[i-1][j]+1, distanceMatrix[i][j-1]+1, distanceMatrix[i-1][j-1]+ sub_cost)
            if distanceMatrix[i][j] < min:
                min = distanceMatrix[i][j]
        if min > currentDistance:
            return currentDistance
    # print(distanceMatrix)

    return distanceMatrix[n][m]

def OSA_Distance(source, target, currentDistance):
    n = len(target)
    m = len(source)

    distanceMatrix = [[0] * (m + 1) for i in range(n + 1)]
    for i in range(1, n + 1):
        distanceMatrix[i][0] = i
    for j in range(1, m + 1):
        distanceMatrix[0][j] = j
    min = 50
    for j in range(1, m + 1):
        min = j
        for i in range(1, n + 1):
            if source[j - 1] == target[i - 1]:
                sub_cost = 0
            else:
                sub_cost = 1
            distanceMatrix[i][j] = MIN(distanceMatrix[i - 1][j] + 1, distanceMatrix[i][j - 1] + 1,
                                       distanceMatrix[i - 1][j - 1] + sub_cost)
            #the difference from the algorithm for Levenshtein distance is the additionof one recurrence
            if i > 1 and j > 1 and target[i-1]==source[j-2] and target[i-2] == source[j-1]:
                if distanceMatrix[i][j] > (distanceMatrix[i-2][j-2]+sub_cost):
                    distanceMatrix[i][j] = (distanceMatrix[i - 2][j - 2] + sub_cost)

            if distanceMatrix[i][j] < min:
                min = distanceMatrix[i][j]
        if min > currentDistance:
            return currentDistance
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
        if min > currentDistance:
            return currentDistance
        v2 = v0
        v0 = v1
        v1 = v2
        # print(v0)
    return v0[n]

def OSA_improved(source, target, currentDistance):
    n =  len(target)
    m = len(source)
    v0 = [0]*(n+1)
    # print(len(v_list),n)
    # v0 = v_list[n]
    v1 = [0]*(n+1)
    v_minus1 = [0] * (n + 1)
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
            if i > 0 and j > 0 and target[j] ==source[i-1] and target[j-1] ==source[i]:
                if v1[j+1] > (v_minus1[j-1] + sub_cost):
                    v1[j+1] = (v_minus1[j-1] + sub_cost)

            if v1[j+1] < min:
                min = v1[j+1]
        if min > currentDistance:
            return currentDistance
        v_minus1 = v0
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

                for target in dict:
                    # distance = LevenshteinDistanceImproved(source, target, minDistance)
                    # distance = LevenshteinDistance(source, target,minDistance)
                    distance = OSA_improved(source, target,minDistance)
                    # distance = OSA_Distance(source, target,minDistance)
                    if distance < minDistance:
                        spelledWord = target
                        minDistance = distance
                        if minDistance == 1:
                            break
                f.write(spelledWord + " "+ str(minDistance)+"\n")
            # else:
            #     f.write(source + " 0\n")

            count +=1
            if count % 5 == 0:
                print(count)
                end = default_timer()
                print("time: ", (end - start)/60)
    end = default_timer()
    print("Running time: ", (end - start) / 60)

def task1():
    # start = default_timer()
    print("Running...")
    dictData, rawData = readFiles("dictionary.txt", "raw.txt")
    # print(Counter(rawData).most_common())
    writeOutput(dictData, rawData, "output1.txt")
    # end = default_timer()
    # print("Running time: ", (end - start))

task1()
# print(LevenshteinDistanceImproved("BTE", "ACET", 10))
