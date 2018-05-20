import csv
import math

def convertStringToInt(v):
    s = 0
    if v.endswith('k'):
        temp = v.replace('k','')
        s = float(temp)*1000
        s = int(s)
    elif v.endswith('m'):
        temp = v.replace('m','')
        s = float(temp)*1000000
        s = int(s)
    elif "," in v:
        temp = v.replace(',','')
        s = int(temp)
    else:
        s = int(v)
    return s

def parseText(filename):
    results = []
    with open(filename) as f:
        data = f.readlines()
        line = [x.strip() for x in data]
        for i in range(len(line)):
            values = line[i].split("\t")
            if i == 0:
                values.pop(0)
                results.append(values)
            else:
                result = []
                for j in range(len(values)):
                    v = values[j]
                    # skip username
                    if j != 0:
                        # columns 5 to 7 need special handling
                        if j>=5 and j<=7:
                            v = getSumFromString(v)
                        else:
                            v = convertStringToInt(v)
                            # group likes into diffenrent groups
                            if j == 8:
                                v = groupLikeCount(v)
                        result.append(v)
                results.append(result)
    return results

def writeToCSV(data,pathname):
    with open(pathname, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

def groupLikeCount(count):
    # print(count)
    res = math.log10(count)
    res = (int)(2*res)
    # print(res)
    return res

def getSumFromString(s):
    data = s.split(';')
    data = data[:-1] #skip last one because s ends with ;
    total = 0
    for d in data:
        d = convertStringToInt(d)
        total += d
    return total

def getCategoryRange():
    category = 0
    start = 1
    for i in range(1,10000001):
        if groupLikeCount(i) !=category:
            print("category "+str(category)+" starts at count "+str(start)+" and ends at "+str(i-1))
            start = i
            category += 1

if __name__ == "__main__":
    filename = "instagramDataset.txt"
    results = parseText(filename)
    writeToCSV(results,"dataset.csv")
    getCategoryRange()
