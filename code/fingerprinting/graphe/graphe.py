import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from statistics import mean, median
import matplotlib.pyplot as plt
import argparse


def compute_class_from_string(string, max_i):
    split_string = string.split(' ')
    i, j = int(split_string[1]), int(split_string[2])
    return max_i * j + i


def read_training_set(file_name, max_i):
    training_samples, training_classes = [], []
    with open(file_name, 'r') as f:
        first_line = f.readline()
        training_class = compute_class_from_string(first_line, max_i)
        lines = f.readlines()
        for line in lines:
            if line[0] == 'c':
                # This is a new class
                training_class = compute_class_from_string(line, max_i)
            else:
                # This is a lign with RSSIs
                rssis = line.split(',')
                rssi1 = int(rssis[0].split(':')[-1])
                rssi2 = int(rssis[1].split(':')[-1])
                rssi3 = int(rssis[2].split(':')[-1])
                sample = [rssi1, rssi2, rssi3]
                training_samples.append(sample)
                training_classes.append(training_class)

    return np.array(training_samples), np.array(training_classes)


def read_and_compute_class(file_name, clf, use_neural_network, scaler):
    classes = []
    list_rssi_a, list_rssi_b, list_rssi_c = [], [], []

    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.split(',')
            rssi_a = int(split_line[0].split(':')[-1])
            rssi_b = int(split_line[1].split(':')[-1])
            rssi_c = int(split_line[2].split(':')[-1])
            rssis = [rssi_a, rssi_b, rssi_c]

            list_rssi_a.append(rssi_a)
            list_rssi_b.append(rssi_b)
            list_rssi_c.append(rssi_c)

            if use_neural_network:
                classes.append(clf.predict(scaler.transform([rssis])))
            else:
                classes.append(clf.predict([rssis]))

    mean_rssis = [
            mean(list_rssi_a),
            mean(list_rssi_b),
            mean(list_rssi_c)
            ]
    median_rssis = [
            median(list_rssi_a),
            median(list_rssi_b),
            median(list_rssi_c)
            ]
    if use_neural_network:
        mean_class = clf.predict(scaler.transform([mean_rssis]))
        median_class = clf.predict(scaler.transform([median_rssis]))
    else:
        mean_class = clf.predict([mean_rssis])
        median_class = clf.predict([median_rssis])

    return classes, mean_class, median_class


def retreive_ij_from_class(value_class, max_i):
    i, j = value_class % max_i, value_class // max_i
    if (i == 0):
        i = max_i
        j -= 1
    return i, j


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="nom du fichier contenant les RSSI du point à localiser")
    parser.add_argument('-k', dest='nb_neighbors', default=1, type=int,
                        help="donne le nombre de plus proche voisins à utiliser dans l'algorithme de même nom (défaut: 1)")
    parser.add_argument('-n', dest='use_neural_network', action='store_true',
                        help="utilise les réseaux de neurones (si non précisé, utilise la méthode des k plus proches voisins)")
    parser.add_argument('-t', dest='plot_trajectory', action='store_true',
                        help="affiche la trajectoire au lieu d'un nuage de points")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    max_i = 12
    training_samples, training_classes = read_training_set(
        "clean_training_data.csv", max_i)

    if args.use_neural_network:
        scaler = StandardScaler()
        scaler.fit(training_samples)
        training_samples = scaler.transform(training_samples)
        clf = MLPClassifier(solver='lbfgs', max_iter=2000)
    else:
        scaler = None
        clf = KNeighborsClassifier(n_neighbors=args.nb_neighbors)

    clf.fit(training_samples, training_classes)

    test_classes, mean_class, median_class = read_and_compute_class(
        args.filename, clf, args.use_neural_network, scaler)

    # Plots the mean and median classes
    i, j = retreive_ij_from_class(mean_class, max_i)
    plt.plot(i, j, 'ro', label="Moyenne")
    i, j = retreive_ij_from_class(median_class, max_i)
    plt.plot(i, j, 'yo', label="Médiane")

    # Plots the points
    I, J = [], []
    for c in test_classes:
        i, j = retreive_ij_from_class(c[0], max_i)
        I.append(i)
        J.append(j)
    if args.plot_trajectory:
        plt.plot(I[0], J[0], 'o', color='orange', label="Début")
        plt.plot(I[-1], J[-1], 'go', label="Fin")
        I, J = np.array(I), np.array(J)
        plt.quiver(I[:-1], J[:-1], I[1:]-I[:-1], J[1:]-J[:-1],
                   scale_units='xy', angles='xy', scale=1, width=0.003,
                   color=plt.cm.rainbow(np.linspace(0, 1, I.shape[0])),
                   label="Trajectoire")
    else:
        plt.plot(I, J, 'b+', label="Points M")
    plt.xlim(0, 13)
    plt.ylim(0, 4)
    plt.xlabel("i")
    plt.ylabel("j")
    plt.gca().invert_yaxis()
    plt.title(args.filename)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
