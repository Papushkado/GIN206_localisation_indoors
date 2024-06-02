import numpy as np
import math 

def dist(x, y, z):
    return x * x + y * y + z * z
#Je suppose que a,b,c,d sont des listes contenant par exemple [xa,ya,za,da*2]

def rssi_to_distance(rssi):
    A = 50.0 #atténuation à 1 m
    n = 2.0  #Coefficient pour un trajet 
    dist=10**((A-rssi)/(n*10))
    return dist
def initialisation(rssi_ab,rssi_ac,rssi_bc,rssi_ad,rssi_cd):
    d_ab,d_ac,d_bc,d_ad=rssi_to_distance(rssi_ab),rssi_to_distance(rssi_ac),rssi_to_distance(rssi_bc),rssi_to_distance(rssi_ad)
    d_cd=rssi_to_distance(rssi_cd)
    cos_a=(d_bc**2-d_ab**2-d_ac**2)/(-2*d_ab*d_ac)
    p=(d_ab+d_ac+d_bc)/2
    S=math.sqrt(p*(p-d_ab)*(p-d_ac)*(p-d_bc))
    sin_a=(2*S)/(d_ab*d_ac)
    cos_d=(d_cd**2-d_ad**2-d_ac**2)/(-2*d_ad*d_ac)
    p2=(d_ac+d_ad+d_cd)/2
    S2=math.sqrt(p2*(p2-d_ac)*(p2-d_ad)*(p2-d_cd))
    sin_d=(2*S2)/(d_ac*d_ad)
    return ([0,0,0],[d_ab,0,0],[cos_a*d_ac,sin_a*d_ac,0],[d_ad*cos_a*cos_d,d_ad*sin_a*cos_d,d_ad*sin_d])

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
    


