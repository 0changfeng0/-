import numpy as np

if __name__ == '__main__':
    a = np.array([[1, 2], [3, 4]])
    print(a.shape)
    b = np.array([[1, 2], [3, 4]])
    print(b.shape)
    x = np.expand_dims(a, axis=2)
    print(x.shape)
    y = np.expand_dims(b, axis=2)
    print(y.shape)
    c = np.concatenate((x, y), axis=2)
    print(c.shape)
    print(c)
