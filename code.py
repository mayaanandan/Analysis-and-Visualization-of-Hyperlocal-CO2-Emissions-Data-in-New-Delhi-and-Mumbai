from urllib.request import urlopen
import json
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from pywebio.input import input_group,input,radio,select
import matplotlib.pyplot as plt

def loop1():
    data = input_group("Air checker",[
    select("Select a parameter",['PM1','PM25','PM10','CO2','NO2','OZONE'], name ="param"),
    radio("Select a city",options=['Delhi','Mumbai'], name ="city"),
    select("Select a month",['01','02','03','04','05','06','07','08','09','10','11','12'], name ="month"),
    input("Enter start date (dd): ", name ="lower_d"),
    input("Enter end date (dd): ", name ="upper_d"),
    input("Enter start hour (hh): ", name ="lower_t"),
    input("Enter end hour (hh): ", name ="upper_t")])
    param = data['param']
    city = data['city']
    month = data['month']
    lower_d = data['lower_d']
    upper_d = data['upper_d']
    lower_t = data['lower_t']
    upper_t = data['upper_t']
    if city=="Delhi":
        each = "delhi"
    if city=="Mumbai":
        each = "mumbai"
    mapp = {}
    mapper = open("mapping.txt","r")
    maplines = mapper.readlines()
    mapper.close()
    for mlines in maplines:
        mlines = mlines.strip()
        mlines = mlines.split(":")
        mm1 = mlines[0]
        mm2 = mlines[1]
        mapp[mm1] = mm2
    tempfile = open("temp.csv","w")
    tempfile.write("ID,PM1,PM25,PM10,CO2,NO2,OZONE,Freq,District\n")
    temp2 = open(each+"_blank.csv","r")
    tlines = temp2.readlines()
    for tline in tlines[1:]:
        tempfile.write(tline)
    tempfile.write("\n")
    temp2.close()
    sensordict = {}
    for date in range(int(lower_d),int(upper_d)+1):
        for hour in range(int(lower_t),int(upper_t)+1):
            if len(str(date))!=2:
                date = "0"+str(date)
            if len(str(hour)) !=2:
                hour = "0"+str(hour)
            try:
                file = open("cities/"+each+"/months/"+str(month)+"/"+str(date)+"/"+str(hour)+"/"+"data.csv","r")
                lines = file.readlines()
                file.close()
                for line in lines:
                    line = line.strip()
                    line = line.split(",")
                    sensorID = line[-4]
                    try:
                        tup = sensordict[sensorID]
                        temptup = list(tup)
                        freq = temptup[-1]
                        freq +=1
                        templist = line[3:9]
                        for i in range (len(temptup)-1):
                            templist[i] = ((float(templist[i])*float(freq))+float(temptup[i]))/float(freq)
                        templist.append(freq)
                        sensordict[sensorID] = tuple(templist)
                    except:
                        tempval = tuple(line[3:9]+[1])
                        sensordict[sensorID] = tempval
            except:pass
    for key in sensordict:
        a = str(sensordict[key])
        a = a.replace("(","")
        a = a.replace(")","")
        key =str(int(float(key)))
        tempfile.write(str(mapp[key])+","+a+","+key+"\n")
    tempfile.close()
    if param =='PM1':
        rangenum = 50
    if param =='PM25':
        rangenum = 50
    if param =='PM10':
        rangenum = 500
    if param =='CO2':
        rangenum = 1000
    if param =='NO2':
        rangenum = 25
    if param =='OZONE':
        rangenum = 50
    with open('India_AC.json','r') as response:
        counties = json.load(response)
        df = pd.read_csv("temp.csv",dtype={"ID": str})
    fig = px.choropleth(df, geojson=counties, locations='ID', color=param,color_continuous_scale="Reds",range_color=(0,rangenum),scope="asia",
                               labels={'PM1':'PM1','PM25':'PM25','PM10':'PM10','CO2':'CO2','NO2':'NO2','OZONE':'OZONE','District':"District"},
                               hover_data=['PM1','PM25','PM10','CO2','NO2','OZONE'])
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_geos(fitbounds="locations", visible=False, resolution=110, showsubunits=True, subunitcolor="Black")
    fig.show()
    loop()

