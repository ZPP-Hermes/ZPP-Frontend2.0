# w tej klasie bedziemy przechowywac skrypty R-owe dla aplikacji
class Rscript():
    #robocze pobieranie danych z csv, na zmienną dir2 nalezy pobrac sciezke do danych
    arules = '''dir2 <- "~/ZPP/ZPP-SSDT/nowyskrypt/ZPP_dane.csv"
    dir <- paste(getwd(), "/ZPP_dane.csv", sep="")
    data <- read.csv(dir, sep=",")
    trainingIdx = sample(1:nrow(data), round(3*(nrow(data)/5)))
    obow <- as.matrix(data[,1:30])
    obier <- as.matrix(data[,31:50])
    sem <- as.matrix(data[,51])

    #-----------reguly dla przedmiotow obieralnych---------------------

    #tworzenie koszykow przedmiotow obieralnych
    install.packages('arules')
    library(arules)

    colnames(obier) <- NULL
    rows <- dim(obier)[1]
    l <- list()
    for (i in 1:rows)
    {
      l[[i]] <- which(obier[i,]>0)
    }
    koszykObier <- as(l, "transactions")

    #szukanie regul dla przedmiotow obieralnych, postaci jesli ktos co wzial to prawdopodobnie wzial rowniez to
    bestObier = sort(itemFrequency(koszykObier)[which(itemFrequency(koszykObier) >= sort(itemFrequency(koszykObier), decreasing = T)[5])], decreasing = TRUE)

    ruleObier = apriori(koszykObier, parameter = list(supp = 0.0002, conf = 0.8, minlen = 2,
                        target = "rules", originalSupport = FALSE), appearance = NULL, control = list(sort = -1))

    ruleObier = sort(ruleObier, decreasing = T, by = "lift")
    rules = subset(ruleObier, lhs %in% paste(2))

    #mozemy sobie zobaczyc nasze reguly

    inspect(ruleObier[1:10])

    #mozemy zobaczyc co nasze reguly zaproponuja jakiemus studentowi z danych regul
    student <- which(obier[1,]>0)
    pr <- 1/8

    #funkcja zwracajaca wektor proponowanych przedmiotow dla danego studenta
    #pobiera wektor wybranych przedmiotow obieralnych oraz procent przedmiotow branych pod uwage

    getRecomSub <- function(student, pr) {
      Idx = sample(1:length(student), round(pr*length(student)))
      student <- student[Idx]
      n <- length(student)
      rules <- ruleObier
      for (i in 1:n)
      {
        rules = subset(rules, lhs %in% paste(student[i]))
      }
      subMatr <- as(rhs(rules), "matrix")
      m <- dim(subMatr)[1]
      recomSub <- vector()
      for (i in 1:m)
      {
        recomSub <- c(recomSub, which(subMatr[i,]>0))
      }
      recomSub <- unique(recomSub)
      return(recomSub)
    }'''
