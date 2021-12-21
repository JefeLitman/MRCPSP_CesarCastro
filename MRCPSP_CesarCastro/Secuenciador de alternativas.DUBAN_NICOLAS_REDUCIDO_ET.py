import numpy as np
from random import gauss
import random
random.seed(0)
#actividad inicial y final son ficticias: act 1 y act n+2 .  i inicia en 2 (actividad 2 que realmente es la 1, 3 que es la 2 y asi sucesivamente hasta que y termina en: numero actividades reales + 2 osea 9, por eso i=8 es realmente actividad 7 y i=9 es la ficticia final) 
ka = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
i = ka[1:28]
#k inicia en 1 (actividad 1 que es la actividad inicial ficticia, sigue en 2 que es la 1, 3 que es la 2 y asi sucesivamente hasta que y termina en: numero actividades reales + 1 osea 8, por eso k=8 es realmente actividad 7)
#recursos 
#recurso renovables -> r 7
R = [1,2,3]
#b maxima cantidad de recurso disponible por periodo de tiempo en orden PL (project leader) QA (quality assesment y DE (designer engineer)
B=[10,10,5]
#relacion de precedencia cuando actividad k precede a actividad i
#tabla de precedencias
def p(k,i):
    actividadk = k
    actividadi = i
    precedencia = 0
    if actividadi == int(2) and actividadk == int(1):
        precedencia = 1
        return precedencia
    if actividadi == int(3) and actividadk == int(1):
        precedencia = 1
        return precedencia
    if actividadi == int(4) and actividadk == int(1):
        precedencia = 1
        return precedencia
    if actividadi == int(7) and actividadk == int(1):
        precedencia = 1
        return precedencia
    if actividadi == int(5) and actividadk == int(2):
        precedencia = 1
        return precedencia
    if actividadi == int(5) and actividadk == int(3):
        precedencia = 1
        return precedencia
    if actividadi == int(5) and actividadk == int(4):
        precedencia = 1
        return precedencia
    if actividadi == int(6) and actividadk == int(5):
        precedencia = 1
        return precedencia
    if actividadi == int(8) and actividadk == int(6):
        precedencia = 1
        return precedencia
    if actividadi == int(8) and actividadk == int(7):
        precedencia = 1
        return precedencia
    if actividadi == int(9) and actividadk == int(8):
        precedencia = 1
        return precedencia
    if actividadi == int(10) and actividadk == int(9):
        precedencia = 1
        return precedencia
    if actividadi == int(11) and actividadk == int(9):
        precedencia = 1
        return precedencia
    if actividadi == int(12) and actividadk == int(9):
        precedencia = 1
        return precedencia
    if actividadi == int(13) and actividadk == int(10):
        precedencia = 1
        return precedencia
    if actividadi == int(13) and actividadk == int(11):
        precedencia = 1
        return precedencia
    if actividadi == int(14) and actividadk == int(12):
        precedencia = 1
        return precedencia
    if actividadi == int(14) and actividadk == int(13):
        precedencia = 1
        return precedencia
    if actividadi == int(15) and actividadk == int(14):
        precedencia = 1
        return precedencia
    if actividadi == int (16) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi == int(17) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi == int (19) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi == int(20) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi == int(23) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi == int(24) and actividadk == int(15):
        precedencia = 1
        return precedencia
    if actividadi ==int(18) and actividadk == int(17):
        precedencia = 1
        return precedencia
    if actividadi == int(21) and actividadk == int (20):
        precedencia = 1
        return precedencia
    if actividadi == int(22) and actividadk == int(16):
        precedencia = 1 
        return precedencia
    if actividadi == int (22) and actividadk == int(18):
        precedencia = 1
        return precedencia
    if actividadi == int(22) and actividadk == int (19):
        precedencia = 1
        return precedencia
    if actividadi == int(22) and actividadk == int(21):
        precedencia = 1
        return precedencia
    if actividadi == int(25) and actividadk == int(22):
        precedencia = 1
        return precedencia
    if actividadi == int(25) and actividadk == int(24):
        precedencia = 1
        return precedencia
    if actividadi == int(25) and actividadk == int(23):
        precedencia = 1
        return precedencia
    if actividadi == int(26) and actividadk == int(25):
        precedencia = 1
        return precedencia
    if actividadi == int(27) and actividadk == int(26):
        precedencia = 1
        return precedencia
    if actividadi == int(28) and actividadk == int(27):
        precedencia = 1
        return precedencia
    if actividadi == int(23) and actividadk == int(16):
        precedencia = 1
        return precedencia
    if actividadi == int (23) and actividadk == int(18):
        precedencia = 1
        return precedencia
    if actividadi == int (23) and actividadk == int(19):
        precedencia = 1
        return precedencia
    if actividadi == int (23) and actividadk == int(21):
        precedencia = 1
        return precedencia
    if actividadi == int (24) and actividadk == int (16):
        precedencia = 1
        return precedencia
    if actividadi == int(24) and actividadk == int(18):
        precedencia = 1
        return precedencia
    if actividadi == int(24) and actividadk == int(19):
        precedencia = 1
        return precedencia
    if actividadi == int(24) and actividadk == int(21):
        precedencia = 1
        return precedencia
    return precedencia #pensar en una forma para cambiar la matriz de precedencia 
