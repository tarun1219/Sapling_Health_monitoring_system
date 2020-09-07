import pandas
import matplotlib.pyplot as plt
lis=['e501','e502','e503','e504','e505']
for i in range(5):
    df3=pandas.read_csv(lis[i]+".csv")
    x=df3.Time
    y=df3.Moisture
    plt.figure(i)
    plt.plot(x, y)
    plt.xlabel('TIME')
    plt.ylabel('MOISTURE CONTENT')
    plt.title(lis[i])
    plt.savefig(lis[i]+'.jpg',bbox_inches='tight')
for i in range(5):
    df3=pandas.read_csv(lis[i]+".csv")
    x=df3.Time
    y=df3.Moisture
    plt.plot(x, y) 
    plt.xlabel('TIME') 
    plt.ylabel('MOISTURE CONTENT')
    if i==4:
        plt.title('Blue-e501 Orange-e502 Green-e503 Red-e504 Violet-e505')
    if i==4:
        plt.savefig('mixed_graph.jpg',bbox_inches='tight')
print("Graphs made!!!")