def loop2():

    senslist = ['862549045591784','862549045591669','862549045501346','862549045554568','862549045496307','862549045589630','862549045592279','862549045591503','862549045497982','862549045592543','862549045592600','862549045589598','862549045589796','862549045501650','862549045480913','862549045592014','862549045552778','862549045554592','862549045480012','862549045484980','862549045589895','862549045480574','862549045589648','862549045591776','862549045552455','862549045500868','862549045589846','862549045591545','862549045501122','862549045554618','862549045591529','862549045589440','862549045501643','862549045589119','862549045589606','862549045591800','862549045495598','862549045589838','862549045589499','862549045592196','862549045480756','862549045481903','862549045479071','862549045589861','862549045589135','862549045589812','862549045500934',]
    senslistt = []
    mappp = {'862549045495598': 'Khar West', '862549045480913': 'Korakendra', '862549045589838': 'Bandra West', '862549045481903': 'Matunga', '862549045592014': ' king circle', '862549045552778': 'Marine Drive', '862549045554592': 'Bhandup', '862549045480012': 'Girgaon', '862549045484980': 'Mira Road', '862549045589499': 'Khar West', '862549045589895': 'Goregaon West ', '862549045480574': 'Nepeansea Road ', '862549045589648': 'Mulund East ', '862549045591776': 'Trombay', '862549045589861': 'Pali Hill', '862549045592196': 'GokulDham', '862549045552455': 'Sher e Punjab', '862549045480756': 'Thakur Complex', '862549045500868': 'Kalina', '862549045589846': ' Bandra (East)', '862549045591545': 'JUHU', '862549045479071': ' Chembur', '862549045501122': 'Vile Parle(E)', '862549045554618': 'Worli', '862549045591529': ' Powai ', '862549045589440': 'Mahavir nagar', '862549045501643': 'Mumbai Central', '862549045589119': 'Mulund West ', '862549045589606': 'Dahisar', '862549045589135': 'Shivaji Park', '862549045589812': 'Versova ', '862549045591800': 'Ghatcoper East', '862549045591784': 'Kalkaji', '862549045591669': 'Malvia Nagar'}
    mapppp = {}
    for each in mappp:
        val = mappp[each]
        senslistt.append(val)
        mapppp[val] = each

    data = input_group("Air checker",[
    select("Select a parameter",['PM1','PM25','PM10','CO2','NO2','OZONE'], name ="param"),
    radio("Select a city",options=['Delhi','Mumbai'], name ="city"),
    select("Select a sensor ID",senslistt, name ="ID"),
    select("Select a month",['01','02','03','04','05','06','07','08','09','10','11','12'], name ="month"),
    input("Enter start date (dd): ", name ="lower_d"),
    input("Enter end date (dd): ", name ="upper_d"),
    input("Enter start hour (hh): ", name ="lower_t"),
    input("Enter end hour (hh): ", name ="upper_t"),
    radio("Select visualisation type",options=['Daily','Hourly'], name ="typee"),])
    param = data['param']
    if param=="PM1":
        paramm = "1"
    if param=="PM25":
        paramm = "2"
    if param=="PM10":
        paramm = "3"
    if param=="CO2":
        paramm = "4"
    if param=="NO2":
        paramm = "5"
    if param=="OZONE":
        paramm = "6"
    city = data['city']
    month = data['month']
    lower_d = data['lower_d']
    upper_d = data['upper_d']
    lower_t = data['lower_t']
    upper_t = data['upper_t']
    typee = data['typee']
    ID = data['ID']
    ID = mapppp[ID]
    if city=="Delhi":
        each = "delhi"
    if city=="Mumbai":
        each = "mumbai"
    mapp = {}
    mapper = open("mapping.txt","r")
    maplines = mapper.readlines()
    mapper.close()
    for mlines in maplines:
        mlines = mlines.strip()
        mlines = mlines.split(":")
        mm1 = mlines[0]
        mm2 = mlines[1]
        mapp[mm1] = mm2

    tempfile = open("temp.csv","w")
    tempfile.write("ID,PM1,PM25,PM10,CO2,NO2,OZONE,Freq,District,DATE,HOUR\n")

    for date in range(int(lower_d),int(upper_d)+1):
        sensordict = {}
        for hour in range(int(lower_t),int(upper_t)+1):

            if typee=="Hourly":
                sensordict = {}
        
            if len(str(date))!=2:
                date = "0"+str(date)
            if len(str(hour)) !=2:
                hour = "0"+str(hour)
            try:
                file = open("cities/"+each+"/months/"+str(month)+"/"+str(date)+"/"+str(hour)+"/"+"data.csv","r")
                lines = file.readlines()
                file.close()
                for line in lines:
                    line = line.strip()
                    line = line.split(",")
                    sensorID = line[-4]
                    try:
                        tup = sensordict[sensorID]
                        temptup = list(tup)
                        freq = temptup[-1]
                        freq +=1
                        templist = line[3:9]
                        for i in range (len(temptup)-1):
                            templist[i] = ((float(templist[i])*float(freq))+float(temptup[i]))/float(freq)
                        templist.append(freq)
                        sensordict[sensorID] = tuple(templist)
                    except:
                        tempval = tuple(line[3:9]+[1])
                        sensordict[sensorID] = tempval
            except:pass
            if typee=="Hourly":
                for key in sensordict:
                    a = str(sensordict[key])
                    a = a.replace("(","")
                    a = a.replace(")","")
                    key =str(int(float(key)))
                    if str(key) == ID:
                        tempfile.write(str(mapp[key])+","+a+","+key+","+str(date)+","+str(hour)+"\n")
        if typee=="Daily":
            for key in sensordict:
                a = str(sensordict[key])
                a = a.replace("(","")
                a = a.replace(")","")
                key =str(int(float(key)))
                if str(key) == ID:
                    tempfile.write(str(mapp[key])+","+a+","+key+","+str(date)+","+str(hour)+"\n")
    tempfile.close()
    tempfile1 = open("temp.csv","r")
    ftempread = tempfile1.read()
    ftempread = ftempread.replace("'","")
    tempfile1.close()
    tempfile1 = open("temp.csv","w")
    tempfile1.write(ftempread)
    tempfile1.close()

    dataa = pd.read_csv('temp.csv')

    df = pd.DataFrame(dataa)

    #create bar graph
    if typee=="Daily":
        X = list(df.iloc[:, -2])
        xx = "Dates"
    if typee=="Hourly":
        X = list(df.iloc[:, -1])
        xx = "Hours"
    Y = list(df.iloc[:, int(paramm)])
      
    # Plot the data using bar() method
    plt.bar(X, Y, color='r')
    plt.title("Air Quality")
    plt.xlabel(xx)
    plt.ylabel(param)
      
    plt.show()
    loop()

