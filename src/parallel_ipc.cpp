#include <iostream>
#include <cmath>
#include <cstdlib>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <ctime>

using namespace std;

const double G = 6.674e-11;
const double DT = 0.01;

int main(int argc, char* argv[]) {
    int N = (argc > 1) ? atoi(argv[1]) : 1000;
    int K = (argc > 2) ? atoi(argv[2]) : 4;

    size_t array_size = N * sizeof(double);
    int shm_id = shmget(IPC_PRIVATE, array_size * 5, IPC_CREAT | 0666);
    if (shm_id < 0) { perror("shmget"); exit(1); }
    
    double* shm_ptr = (double*)shmat(shm_id, NULL, 0);
    double* shm_x    = shm_ptr;
    double* shm_y    = shm_ptr + N;
    double* shm_vx   = shm_ptr + (N * 2);
    double* shm_vy   = shm_ptr + (N * 3);
    double* shm_mass = shm_ptr + (N * 4);

    srand(42);
    for (int i = 0; i < N; i++) {
        shm_x[i] = (rand() % 1000) / 10.0;
        shm_y[i] = (rand() % 1000) / 10.0;
        shm_vx[i] = (rand() % 10) / 10.0;
        shm_vy[i] = (rand() % 10) / 10.0;
        shm_mass[i] = (rand() % 10000) + 1000.0;
    }

    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int p = 0; p < K; p++) {
        if (fork() == 0) { // Proceso Hijo
            int start_part = (N / K) * p;
            int end_part = (p == K - 1) ? N : start_part + (N / K);

            for (int i = start_part; i < end_part; i++) {
                double fx = 0.0, fy = 0.0;
                for (int j = 0; j < N; j++) {
                    if (i == j) continue;
                    double dx = shm_x[j] - shm_x[i];
                    double dy = shm_y[j] - shm_y[i];
                    double dist = sqrt(dx*dx + dy*dy) + 1e-9;
                    
                    double force = (G * shm_mass[i] * shm_mass[j]) / (dist * dist);
                    fx += force * (dx / dist);
                    fy += force * (dy / dist);
                }
                shm_vx[i] += (fx / shm_mass[i]) * DT;
                shm_vy[i] += (fy / shm_mass[i]) * DT;
                shm_x[i] += shm_vx[i] * DT;
                shm_y[i] += shm_vy[i] * DT;
            }
            shmdt(shm_ptr);
            exit(0);
        }
    }

    for (int p = 0; p < K; p++) {
        wait(NULL); // Padre espera
    }

    clock_gettime(CLOCK_MONOTONIC, &end);
    double elapsed = (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;

    cout << elapsed << endl;

    shmdt(shm_ptr);
    shmctl(shm_id, IPC_RMID, NULL);

    return 0;
}