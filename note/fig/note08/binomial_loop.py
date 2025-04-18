import numpy as np
from params import *
import time

S = np.zeros((M + 1, M + 1), dtype=np.float64)  
S[0, 0] = S0
for j in range(1, M + 1, 1):
    for i in range(j + 1):
        S[i, j] = S[0, 0] * (u ** (j - i)) * (d ** i)

iv = np.zeros((M + 1, M + 1), dtype=np.float64)  
z = 0
for j in range(0, M + 1, 1):
    for i in range(z + 1):
        iv[i, j] = round(max(S[i, j] - K, 0), 8)
    z += 1

start_time = time.time()

pv = np.zeros((M + 1, M + 1), dtype=np.float64)  
pv[:, M] = iv[:, M]
z = M + 1
for j in range(M - 1, -1, -1):
    z -= 1
    for i in range(z):
        pv[i, j] = (q * pv[i, j + 1] + (1 - q) * pv[i + 1, j + 1]) * df

print(pv)
print('Value of European call option is %8.3f' % pv[0, 0])
print('elapsed: %f seconds' % (time.time() - start_time,))
