#include "utils/imageutil.hpp"
#include "gpuaccel/gpuaccel.hpp"
#include <iostream>

using namespace std;

#define MAX_ITERATIONS 256

int main() {
    try {
        FreeImage_Initialise();
        cout << "Set image resolution (e.g 1920 1080): ";
        int width, height;
        cin >> width >> height;
        if (width <= 0 || height <= 0) throw runtime_error("Invalid image dimensions.");
        cout << "Rendering a " << width << "x" << height << "px Mandelbrot set with " << MAX_ITERATIONS << " max iterations." << endl;
        cout << "Choose a rendering mode:" << endl;
        cout << "1. Serial (single-threaded)" << endl;
        cout << "2. Parallel (multi-threaded)" << endl;
        cout << "3. OpenCL (GPU acceleration)" << endl;
        cout << "Enter your choice (1 - 3): ";
        int choice;
        cin >> choice;
        cout << "Choose an output filename (with extension): ";
        string filename;
        FREE_IMAGE_FORMAT format = FIF_PNG; // Default format
        FIBITMAP* bitmap;
        cin >> filename;
        if (filename.empty()) throw runtime_error("Filename cannot be empty.");
        if (filename.substr(filename.find_last_of(".") + 1) == "bmp") format = FIF_BMP;
        switch (choice) {
            case 2:
                bitmap = renderParallel(width, height, MAX_ITERATIONS);
                cout << "Rendered in parallel mode." << endl;
                break;
            case 3:
                bitmap = renderOpenCL(width, height, MAX_ITERATIONS);
                cout << "Rendered using OpenCL." << endl;
                break;
            default:
                bitmap = renderSerial(width, height, MAX_ITERATIONS);
                cout << "Rendered in serial mode." << endl;
                break;
        }
        saveImage(format, bitmap, filename);
        cout << "Image saved as " << filename << endl;
        FreeImage_DeInitialise();
        return 0;
    }
    catch (const exception& e) {
        cerr << e.what() << endl;
        return 1;
    }
    
}