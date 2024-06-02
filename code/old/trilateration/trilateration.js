function determinant3(mat) {
    const det = mat[0][0] * (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1]) -
                mat[0][1] * (mat[1][0] * mat[2][2] - mat[1][2] * mat[2][0]) +
                mat[0][2] * (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]);
    console.log("Le déterminant est " + det);
    return det;
}

function inverse(mat) {
    const inv = [[], [], []];
    const det = determinant3(mat);

    if (det === 0) {
        console.log("Problème chef");
        return inv;
    }

    const fact = 1.0 / det;

    inv[0][0] = (mat[1][1] * mat[2][2] - mat[1][2] * mat[2][1]) * fact;
    inv[0][1] = (mat[0][2] * mat[2][1] - mat[0][1] * mat[2][2]) * fact;
    inv[0][2] = (mat[0][1] * mat[1][2] - mat[0][2] * mat[1][1]) * fact;
    inv[1][0] = (mat[1][2] * mat[2][0] - mat[1][0] * mat[2][2]) * fact;
    inv[1][1] = (mat[0][0] * mat[2][2] - mat[0][2] * mat[2][0]) * fact;
    inv[1][2] = (mat[0][2] * mat[1][0] - mat[0][0] * mat[1][2]) * fact;
    inv[2][0] = (mat[1][0] * mat[2][1] - mat[1][1] * mat[2][0]) * fact;
    inv[2][1] = (mat[0][1] * mat[2][0] - mat[0][0] * mat[2][1]) * fact;
    inv[2][2] = (mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]) * fact;

    return inv;
}

function printMatrix(mat) {
    for (let i = 0; i < 3; i++) {
        console.log(mat[i].join(' '));
    }
}

function product(mat1, mat2) {
    const result = [[], [], []];

    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            result[i][j] = 0;
            for (let k = 0; k < 3; k++) {
                result[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }

    return result;
}

function transpose(mat) {
    const transpose = [[], [], []];
    transpose[0][0] = mat[0][0]; transpose[0][1] = mat[1][0]; transpose[2][0] = mat[0][2];
    transpose[1][1] = mat[1][1]; transpose[0][2] = mat[2][0]; transpose[1][0] = mat[0][1];
    transpose[2][2] = mat[2][2]; transpose[1][2] = mat[2][1]; transpose[2][1] = mat[1][2];

    return transpose;
}

function aloisisaffiching(vector) {
    for (let i = 0; i < 3; i++) {
        console.log(vector[i]);
    }
}

function merciAloisFranchementBouh(mat, vector) {
    const result = [0, 0, 0];

    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            result[i] += mat[i][j] * vector[j];
        }
    }

    return result;
}

function main() {
    const da = 2.0;
    const db = 3.0;
    const dc = 4.0;
    const dd = 75.0;

    const xa = 1.0;
    const ya = 21.0;
    const za = 3.0;

    const oa = dist(xa, ya, za);

    const xb = 1.0;
    const yb = 23.0;
    const zb = 3.0;

    const ob = dist(xb, yb, zb);

    const xc = 17.0;
    const yc = 29.0;
    const zc = 3.0;

    const oc = dist(xc, yc, zc);

    const xd = 2.0;
    const yd = 1.0;
    const zd = 30.0;

    const od = dist(xd, yd, zd);

    const u = [
        (da * da - db * db + ob - oa) * 0.5,
        (da * da - dc * dc + oc - oa) * 0.5,
        (da * da - dd * dd + od - oa) * 0.5
    ];

    aloisisaffiching(u);

    const p = [
        [xb - xa, xc - xa, xd - xa],
        [yb - ya, yc - ya, yd - ya],
        [zb - za, zc - za, zd - za]
    ];

    printMatrix(p);

    const pete = transpose(inverse(p));

    printMatrix(pete);

    const final = merciAloisFranchementBouh(pete, u);
    aloisisaffiching(final);
}

function dist(x, y, z) {
    return x * x + y * y + z * z;
}

main();
