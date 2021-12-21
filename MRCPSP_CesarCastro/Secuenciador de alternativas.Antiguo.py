import numpy as np
from random import gauss
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
    return precedencia 
#table u(k,r)  recurso renovable r que requiere la actividad k por periodo de tiempo 
u=np.array([[0,0,0],[5,0,0],[0,0,5],[2,0,5],[8,0,0],[5,0,0],[4,0,0],[0,0,0],[0,0,0],[0,10,0],[0,10,1],[0,0,0],[0,0,0],[0,0,0],[10,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0],[5,0,0],[5,0,0],[0,10,0],[10,0,0],[0,0,0],[2,0,0],[0,0,0]])
# n = nuemero de actividades con fictiacias
n = 28
#tiempos de inicio segun la linea base
def Ascl(k):
    actividadk = "rectifique el numero de actividad ingresada"
    tislb = [0,0,0,4,6,7,0,8,10,28,30,32,33,39,41,42,42,54,42,42,52,60,58,56,64,66,70,90]
    if k == ka[0]:
        actividadk = tislb[0]
        return actividadk
    if k == ka[1]:
        actividadk = tislb[1]
        return actividadk
    if k == ka[2]:
        actividadk = tislb[2]
        return actividadk
    if k == ka[3]:
        actividadk = tislb[3]
        return actividadk
    if k == ka[4]:
        actividadk = tislb[4]
        return actividadk
    if k == ka[5]:
        actividadk = tislb[5]
        return actividadk
    if k == ka[6]:
        actividadk = tislb[6]
        return actividadk
    if k == ka[7]:
        actividadk = tislb[7]
        return actividadk
    if k == ka[8]:
        actividadk = tislb[8]
        return actividadk
    if k == ka[9]:
        actividadk = tislb[9]
        return actividadk
    if k == ka[10]:
        actividadk = tislb[10]
        return actividadk
    if k ==  ka[11]:
        actividadk = tislb[11]
        return actividadk
    if k == ka[12]:
        actividadk = tislb[12]
        return actividadk
    if k == ka[13]:
        actividadk = tislb[13]
        return actividadk
    if k== ka[14]:
        actividadk = tislb[14]
        return actividadk
    if k == ka[15]:
        actividadk = tislb[15]
        return actividadk
    if k ==  ka[16]:
        actividadk = tislb[16]
        return actividadk
    if k ==  ka[17]:
        actividadk = tislb[17]
        return actividadk
    if k ==  ka[18]:
        actividadk = tislb[18]
        return actividadk
    if k ==  ka[19]:
        actividadk = tislb[19]
        return actividadk
    if k ==  ka[20]:
        actividadk = tislb[20]
        return actividadk
    if k ==  ka[21]:
        actividadk = tislb[21]
        return actividadk
    if k == ka[22]:
        actividadk = tislb[22]
        return actividadk
    if k == ka[23]:
        actividadk = tislb[23]
        return actividadk
    if k == ka[24]:
        actividadk = tislb[24]
        return actividadk
    if k == ka[25]:
        actividadk = tislb[25]
        return actividadk
    if k == ka[26]:
        actividadk = tislb[26]
        return actividadk
    if k == ka[27]:
        actividadk = tislb[27]
        return actividadk
    return actividadk
