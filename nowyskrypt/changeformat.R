dir <- paste(getwd(), "/dane.csv", sep="")
data1 <- read.csv(dir, sep=",")
data1 <- data.matrix(data1)
data2=data1[data1[,2]<51,1:3]
data3=data1[data1[,2]>50,1:2]
matrix1= matrix(unlist(list(rep(0,51*max(data1[,1])))),ncol=51,byrow=TRUE)
for(i in 1:nrow(data2)){
	matrix1[data2[i,1],data2[i,2]] = data2[i,3]
}
for(i in 1:nrow(data3)){
	matrix1[data3[i,1],51] = data3[i,2]-50
}
