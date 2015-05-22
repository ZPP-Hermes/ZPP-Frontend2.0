import pyRserve
import Rscripts
from models import Mark
import numpy as np

def prepData():
    dataPr = Mark.objects.all()
    dataPr = dataPr.values_list()
    colNum = len(dataPr[1])
    dataList = []
    for i in range(colNum):
        dataList += [id[i] for id in dataPr]
    dataR = np.array(dataList)
    dataR.shape = (colNum, len(dataList) / colNum)
    dataR = np.transpose(dataR)
    dataR = dataR.astype(int)
    return dataR

conn = pyRserve.connect()
conn.r.data1 = prepData()
conn.r(Rscripts.Rscript.dataGen)
conn.r(Rscripts.Rscript.arules)
conn.r(Rscripts.Rscript.easiestWay)
conn.r(Rscripts.Rscript.knn)
conn.r(Rscripts.Rscript.random)
#tu bedziemy chcieli wczytywac dane z bazy
#conn.r.data = prepData()

#funkcja bioraca dane z bazy i przerabiajaca na macierz do R, ja jeszcze trzeba przerobic

#strategie predykcyjne
def getRecomSubStrategy1(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('getRecomSub(which(gotMarks>0),0.5)')
    recom = [int(x+30) for x in recommendSubjects]
    return recom

def getRecomSubStrategy2(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('recomEasySub(gotMarks)')
    recom = [int(x+30) for x in recommendSubjects]
    return recom

def getRecomSubStrategy3(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('random(gotMarks)')
    recom = [int(x+30) for x in recommendSubjects]
    return recom

def getRecomSubStrategy4(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('recomNearestSub(5,gotMarks)')
    recom = [int(x+30) for x in recommendSubjects]
    return recom

