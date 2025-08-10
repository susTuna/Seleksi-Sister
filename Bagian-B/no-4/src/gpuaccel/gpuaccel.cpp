#include "gpuaccel/gpuaccel.hpp"

using namespace std;

const char* mandelbrotKernel = R"(
__kernel void mandelbrot(__global uchar *image, const int width, const int height, 
                        const float xMin, const float xMax, 
                        const float yMin, const float yMax, const int maxIterations) {
    int x = get_global_id(0);
    int y = get_global_id(1);

    if (x >= width || y >= height) return;

    float real = xMin + (xMax - xMin) * ((float)x / (width - 1));
    float imag = yMin + (yMax - yMin) * ((float)y / (height - 1));
    
    float zr = 0.0f;
    float zi = 0.0f;
    float zr2 = 0.0f;
    float zi2 = 0.0f;
    int iter = 0;
    
    float q = pow((real - 0.25f), 2) + pow(imag, 2);
    if (q * (q + (real - 0.25f)) < 0.25f * pow(imag, 2)) {
        iter = maxIterations;
    } else {
        while (iter < maxIterations && zr2 + zi2 < 4.0f) {
            zi = 2.0f * zr * zi + imag;
            zr = zr2 - zi2 + real;
            zr2 = zr * zr;
            zi2 = zi * zi;
            iter++;
        }
    }

    uchar r, g, b;
    
    if (iter == maxIterations) {
        r = 0;
        g = 0;
        b = 25;
    } else {
        float normalized = (float)iter / maxIterations;

        r = (uchar)(255 * normalized);
        g = (uchar)(255 * normalized);
        b = (uchar)(255 - 255 * normalized);
    }

    int pixelIndex = (y * width + x) * 3;
    image[pixelIndex]     = b;  // B
    image[pixelIndex + 1] = g;  // G
    image[pixelIndex + 2] = r;  // R
}
)";

FIBITMAP* renderOpenCL(int width, int height, int maxIterations) {
    cl_int err;
    cl_platform_id platform;
    cl_device_id device;
    cl_context context;
    cl_command_queue queue;
    cl_mem imageBuffer;
    cl_program program;
    cl_kernel kernel;

    err = clGetPlatformIDs(1, &platform, nullptr);
    if (err != CL_SUCCESS) throw runtime_error("Failed to get OpenCL platform: " + to_string(err));
    err = clGetDeviceIDs(platform, CL_DEVICE_TYPE_GPU, 1, &device, nullptr);
    if (err != CL_SUCCESS) throw runtime_error("Failed to get OpenCL device: " + to_string(err));
    char deviceName[256];
    clGetDeviceInfo(device, CL_DEVICE_NAME, sizeof(deviceName), deviceName, NULL);
    cout << "Using OpenCL device: " << deviceName << endl;

    context = clCreateContext(nullptr, 1, &device, nullptr, nullptr, &err);
    if (err != CL_SUCCESS) throw runtime_error("Failed to create OpenCL context: " + to_string(err));

    #ifdef CL_VERSION_2_0
    queue = clCreateCommandQueueWithProperties(context, device, 0, &err);
    #else
    queue = clCreateCommandQueue(context, device, 0, &err);
    #endif
    if (err != CL_SUCCESS) throw runtime_error("Failed to create command queue: " + to_string(err));

    program = clCreateProgramWithSource(context, 1, &mandelbrotKernel, nullptr, &err);
    if (err != CL_SUCCESS) throw runtime_error("Failed to create program: " + to_string(err));
    err = clBuildProgram(program, 1, &device, nullptr, nullptr, nullptr);
    if (err != CL_SUCCESS) {
        size_t logSize;
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, 0, nullptr, &logSize);
        vector<char> log(logSize);
        clGetProgramBuildInfo(program, device, CL_PROGRAM_BUILD_LOG, logSize, log.data(), nullptr);
        cerr << "OpenCL program build error: " << log.data() << endl;
        throw runtime_error("Failed to build OpenCL program");  
    }

    kernel = clCreateKernel(program, "mandelbrot", &err);
    if (err != CL_SUCCESS) throw runtime_error("Failed to create kernel: " + to_string(err));

    vector<unsigned char> imageData(width * height * 3);
    imageBuffer = clCreateBuffer(context, CL_MEM_WRITE_ONLY, imageData.size(), nullptr, &err);
    if (err != CL_SUCCESS) throw runtime_error("Failed to create image buffer: " + to_string(err));

    float xMin = static_cast<float>(MIN_REAL);
    float xMax = static_cast<float>(MAX_REAL);
    float yMin = static_cast<float>(MIN_IMAG);
    float yMax = static_cast<float>(MAX_IMAG);

    err = clSetKernelArg(kernel, 0, sizeof(cl_mem), &imageBuffer);
    err |= clSetKernelArg(kernel, 1, sizeof(int), &width);
    err |= clSetKernelArg(kernel, 2, sizeof(int), &height);
    err |= clSetKernelArg(kernel, 3, sizeof(float), &xMin);
    err |= clSetKernelArg(kernel, 4, sizeof(float), &xMax);
    err |= clSetKernelArg(kernel, 5, sizeof(float), &yMin);
    err |= clSetKernelArg(kernel, 6, sizeof(float), &yMax);
    err |= clSetKernelArg(kernel, 7, sizeof(int), &maxIterations);
    if (err != CL_SUCCESS) throw runtime_error("Failed to set kernel arguments: " + to_string(err));

    size_t globalWorkSize[2] = { static_cast<size_t>(width), static_cast<size_t>(height) };
    size_t maxWorkGroupSize;
    clGetDeviceInfo(device, CL_DEVICE_MAX_WORK_GROUP_SIZE, sizeof(maxWorkGroupSize), &maxWorkGroupSize, nullptr);
    size_t workGroupSide = 16;
    while (workGroupSide * workGroupSide > maxWorkGroupSize) {
        workGroupSide /= 2;
    }
    size_t localWorkSize[2] = { workGroupSide, workGroupSide };
    cout << "Using work group size: " << localWorkSize[0] << "x" << localWorkSize[1] << endl;

    err = clEnqueueNDRangeKernel(queue, kernel, 2, nullptr, globalWorkSize, localWorkSize, 0, nullptr, nullptr);
    if (err != CL_SUCCESS) {
        cout << "Work group size failed, trying with default size." << endl;
        err = clEnqueueNDRangeKernel(queue, kernel, 2, nullptr, globalWorkSize, nullptr, 0, nullptr, nullptr);
        if (err != CL_SUCCESS) throw runtime_error("Failed to execute kernel: " + to_string(err));
    }

    err = clEnqueueReadBuffer(queue, imageBuffer, CL_TRUE, 0, imageData.size(), imageData.data(), 0, nullptr, nullptr);
    if (err != CL_SUCCESS) throw runtime_error("Failed to read results: " + to_string(err));

    FIBITMAP* bitmap = FreeImage_Allocate(width, height, 24);
    if (!bitmap) throw runtime_error("Failed to allocate FreeImage bitmap");

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int pixelIndex = (y * width + x) * 3;
            RGBQUAD color;
            color.rgbRed = imageData[pixelIndex + 2];   // R
            color.rgbGreen = imageData[pixelIndex + 1]; // G
            color.rgbBlue = imageData[pixelIndex];       // B
            FreeImage_SetPixelColor(bitmap, x, y, &color);
        }
    }
    clReleaseMemObject(imageBuffer);
    clReleaseKernel(kernel);
    clReleaseProgram(program);
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
    return bitmap;
}