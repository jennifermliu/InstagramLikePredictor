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
                    if j != 0:
                        if j>=5 and j<=7:
                            v = getSumFromString(v)
                        else:
                            v = convertStringToInt(v)
                        result.append(v)

                results.append(result)
    return results

def writeToCSV(data,pathname):
    with open(pathname, "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)

def groupLikeCount(count):
    res = math.log10(count)
    res = (int)(2*res)
    return res

def getSumFromString(s):
    data = s.split(';')
    data = data[:-1]
    total = 0
    for d in data:
        d = convertStringToInt(d)
        total += d
    return total

if __name__ == "__main__":
    filename = "instagramDataset.txt"
    results = parseText(filename)
    writeToCSV(results,"dataset.csv")
