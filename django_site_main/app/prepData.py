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