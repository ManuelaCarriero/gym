# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 11:42:29 2022

@author: asus
"""

from scipy.integrate import odeint
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns
import pandas as pd
import scipy.stats as st

# derivative
def logistic(state, time, α, β):
    N = state
    δN = α*N - β*N**2
    return δN

# time steps
#time = np.linspace(0, 1, 2**7+1)
#☺2**7+1
time = np.linspace(0, 1, 11)
# starting status
N0 = 0.1

# parameters
α = 10
β = 1


np.linspace(0, 1, 2**3+1)

res = odeint(logistic, y0=N0, t=time, args=(α,β))

res.shape

fig, ax = plt.subplots()
ax.plot(time, res, label="population", marker='^')
ax.set_xlabel("time (a.u.)")
ax.set_ylabel("population (a.u.)")
ax.axhline(α/β, label='carrying capacity', color='gray', linewidth=3, linestyle='--')
ax.legend()
ax.grid()
sns.despine(fig, trim=True, bottom=True, left=True)

def f(**kwargs):
    return kwargs

f(a=1)








############################proofolina########################
def iterables_square_maker(givemealist):
    new_givemealist=[]
    for i in givemealist:
        i = i ** 2
        new_givemealist.append(i)
    return new_givemealist

listing = [4, 3 , 5]
iterables_square_maker(listing)

###########appending items to an empty list is not so trivial as in lists######
def f(**dictionary):
    new_dictionary = {}
    for key, value in dictionary.items():
        value = value**2
        new_dictionary[key] = value
    return new_dictionary 

f(a = 4) #{'a': 16}

def f(a, **dictionary):
    new_dictionary = {}
    for key, value in dictionary.items():
        value = a**2
        new_dictionary[key] = value
    return new_dictionary 

f(a=4, b=1)#{'b': 16}
f(a=4,b='constant')#{'b': 16}
f(a=0.1,b=4)#{'b': 0.010000000000000002}
f(a=4, b=1, c=4)#{'b': 16, 'c': 16}

#My proof that works

listing = [4, 3 , 5]
names = ['a', 'b', 'c']

a_dict = {}

for i, j in zip(listing, names):
    a_dict[j] = i

a_dict
a_dict.items()

#from SE
def add_element(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = []
    dictionary[key].append(value)
    
dictionary = {}

for i, j in zip(listing, names):
    add_element(dictionary, j, i) #{'a': [4], 'b': [3], 'c': [5]} something of weird

dictionary
####################################################################

def to_df(result, columns, **other_info):
    res_df = pd.DataFrame(result, columns=columns)
    for key, value in other_info.items():
        res_df[key] = value
    return res_df

to_df([1,2,3],'a')
#TypeError: Index(...) must be called with a collection of some kind, 'a' was passed

to_df([1,2,3], ['a']) # In this way it works

results=[1,2,3]
to_df(results, columns = ['a']) # In this way it works as in the project

#to_df(listing = [1,2,3], ['a'])
#SyntaxError: positional argument follows keyword argument

to_df(listing = [1,2,3], columns = ['a'])
#TypeError: to_df() missing 1 required positional argument: 'result'

to_df(res, ['population'], N0=N0, α=α, β=β, time=time).head()

q = np.linspace(0,1,12)[1:-1]

q = np.linspace(0,1,11)[1:-1]

q

#######################################################
# Using the above nested radical formula for g=phi_d 
# or you could just hard-code it. 
# phi(1) = 1.61803398874989484820458683436563 
# phi(2) = 1.32471795724474602596090885447809 
def phi(d, precision=30): 
    x = 2.00
    for i in range(precision): 
        x = pow(1+x,1/(d+1)) 
    return x

def identity(x):
    return x

# this is an array version, for testing speed
def a_generate(ndim, Npoints, *, seed=0.5, mapper=identity):
    # get the base for the dimension
    g = phi(ndim) 
    # this is the inizialization constant for the array
    alpha = ((1/g)**np.arange(1, ndim+1))%1  
    # reshaping to allow broadcasting
    alpha = alpha.reshape(1, -1) 
    # just the count of the sequence
    base = np.arange(Npoints).reshape(-1, 1) 
    # perform the actual calculation
    z = seed + alpha*base 
    # tale only the decimal part
    z = z % 1
    # return a mapped version to some distribution
    return mapper(z) 

#############################################################

# randomly generate alpha values
mapper = st.norm(loc=[10], scale=0.5).isf
# 50 values around the average value
alphas = a_generate(1, 50, mapper=mapper)
β = 1

time = np.linspace(0, 1, 2**7+1)

results = []
for idx, (α, ) in enumerate(alphas):
    res = odeint(logistic, y0=N0, t=time, args=(α, β))
    res_df = to_df(res, ['population'], α=α, β=β, time=time, simulation_run=idx)
    results.append(res_df)
results = pd.concat(results, ignore_index=True)
#ignore_index=True because otherwise 
#you have that the index has duplicate values
#ValueError: cannot reindex from a duplicate axis when trying to plot
results

#it finds duplicated indexes:
results[results.index.duplicated()]
#it gives Empty DataFrame. 
#without ignore_index=True you would obtain all the dataframe !

sns.lineplot("time", 'population', data=results, hue='α',
             estimator=None, units='simulation_run')

#cambiando (α, ) in α ottieni l'errore 
#ValueError: Length of values (1) does not match length of index (129)

########Try##############################
dist = st.gamma(2.0,loc=0,scale=1)
alphas = dist.rvs(50)
β = 1

time = np.linspace(0, 1, 2**7+1)

results = []
for idx, α in enumerate(alphas):
    res = odeint(logistic, y0=N0, t=time, args=(α, β))
    res_df = to_df(res, ['population'], α=α, β=β, time=time, simulation_run=idx)
    results.append(res_df)
results = pd.concat(results, ignore_index=True)
#ignore_index=True because otherwise 
#you have that the index has duplicate values
#ValueError: cannot reindex from a duplicate axis when trying to plot
results


sns.lineplot("time", 'population', data=results, hue='α',
             estimator=None, units='simulation_run')

#In questo caso lasciando (α, )
#TypeError: cannot unpack non-iterable numpy.float64 object 


