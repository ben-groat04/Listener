import numpy as np
E=np.load('/tmp/form_env.npz')
def lvl(k,a,b):
    x=E[k][int(a*100):int(b*100)]; return 10*np.log10(np.mean(10**(x/10))+1e-30)
B=[11.3,24.4,32.2,38.0,43.4,47.4,55.0,64.8,73.0,80.8,104,109.3,113.4,133.4,193.0,224.0,
   225,264.0,272,283,286.5,306,317.1,322.5,329,342.8]
B=[11.3,24.4,43.4,47.4,64.8,80.8,104.5,109.3,113.4,126.0,133.4,193.0,224.0,251.5,258,276.5,286.5,317.1,322.5,329.0]
print('t | drums | bass | vocals | other | mix (dB 2s before -> 2s after)')
for t in B:
    print('%d:%04.1f'%(t//60,t%60),' | '.join('%.0f->%.0f'%(lvl(k,t-2.5,t-0.1),lvl(k,t+0.1,t+2.5)) for k in ['drums','bass','vocals','other','mix']))
