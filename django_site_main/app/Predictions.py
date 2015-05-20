import pyRserve
import os

import Rscripts


conn = pyRserve.connect()
conn.r(Rscripts.Rscript.arules)
conn.r(Rscripts.Rscript.easiestWay)
# tu bedziemy chcieli wczytywac dane z bazy
#conn.r.data = prepData()

#funkcja bioraca dane z bazy i przerabiajaca na macierz do R, ja jeszcze trzeba przerobic
def prepData():
    dataPr = Mark.objects.all()
    dataPr = dataPr.values_list()
    colNum = len(dataPr[1])
    dataList = []
    for i in range(colNum):
        dataList += [id[i] for id in dataPr]
    dataR = np.array(dataList)
    dataR.shape = (colNum, len(dataList) / colNum)
    return dataR


#strategie predykcyjne
def getRecomSubStrategy1(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('getRecomSub(which(gotMarks>0),0.5)')
    recom = [x + 30 for x in recommendSubjects]
    return recom


def getRecomSubStrategy2(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('recomEasySub(gotMarks)')
    recom = [int(x + 30) for x in recommendSubjects]
    return recom

