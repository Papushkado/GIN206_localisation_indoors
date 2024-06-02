import numpy as np
import matplotlib.pyplot as plt
import statistics
import argparse


alphas = {}
betas = {
        "M<-A": 2,
        "M<-B": 1.35,
        "M<-C": 2.5,
        "A<-B": 1.5,
        "B<-C": 1.5,
        "C<-A": 2.7,
        }


def read_and_compute_alpha(filename, variablename, mean_method):
    with open(filename, 'r') as f:
        list_rssi = []
        lines = f.readlines()
        for line in lines:
            rssi = int(line.split(':')[-1])
            list_rssi.append(rssi)
        alphas[variablename] = mean_method(list_rssi)


def init_alphas(mean_method):
    read_and_compute_alpha("ma.txt", "M<-A", mean_method)
    read_and_compute_alpha("mb.txt", "M<-B", mean_method)
    read_and_compute_alpha("mc.txt", "M<-C", mean_method)
    read_and_compute_alpha("ab.txt", "A<-B", mean_method)
    read_and_compute_alpha("bc.txt", "B<-C", mean_method)
    read_and_compute_alpha("ca.txt", "C<-A", mean_method)


def init_rssis_abc(mean_method):
    init_filename = "clean_init.csv"
    list_rssi_ab, list_rssi_bc, list_rssi_ac = [], [], []

    with open(init_filename, 'r') as f:
        lines = f.readlines()

        for line in lines:
            split_line = line.split(',')
            rssi_ab = int(split_line[0].split(':')[-1])
            rssi_bc = int(split_line[1].split(':')[-1])
            rssi_ac = int(split_line[2].split(':')[-1])
            list_rssi_ab.append(rssi_ab)
            list_rssi_bc.append(rssi_bc)
            list_rssi_ac.append(rssi_ac)

    return (mean_method(list_rssi_ab),
            mean_method(list_rssi_bc),
            mean_method(list_rssi_ac))


def rssi_to_distance(variablename, rssi):
    exponent = alphas[variablename] - rssi
    dist = 10 ** (exponent / (10 * betas[variablename]))
    return dist


def initialisation(negative_c, rssi_ab, rssi_bc, rssi_ac, verbose):
    d_ab = rssi_to_distance("A<-B", rssi_ab)
    d_bc = rssi_to_distance("B<-C", rssi_bc)
    d_ac = rssi_to_distance("C<-A", rssi_ac)
    if verbose:
        print("AB : %f" % d_ab)
        print("BC : %f" % d_bc)
        print("AC : %f" % d_ac)
        print("Égalité triangulaire : %s" % (d_ab + d_bc >= d_ac))

    x_c = (d_ab ** 2 + d_ac ** 2 - d_bc ** 2) / (2 * d_ab)
    y_c = np.sqrt(d_ac ** 2 - x_c ** 2)
    if negative_c:
        y_c *= -1

    pointA = np.array([0, 0])
    pointB = np.array([d_ab, 0])
    pointC = np.array([x_c, y_c])

    P = np.zeros((2, 2))
    P[0, 0] = d_ab
    P[1, 0] = x_c
    P[1, 1] = y_c
    Pinv = np.linalg.inv(P)
    if verbose:
        print("Conditionnement de P : %f" % np.linalg.cond(P))

    return pointA, pointB, pointC, Pinv


def trilateration(rssi_a, rssi_b, rssi_c, OB2, OC2, Pinv):
    d_AM = rssi_to_distance("M<-A", rssi_a)
    d_BM = rssi_to_distance("M<-B", rssi_b)
    d_CM = rssi_to_distance("M<-C", rssi_c)

    U = np.array([d_AM ** 2 - d_BM ** 2 + OB2,
                  d_AM ** 2 - d_CM ** 2 + OC2]) / 2

    return np.dot(Pinv, U)


def squared_norm2(point):
    return point[0] ** 2 + point[1] ** 2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="nom du fichier contenant les RSSI du point à localiser")
    parser.add_argument('-n', dest='yc_negative', action='store_true',
                        help="rend l'ordonnée de C négative")
    parser.add_argument('-m', dest='use_mean', action='store_true',
                        help="utilise la moyenne au lieu de la médiane")
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help="verbose : affiche des données supplémentaires sur le stdout")
    parser.add_argument('-t', dest='plot_trajectory', action='store_true',
                        help="affiche la trajectoire au lieu d'un nuage de points")
    args = parser.parse_args()
    return args


