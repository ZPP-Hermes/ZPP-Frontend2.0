import pyRserve
import os

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
conn.r(Rscripts.Rscript.semKnn)
conn.r(Rscripts.Rscript.semRf)
conn.r(Rscripts.Rscript.marksKnn)

#strategie predykcyjne
def getRecomSubStrategy1(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('getRecomSub(which(gotMarks>0),1)')
    recom = map(lambda x:int(x)+30, recommendSubjects)
    return recom


def getRecomSubStrategy2(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('recomEasySub(gotMarks)')
    recom = map(lambda x:int(x)+30, recommendSubjects)
    return recom

def getRecomSubStrategy3(marks):
    conn.r.gotMarks = marks[30:50]
    recommendSubjects = conn.r('random(gotMarks)')
    recom = map(lambda x:int(x)+30, recommendSubjects)
    return recom

def getRecomSubStrategy4(marks):
    conn.r.gotMarks = marks
    recommendSubjects = conn.r('recomNearestSub(5,gotMarks)')
    recom = map(int, recommendSubjects)
    return recom

def getRecomSemStrategy1(marks):
    conn.r.gotMarks = marks
    recomSem = conn.r('predictRf(gotMarks)')
    return int(recomSem)+50

def getRecomSemStrategy2(marks):
    conn.r.gotMarks = marks
    recomSem = conn.r('recomNearestSem(10,gotMarks)')
    return int(recomSem)+50

def predictMark(marks, subject):
    conn.r.gotMarks = marks
    conn.r.subject = subject
    predictMark = conn.r('recomNearestMarks(gotMarks, subject)')
    return int(predictMark)
