#include "algorithm/mandelbrot.hpp"

using namespace std;

MandelbrotResult calculateMandelbrot(complex<double> c, int maxIterations) {
    complex<double> z = 0;
    int iterations = 0;

    double q = pow((c.real() - 0.25), 2) + pow(c.imag(), 2);
    if (q * (q + (c.real() - 0.25)) < 0.25 * pow(c.imag(), 2)) {
        iterations = maxIterations; //quick bounce out
        return {iterations};
    }

    while (abs(z) <= 2.0 && iterations < maxIterations) {
        z = z * z + c;
        iterations++;
    }
    return {iterations};
}