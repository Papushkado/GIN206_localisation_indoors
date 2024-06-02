import numpy as np
import math 
import requests
import json
import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D #Pour la 3D mais pour l'instant pas implémenté

def dist(x, y, z):
    return x * x + y * y + z * z
#Je suppose que a,b,c,d sont des listes contenant par exemple [xa,ya,za,da*2]

def rssi_to_distance(rssi):
    A = 50.0 #atténuation à 1 m
    n = 2.0  #Coefficient pour un trajet 
    dist=10**((A-rssi)/(n*10))
    return dist
#Décommenter pour la 3D
def initialisation(rssi_ab,rssi_ac,rssi_bc):#,rssi_ad,rssi_cd):
    d_ab,d_ac,d_bc=rssi_to_distance(rssi_ab),rssi_to_distance(rssi_ac),rssi_to_distance(rssi_bc)
    #d_adrssi_to_distance(rssi_ad)
    #d_cd=rssi_to_distance(rssi_cd)
    cos_a=(d_bc**2-d_ab**2-d_ac**2)/(-2*d_ab*d_ac)
    p=(d_ab+d_ac+d_bc)/2
    S=math.sqrt(p*(p-d_ab)*(p-d_ac)*(p-d_bc))
    sin_a=(2*S)/(d_ab*d_ac)
    #cos_d=(d_cd**2-d_ad**2-d_ac**2)/(-2*d_ad*d_ac)
    #p2=(d_ac+d_ad+d_cd)/2
    #S2=math.sqrt(p2*(p2-d_ac)*(p2-d_ad)*(p2-d_cd))
    #sin_d=(2*S2)/(d_ac*d_ad)
    return ([0,0,0],[d_ab,0,0],[cos_a*d_ac,sin_a*d_ac,0])#,[d_ad*cos_a*cos_d,d_ad*sin_a*cos_d,d_ad*sin_d])

def trilateration(a,b,c,d):
    p=np.zeros(3,3)
    for j in range(3):
        p[j,0]=b[j]-a[j]
        p[j,1]=c[j]-a[j]
        p[j,2]=c[j]-a[j]
    u=(1/2)*np.array([[a[3]-b[3]+dist(b[0],b[1],b[2])-dist(a[0],a[1],a[2])],[a[3]-c[3]+dist(c[0],c[1],c[2])-dist(a[0],a[1],a[2])],[a[3]-d[3]+dist(d[0],d[1],d[2])-dist(a[0],a[1],a[2])]])
    det=np.linalg.det(p)
    if det :
        return np.dot(np.transpose(np.linalg.inv(p)),u)
    else : 
        print("Les calculs ne sont pas bons Kevin, la matrice n'est pas inversible ! ")
        return -1
    

def main():
    json_file = "data.json"
    with open(json_file, 'r') as f:
        data = json.load(f)
#64.6 : -93 
#Dans l'ordre le programme C print AB,BC,AC
    with serial.Serial('/dev/ttyUSB0', 115200) as ser:
        while True:
            rssi=[]
            flag=True
            line = ser.readline()
            line = line.decode('ascii')
            if (line == "Done\n"):
                if flag:
                    init2=initialisation(data['Init from 2.3'],data['Init from 12.6'],data['Init from 6.7'])
                    flag=False
                else:
                    cheh=np.copy(init2)
                    data=trilateration(cheh[0].append(rssi_to_distance(rssi[0])),cheh[1].append(rssi_to_distance(rssi[1])),cheh[2].append(rssi_to_distance(rssi[2])))
                    save_data_to_json(data, json_file)
                rssi=[]
                data = {} 
            else:
                _ , rssi = line.split(':')
                rssi.append(int(rssi))
            data = json.load(f)
            plot_data(data)


def save_data_to_json(data, json_file):
    with open(json_file, 'w') as f:
        json.dump(data, f)


def plot_data(data):
    x = list(map(int, data.keys()))
    y = list(data.values())

    plt.scatter(x, y)
    plt.title('Indoors Localization')
    plt.grid(True)
    plt.show()

def add_data_to_json(data, json_file):
    with open(json_file, 'r') as f:
        existing_data = json.load(f)

    existing_data.update(data)

    with open(json_file, 'w') as f:
        json.dump(existing_data, f)



if __name__ == "__main__":
    main()


