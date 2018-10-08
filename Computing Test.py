import time
from numpy import *
from scipy import stats

# Set some parameters
numbvars=300
numbsims=10**5
corr=.5

# Define mean vector and covariance matrix
meanvec=zeros(numbvars,)
covmat=zeros((numbvars,numbvars))
for i in list(range(0,numbvars)):
    for j in list(range(0,numbvars)):
        if i==j:
            covmat[i][j]=1
        else:
            covmat[i][j]=.5

# Start the clock
start=time.time()

# Simulate random variables
rands=random.multivariate_normal(meanvec,covmat,numbsims)

intermed=time.time()

# Perform operation on random variables
binvars=zeros((numbsims,numbvars))
for i in list(range(0,numbsims)):
    for j in list(range(0,numbvars)):
        if rands[i][j]>=1:
            binvars[i][j]=1
        else:
            binvars[i][j]=0

# Stop the clock
end=time.time()

print(mean(binvars))
print("Random Time: ",intermed-start)
print("Operation Time: ",end-intermed)
print("Total Time: ",end-start)