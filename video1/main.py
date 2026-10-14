import numpy as np
import struct
import sys
import json

version = "2.0.0"
path = fr"d:\python\neural_network\video1"
open_params = False
node = False
path_to = ""

def interface():
    print("Which library do you want to train your model on? \n1 MNIST \n 2 node")
    x = input()
    return x

def load_images(filename):
    with open(filename, 'rb') as f:
        magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
        data = np.frombuffer(f.read(), dtype=np.uint8)
        data = data.reshape(num, rows * cols)
        return data

def load_labels(filename):
    with open(filename, 'rb') as f:
        magic, num = struct.unpack(">II", f.read(8))
        labels = np.frombuffer(f.read(), dtype=np.uint8)
        return labels

X_test = load_images(fr"{path}\training\MNIST\t10k-images.idx3-ubyte")
Y_test = load_labels(fr"{path}\training\MNIST\t10k-labels.idx1-ubyte")
X_test = X_test.T / 255.0

def load_NODE():
    with open("training/NODE/data.json", "r") as f:
        data = json.load(f)

    X_train = []
    Y_train = []

    for item in data:
        X_train.append(item["model_image"])
        Y_train.append(int(item["model_label"]))
    
    X_train = np.array(X_train)
    Y_train = np.array(Y_train)
    return X_train, Y_train


def init_random_params():
    W1 = np.random.rand(128, 784) - 0.5
    b1 = np.random.rand(128, 1) - 0.5

    W2 = np.random.rand(10, 128) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    
    return W1, b1, W2, b2

def init_open_params(path_to):
    try:
        data = np.load(fr"{path}\models\{path_to}")
        W1 = data["W1"]
        b1 = data["b1"]
        W2 = data["W2"]
        b2 = data["b2"]
        return W1, b1, W2, b2
    except:
        return init_random_params()

def init_params():
    if open_params:
        return init_open_params(path_to )
    return init_random_params()


def get_predictions(A2):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y):
    #print(predictions, Y)
    return np.sum(predictions == Y) / Y.size


def reLu(Z):
    return np.maximum(0, Z)


def deriv_reLu(Z):
    #return Z > 0 ? 1 : 0
    #jebać python pozdrawiam
    return (Z > 0).astype(int)


def softmax(Z):
    expZ = np.exp(Z - np.max(Z, axis=0, keepdims=True)) # stabilizacja numeryczna
    return expZ / np.sum(expZ, axis=0, keepdims=True)

# import math

# def softmax(values):
#     exp_vals = [math.exp(v) for v in values]
#     total = sum(exp_vals)
#     return [ev / total for ev in exp_vals]

# print(softmax([2.0, 1.0, 0.1]))
    

def forward_prop(W1, b1, W2, b2, X):
    Z1 = W1.dot(X) + b1
    A1 = reLu(Z1)

    Z2 = W2.dot(A1) + b2
    A2 = softmax(Z2)

    return Z1, A1, Z2, A2


def one_hot(Y):
    one_hot_Y = np.zeros((10, Y.size))
    one_hot_Y[Y, np.arange(Y.size)] = 1
    return one_hot_Y


def back_prop(Z1, A1, Z2, A2, W2, X, Y):
    m = Y.size
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    dW2 = (1 / m) * dZ2.dot(A1.T)
    db2 = (1 / m) * np.sum(dZ2, axis=1, keepdims=True)
    dZ1 = W2.T.dot(dZ2) * deriv_reLu(Z1)

    dW1 = (1 / m) * dZ1.dot(X.T)
    db1 = (1 / m) * np.sum(dZ1, axis=1, keepdims=True)

    return dW1, db1, dW2, db2


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, aplha):
    W1 = W1 - aplha * dW1
    b1 = b1 - aplha * db1

    W2 = W2 - aplha * dW2
    b2 = b2 - aplha * db2

    return W1, b1, W2, b2


def gradient_descent(X, Y, iterations, aplha):
    permutation = np.random.permutation(X.shape[1])
    X = X[:, permutation]
    Y = Y[permutation]
    W1, b1, W2, b2 = init_params()

    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = back_prop(Z1, A1, Z2, A2, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, aplha)

        if node:
            probs = A2[:, 0].tolist()
            prediction = int(np.argmax(A2[:, 0]))
        else:
            probs = A2.T.tolist()
            prediction = get_predictions(A2).tolist()
        ac = get_accuracy(get_predictions(A2), Y)
    
        print(json.dumps({
            "prediction": predictions,
            "probabilities": probs,
            "accuracy": float(get_accuracy(get_predictions(A2), Y))
        }))

    return W1, b1, W2, b2, ac

def main(file_name = "", node_mode=False):
    global open_params, path_to, X_train, Y_train, node
    if(node):
        iterations = 1
        # obraz
        data = json.loads(sys.stdin.readline())
        
        X_train = np.array(data["image"], dtype=float).reshape(784, 1) / 255.0
        Y_train = np.array([int(data["label"])])
    else:
        iterations = 1000
        open_params = True
        if file_name != "":
            path_to = file_name
        else:
            x = interface()
            if x == "1":
                X_train = load_images(fr"{path}\training\MNIST\train-images.idx3-ubyte")
                Y_train = load_labels(fr"{path}\training\MNIST\train-labels.idx1-ubyte")
            elif x == "2":
                X_train, Y_train = load_NODE()
                unique, counts = np.unique(Y_train, return_counts=True)
                print(dict(zip(unique, counts)))
            X_train = X_train.T / 255.0
    
    if x != "2":
        W1, b1, W2, b2, ac = gradient_descent(X_train, Y_train, iterations, 0.05)
    else:
        W1, b1, W2, b2 = init_params()
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X_train)
        print(json.dumps({
            "Z1": Z1,
            "A1": A1,
            "Z2": Z2,
            "A2": A2
        }))
    
    

    # with open(rf"{path}\models\[{version}]-{round(ac, 5)}-${round(np.random.rand(1)[0], 5)}.txt", "a") as f:
    #     np.set_printoptions(threshold=np.inf)
    #     f.write(f"{W1}||{b1}||{W2}||{b2}")

    np.savez(rf"{path}\models\[{version}]-{round(ac, 5)}-${round(np.random.rand(1)[0], 5)}.npz", W1=W1, b1=b1, W2=W2, b2=b2)

main("[2.0.0]-1.0-$0.90187.npz", node_mode=False)
#"[1.3.0]-0.891-$0.23733.npz"
#[2.0.0]-1.0-$0.90187.npz
#main(node=True)