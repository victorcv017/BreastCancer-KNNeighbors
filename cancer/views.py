from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.staticfiles.storage import staticfiles_storage
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import preprocessing, neighbors
import pandas as pd


def index(request):
    predict = 0
    data = 0
    proba = np.array([100, 0])
    send = False
    patient = ""
    dataset = staticfiles_storage.path('cancer/dataset/breast-cancer-wisconsin.data.txt')
    df = pd.read_csv(dataset, header = None)
    df.columns = ["name" , "V1" , "V2" , "V3", "V4" , "V5" , "V6" , "V7" , "V8" , "V9" , "class"]
    df= df.drop(["name"],1)
    df.replace("?", -99999, inplace=True)
    Y = df["class"]
    X = df[[ "V1" , "V2" , "V3", "V4" , "V5" , "V6" , "V7" , "V8" , "V9"]]
    X_train , X_test , Y_train , Y_test = train_test_split(X,Y , test_size = 0.2)
    m = df[["V1", "V7","class"]]
    clf = neighbors.KNeighborsClassifier()
    clf.fit(X_train, Y_train)
    accuracy = clf.score(X_test, Y_test)
    if request.method == 'POST':
        data = request.POST
        sample_measure = np.array(
        [
        data["V1"], 
        data["V2"],
        data["V3"],
        data["V4"],
        data["V5"],
        data["V6"], 
        data["V7"],
        data["V8"], 
        data["V9"]
        ])
        sample_measure = sample_measure.reshape(1,-1)
        predict = clf.predict(sample_measure)
        proba = clf.predict_proba(sample_measure)
        proba = proba[0]
        patient = data['name']
        send = True

    return render(request, 'cancer/index.html' ,{ 
        'accuracy' : accuracy * 100,
        'predict' : predict,
        'data' : data,
        'dif' : 100.0 - accuracy * 100,
        'benigno' : proba[0] * 100,
        'maligno' : proba[1] * 100,
        'send' : send,
        'patient' : patient,
        'coordb': m[m["class"] == 2],
        "coordm" : m[m["class"] == 4],
        })

def explanation(request):
    return render(request, 'cancer/explanation.html')