def main():
    # First get args and initialise alphas values
    args = parse_args()
    if args.use_mean:
        mean_method = statistics.mean
    else:
        mean_method = statistics.median

    init_alphas(mean_method)

    # Then initialise the rssi between A, B and C
    rssi_ab, rssi_bc, rssi_ac = init_rssis_abc(mean_method)

    # Then calculates the three points and inverse matrix
    pointA, pointB, pointC, Pinv = initialisation(
        args.yc_negative, rssi_ab, rssi_bc, rssi_ac, args.verbose)

    OB2 = squared_norm2(pointB)
    OC2 = squared_norm2(pointC)

    plt.plot(pointA[0], pointA[1], 'r+', label="Points de référence")
    plt.plot(pointB[0], pointB[1], 'r+')
    plt.plot(pointC[0], pointC[1], 'r+')

    # Finally read the main file and plot
    x, y = [], []
    list_rssi_a, list_rssi_b, list_rssi_c = [], [], []
    with open(args.filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            split_line = line.split(',')
            rssi_a = int(split_line[0].split(':')[-1])
            rssi_b = int(split_line[1].split(':')[-1])
            rssi_c = int(split_line[2].split(':')[-1])
            loc_point = trilateration(
                rssi_a, rssi_b, rssi_c, OB2, OC2, Pinv)

            x.append(loc_point[0])
            y.append(loc_point[1])
            list_rssi_a.append(rssi_a)
            list_rssi_b.append(rssi_b)
            list_rssi_c.append(rssi_c)

    if args.plot_trajectory:
        plt.plot(x[0], y[0], 'o', color='orange', label="Début")
        plt.plot(x[-1], y[-1], 'go', label="Fin")
        x, y = np.array(x), np.array(y)
        plt.quiver(x[:-1], y[:-1], x[1:]-x[:-1], y[1:]-y[:-1],
                   scale_units='xy', angles='xy', scale=1,
                   width=0.003, label="Trajectoire",
                   color=plt.cm.rainbow(np.linspace(0, 1, x.shape[0])))
    else:
        plt.plot(x, y, 'b+', label="Points M")

    mean_RSSI_point = trilateration(
            mean_method(list_rssi_a),
            mean_method(list_rssi_b),
            mean_method(list_rssi_c),
            OB2, OC2, Pinv)

    plt.plot(mean_RSSI_point[0], mean_RSSI_point[1],
             'ro', label="Moyenne RSSI")
    plt.plot(mean_method(x), mean_method(y), 'yo', label="Moyenne XY")

    plt.xlim(-10, 30)
    plt.ylim(-20, 20)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(args.filename)
    plt.legend()

    if args.verbose:
        print()
        mean_a = statistics.mean(list_rssi_a)
        median_a = statistics.median(list_rssi_a)
        std_a = statistics.stdev(list_rssi_a)
        print("Moyenne RSSI AM : %f dBm" % mean_a)
        print("Médiane RSSI AM : %f dBm" % median_a)
        print("Écart-type RSSI AM : %f dBm" % std_a)
        ecart_a_moins = np.abs(rssi_to_distance("M<-A", mean_a) - rssi_to_distance("M<-A", mean_a - std_a))
        ecart_a_plus = np.abs(rssi_to_distance("M<-A", mean_a) - rssi_to_distance("M<-A", mean_a + std_a))
        print("Écart de distance AM Moyenne / Moyenne - Écart-type : %f" % ecart_a_moins)
        print("Écart de distance AM Moyenne / Moyenne + Écart-type : %f" % ecart_a_plus)
        print()
        mean_b = statistics.mean(list_rssi_b)
        median_b = statistics.median(list_rssi_b)
        std_b = statistics.stdev(list_rssi_b)
        print("Moyenne RSSI BM : %f dBm" % mean_b)
        print("Médiane RSSI BM : %f dBm" % median_b)
        print("Écart-type RSSI BM : %f dBm" % std_b)
        ecart_b_moins = np.abs(rssi_to_distance("M<-B", mean_b) - rssi_to_distance("M<-A", mean_b - std_b))
        ecart_b_plus = np.abs(rssi_to_distance("M<-B", mean_b) - rssi_to_distance("M<-A", mean_b + std_b))
        print("Écart de distance BM Moyenne / Moyenne - Écart-type : %f" % ecart_b_moins)
        print("Écart de distance BM Moyenne / Moyenne + Écart-type : %f" % ecart_b_plus)
        print()
        mean_c = statistics.mean(list_rssi_c)
        median_c = statistics.median(list_rssi_c)
        std_c = statistics.stdev(list_rssi_c)
        print("Moyenne RSSI CM : %f dBm" % mean_c)
        print("Médiane RSSI CM : %f dBm" % median_c)
        print("Écart-type RSSI CM : %f dBm" % std_c)
        ecart_c_moins = np.abs(rssi_to_distance("M<-C", mean_c) - rssi_to_distance("M<-C", mean_c - std_c))
        ecart_c_plus = np.abs(rssi_to_distance("M<-C", mean_c) - rssi_to_distance("M<-C", mean_c + std_c))
        print("Écart de distance CM Moyenne / Moyenne - Écart-type : %f" % ecart_c_moins)
        print("Écart de distance CM Moyenne / Moyenne + Écart-type : %f" % ecart_c_plus)

    plt.show()


if __name__ == "__main__":
    main()
