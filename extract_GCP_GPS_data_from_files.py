__author__ = 'singhdj2'

import os

#myDir = "/Users/singhdj2/Desktop"
myDir = "/Users/singhdj2/Documents/Kansas_State_University_2014-/Doctoral_Research/Projects_data/" \
        "UAV_pipeline_work/GCP_information_all_tests/GCP_NFM_Sorghum_NAM_08042015"
myOutFile = "/Users/singhdj2/Desktop/combined_GCP_file.txt"
fileList = os.listdir(myDir)

try:
    for fn in fileList:
        fullPath = myDir + '/' + fn
        if fullPath.endswith(".txt") or fullPath.endswith(".TXT"):
            with open(fullPath, 'r') as logFile:
                print "file" , fullPath, "is opened"
                i = 0
                line = logFile.readlines()
                for row in line :
                    if row[0:6] == '$GPGGA':
                        rowFields  = row.split(',')
                        if len(rowFields) > 10 :
                            gpsLat = str(rowFields[2])
                            gpsNorthing = str(rowFields[3])
                            gpsLong = str(rowFields[4])
                            gpsEasting = str(rowFields[5])
                            gpsAlt = str(rowFields[9])
                            latLongAlt = (fn + ',' + gpsLat + ',' + gpsNorthing + ',' + gpsLong + ',' + gpsEasting + ',' + gpsAlt + '\n')
                            i += 1
                        with open(myOutFile, 'a') as writeFile :
                            writeFile.write(latLongAlt)
                #print gpsLat , gpsLong, gpsAlt
                print '$GPGGA lines: ' , i
    print '******' , 'New file is located at' , myOutFile , '*******'
except Exception, e :
    #print '*** Error*** Unable to process the GPS log file. Please check that the file specified is a valid gps log. '
    print '*** Error Code:',e
