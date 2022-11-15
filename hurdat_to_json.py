
import json
import sys

# initialize parameters

filename = sys.argv[1]
outfile = sys.argv[2]


# convert W and S coords to negative float and E / W to positive float

def convCords(coord):

    hem = coord[-1]
    coordFixed = coord.strip(coord[-1])
    if (hem == 'E' or hem == 'N'):
        coordFixed = float(coordFixed)

    elif (hem == 'W' or hem == 'S'):
        coordFixed = float(coordFixed) * -1

    else:
        print("fatal error - invalid coordinate")

def convertRecords(filename, outfile):

    
    dict2 = []
    stormID = 'stormID'
    stormName = 'stormName'
    stormDate = 'stormDate'
    stormTime = 'stormTime'
    isLandFall = 'isLandFall'
    stormType = 'stormType'
    lat = 'lat'
    lon = 'lon'
    maxWind = 'maxWind'
    minPressure = 'minPressure'
    result = {}
    lineNumber = 1

    with open(filename) as fh:

        for line in fh:
        
            firstLine = line.split(',')
            firstWord = firstLine[0]
            
            if (firstWord[0] == 'A'): #determine if new storm entry and get storm name and id
                numAdv = firstLine[2]
                stormIDValue = firstWord
                stormNameValue = firstLine[1].strip()
                
                
            elif (firstWord[0] == '2' or '1'): #read position data

                try: # check for proper formatting and extract
                    fixedLat = convCords(firstLine[4])
                    fixedlon = convCords(firstLine[5])
                    stormTimeValue = firstLine[1].strip(firstLine[1][0])
                    isLandfallValue = firstLine[2].strip(firstLine[2][0])
                    stormTypeValue = firstLine[3].strip(firstLine[3][0])
                    temp2 = {stormID:stormIDValue, stormName:stormNameValue, stormDate:firstWord, stormTime:stormTimeValue, isLandFall:isLandfallValue, stormType:stormTypeValue, lat:fixedLat, lon:fixedlon, maxWind:int(firstLine[6]), minPressure:float(firstLine[7])}
                    dict2.append(temp2) #append new line to dictionary
                except:
                    print('Invalid Line Format')
                    print(firstWord[0])
                    
                
            else:
                print('Error: Invalid Data')
                print(firstWord[0])

            lineNumber = lineNumber + 1
            
    # write json out to file

    result["storms"] = dict2 #
    out_file = open(outfile, "w")
    json.dump(result, out_file, indent=2)

convertRecords(filename, outfile)

