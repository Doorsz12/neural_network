import numpy as np

n = [2, 3, 3, 1]

W1 = np.random.randn(n[1], n[0])
W2 = np.random.randn(n[2], n[1])
W3 = np.random.randn(n[3], n[2])
b1 = np.random.randn(n[1], 1)
b2 = np.random.randn(n[2], 1)
b3 = np.random.randn(n[3], 1)

print("Weights for layer 1 shape:", W1.shape)
print("Weights for layer 2 shape:", W2.shape)
print("Weights for layer 3 shape:", W3.shape)
print("bias for layer 1 shape:", b1.shape)
print("bias for layer 2 shape:", b2.shape)
print("bias for layer 3 shape:", b3.shape)

X = np.array([
    [150, 70], # it's our boy Jimmy again! 150 pounds, 70 inches tall. 
    [254, 73],
    [312, 58],
    [120, 60],
    [154, 61],
    [212, 65],
    [216, 67],
    [145, 67],
    [184, 64],
    [130, 69]
])

print(X.shape) # prints (10, 2)

A0 = X.T
print(A0.shape) # prints (2, 10)

y = np.array([
    0,  # whew, thank God Jimmy isn't at risk for cardiovascular disease.
    1,   # damn, this guy wasn't as lucky
    1, # ok, this guy should have seen it coming. 5"8, 312 lbs isn't great.
    0,
    0,
    1,
    1,
    0,
    1,
    0
])
m = 10

Y = y.reshape(n[3], m)
print(Y.shape)

def g(x):
  return np.round(1 / (1 + np.exp(-1 * x)), 10)

print(g(np.array([-99, 1, 2, 4, 99])))

m = 10

# layer 1 calculations

Z1 = W1 @ A0 + b1  # the @ means matrix multiplication

assert Z1.shape == (n[1], m) # just checking if shapes are good
A1 = g(Z1)

# layer 2 calculations
Z2 = W2 @ A1 + b2
assert Z2.shape == (n[2], m)
A2 = g(Z2)

# layer 3 calculations
Z3 = W3 @ A2 + b3
assert Z3.shape == (n[3], m)
A3 = g(Z3)