#table u(k,r)  recurso renovable r que requiere la actividad k por periodo de tiempo 
u=np.array([[0,0,0],[5,0,0],[0,0,5],[2,0,5],[8,0,0],[5,0,0],[4,0,0],[0,0,0],[0,0,0],[0,10,0],[0,10,1],[0,0,0],[0,0,0],[0,0,0],[10,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[5,0,0],[5,0,0],[0,10,0],[10,0,0],[0,0,0],[2,0,0],[0,0,0]])
# n = nuemero de actividades con fictiacias #pensar en una forma distinta de escribir esto 
n = 28
#tiempos de inicio segun la linea base
Ascl = [0,0,0,4,6,7,0,8,10,28,30,32,33,39,41,42,42,54,42,42,52,60,58,56,64,66,70,90]
#ObjAscl es el Makespan generado por la linea base en la programacion proactiva, que tambien es igual a Asc(k) de la actividad 28 en este caso la ultima actividad   
ObjAscl = Ascl[27]
#robustez de la solucion
RobustezAscl=0
#robustez de la calidad
ROBAscl = 0
# tiempo de duracion de cada actividad
d=[0]*28
#Creacion lista de actividades
# z(k) prioridad de cada actividad segun la programacion proactiva
print("prioridad de cada actividad segun la programacion proactiva")
def Z():
    qq = n
    con = 0
    ya = []
    ya1=[]
    jj = 0
    for xk in ka:
        for xi in i:
            if Ascl[xk-1]<Ascl[xi-1]:
                    qq=qq-1
        ya.append(qq)
        qq = n                                   
    for xk in ka:
        for xi in i:  
            if ya[xk-1] == ya[xi-1]:
                con = con + 1
        if con>0:
            ya[xk-1] = ya[xk-1] - con
        if jj>0:
            ya[xk-1] = ya[xk-1] + 1       
        jj = jj + 1
        con=0
        ya1.append(ya[xk-1])
    return ya1
z = Z()
print(z)
#********************PARA EL PROCEDIMINETO ASCL ...... SGS 
# Escenarios - programacion reactiva - SGS paralelo
print("¡Hola!"," ingrese la cantidad de escenarios")
x = int(input())
xx=x
print(f"Los indices para los {x} escenarios serán calculados")
print(f"¿desea ver la duracion para cada actividad en los {x} escenarios?")
print("NOTA: a cualquier pregunta responda si o no")
x1 = str(input())
e = list(range(1,x+1))
#tiempo donde inicia cada actividad segun sgs
# Smc es el tiempo de inicio en programación reactiva despues de aplicar SGS 
#obj(e) es el makespan en programación reactiva despues de aplicar SGS para cada actividad k en cada escenario e
SMC=[]
toi=[]
TOID=[]
ii=[0]*28
for xe in e:    
    #actividades completadas en el SGS en un momento dado Tg 
    c = [0]*28
    #numero total de precendencias de cada actividad
    np = [0,1,1,1,3,1,1,2,1,1,1,1,2,2,1,1,1,1,1,1,1,4,5,5,3,1,1,1]#aqui puedo poner la suma de predecesores de cada actividad 
    #total de actividades finalizadas para la tarea k en la etapa g
    To= [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #tiempo de finalización de actividades activas
    af= [0]*28
    #actividades elegibles en la etapa g
    eleg=[0]*28
    #tiempo donde finaliza cada actividad
    f=[0]*28
    # orden de las actividaddes elegibles en la etapa g
    w=[0]*28
    # actividades activas en el momento Tg
    act=[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #tiempo o momento que corresponde a la etapa g (Variable auxiliar)
    H =20000
    #etapa
    g = 0  
    #tiempo o momento que corresponde a la etapa g (Variable principal) - tiempo transcurrido en la etapa g 
    Tg = 0
    #contador 
    y = 1
    m = 0
    cont = 0
    ww = 0
    vw = 0
    while y<=n-1:
        g=g+1
        for xk in range(len(ka)):
            af[xk] = (act[xk])*(f[xk])
        if g>1:
            H=20000
            for xk in range(len(ka)):
                if af[xk]>0:
                    if af[xk]<=H:
                        H=af[xk]
            for xk in range(len(ka)): 
                if af[xk]==H:
                    for RR in range(len(R)):
                        B[RR]=B[RR]+u[xk][RR]
        else:
            H=0
        Tg=H
        for xk in range(len(ka)):
            if f[xk]==Tg:
                if c[xk]==0:
                    c[xk] = c[xk] + act[xk]
                    act[xk] = act[xk] - c[xk]
        for xi in i: 
            for xk in ka:
                toi.append(c[xk-1]*p(xk,xi))
        T=0
        for Rs in list(range(28,756+1,28)):
            TOID.append(sum(toi[T:Rs]))
            T=Rs
        for xp in range(len(i)):
            To[xp+1]=TOID[xp]
        for x in toi[:]:
            toi.remove(x)
        for xs in TOID[:]:
            TOID.remove(xs)
        for xk in range(len(ka)):
            if To[xk]==np[xk]:
                eleg[xk] = 1-c[xk]-act[xk]
            else:
                eleg[xk]=0
        for xk in range(len(ka)): 
            w[xk]= eleg[xk]*z[xk]
        m=1
        ww=0
        for xk in range(len(ka)):
            ww=ww+w[xk]
        while ww>0:
            for xk in range(len(ka)):
                if w[xk]==m:
                    if u[xk][0]<=B[0]:
                        cont = cont + 1
                    if u[xk][1]<=B[1]:
                        cont = cont + 1
                    if u[xk][2]<=B[2]:
                        cont = cont + 1
                    if cont==3:
                        act[xk]=1
                        eleg[xk]=0
                        if ka[xk]==1:
                            d[xk]=0
                        if ka[xk]==2:
                            d[xk]= round(gauss(1,0.1))
                        if ka[xk]==3:
                            d[xk]= round(gauss(4,0.4))
                        if ka[xk]==4:
                            d[xk]= round(gauss(2,0.2))
                        if ka[xk]==5:
                            d[xk]= round(gauss(1,0.1))
                        if ka[xk]==6:
                            d[xk]= round(gauss(1,0.1))
                        if ka[xk]==7:
                            d[xk]= round(gauss(6,0.6))
                        if ka[xk]==8:
                            d[xk]= round(gauss(2,0.2))
                        if ka[xk]==9:
                            d[xk]= round(gauss(16,1.6))
                        if ka[xk]==10:
                            d[xk]= round(gauss(2,0.2))
                        if ka[xk]==11:
                            d[xk]= round(gauss(2,0.2))
                        if ka[xk]==12:
                            d[xk]= round(gauss(6,0.6))
                        if ka[xk]==13:
                            d[xk]= round(gauss(4,0.4))
                        if ka[xk]==14:
                            d[xk]= round(gauss(1,0.1))
                        if ka[xk]==15:
                            d[xk]= round(gauss(1,0.1))
                        if ka[xk]==16:
                            d[xk]= round(gauss(8,0.8))
                        if ka[xk]==17:
                            d[xk]= round(gauss(12,1.2))
                        if ka[xk]==18:
                            d[xk]= round(gauss(10,1))
                        if ka[xk]==19:
                            d[xk]= round(gauss(10,1))
                        if ka[xk]==20:
                            d[xk]= round(gauss(10,1))
                        if ka[xk]==21:
                            d[xk]=round(gauss(8,0.8))
                        if ka[xk]==22:
                            d[xk]=round(gauss(1,0.1))
                        if ka[xk]==23:
                            d[xk]=round(gauss(4,0.4))
                        if ka[xk]==24:
                            d[xk]=round(gauss(8,0.8))
                        if ka[xk]==25:
                            d[xk]=round(gauss(2,0.2))
                        if ka[xk]==26:
                            d[xk]=round(gauss(4,0.4))
                        if ka[xk]==27:
                            d[xk]=round(gauss(8,0.8))
                        if ka[xk]==28:
                            d[xk]=0
                        f[xk]=Tg+d[xk]
                        y=y+1
                        for xr in range(len(R)):
                            B[xr]= B[xr]- u[xk][xr]
                    else:
                        eleg[xk]=0
                        act[xk]=0
                cont=0
            m=m+1
            for xk in range(len(ka)):
                w[xk]=eleg[xk]*z[xk]
            vw=0
            for xk in range(len(ka)):
                vw=vw+w[xk]
            ww=vw
    for xk in range(len(ka)):
        ii[xk]=0
        ii[xk] = f[xk]-d[xk]
        SMC.append(ii[xk])
    if x1=="si":
        print("tiempo que dura cada actividad en el escenario:",xe,d)
print("desea conocer tiempo de inicio en programación reactiva para algún escenario en especial?")
ds1=[]
def smc(E):
    devuelta = "rectifique el numero del escenario"
    if E!=0:
        SMC1=SMC[(E*28)-28:(28*E)]
        return SMC1 
    return devuelta
x31=str(input())
if x31=="si":
    print("ingrese el numero del escenario")
    w34=int(input())
    print(smc(w34))
if x31=="no":
    print(".-.")
obj=[]
for xe in list(range(27,(xx*28),28)):
    obj.append(abs(SMC[xe]))
print("desea conocer la lista del makespan de cada escenario?")
qua=str(input())
if qua=="si":
    print(obj)
print("desea conocer el mejor makespan de todos los escenarios?")
que=str(input())
if que=="si":
    menor=obj[0]
    posicion=0
    for tete in range(xx):
        if obj[tete]<=menor:
            menor=obj[tete]
            posicion=tete
    posicion=posicion+1
    print(menor)
    print("el mejor makespan esta en el escenario:",posicion)
if que=="no":
    print(".-.")
for xk1 in range(len(ka)):
    for xex in e:
        ds1.append(abs(Ascl[xk1]-smc(xex)[xk1]))
q1=0
DS1=[]
for Rs1 in list(range(xx,(xx*28)+1,xx)):
            DS1.append(sum(ds1[q1:Rs1])/xx)
            q1=Rs1
RobustezAscl = sum(DS1)
robascl=[]
for xe in list(range(27,(xx*28),28)):
    robascl.append(abs(ObjAscl-SMC[xe]))
ROBAscl = sum(robascl)/xx
print("robustez de la solucion")
print(RobustezAscl)
print("robustez de la calidad")
print(ROBAscl)