def loop4():

    ids = ['862549045591784','862549045591669','862549045501346','862549045554568','862549045496307','862549045589630','862549045592279','862549045591503','862549045497982','862549045592543','862549045592600','862549045589598','862549045589796','862549045501650','862549045480913','862549045592014','862549045552778','862549045554592','862549045480012','862549045484980','862549045589895','862549045480574','862549045589648','862549045591776','862549045552455','862549045500868','862549045589846','862549045591545','862549045501122','862549045554618','862549045591529','862549045589440','862549045501643','862549045589119','862549045589606','862549045591800','862549045495598','862549045589838','862549045589499','862549045592196','862549045480756','862549045481903','862549045479071','862549045589861','862549045589135','862549045589812','862549045500934']
    mappp = {'862549045495598': 'Khar West', '862549045480913': 'Korakendra', '862549045589838': 'Bandra West', '862549045481903': 'Matunga', '862549045592014': ' king circle', '862549045552778': 'Marine Drive', '862549045554592': 'Bhandup', '862549045480012': 'Girgaon', '862549045484980': 'Mira Road', '862549045589499': 'Khar West', '862549045589895': 'Goregaon West ', '862549045480574': 'Nepeansea Road ', '862549045589648': 'Mulund East ', '862549045591776': 'Trombay', '862549045589861': 'Pali Hill', '862549045592196': 'GokulDham', '862549045552455': 'Sher e Punjab', '862549045480756': 'Thakur Complex', '862549045500868': 'Kalina', '862549045589846': ' Bandra (East)', '862549045591545': 'JUHU', '862549045479071': ' Chembur', '862549045501122': 'Vile Parle(E)', '862549045554618': 'Worli', '862549045591529': ' Powai ', '862549045589440': 'Mahavir nagar', '862549045501643': 'Mumbai Central', '862549045589119': 'Mulund West ', '862549045589606': 'Dahisar', '862549045589135': 'Shivaji Park', '862549045589812': 'Versova ', '862549045591800': 'Ghatcoper East', '862549045591784': 'Kalkaji', '862549045591669': 'Malvia Nagar'}
    data = input_group("Air checker",[
    select("Select a parameter",['PM1','PM25','PM10','CO2','NO2','OZONE'], name ="param"),
    radio("Select a city",options=['Delhi','Mumbai'], name ="city"),
    select("Select a month",['01','02','03','04','05','06','07','08','09','10','11','12'], name ="month"),
    input("Enter start date (dd): ", name ="lower_d"),
    input("Enter end date (dd): ", name ="upper_d"),
    input("Enter start hour (hh): ", name ="lower_t"),
    input("Enter end hour (hh): ", name ="upper_t"),
    select("Select top-k",['Top 10','Top 5','Top 3','Bottom 3','Bottom 5','Bottom 10'], name ="topk")])
    param = data['param']
    if param=="PM1":
        paramm = "1"
    if param=="PM25":
        paramm = "2"
    if param=="PM10":
        paramm = "3"
    if param=="CO2":
        paramm = "4"
    if param=="NO2":
        paramm = "5"
    if param=="OZONE":
        paramm = "6"
    city = data['city']
    month = data['month']
    lower_d = data['lower_d']
    upper_d = data['upper_d']
    lower_t = data['lower_t']
    upper_t = data['upper_t']

    if data['topk'] == "Top 10":
        topkk = -10
    if data['topk'] == "Top 5":
        topkk = -5
    if data['topk'] == "Top 3":
        topkk = -3
    if data['topk'] == "Bottom 3":
        topkk = 3
    if data['topk'] == "Bottom 5":
        topkk = 5
    if data['topk'] == "Bottom 10":
        topkk = 10

    if city=="Delhi":
        each = "delhi"
    if city=="Mumbai":
        each = "mumbai"
    mapp = {}
    mapper = open("mapping.txt","r")
    maplines = mapper.readlines()
    mapper.close()
    for mlines in maplines:
        mlines = mlines.strip()
        mlines = mlines.split(":")
        mm1 = mlines[0]
        mm2 = mlines[1]
        mapp[mm1] = mm2

    tempfile = open("temp.csv","w")
    tempfile.write("ID,PM1,PM25,PM10,CO2,NO2,OZONE,Freq,District,DATE,HOUR\n")
    temp2 = open(each+"_blank.csv","r")
    tlines = temp2.readlines()
    mappp['862549045589846'] = 'Bandra (East)'
    mapp['862549045589861']= '2832'
    mappp['862549045589861']= 'Pali Hill'
    for tpline in tlines:
        tpline = tpline.strip()
        tpline = tpline.split(",")
        numid = tpline[0]
        strid = tpline[-1]
        mappp[numid] = strid
    temp2.close()
    sensordict = {}
    for date in range(int(lower_d),int(upper_d)+1):
        for hour in range(int(lower_t),int(upper_t)+1):
            if len(str(date))!=2:
                date = "0"+str(date)
            if len(str(hour)) !=2:
                hour = "0"+str(hour)
            try:
                file = open("cities/"+each+"/months/"+str(month)+"/"+str(date)+"/"+str(hour)+"/"+"data.csv","r")
                lines = file.readlines()
                file.close()
                for line in lines:
                    line = line.strip()
                    line = line.split(",")
                    sensorID = line[-4]
                    try:
                        tup = sensordict[sensorID]
                        mappp[sensorID] = line[-2]
                        temptup = list(tup)
                        freq = temptup[-1]
                        freq +=1
                        templist = line[3:9]
                        for i in range (len(temptup)-1):
                            templist[i] = ((float(templist[i])*float(freq))+float(temptup[i]))/float(freq)
                        templist.append(freq)
                        sensordict[sensorID] = tuple(templist)
                    except:
                        tempval = tuple(line[3:9]+[1])
                        sensordict[sensorID] = tempval
            except:pass
    for key in sensordict:
        a = str(sensordict[key])
        a = a.replace("(","")
        a = a.replace(")","")
        key =str(int(float(key)))
        tempfile.write(str(mapp[key])+","+a+","+key+","+str(date)+","+str(hour)+","+str(mappp[key])+"\n")
    tempfile.close()
    tempfile1 = open("temp.csv","r")
    ftempread = tempfile1.read()
    ftempread = ftempread.replace("'","")
    tempfile1.close()
    tempfile1 = open("temp.csv","w")
    tempfile1.write(ftempread)
    tempfile1.close()

    tempdict = {}
    tfile1 = open("temp.csv","r")
    ftempread = tfile1.readlines()
    for tline in ftempread[1:]:
        tline = tline.strip()
        tline = tline.replace(" ","")
        tline = tline.split(",")
        idd = tline[-1]
        paramm = int(paramm)
        val = float(tline[paramm])
        tempdict[idd]=val

    top20 = sorted(tempdict.items(), key=lambda x: x[1])
    if topkk < 0:
        top20 = top20[topkk:]
    if topkk > 0:
        top20 = top20[0:topkk]
    plt.bar(range(len(top20)), [val[1] for val in top20], color ="r", align='center')
    plt.xticks(range(len(top20)), [val[0] for val in top20])
    plt.title("Air Quality")
    plt.xlabel("Location")
    plt.ylabel(param)
    plt.xticks(rotation=50)
    plt.tight_layout()
    plt.show()
    loop()

