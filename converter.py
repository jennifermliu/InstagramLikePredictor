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

# f = open("./dataset/fixedtotalDataset.txt","r")
# fw = open("./dataset/finalDataset.txt","w")
# lines = f.readlines()
# for line in lines:
#     if line.strip() == "":
#         continue
#     else:
#         fw.write(line)
# f.close()
# fw.close()


# def fixedbug(s):
#     res = ''
#     i = 0
#     for ss in s:
#         if ss == ',':
#            i = 0
#            res += ss
#         elif i < 3:
#             res += ss
#             i += 1
#         else:
#             res += ';' + ss
#             i = 1
#     return res

# f = open("./dataset/totalDataset.txt","r")
# fw = open("./dataset/fixedtotalDataset.txt","w")
# lines = f.readlines()
# for line in lines:
#     fea = ''
#     feas = line.split("\t")
#     # print (len(feas))
#     # break
#     if len(feas) > 10:
#         feas[10] = fixedbug(feas[10])
#         fea = '\t'.join(feas)
#         fw.write(fea)
#         fw.write('\n')
# f.close()
# fw.close()

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
                        
                        # if j == 4:
                        #     # print (v)
                        #     vv = str(int(v)+1) + ":" + str(v)
                        #     v = vv
                        # columns 5 to 7 need special handling
                        if j>=6 and j<=8:
                            v = getSumFromString(v)
                        elif j==10:
                            v = getSumFromString(v)
                        else:
                            v = convertStringToInt(v)
                            # group likes into diffenrent groups
                            if j == 11:
                                v = groupLikeCount(v)
                                # v = str(vv+1) + ":" + str(vv)
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
    res = (int)(res)
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
    filename = "dataset/finalDataset.txt"
    results = parseText(filename)
    writeToCSV(results,"dataset.csv")
    getCategoryRange()
