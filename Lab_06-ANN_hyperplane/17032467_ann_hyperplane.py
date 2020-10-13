from sklearn import datasets
iris = datasets.load_iris()

X = [[d[1],d[2]] for d in iris.data]
names = [iris.target_names[1],iris.target_names[2]]
Y = iris.target

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.8)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# imports
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import vis

activation_functions = ['identity', 'logistic', 'tanh', 'relu']
hidden_layers = [(3), (3,3), (3,3,3)]
fig = plt.figure()
for i,actfcn in enumerate(activation_functions):
  for j,hlyr in enumerate(hidden_layers):
    mlp = MLPClassifier(hidden_layer_sizes=hlyr, activation=actfcn, max_iter=1000)
    mlp.fit(X_train, y_train)
    ax = fig.add_subplot(len(hidden_layers), len(activation_functions), j*len(activation_functions)+i+1)
    ax.set_title('{},{},{}'.format(actfcn,str(hlyr),round(mlp.score(X_test,y_test),2)))
    vis.vis2d(ax, mlp, X_train, y_train, X_test, y_test)
    ax.set_xticks([])
    ax.set_yticks([])

# show plots
plt.show()