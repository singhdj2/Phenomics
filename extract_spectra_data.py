__author__ = 'singhdj2'

import os

#myDir = "/Users/singhdj2/Desktop"
myDir = "/Users/singhdj2/Documents/Kansas_State_University_2014-/Doctoral_Research/Projects_data/" \
        "UAV_pipeline_work/calibration/15ASH_LF_asd_file/ASD_reading"
myOutFile = "/Users/singhdj2/Desktop/combined_spectra_file.txt"
fileList = os.listdir(myDir)

try:
    for fn in fileList:
        fullPath = myDir + '/' + fn
        if fullPath.endswith(".txt") or fullPath.endswith(".TXT"):
            with open(fullPath, 'r') as logFile:
                print "file" , fullPath, "is opened"

                line = logFile.readlines()
                for row in line :
                    rowFields  = row.split('\t')
                    if rowFields[0] == 'Wavelength':
                        #FileName = str(rowFields[1]).rstrip('\n')
                        f_name = str(rowFields[1]).rstrip('\r\n')
                    elif rowFields[0] == '460' or rowFields[0] == '525' or rowFields[0] == '710' :
                        data = f_name + ',' + str(rowFields[0]).rstrip('\r\n') + ',' + str(rowFields[1]).rstrip('\r')[1:]

                        #f_data = (data + "," + f_name)
                        print data
                        with open(myOutFile, 'a') as writeFile :
                            writeFile.write(data)

    print '******' , 'New file is located at' , myOutFile , '*******'
except Exception, e :
    #print '*** Error*** Unable to process the data file. Please check that the file specified is a valid text file. '
    print '*** Error Code:',e
