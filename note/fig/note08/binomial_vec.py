import numpy as np
from params import *
import time

mu = np.arange(M + 1)
mu = np.resize(mu, (M + 1, M + 1))
md = np.transpose(mu)
mu = u ** (mu - md)
md = d ** md
S = S0 * mu * md

start_time = time.time()

# present value array initialized with inner values
pv = np.maximum(S - K, 0)      
z = 0
for i in range(M - 1, -1, -1): # backwards induction
    pv[0:M-z, i] = (q * pv[0:M-z, i+1] + (1 - q) * pv[1:M-z+1, i+1]) * df
    z += 1

print(pv)
print('Value of European call option is %8.3f' % pv[0, 0])
print('vector elapsed: %f seconds.' % (time.time() - start_time,))