#ObjAscl es el Makespan generado por la linea base en la programacion proactiva, que tambien es igual a Asc(k) de la actividad 28 en este caso la ultima actividad   
ObjAscl = Ascl(27)
#robustez de la solucion
RobustezAscl=0
#robustez de la calidad
ROBAscl = 0
# tiempo de duracion de cada actividad
d=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#Creacion lista de actividades
# z(k) prioridad de cada actividad segun la programacion proactiva
def Z():
    qq = n
    con = 0
    ya = []
    ya1=[]
    jj = 0
    for xk in ka:
        for xi in i:
            if Ascl(xk)<Ascl(xi):
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
def z(k):
    actividadk = k
    prioridad = 0
    if actividadk==1:
        prioridad=1
        return prioridad
    if actividadk==2:
        prioridad=2
        return prioridad
    if actividadk==3:
        prioridad=3
        return prioridad
    if actividadk==4:
        prioridad=5
        return prioridad
    if actividadk==5:
        prioridad=6
        return prioridad
    if actividadk==6:
        prioridad=7
        return prioridad
    if actividadk==7:
        prioridad=4
        return prioridad
    if actividadk==8:
        prioridad=8
        return prioridad
    if actividadk==9:
        prioridad=9
        return prioridad
    if actividadk==10:
        prioridad=10
        return prioridad
    if actividadk==11:
        prioridad=11
        return prioridad
    if actividadk==12:
        prioridad=12
        return prioridad
    if actividadk==13:
        prioridad=13
        return prioridad
    if actividadk==14:
        prioridad=14
        return prioridad
    if actividadk==15:
        prioridad=15
        return prioridad
    if actividadk==16:
        prioridad=16
        return prioridad
    if actividadk==17:
        prioridad=17
        return prioridad
    if actividadk==18:
        prioridad=21
        return prioridad
    if actividadk==19:
        prioridad=18
        return prioridad
    if actividadk==20:
        prioridad=19
        return prioridad
    if actividadk==21:
        prioridad=20
        return prioridad
    if actividadk==22:
        prioridad=24
        return prioridad
    if actividadk==23:
        prioridad=23
        return prioridad
    if actividadk==24:
        prioridad=22
        return prioridad
    if actividadk==25:
        prioridad=25
        return prioridad
    if actividadk==26:
        prioridad=26
        return prioridad
    if actividadk==27:
        prioridad=27
        return prioridad
    if actividadk==28:
        prioridad=28
        return prioridad
