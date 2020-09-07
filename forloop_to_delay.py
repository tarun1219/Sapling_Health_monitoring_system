'''date=str(datetime.now())

        df=pandas.read_csv("imp_data.csv")'''
import random,time
report=[] 
def rand():
    return random.randint(65,75)
for i in range(5):
    moist=rand()
    report.append(moist)
    time.sleep(30)
    print("Value taken.\n")
    
for i in range(5):
    print(report[i]+"\n")
