import numpy as np
import scipy
import plotly.plotly as py
import plotly.graph_objs as go
from plotly.tools import FigureFactory as FF


import pandas as pd
import os,math,time
import statistics
import matplotlib.pyplot as plt
import csv

PRINTS = True
def retrive_result_list(result_folder,name):
    result_files = os.listdir(result_folder)
    result_files = [result_folder + j for j in result_files if j.endswith(".csv")]
    result_files.sort()

    for i in result_files:
        if "evaluation" in i:
            with open(i, 'r') as f:
                reader = csv.reader(f)
                evaluation = list(reader)
        elif "init" in i:
            with open(i, 'r') as f:
                reader = csv.reader(f)
                initData = list(reader)
        elif "log" in i:
            with open(i, 'r') as f:
                reader = csv.reader(f)
                logData = list(reader)
        elif "response" in i:
            with open(i, 'r') as f:
                reader = csv.reader(f)
                response = list(reader)
    #evaluation = [i[0].split("%s") for i in evaluation]
    temp=[]
    for i in evaluation:
       v= i[0].split(" ")
       temp.append(v)
    evaluation=temp
    if PRINTS:
        print(evaluation)
    response=[float(i[0]) for i in response]
    if PRINTS:
        print(response)
    initData =[int(i[0])for i in initData]
    if PRINTS:
        print(initData)
    temp =[]
    for j in logData:
        q=j[0].split(" ")
        temp.append([int(q[0]),int(q[1]),float(q[2]),float(q[3]),str(q[4]),str(q[5])])
    logData=temp
    if PRINTS:
        print(logData)

    for i in range(len(response)):
        evaluation[i].append(response[i])
        evaluation[i].append(name)
    for i in range(len(logData)):
        logData[i].append(name)
    if PRINTS:
        print(evaluation)

    return evaluation,logData,initData


def compile_results():
    print("\nLoading the Results Directory")
    read_results = os.listdir("Final_result_spaceInvader")
    final_result_directory = [i for i in read_results if not i.endswith(".txt")and not i.endswith(".csv")]
    for i in range(len(final_result_directory)):
        final_result_directory[i] = "Final_result_spaceInvader/" + final_result_directory[i] + "/"
    print("\nFound the following directories:")
    if PRINTS:
        print(final_result_directory)
    name=[i.split("/")for i in final_result_directory]
    name=[i[1] for i in name]
    if PRINTS:
        print(name)

    Total_evaluation = []
    Total_logData = []

    for i in range(len(final_result_directory)):
        evaluation, logData, initData= retrive_result_list(final_result_directory[i],name[i])
        for i in evaluation:
            Total_evaluation.append(i)
        for j in logData:
            Total_logData.append(j)

    #ev ["happy" , "sad", "angry"
    ev_count_ims = [0, 0, 0]
    ev_count_random = [0, 0, 0]

    # dif= ["Easy" , "Medium", "Hard"
    dif_count_ims = [0, 0, 0]
    dif_count_random = [0, 0, 0]
    for i in Total_evaluation:
        if i[2] == "Random":
            if i[0] == "happy":
                ev_count_random[0]+=1
            elif i[0]=="sad":
                ev_count_random[1]+=1
            elif i[0] == "angry":
                ev_count_random[2]+=1

            if i[1] == "Easy":
                dif_count_random[0]+=1
            elif i[1]=="Medium":
                dif_count_random[1]+=1
            elif i[1] == "Hard":
                dif_count_random[2]+=1
        elif i[2] == "IMS":
            if i[0] == "happy":
                ev_count_ims[0]+=1
            elif i[0]=="sad":
                ev_count_ims[1]+=1
            elif i[0] == "angry":
                ev_count_ims[2]+=1
            if i[1] == "Easy":
                dif_count_ims[0] += 1
            elif i[1] == "Medium":
                dif_count_ims[1] += 1
            elif i[1] == "Hard":
                dif_count_ims[2] += 1

    IMS_sub= [i[3] for i in Total_evaluation if i[2] == "IMS"]
    Random_sub = [i[3] for i in Total_evaluation if i[2] == "Random"]


    if PRINTS:
        print(ev_count_ims,ev_count_random)
        print(dif_count_ims, dif_count_random)

    save_count(open("Counted_results.txt","w"),a=dif_count_ims,b=dif_count_random,
               c=ev_count_ims,d=ev_count_random,
               meanIms=statistics.mean(IMS_sub),meanRandom=statistics.mean(Random_sub))

    return Total_evaluation, Total_logData



def save_count(File,a,b,c,d, meanIms,meanRandom):
    File.write("In IMS:\n")
    total=a[0]+a[1]+a[2]
    File.write("Total Easy: "+str(a[0])+ " That is "+"{0:.2f}".format((a[0]/total)*100)+"%"'\n')
    File.write("Total Medium: " + str(a[1]) + " That is " + "{0:.2f}".format((a[1] / total) * 100) + "%"'\n')
    File.write("Total Hard: " + str(a[2]) + " That is " + "{0:.2f}".format((a[2] / total) * 100) + "%"'\n\n')

    total = c[0] + c[1] + c[2]
    File.write("Total Happy: " + str(c[0]) + " That is " + "{0:.2f}".format((c[0] / total) * 100) + "%"'\n')
    File.write("Total Sad: " + str(c[1]) + " That is " + "{0:.2f}".format((c[1] / total) * 100) + "%"'\n')
    File.write("Total Angry: " + str(c[2]) + " That is " + "{0:.2f}".format((c[2] / total) * 100) + "%"'\n\n')

    File.write("Average Response Time: "+"{0:.2f}".format(meanIms)+"\n\n")

    File.write("In Random:\n")
    total = b[0] + b[1] + b[2]
    File.write("Total Easy: " + str(b[0]) + " That is " + "{0:.2f}".format((b[0] / total) * 100) + "%"'\n')
    File.write("Total Medium: " + str(b[1]) + " That is " + "{0:.2f}".format((b[1] / total) * 100) + "%"'\n')
    File.write("Total Hard: " + str(b[2]) + " That is " + "{0:.2f}".format((b[2] / total) * 100) + "%"'\n\n')

    total = d[0] + d[1] + d[2]
    File.write("Total Happy: " + str(d[0]) + " That is " + "{0:.2f}".format((d[0] / total) * 100) + "%"'\n')
    File.write("Total Sad: " + str(d[0]) + " That is " + "{0:.2f}".format((d[1] / total) * 100) + "%"'\n')
    File.write("Total Angry: " + str(d[2]) + " That is " + "{0:.2f}".format((d[2] / total) * 100) + "%"'\n\n')

    File.write("Average Response Time: "+"{0:.2f}".format(meanRandom)+"\n\n")




evaluation,logdata=compile_results()
np.savetxt('total_evaluation_List.csv', evaluation, fmt='%s')
np.savetxt('total_log_List.csv', logdata, fmt='%s')