#********************PARA EL PROCEDIMINETO ASCL ...... SGS 
# Escenarios - programacion reactiva - SGS paralelo
e = [1,2,3,4,5,6,7,8]
#tiempo donde inicia cada actividad segun sgs
# Smc es el tiempo de inicio en programación reactiva despues de aplicar SGS 
#obj(e) es el makespan en programación reactiva despues de aplicar SGS para cada actividad k en cada escenario e
SMC=[]
toi=[]
ii=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
for xe in e:    
    #actividades completadas en el SGS en un momento dado Tg 
    c = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #numero total de precendencias de cada actividad
    np = [0,1,1,1,3,1,1,2,1,1,1,1,2,2,1,1,1,1,1,1,1,4,5,5,3,1,1,1]
    #total de actividades finalizadas para la tarea k en la etapa g
    To= [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #tiempo de finalización de actividades activas
    af= [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #actividades elegibles en la etapa g
    eleg=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    #tiempo donde finaliza cada actividad
    f=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    # orden de las actividaddes elegibles en la etapa g
    w=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
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
        toi2=toi[0:28]
        toi3=toi[28:56]
        toi4=toi[56:84]
        toi5=toi[84:112]
        toi6=toi[112:140]
        toi7=toi[140:168]
        toi8=toi[168:196]
        toi9=toi[196:224]
        toi10=toi[224:252]
        toi11=toi[252:280]
        toi12=toi[280:308]
        toi13=toi[308:336]
        toi14=toi[336:364]
        toi15=toi[364:392]
        toi16=toi[392:420]
        toi17=toi[420:448]
        toi18=toi[448:476]
        toi19=toi[476:504]
        toi20=toi[504:532]
        toi21=toi[532:560]
        toi22=toi[560:588]
        toi23=toi[588:616]
        toi24=toi[616:644]
        toi25=toi[644:672]
        toi26=toi[672:700]
        toi27=toi[700:728]
        toi28=toi[728:756]
        TOID=[sum(toi2),sum(toi3),sum(toi4),sum(toi5),sum(toi6),sum(toi7),sum(toi8),sum(toi9),sum(toi10),sum(toi11),sum(toi12),sum(toi13),sum(toi14),sum(toi15),sum(toi16),sum(toi17),sum(toi18),sum(toi19),sum(toi20),sum(toi21),sum(toi22),sum(toi23),sum(toi24),sum(toi25),sum(toi26),sum(toi27),sum(toi28)]
        for xp in range(len(i)):
            To[xp+1]=TOID[xp]
        for x in toi[:]:
            toi.remove(x)
        for xk in range(len(ka)):
            if To[xk]==np[xk]:
                eleg[xk] = 1-c[xk]-act[xk]
            else:
                eleg[xk]=0
        for xk in range(len(ka)): 
            w[xk]= eleg[xk]*z(xk+1)
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
                w[xk]=eleg[xk]*z(xk+1)
            vw=0
            for xk in range(len(ka)):
                vw=vw+w[xk]
            ww=vw
    for xk in range(len(ka)):
        ii[xk]=0
        ii[xk] = f[xk]-d[xk]
        SMC.append(ii[xk])
    print("tiempo que dura cada actividad en el escenario:",xe,d)
def smc(E):
    devuelta = "rectifique el numero del escenario"
    if E==e[0]:
        SMC1=SMC[0:28]
        return SMC1
    if E==e[1]:    
        SMC2=SMC[28:56]
        return SMC2
    if E==e[2]:
        SMC3=SMC[56:84]
        return SMC3
    if E==e[3]:
        SMC4=SMC[84:112]
        return SMC4
    if E==e[4]:
        SMC5=SMC[112:140]
        return SMC5
    if E==e[5]:
        SMC6=SMC[140:168]
        return SMC6
    if E==e[6]:
        SMC7=SMC[168:196]
        return SMC7
    if E==e[7]:
        SMC8=SMC[196:224]
        return SMC8
    return devuelta
def OBJ(E):
    devuelta = "rectifique el numero del escenario"
    if E==e[0]:
        OBJ1=SMC[27]
        return OBJ1
    if E==e[1]:    
        OBJ2=SMC[55]
        return OBJ2
    if E==e[2]:
        OBJ3=SMC[83]
        return OBJ3
    if E==e[3]:
        OBJ4=SMC[111]
        return OBJ4
    if E==e[4]:
        OBJ5=SMC[139]
        return OBJ5
    if E==e[5]:
        OBJ6=SMC[167]
        return OBJ6
    if E==e[6]:
        OBJ7=SMC[195]
        return OBJ7
    if E==e[7]:
        OBJ8=SMC[223]
        return OBJ8
    return devuelta
ds=[]
for xk in ka: 
    for xe in e:
        ds.append(abs(Ascl(xk)-smc(xe)[xk-1]))
ds1=ds[0:8]
ds2=ds[8:16]
ds3=ds[16:24]
ds4=ds[24:32]
ds5=ds[32:40]
ds6=ds[40:48]
ds7=ds[48:56]
ds8=ds[56:64]
ds9=ds[64:72]
ds10=ds[72:80]
ds11=ds[80:88]
ds12=ds[88:96]
ds13=ds[96:104]
ds14=ds[104:112]
ds15=ds[112:120]
ds16=ds[120:128]
ds17=ds[128:136]
ds18=ds[136:144]
ds19=ds[144:152]
ds20=ds[152:160]
ds21=ds[160:168]
ds22=ds[168:176]
ds23=ds[176:184]
ds24=ds[184:192]
ds25=ds[192:200]
ds26=ds[200:208]
ds27=ds[208:216]
ds28=ds[216:224]
DS=[sum(ds1)/8,sum(ds2)/8,sum(ds3)/8,sum(ds4)/8,sum(ds5)/8,sum(ds6)/8,sum(ds7)/8,sum(ds8)/8,sum(ds9)/8,sum(ds10)/8,sum(ds11)/8,sum(ds12)/8,sum(ds13)/8,sum(ds14)/8,sum(ds15)/8,sum(ds16)/8,sum(ds17)/8,sum(ds18)/8,sum(ds19)/8,sum(ds20)/8,sum(ds21)/8,sum(ds22)/8,sum(ds23)/8,sum(ds24)/8,sum(ds25)/8,sum(ds26)/8,sum(ds27)/8,sum(ds28)/8]
RobustezAscl = sum(DS)
robascl=[]
for xe in e:
    robascl.append(abs(ObjAscl-OBJ(xe)))
ROBAscl = sum(robascl)/8
print("tiempo de inicio en programacion reactiva despues de aplicar SGS")
print(1,smc(1))
print(2,smc(2))
print(3,smc(3))
print(4,smc(4))
print(5,smc(5))
print(6,smc(6))
print(7,smc(7))
print(8,smc(8))
print("makespan en programacion reactiva despues de aplicar SGS para cada escenario e")
print(OBJ(1),OBJ(2),OBJ(3),OBJ(4),OBJ(5),OBJ(6),OBJ(7),OBJ(8))
print("robustez de la solucion")
print(RobustezAscl)
print("robustez de la calidad")
print(ROBAscl)

