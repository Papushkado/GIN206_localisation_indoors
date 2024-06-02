#include <stdarg.h>
#include <stdio.h>

typedef struct {
    float data[3][3];
} matrix;

typedef struct {
    float data[3];
} aloisismean;



float determinant3(matrix mat){

    float det =  mat.data[0][0] * (mat.data[1][1] * mat.data[2][2] - mat.data[1][2] * mat.data[2][1]) -
           mat.data[0][1] * (mat.data[1][0] * mat.data[2][2] - mat.data[1][2] * mat.data[2][0]) +
           mat.data[0][2] * (mat.data[1][0] * mat.data[2][1] - mat.data[1][1] * mat.data[2][0]);
    printf("Le déterminant est %f \n",det);
    return det;
    };

matrix inv(matrix mat){
    matrix inv; 
    float det = determinant3(mat);

    if (det==0){
        printf("Problème chef");
        return inv;
    }

    float fact = (1.0)/det;

    inv.data[0][0] = (mat.data[1][1] * mat.data[2][2] - mat.data[1][2]*mat.data[2][1])*fact;
    inv.data[0][1] = (mat.data[0][2] * mat.data[2][1] - mat.data[0][1] *mat.data[2][2]) * fact;
    inv.data[0][2] = (mat.data[0][1] * mat.data[1][2]- mat.data[0][2] * mat.data[1][1]) * fact;
    inv.data[1][0] = (mat.data[1][2] *mat.data[2][0] - mat.data[1][0] * mat.data[2][2]) * fact;
    inv.data[1][1] = (mat.data[0][0] * mat.data[2][2] - mat.data[0][2] * mat.data[2][0]) * fact;
    inv.data[1][2] = (mat.data[0][2] * mat.data[1][0] -mat.data[0][0]*mat.data[1][2]) * fact;
    inv.data[2][0] = (mat.data[1][0] * mat.data[2][1] - mat.data[1][1]* mat.data[2][0]) * fact;
    inv.data[2][1] = (mat.data[0][1] * mat.data[2][0] - mat.data[0][0] * mat.data[2][1]) * fact;
    inv.data[2][2] = (mat.data[0][0] * mat.data[1][1] - mat.data[0][1] * mat.data[1][0]) * fact;

    return inv;
    

};

void affiche(matrix mat) {
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%.2f ", mat.data[i][j]);
        }
        printf("\n");
    }
};

matrix produit(matrix mat1, matrix mat2) {
    matrix result;

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result.data[i][j] = 0;
            for (int k = 0; k < 3; k++) {
                result.data[i][j] += mat1.data[i][k] * mat2.data[k][j];
            }
        }
    }

    return result;
};

matrix transpose(matrix mat){
    matrix transpose;
    transpose.data[0][0]=mat.data[0][0];transpose.data[0][1]=mat.data[1][0];transpose.data[2][0]=mat.data[0][2];
    transpose.data[1][1]=mat.data[1][1];transpose.data[0][2]=mat.data[2][0];transpose.data[1][0]=mat.data[0][1];
    transpose.data[2][2]=mat.data[2][2];transpose.data[1][2]=mat.data[2][1];transpose.data[2][1]=mat.data[1][2];

    return transpose;
};

float dist(float x, float y, float z){
    return x*x+y*y+z*z;
};

void aloisisaffiching(aloisismean vector) {
    for (int i = 0; i < 3; i++) {
        printf("%f\n", vector.data[i]);
    }
};

aloisismean merciAloisFranchementBouh(matrix mat, aloisismean vector) {
    aloisismean result = {{0, 0, 0}};

    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            result.data[i] += mat.data[i][j] * vector.data[j];
        }
    }

    return result;
}



int main(char* argv){

    //Test
    /*matrix matrice;

    matrice.data[0][0] = 1.0; matrice.data[0][1] = 2.0; matrice.data[0][2] = 3.0;
    matrice.data[1][0] = 4.0; matrice.data[1][1] = 2.0; matrice.data[1][2] = 6.0;
    matrice.data[2][0] = 7.0; matrice.data[2][1] = 8.0; matrice.data[2][2] = 9.0;

    determinant3(matrice);
    matrix inverse = inv(matrice);
    affiche(inverse);
    matrix id = produit(matrice,inverse);
    affiche(id);*/

    //Fin Test

    /*
    float da = argv[2];
    float db = argv[3];
    float dc = argv[4];
    float dd = argv[5];
    */

    float da = 2.0;
    float db = 3.0;
    float dc = 4.0;
    float dd = 75.0;
    printf("%f",da);

    float xa = 1.0;
    float ya = 21.0;
    float za = 3.0; 

    float oa = dist(xa,ya,za);

    float xb = 1.0;
    float yb = 23.0;
    float zb = 3.0; 

    float ob = dist(xb,yb,zb);

    float xc = 17.0;
    float yc = 29.0;
    float zc = 3.0; 

    float oc = dist(xc,yc,zc);

    float xd = 2.0;
    float yd = 1.0;
    float zd = 30.0; 

    float od = dist(xd,yd,zd);


    aloisismean u;
    u.data[0]=(da*da-db*db+ob-oa)*0.5;
    u.data[1]=(da*da-dc*dc+oc-oa)*0.5;
    u.data[2]=(da*da-dd*dd+od-oa)*0.5;

    aloisisaffiching(u);

    matrix p;

    p.data[0][0] = xb-xa; p.data[0][1] = xc-xa; p.data[0][2] = xd-xa;
    p.data[1][0] = yb-ya; p.data[1][1] = yc-ya; p.data[1][2] = yd-ya;
    p.data[2][0] = zb-za; p.data[2][1] = zc-za; p.data[2][2] = zd-za;

    affiche(p);

    matrix pete = transpose(inv(p));

    affiche(pete);

    aloisismean final = merciAloisFranchementBouh(pete, u);
    aloisisaffiching(final);

    return 0; 
};