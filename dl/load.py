
# read model
########################################################################
from tensorflow import keras
model = keras.models.load_model('my_model')

print(model.summary())

import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('dl.dat')
x = df.drop(['ind','mu'],axis=1)
y = df['mu']
########################################################################
# 標準化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
x = scaler.fit_transform(x)
########################################################################

X_train, X_test, y_train, y_test =  \
    train_test_split(x, y, test_size=0.3, random_state=0 )

#predictions = model.predict(X_test)
#print(X_test.iloc[3])

y_target = model.predict(X_test)
#print(y_test,y_target)
#print(X_test['mu'])
#print(X_test)

#print(predictions)

import matplotlib.pyplot as plt


import numpy as np
x = np.arange( 0.0, 10.0, 1.0/100.0 )
fig = plt.figure(figsize=(6,6))
y = x

ax = plt.axes()
ax.scatter(y_test,y_target,ec='b',fc='None')
ax.plot(x,y,color = 'red')

ax.set_xlabel('Test Data')
ax.set_ylabel('True Value')

#plt.scatter(y_target,X_test['nu'])
plt.show()


x = df.drop(['ind','mu'],axis=1)
y = df['mu']
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)


#
n_target = 3
nStart = (n_target-1) * 102
nEnd = n_target * 102

y_target=model.predict(x_scaled[nStart:nEnd])

"""
print(x_scaled[0:100])
print(x_scaled[0:100,7])
print(y_target)
print(y.iloc[0:100])
"""

fig = plt.figure(figsize=(6,6))
ax = plt.axes()
ax.scatter(y_target,x_scaled[nStart:nEnd,7],\
           label='DL',ec='red',fc='None')
ax.scatter(y[nStart:nEnd],x_scaled[nStart:nEnd,7],\
           label='MN Diagram',ec='None',fc='b')
ax.legend()
plt.show()
#print(df.iloc[0:100,8],y_target)
