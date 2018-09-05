
###-----------------------------------------------------------------
##  *This R script reads the tersus raw files and 
##    aggregates the latitude, longitude, and altitude 
##    GPS survey data and outputs 'gps-summary-survey_' CSV file 
##    for a complete set of survey tersus/gps files.
##  *Input: Path to the raw survey files with extenstion '.trs'
##  *Author: Daljit Singh (singhdj2@ksu.edu)
##  *Created: 2018-04-16
##  *Updated: 2018-09-05
##  *Future addition: condition to handle negative lat/long values
###-----------------------------------------------------------------

## load required packages 
if (!require(pacman)) {
  install.packages(pacman)
}
library(pacman)
p_load(tidyverse)


## function definition
getLatLongFilesFunc <- function(myDir){
  # list of text files in myDir
  fileList <- list.files(myDir,pattern = '.trs')
  cat('**There are total ',length(fileList), ' files to process. \n')
  
  # condition to check if file list is empty
  stopifnot(!is.null(fileList))
  
  # create empty vector to hold aggregated values
  out = NULL
  # loop to go through each element of file list
  for (f in fileList){
    cat('Processing: ',f,'\n')
    inPath <- paste0(myDir,'/',f)   #full path to file
    dat <- read.table(inPath,stringsAsFactors = F,skipNul = T,skip = 2)  #read table
    ## Piped function to: filter data with complete data rows, RTK fix ('4');
    ##  aggregate lat, long info
    dat <- dat %>% filter(str_detect(V1,'GPGGA')) %>% 
      filter(dim(str_split(V1,',',simplify = T))[2] > 10) %>%
      separate(V1,sep = ',',remove = T, into = paste0('V',1:15)) %>% 
      filter(V7=='4') %>%
      na.omit() %>%
      mutate_at(vars('V3','V5','V10'),as.numeric) %>%
      mutate(V3 = V3/100,
             V5 = V5/100,
             latDDD = (as.numeric(str_sub(V3,1,2)) + (as.numeric(paste0(str_sub(V3,4,5),'.',str_sub(V3,6,-1)))/60)),
             longDDD = (as.numeric(str_sub(V5,1,2)) + (as.numeric(paste0(str_sub(V5,4,5),'.',str_sub(V5,6,-1)))/60))) %>%
      summarise(latDDD=mean(latDDD),
                longDDD=mean(longDDD),
                altDDD=mean(V10),
                numRows=n()) %>%
      mutate(fileName=f) %>%
      select(fileName,latDDD:numRows)
    # bind the aggr data to output vector
    out <- bind_rows(out, dat)
  }
  # create a file name for output CSV file
  fName= paste0(myDir,'/gnss-summary-survey_',Sys.Date(),'.csv')
  # write file to disk
  write.csv(out,fName,row.names = F)
  #out
}

## Function usage
cat("***** Function usage step 1: source('path/to/getLatLongFiles/function/file.R') \n")
cat("***** Function usage step 2: getLatLongFilesFunc('path/to/my/gps/directory/') \n") 

#getLatLongFilesFunc('/image_data/MAHYCO_2017/RTK_issue/')
