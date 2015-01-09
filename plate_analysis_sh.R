
args = commandArgs(trailingOnly = TRUE)
input_file = args[1]

numReads = as.integer(args[2])

time = as.integer(args[3])
#print(numReads)
#cat("How many times did you read each plate? ")
#ncol <- readLines(file("stdin"),1)
library(methods)
rownames = c("A1","A2","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12","B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","B11","B12",
             "C1","C2","C3","C4","C5","C6","C7","C8","C9","C10","C11","C12","D1","D2","D3","D4","D5","D6","D7","D8","D9","D10","D11","D12","E1","E2","E3","E4","E5",
             "E6","E7","E8","E9","E10","E11","E12","F1","F2","F3","F4","F5","F6","F7","F8","F9","F10","F11","F12","G1","G2","G3","G4","G5","G6","G7","G8","G9","G10","G11","G12","H1",
             "H2","H3","H4","H5","H6","H7","H8","H9","H10","H11","H12")

mat = read.table(input_file,header=F, sep=",", row.names=rownames)

output=matrix(unlist(mat),ncol = numReads,byrow=F)

dimnames(output) = list(rownames, seq(1,length(output[1,])))
blnk_test = vector()
blnk_vector = scan("settings.txt",sep=",")
for (x in blnk_vector){
blnk_test = rbind(blnk_test,output[x,])}


#all of A
#blnk = subset(output[1:12,])
#all of H
#blnk = rbind(blnk,output[85:96,])

#all of F
#blnk = rbind(blnk,output[61:72,])

#all of G
#blnk = rbind(blnk,output[73:84,])

#all of 1
#blnk = rbind(blnk,output[13,])
#blnk = rbind(blnk,output[25,])
#blnk = rbind(blnk,output[37,])
#blnk = rbind(blnk,output[49,])
#blnk = rbind(blnk,output[61,])
#blnk = rbind(blnk,output[73,])
#all of 11
#blnk = rbind(blnk,output[23,])
#blnk = rbind(blnk,output[35,])
#blnk = rbind(blnk,output[47,])
#blnk = rbind(blnk,output[59,])
#blnk = rbind(blnk,output[71,])
#blnk = rbind(blnk,output[83,])
##all of 12
#blnk = rbind(blnk,output[24,])
#blnk = rbind(blnk,output[36,])
#blnk = rbind(blnk,output[48,])
#blnk = rbind(blnk,output[60,])
#blnk = rbind(blnk,output[72,])
#blnk = rbind(blnk,output[84,])
##B6 and G6
#blnk = rbind(blnk,output[18,])
#blnk = rbind(blnk,output[78,])
#background level
bg = mean(blnk_test)

# matrix with background subtracted
#blnk_vector=c(1,2,3,4,5,6,7,8,9,10,11,12,85,86,87,88,89,90,91,92,93,94,95,96,13,25,37,49,61,73,23,35,47,59,71,83,24,36,48,60,72,84,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84)

output.sans.bg = output-bg

output.sans.bg.log = log(output.sans.bg)
output.sans.bg.log[which(is.nan(output.sans.bg.log))]=NA
#linear fit lm(y~x) where y is data and x is vector sequence of length of data
#lm(output.sans.bg[14,5:15]~seq(1,length(output.sans.bg[14,5:15])),na.action=na.omit)
#vector of linear fits of all cells
lm.fits=vector()
#p1 is lower bound and p2 is upper bound points for linear fit
#p1=10
#p2=15
#for (i in 1:96) {
#  z = try(lm(output.sans.bg.log[i,p1:p2]~seq(from=(p1*15),to=(p2*15),by=15, na.action=na.omit)))
#  if(is(z,"try-error")){lm.fits=append(lm.fits,NA)}
#  else{lm.fits=append(lm.fits,z$coefficients[2])}

#  }
#lm.fits.tbl = as.data.frame(lm.fits)
#row.names(lm.fits.tbl)=rownames
#print(lm.fits.tbl)





#which(abs(output.sans.bg.log-2)==min(abs(output.sans.bg.log-2)))
for (i in 1:96){
  y = as.vector(t(output.sans.bg.log[i,]))
  #max and min give first occurence of each
  #rng = range(y, na.rm = TRUE)
  #makes na extremely small, otherwise NA gives integer(0) error
  y[is.na(y)] <- -1000
  ppmax = which.max(y)
  
  for (i2 in 1:ppmax){
    y2 = y[1:ppmax]
    if(ppmax > 6){
      p1 = which(abs(y2-(-4))==min(abs(y2-(-4))))
      p2 = which(abs(y2-(-2))==min(abs(y2-(-2))))
      
    } else if(is.element(i,blnk_vector)){
      p1 = which(abs(y2-(-4))==min(abs(y2-(-4))))
      p2 = which(abs(y2-(-2))==min(abs(y2-(-2))))
    }else{print ("FATAL ERROR. FATAL ERROR. OUTLIER MESSING UP DATA")
          print (i)
          print (ppmax)}
  }
  
  z = try(lm(output.sans.bg.log[i,p1:p2[1]]~seq(from=(p1*time),to=(p2[1]*time),by=time)),silent=TRUE)
  if(is(z,"try-error")){lm.fits=append(lm.fits,NA)}
  else{lm.fits=append(lm.fits,z$coefficients[2])}
  
  #}
  
}
mainDir = getwd()
subDir = toString(input_file)
subDir2 = sub('.txt$', '', subDir)
lm.fits.tbl = as.data.frame(lm.fits)
row.names(lm.fits.tbl)=rownames
print(lm.fits.tbl)
outputFile = paste("FITS_",input_file)
dir.create(file.path(mainDir, subDir2), showWarnings = FALSE)
setwd(file.path(mainDir, subDir2))

write.table(lm.fits.tbl,file = outputFile)
for (i in 1:96){
  tryCatch({
    plot(output.sans.bg.log[i,], main = rownames[i])
    },error =function(e){cat("ERROR: ", conditionMessage(e), "\n")})
    
    
  }

setwd(mainDir)

