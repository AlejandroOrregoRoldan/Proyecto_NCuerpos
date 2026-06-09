#include <iostream>
#include <vector>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

const double G = 6.674e-11;
const double DT = 0.01;

// Estructura de Arreglos (SoA) para maximizar rendimiento
struct Universe {
    double *x, *y, *vx, *vy, *mass;
};

void init_universe(Universe &u, int n) {
    u.x = new double[n]; u.y = new double[n];
    u.vx = new double[n]; u.vy = new double[n];
    u.mass = new double[n];

    srand(42); // Semilla fija para consistencia
    for (int i = 0; i < n; i++) {
        u.x[i] = (rand() % 1000) / 10.0;
        u.y[i] = (rand() % 1000) / 10.0;
        u.vx[i] = (rand() % 10) / 10.0;
        u.vy[i] = (rand() % 10) / 10.0;
        u.mass[i] = (rand() % 10000) + 1000.0;
    }
}

void free_universe(Universe &u) {
    delete[] u.x; delete[] u.y; 
    delete[] u.vx; delete[] u.vy; delete[] u.mass;
}

int main(int argc, char* argv[]) {
    int N = (argc > 1) ? atoi(argv[1]) : 1000;

    Universe u;
    init_universe(u, N);

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i = 0; i < N; i++) {
        double fx = 0.0, fy = 0.0;
        for (int j = 0; j < N; j++) {
            if (i == j) continue;
            double dx = u.x[j] - u.x[i];
            double dy = u.y[j] - u.y[i];
            double dist = sqrt(dx*dx + dy*dy) + 1e-9;
            
            double force = (G * u.mass[i] * u.mass[j]) / (dist * dist);
            fx += force * (dx / dist);
            fy += force * (dy / dist);
        }
        u.vx[i] += (fx / u.mass[i]) * DT;
        u.vy[i] += (fy / u.mass[i]) * DT;
        u.x[i] += u.vx[i] * DT;
        u.y[i] += u.vy[i] * DT;
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
    
    // Imprime SOLO el tiempo para que Python lo lea
    cout << elapsed << endl;

    free_universe(u);
    return 0;
}