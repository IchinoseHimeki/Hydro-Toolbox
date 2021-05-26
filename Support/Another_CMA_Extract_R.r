# Another CMA Extraction Conducted into R.
# My First try in R, so it is considerably buggy and hard to read.
# It's 3:00! Time to get some Tea!
# And when it comes to 7:00, time to relax!
library(data.table)
getwd()
inputfiles <- dir(path="./inputs", "*.TXT")
Extract <- function(Files)
  Data<-read.table(paste("./inputs/",Files,sep=""),col.names=c('Station','Lat','Lon','Alt','Year','Month','Day','PRE8-20','PRE20-8','PRE8-8','CODE1','CODE2','CODE3'),header=FALSE)
raw<-lapply(inputfiles,Extract)
# Binding all inputs into a big data frame.
allData <- rbindlist(raw, use.names=TRUE, fill=FALSE, idcol=NULL)
# Format Date Values.
allData$Date <- as.Date(paste(allData$Year,allData$Month,allData$Day),format="%Y %m %d")
# Reconstructing data frame.
dateData<-data.frame(allData$Station,allData$Date,allData$PRE8.20,allData$PRE20.8,allData$PRE8.8)
# Which cols would you want to save?
colnames(dateData) <- c('Station','Date','PRE8-20','PRE20-8','PRE8-8')
# A simple fix towards 999990, which probably means little value.
# And 999998 is quite tricky, please refer to data for further details.
dateData$`PRE8-20`[dateData$`PRE8-20`=='999990'] <- '0'
dateData$`PRE20-8`[dateData$`PRE20-8`=='999990'] <- '0'
# Choosing which station to use.
stations = c('50136', '53735')
filtered <- subset(dateData,dateData$Station%in% stations,select = c("Station","Date","PRE8-8"))
write.table(filtered,file="./outputs/results.csv",col.names = TRUE, row.names= FALSE,sep=",")