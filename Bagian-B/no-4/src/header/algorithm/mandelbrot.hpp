#ifndef __MANDELBROT_HPP__
#define __MANDELBROT_HPP__

#include <complex>

struct MandelbrotResult {
    int iterations;
};

MandelbrotResult calculateMandelbrot(std::complex<double> c, int maxIterations);

#endif // __MANDELBROT_HPP__