import os
import glob
import cv2
import numpy as np

def load_data(data_dir):
    image_paths = glob.glob(os.path.join(data_dir, "*.jpg"))

    X_paths = image_paths
    X = []
    for path in X_paths:
        path = cv2.imread(path)
        path = cv2.resize(path, (224, 224))
        X.append(path)
    y = [1 if "focus" in path else 0 for path in X_paths]

    return np.array(X), np.array(y)


# def batch_generator(X, y, batch_size=64, shuffle=False, random_seed=None):
    # X_copy = np.array(X)
    # y_copy = np.array(y)
    # if shuffle:
    #     data = np.column_stack((X_copy, y_copy))
    #     if random_seed:
    #         np.random.seed(random_seed)
    #     np.random.shuffle(data)
    #     X_copy = data[:, 0]
    #     y_copy = data[:, 1].astype(int)
    # for i in range(0, len(X_copy), batch_size):
    #     yield X_copy[i:i+batch_size], y_copy[i:i+batch_size]

if __name__ == "__main__":
    X_train, y_train = load_data("Data/data_train")
    print("Number of images:", len(X_train))
    print("Number of focus images:", sum(y_train))
    print("Number of non-focus images:", len(y_train) - sum(y_train))
    X_test, y_test = load_data("Data/data_test")
    print("Number of images:", len(X_test))
    print("Number of focus images:", sum(y_test))
    print("Number of non-focus images:", len(y_test) - sum(y_test))