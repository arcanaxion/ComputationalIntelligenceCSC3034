import random

class Data:
    def __init__(self, x1, x2, y):
        self.x1 = x1
        self.x2 = x2
        self.y = y

def train_AND(data, initial_w1, initial_w2, initial_theta, alpha=0.1, epochs=1):
    w1 = initial_w1
    w2 = initial_w2
    theta = initial_theta

    for i in range(epochs):
        print("At Epoch {0}: w1 = {1}, w2 = {2}, theta={3}".format(i+1, w1, w2, theta))
        w1, w2, theta = oneEpoch(data, w1, w2, theta, alpha)
    return w1, w2, theta

def hardLimiter(x1, x2, w1, w2, theta):
    return (x1 * w1) + (x2 * w2) - theta

def oneEpoch(data, w1, w2, theta, alpha):
    for i in range(len(data)):
        y = 1 if hardLimiter(data[i].x1, data[i].x2, w1, w2, theta) >= 0 else 0
        error = data[i].y - y
        w1 += (alpha * data[i].x1 * error)
        w2 += (alpha * data[i].x2 * error)
        theta = (alpha * -1 * error)
        print("Values after Iteration {0}: w1 = {1}, w2 = {2}, theta={3}".format(i+1, w1, w2, theta))

    return w1, w2, theta
        

if __name__ == "__main__":
    alpha = 0.1
    random.seed(1)
    initial_w1 = random.uniform(-0.5, 0.5)
    initial_w2 = random.uniform(-0.5, 0.5)
    initial_theta = random.uniform(-0.5, 0.5)
    data = [Data(0,0,0), Data(0,1,0), Data(1,0,0), Data(1,1,1)]
    
    print("Initial values: alpha = {0}, initial w1 = {1}, initial w2 = {2}, initial theta = {3}" \
        .format(alpha, initial_w1, initial_w2, initial_theta))

    trained = train_AND(data, initial_w1, initial_w2, initial_theta, 0.1, 2)
    print(trained)
