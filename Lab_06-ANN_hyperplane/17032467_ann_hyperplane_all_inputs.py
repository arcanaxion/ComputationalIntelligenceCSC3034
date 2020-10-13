from sklearn import datasets
iris = datasets.load_iris()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, train_size=0.8)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# imports
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
import vis

mlp = MLPClassifier(hidden_layer_sizes=(3), max_iter=10000)
mlp.fit(X_train, y_train)

fig = plt.figure()
axes = vis.vis3d(fig, mlp, X_train, y_train, X_test, y_test)
for i,a in enumerate(axes):
  a.set_title(iris.target_names[i])
  a.set_xticklabels([])
  a.get_yaxis().set_visible(False)
axes[-1].set_xticklabels(iris.feature_names)

# show plots
plt.show()