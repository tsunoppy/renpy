import keras
import pandas as pd

from sklearn.model_selection import train_test_split

########################################################################

df = pd.read_csv('dl.dat')

print(df.head())

x = df.drop(['ind','mu'],axis=1)
y = df['mu']


########################################################################
# 標準化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
x = scaler.fit_transform(x)
########################################################################

#print(x.head())
print(y.head())

X_train, X_test, y_train, y_test =  \
    train_test_split(x, y, test_size=0.3, random_state=0 )

print("X_test")
print(X_test.shape)
print(X_test[:,7])
#print(X_train,y_train)

########################################################################
# モデルの作成

from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt


model = Sequential()
print('Xshape',X_train.shape[1])
model.add(Dense(100, activation='relu', input_shape=(X_train.shape[1],)))
#model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1))


# added
from tensorflow.keras import optimizers
optimizer = optimizers.Adam(learning_rate=0.001,
                            beta_1=0.9, beta_2=0.999, amsgrad=True)
model.compile(optimizer=optimizer,
              loss='mse',
              metrics=['mae'])
"""
model.compile(optimizer='adam',
              loss='mse', 
              metrics=['mae'])
"""
# adam
# mse(平均２乗誤差）
# mae（評価関数）今回は関わってこない

hist = model.fit(X_train, y_train,  #トレーニングデータ
                 batch_size=32,  #バッチサイズの指定
                 #epochs=200,      #エポック数の指定
                 epochs=100,      #エポック数の指定
                 verbose=1,       #ログ出力の指定.
                 #verbose=2,       #ログ出力の指定.
                 validation_data=(X_test, y_test))  #テストデータ

if __name__ == '__main__':
    '''
    4. モデルの評価
    '''
    # 誤差の可視化
    loss = hist.history['loss']
    val_loss = hist.history['val_loss']

    fig = plt.figure()
    plt.rc('font', family='serif')
    plt.plot(range(len(loss)), loss,
             color='gray', linewidth=1,
             label='loss')
    plt.plot(range(len(val_loss)), val_loss,
             color='black', linewidth=1,
             label='val_loss')
    plt.xlabel('epochs')
    plt.ylabel('loss')
    plt.legend()
    # plt.savefig('output.jpg')
    plt.show()

    # テストデータの評価
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print('test_loss: {:.3f}, test_acc: {:.3f}'.format(
        loss,
        acc
    ))

#    print ( model.predict(X_test[3]), y_test[3] )

    model.save('my_model')

    y_target = model.predict(X_test)
    import matplotlib.pyplot as plt
    fig = plt.figure()
    #plt.scatter(y_test,y_target)
    #plt.scatter(y_target,X_test['nu'])
    plt.scatter(y_target,X_test[:,7])
    plt.show()

    plt.scatter(y_test,y_target)
    plt.show()
