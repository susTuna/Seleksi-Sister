#ifndef __GPUACCEL_HPP__
#define __GPUACCEL_HPP__

#include "utils/imageutil.hpp"
#include <CL/cl.h>

FIBITMAP* renderOpenCL(int width, int height, int maxIterations); 

#endif // __GPUACCEL_HPP__