def loop3():
    data = input_group("Air checker",[
    select("Select a parameter",['PM1','PM25','PM10','CO2','NO2','OZONE'], name ="param"),
    radio("Select a city",options=['Delhi','Mumbai'], name ="city"),
    select("Select a month",['01','02','03','04','05','06','07','08','09','10','11','12'], name ="month"),
    input("Enter start date (dd): ", name ="lower_d"),
    input("Enter end date (dd): ", name ="upper_d"),
    input("Enter start hour (hh): ", name ="lower_t"),
    input("Enter end hour (hh): ", name ="upper_t"),
    radio("Select visualisation type",options=['Daily','Hourly'], name ="typee"),])
    param = data['param']
    if param=="PM1":
        paramm = "1"
    if param=="PM25":
        paramm = "2"
    if param=="PM10":
        paramm = "3"
    if param=="CO2":
        paramm = "4"
    if param=="NO2":
        paramm = "5"
    if param=="OZONE":
        paramm = "6"
    city = data['city']
    month = data['month']
    lower_d = data['lower_d']
    upper_d = data['upper_d']
    lower_t = data['lower_t']
    upper_t = data['upper_t']
    typee = data['typee']
    if city=="Delhi":
        each = "delhi"
    if city=="Mumbai":
        each = "mumbai"
    mapp = {}
    mapper = open("mapping.txt","r")
    maplines = mapper.readlines()
    mapper.close()
    for mlines in maplines:
        mlines = mlines.strip()
        mlines = mlines.split(":")
        mm1 = mlines[0]
        mm2 = mlines[1]
        mapp[mm1] = mm2
    tempfile = open("temp.csv","w")
    tempfile.write("ID,PM1,PM25,PM10,CO2,NO2,OZONE,Freq,District,DATE,HOUR\n")
    temp2 = open(each+"_blank.csv","r")
    tlines = temp2.readlines()
    temp2.close()
    for date in range(int(lower_d),int(upper_d)+1):
        sensordict = {}
        for hour in range(int(lower_t),int(upper_t)+1):
            if typee=="Hourly":
                sensordict = {}
            if len(str(date))!=2:
                date = "0"+str(date)
            if len(str(hour)) !=2:
                hour = "0"+str(hour)
            try:
                file = open("cities/"+each+"/months/"+str(month)+"/"+str(date)+"/"+str(hour)+"/"+"data.csv","r")
                lines = file.readlines()
                file.close()
                for line in lines:
                    line = line.strip()
                    line = line.split(",")
                    sensorID = 1234
                    try:
                        tup = sensordict[sensorID]
                        temptup = list(tup)
                        freq = temptup[-1]
                        freq +=1
                        templist = line[3:9]
                        for i in range (len(temptup)-1):
                            templist[i] = ((float(templist[i])*float(freq))+float(temptup[i]))/float(freq)
                        templist.append(freq)
                        sensordict[sensorID] = tuple(templist)
                    except:
                        tempval = tuple(line[3:9]+[1])
                        sensordict[sensorID] = tempval
            except:pass
            if typee=="Hourly":
                for key in sensordict:
                    a = str(sensordict[key])
                    a = a.replace("(","")
                    a = a.replace(")","")
                    key =str(int(float(key)))
                    tempfile.write(str(city)+","+a+","+key+","+str(date)+","+str(hour)+"\n")
        if typee=="Daily":
            for key in sensordict:
                a = str(sensordict[key])
                a = a.replace("(","")
                a = a.replace(")","")
                key =str(int(float(key)))
                tempfile.write(str(city)+","+a+","+key+","+str(date)+","+str(hour)+"\n")
    tempfile.close()
    tempfile1 = open("temp.csv","r")
    ftempread = tempfile1.read()
    ftempread = ftempread.replace("'","")
    tempfile1.close()
    tempfile1 = open("temp.csv","w")
    tempfile1.write(ftempread)
    tempfile1.close()
    dataa = pd.read_csv('temp.csv')
    df = pd.DataFrame(dataa)
    if typee=="Daily":
        X = list(df.iloc[:, -2])
        xx = "Dates"
    if typee=="Hourly":
        X = list(df.iloc[:, -1])
        xx = "Hours"
    Y = list(df.iloc[:, int(paramm)])
    plt.bar(X, Y, color='r')
    plt.title("Air Quality")
    plt.xlabel(xx)
    plt.ylabel(param)
    plt.show()
    loop()

def loop():

    data = input_group("Air checker",[
    radio("Select query type",options=['Spatial analysis','District level emissions study','City-wide emissions study','Top-k emissions study'], name ="opt"),
    ])

    if data['opt'] == "Spatial analysis":
        loop1()
    if data['opt'] == "District level emissions study":
        loop2()
    if data['opt'] == "City-wide emissions study":
        loop3()
    if data['opt'] == "Top-k emissions study":
        loop4()

    loop()
loop()
