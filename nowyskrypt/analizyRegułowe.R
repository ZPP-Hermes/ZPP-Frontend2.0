#skrypt implementujący funkcje wyboru przedmiotów obieralnych dla studenta na podstawie reguł asocjacyjnych (koszyki 
#stanowią wybierane przedmioty obieralne dla studentów) oraz wyboru dla niego odpowiedniej grupy 
# na podstawie danych studenta pobieranych z pliku .csv. W przyszłości mozna wykorzystać wiadomości o grupie do analiz

# format funkcji: getRecomSub(v, pr), gdzie
# v <- (wektor ocen z przedmiotów obieralnych studenta (0 gdy nie brał udziału))
# pr <- procent przedmiotów, który ma dopasować się do studenta, domyślnie 50%
# funkcja zwraca wektor przedmiotów proponowanych dla studenta

# getCluster(v,agg), gdzie
# v <- wektor ocen ze wszystich przedmiotów studenta
# agg <- macierz zawierająca średnie oceny dla każdej grupy, domyslnie wytrenowana ze wszystkich przedmiotów
# funkcja zwraca jedną liczbę, numer klastra dla danego studenta

#dane należy umieścić w katalogu roboczym dla R, można go zobaczyć poprzez wywołanie funkcji getwd()
dir <- paste(getwd(), "/ZPP_dane.csv", sep="")
data <- read.csv(dir, sep=",")
trainingIdx = sample(1:nrow(data), round(3*(nrow(data)/5)))
obow <- as.matrix(data[,1:30])
obier <- as.matrix(data[,31:50])
sem <- as.matrix(data[,51])

#-----------reguły dla przedmiotów obieralnych---------------------

#tworzenie koszyków przedmiotów obieralnych
install.package('arules')
library(arules)

colnames(obier) <- NULL
rows <- dim(obier)[1]
l <- list()
for (i in 1:rows)
{
  l[[i]] <- which(obier[i,]>0)
}
koszykObier <- as(l, "transactions")

#szukanie reguł dla przedmiotów obieralnych, postaci jeśli ktoś co wziął to prawdopodobnie wziął również to
bestObier = sort(itemFrequency(koszykObier)[which(itemFrequency(koszykObier) >= sort(itemFrequency(koszykObier), decreasing = T)[5])], decreasing = TRUE)

ruleObier = apriori(koszykObier, parameter = list(supp = 0.0002, conf = 0.8, minlen = 2,
                    target = "rules", originalSupport = FALSE), appearance = NULL, control = list(sort = -1))

ruleObier = sort(ruleObier, decreasing = T, by = "lift")
rules = subset(ruleObier, lhs %in% paste(2))

#możemy sobie zobaczyć nasze reguły

inspect(ruleObier[1:10])

#mozemy zobaczyc co nasze reguły zaproponują jakiemuś studentowi z danych reguł
student <- which(obier[1,]>0)
pr <- 1/8

#funkcja zwracająca wektor proponowanych przedmiotów dla danego studenta
#pobiera wektor wybranych przedmiotów obieralnych oraz procent przedmiotów branych pod uwagę

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
}

getRecomSub <- function(student) {
  Idx = sample(1:length(student), round((1/2)*length(student)))
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
}
getRecomSub(student, pr)


#----------popatrzmy teraz na grupy występujące w danych

data <- as.matrix(data)
dataD <- data[,-51]
dec <- data[,51]
#dobieramy najlepszą liczbę klastrów patrząc na błąd średniokwadratowy

wss <- (nrow(obow)-1)*sum(apply(obow,2,var))
for (i in 2:10) wss[i] <- sum(kmeans(obow, 
                                     centers=i)$withinss)
plot(1:10, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")

# bierzemy pod uwagę tylko obowiązkowe

fitObow <- kmeans(obow, 7) # 7 klastrów
# patrzymy na średnie w klastrach
aggObow <- aggregate(obow,by=list(fitObow$cluster),FUN=mean)
# dodajmy dla każdego studenta gdzie był
dataObow <- data.frame(dataD, fitObow$cluster)

#popatrzmy co się stanie gdy wybierzemy wszystkie przedmioty

wss <- (nrow(dataD)-1)*sum(apply(dataD,2,var))
for (i in 2:10) wss[i] <- sum(kmeans(dataD, 
                                     centers=i)$withinss)
plot(1:10, wss, type="b", xlab="Number of Clusters",
     ylab="Within groups sum of squares")

fitAll <- kmeans(dataD, 5) # 5 klastrów
# patrzymy na średnie w klastrach
aggAll <- aggregate(dataD,by=list(fitAll$cluster),FUN=mean)
# dodajmy dla każdego studenta gdzie był
dataAll <- data.frame(dataD, fitAll$cluster)

# możemy teraz patrzeć do której grupy należy student poprzez najmniejszy błąd średniokwadratowy na wartościach

student <- dataD[4,]
# na wejsciu oceny studenta oraz średnie na klastrach, domyślnie aggAll
getCluster <- function(student, agg)
{
  n <- dim(agg)[1]
  cl <- 1
  min <- 100000000000
  for (i in 1:n)
  {
    mse <- sum((student-agg[i,])^2)
    #print(mse)
    if (mse < min)
    {
      cl <- i
      min <- mse
    }
  }
  return(cl)
}

getCluster <- function(student)
{
  n <- dim(aggAll)[1]
  cl <- 1
  min <- 100000000000
  for (i in 1:n)
  {
    mse <- sum((student-aggAll[i,])^2)
    #print(mse)
    if (mse < min)
    {
      cl <- i
      min <- mse
    }
  }
  return(cl)
}

#możemy dalej wnioskować różne rzeczy na podstawie przydziały do grupy, np wybór patrzeć do jakiej grupy należy student 
#i co wybierali studenci podobni do niego
