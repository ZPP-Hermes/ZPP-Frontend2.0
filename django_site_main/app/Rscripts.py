# w tej klasie bedziemy przechowywac skrypty R-owe dla aplikacji
import os
cwd = os.getcwd()

class Rscript():
    arules = '''library(arules)
    obow <- as.matrix(data[,1:30])
    obier <- as.matrix(data[,31:50])
    sem <- as.matrix(data[,51])
    colnames(obier) <- NULL
    rows <- dim(obier)[1]
    l <- list()
    for (i in 1:rows)
    {
      l[[i]] <- which(obier[i,]>0)
    }
    koszykObier <- as(l, "transactions")

    #szukanie regul dla przedmiotow obieralnych, postaci jesli ktos co wzial to prawdopodobnie wzial rowniez to
    #bestObier = sort(itemFrequency(koszykObier)[which(itemFrequency(koszykObier) >= sort(itemFrequency(koszykObier), decreasing = T)[5])], decreasing = TRUE)

    ruleObier = apriori(koszykObier, parameter = list(supp = 0.001, conf = 0.9, minlen = 2,
                                                      target = "rules", originalSupport = FALSE), appearance = NULL, control = list(sort = -1))

    ruleObier = sort(ruleObier, decreasing = T, by = "lift")


    #funkcja zwracajaca wektor proponowanych przedmiotow dla danego studenta
    #pobiera wektor wybranych przedmiotow obieralnych oraz procent przedmiotow branych pod uwage

    getRecomSub <- function(student, pr) {
      Idx = sample(1:length(student), round(pr*length(student)))
      student <- unlist(student[Idx])
      n <- length(student)
      rules <- ruleObier
      if (n > 0)
      {
        for (i in 1:n)
        {
          rules = subset(rules, lhs %in% paste(student[i]))
        }
        if (length(rules) > 0) {
          subMatr <- as(rhs(rules), "matrix")
          m <- dim(subMatr)[1]
          recomSub <- vector()
          for (i in 1:m)
          {
            recomSub <- c(recomSub, which(subMatr[i,]>0))
          }
          recomSub <- sort(unique(recomSub))
          studNotChosen <- c(1:20)[-student]
          recomSub <- recomSub[recomSub %in% studNotChosen]
        }
        else {
          recomSub = c()
        }
      }
      else {
        recomSub = c()
      }
      return(as.list(recomSub))
    }'''

    easiestWay = '''recomEasySub <- function(student) {
      getSupport <- function(row) {length(subset(data, data[,row] != 0)[,row])}
      getMean <- function(row) {mean(subset(data, data[,row] != 0)[,row])}
      studCount <- dim(data)[1]
      supp <- unlist(lapply(31:50,getSupport))/studCount
      mean <- (unlist(lapply(31:50,getMean))-4)/7
      easyRate <- 1/3*supp + 2/3*mean
      A <- matrix(c(easyRate,1:20),20,2)
      A <- A[order(A[,1], decreasing=TRUE),]
      studNotChosen <- which(student == 0)
      recom <- A[A[,2] %in% studNotChosen,2]
      return(as.list(recom))
    }'''
    knn='''dist <- function(v,w) {
      sum <- 0
      for (i in 1:length(v)) {
        if (xor((v[i] == 0),w[i] == 0)) {
          sum <- sum + 10
        }
        else {
          sum <- sum + abs(v[i] - w[i])
        }
      }
      return(sum)
    }

    recomNearestSub <- function(k, student) {
      n <- dim(data)[1]
      A <- matrix(0,n,2)
      student <- unlist(student)
      A[,1] <- unlist(lapply(1:n, function(i) {dist(student,data[i,])}))
      A[,2] <- c(1:n)
      bestNb <- A[order(A[,1])[1:k],2]
      studNotChosen <- which(student == 0)
      recom <- c()
      for (i in 1:length(bestNb)) {
        nbSub <- which(data[bestNb[i],] > 0)
        recom <- c(recom, nbSub[nbSub %in% studNotChosen])
      }
      sortRecom <- sort(table(recom),decreasing=TRUE)
      len <- min(5,length(sortRecom))
      sub <- as.integer(names(sortRecom[1:len]))
      return(as.list(sub))
    }'''
    random='''random <- function(student) {
      studNotChosen <- which(student == 0)
      n <- length(studNotChosen)
      if (n == 0) {return(list())}
      if (n==1) {return(as.list(c(studNotChosen)))}
      recom <- sample(studNotChosen,prob=rep(1,n))[1:(n/2)]
      return(as.list(recom)) 
    }'''
    dataGen='''data1 <- data.matrix(data1)
    data1 <- data1[,2:4]
    data2=data1[data1[,2]<51,1:3]
    data3=data1[data1[,2]>50,1:2]
    matrix1= matrix(rep(0,51*nrow(data3)),ncol=51,byrow=TRUE)
    for(i in 1:nrow(data2)){
        matrix1[data2[i,1],data2[i,2]] = data2[i,3]
    }
    for(i in 1:nrow(data3)){
        matrix1[as.integer(data3[i,1]),51] = as.integer(data3[i,2])-50
    }
    data <- data.matrix(matrix1)'''
    semKnn = '''mode <- function(x) {
      ux <- unique(x)
      ux[which.max(tabulate(match(x, ux)))]
    }

    recomNearestSem <- function(k, student) {
      student <- unlist(student)
      n <- dim(data)[1]
      A <- matrix(0,n,2)
      for (i in 1:n) {
        A[i,1] <- dist(student,data[i,])
        A[i,2] <- i
      }
      bestNb <- A[order(A[,1])[1:k],2]
      bestSem <- data[bestNb,51]
      return(mode(bestSem))
    }'''
    semRf = '''library(randomForest)
    classifierf<-randomForest(data[,1:50], data[,51])
    predictRf <- function(student) {
      return(round(predict(classifierf, student)))
    }'''
    marksKnn='''recomNearestMarks <- function(student, subject) {
      student <- unlist(student)
      n <- dim(data)[1]
      A <- matrix(0,n,2)
      A[,1] <- unlist(lapply(1:n, function(i) {dist(student,data[i,])}))
      A[,2] <- c(1:n)
      bestNb <- A[order(A[,1])[1:100],2]
      marks <- data[bestNb,subject][data[bestNb,subject] > 0]
      if (length(marks)>0)
      {
        m <- round(mean(marks))
        if (m == 5)
            return(6)
        return(m)
      }
      else
      {
        return(sample(4:11,1,prob=c(5,3,2,1,1,1,1,1)))
      }
    }'''
    subforSemKnn = '''recomNearestSubforSem <- function(k, student, sem) {
      dataSem <- data[data[,51]==(sem-50),]
      student <- unlist(student)
      n <- dim(dataSem)[1]
      A <- matrix(0,n,2)
      A[,1] <- unlist(lapply(1:n, function(i) {dist(student,dataSem[i,])}))
      A[,2] <- c(1:n)
      bestNb <- A[order(A[,1])[1:k],2]
      studNotChosen <- which(student == 0)
      recom <- c()
      for (i in 1:length(bestNb)) {
        nbSub <- which(data[bestNb[i],] > 0)
        recom <- c(recom, nbSub[nbSub %in% studNotChosen])
      }
      sortRecom <- sort(table(recom),decreasing=TRUE)
      len <- min(5,length(sortRecom))
      sub <- as.integer(names(sortRecom[1:len]))
      return(as.list(sub))
    }'''
