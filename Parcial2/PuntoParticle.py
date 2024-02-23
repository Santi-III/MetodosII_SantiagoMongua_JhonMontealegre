import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def System(r,t,lambdaa=0.5,lambdab=0.3):
    
    na,nb,nc = r
    
    dnadt = -na*lambdaa
    dnbdt = na*lambdaa - nb*lambdab
    dncdt = nb*lambdab
    return np.array([dnadt,dnbdt,dncdt])

def Increment(f,r,t,h):
    
    state1 = np.array([r[0],r[1],r[2]])
    K1 = f(state1, t)
    
    state2 = np.array([r[0]+0.5*h*K1[0],r[1]+0.5*h*K1[1],r[2]+0.5*h*K1[2]]])
    K2 = f(state2, t+0.5*h)
    
    state3 = np.array([r[0]+0.5*h*K2[0],r[1]+0.5*h*K2[1],r[2]+0.5*h*K2[2]])
    K3 = f(state3, t+0.5*h)
    
    state4 = np.array([r[0]+h*K3[0],r[1]+h*K3[1],r[2]+h*K3[2]])
    K4 = f(state4, t+h)
    
    Deltaf = h*(K1+2*K2+2*K3+K4)/6
    
    return r+Deltaf

def CheckStep(Delta1,Delta2,Delta3,h,minimo=1e-2,maximo=1e-1):
    
    tolerancia = 0.001
    
    Delta1 = np.abs(Delta1)
    Delta2 = np.abs(Delta2)
    Delta3 = np.abs(Delta3)
    
    if Delta1 < tolerancia:
        h = minimo
        dx = Delta1
        
    else:
        
        if np.abs((Delta1 - Delta2))/Delta1 > maximo:
            h = 0.5*h
            dx = Delta2
        
        elif np.abs((Delta1-Delta3))/Delta1 < minimo:
            h = 2*h
            dx = Delta3
        
        else:
            dx = Delta1
            
    return dx,h

def Adaptativo1(f,r0,t,e=1e-4):
    h = t[1] - t[0]
    tf = t[-1]
    TimeVector = np.array([t])
    Vectors = r
    #  Calcule $h$, $t_{0}$, $t_{f}$.
    #Defina los vectores de tiempo y de soluci´on del sistema.
    while t < tf:
        # Avance h desde el punto actual
        r1 = Increment(f,r,t,h)
        # Avance h desde el siguiente punto
        r2 = Increment(f,r1,t+h,h)
        # Avance 2h desde el punto actual
        rt = Increment(f,r,t,2*h)
        # El error es comparar los avances
        #->h->h y ->2h en sus componentes
        error = np.linalg.norm( r2 - rt )
        # Si el error es menor que la tolerancia (e) -> avanzo 2h
        if error < e:
            t += 2*h
            r = rt
            TimeVector = np.append(TimeVector,t)
            Vectors = np.vstack((Vectors,r))
            # Llene vectores
        # Si el error es muy grande, cambie el paso
        # Seg´un Fehlberg
        q = 0.85 (e/error)^{1/4}
        h = q
        
    return TimeVector, Vectors

t = np.linspace(0,10,50)
N0 = np.array([500,0.,0.])
sol = odeint(System, N0, t, args=(0.5,0.3))
Time,Vectors = Adaptativo1(System,N0,t)

plt.plot(t,sol[:,1],label='Nb odeint')
plt.plot(t,Vectors[:,1],label='Nb Adaptativo')
plt.show()