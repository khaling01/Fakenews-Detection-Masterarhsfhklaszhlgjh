import string
import numpy as np
import pandas as pd
from SVM import SVM
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import re

# Testing


true_data = pd.read_csv('processedTrue.csv')
fake_data = pd.read_csv('processedFake.csv')

data = pd.concat([true_data, fake_data], ignore_index=True, sort=False)
# data.rename (columns= {0: 'index'}, inplace=True)
data.columns = ['index', 'label', 'content']
data.tail()
data['label']
# data.isnull().sum()

if __name__ == "__main__":
    X = data['content']
    y = data['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, shuffle=True, random_state=1)

    #Using Vectorizer
    tfidf_vectorizer=TfidfVectorizer(stop_words='english', max_df=0.7)
    X_train=tfidf_vectorizer.fit_transform(X_train) 
    X_test=tfidf_vectorizer.transform(X_test)


    clf = SVM(n_iters=1000)
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true==y_pred) / len(y_true)
        return accuracy

    print("SVM Accuracy: ", accuracy(y_test, predictions))

    # plot results
    def get_hyperplane(x, w, b, offset):
        return (-w[0] * x - b + offset) / w[1]

    fig, ax = plt.subplots(1, 1, figsize=(10,6))

    plt.set_cmap('PiYG')
    plt.scatter(X_train[:, 0], X_train[:, 1], marker='o', c=y_train, s=100, alpha=0.75)
    plt.scatter(X_test[:, 0], X_test[:, 1], marker="x", c=y_test, s=100, alpha=0.75)

    x0_1 = np.amin(X_train[:, 0])
    x0_2 = np.amax(X_train[:, 0])

    x1_1 = get_hyperplane(x0_1, clf.w, clf.b, 0)
    x1_2 = get_hyperplane(x0_2, clf.w, clf.b, 0)

    x1_1_m = get_hyperplane(x0_1, clf.w, clf.b, -1)
    x1_2_m = get_hyperplane(x0_2, clf.w, clf.b, -1)

    x1_1_p = get_hyperplane(x0_1, clf.w, clf.b, 1)
    x1_2_p = get_hyperplane(x0_2, clf.w, clf.b, 1)

    ax.plot([x0_1, x0_2], [x1_1, x1_2], "-", c='k', lw=1, alpha=0.9)
    ax.plot([x0_1, x0_2], [x1_1_m, x1_2_m], "--", c='grey', lw=1, alpha=0.8)
    ax.plot([x0_1, x0_2], [x1_1_p, x1_2_p], "--", c='grey', lw=1, alpha=0.8)

    x1_min = np.amin(X[:, 1])
    x1_max = np.amax(X[:, 1])
    ax.set_ylim([x1_min - 3, x1_max + 3])

    for spine in ['top','right']:
        ax.spines[spine].set_visible(False)

    plt.show()