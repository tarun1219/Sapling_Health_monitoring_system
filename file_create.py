import pandas
from datetime import *
import csv
import plotly.tools as tls
import matplotlib.pyplot as plt
import numpy as np
df=pandas.DataFrame(columns=["Code"])
date=str(datetime.today())
temp=1
lis=[]
while(temp==1):
    moist=input("Enter code: ")
    lis.append(moist)
    temp=int(input())
df['Code']=lis
df.to_csv("date.csv",index=False)
report=[]
date=str(datetime.now())
df=pandas.read_csv("date.csv")
report=[] 
temp=1
while(temp==1):
    moist=int(input("moisture: "))
    report.append(moist)
    temp=int(input("0/1"))
new_c=date[10:16]
df[new_c]=report
df.to_csv("date.csv")

x=df.Code
y=df[new_c]

plt.bar(x,y,label='moisture content')
plt.xlabel('Plant Code')
plt.ylabel('Moisture')
plt.title(new_c)
plt.legend()
plt.show()

