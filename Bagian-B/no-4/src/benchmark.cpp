#include "utils/imageutil.hpp"
#include "gpuaccel/gpuaccel.hpp"
#include <iostream>
#include <iomanip>
#include <chrono>
#include <vector>
#include <string>

using namespace std;
using namespace chrono;

struct BenchmarkResult {
    string method;
    int width;
    int height;
    int iterations;
    double executionTime; // in milliseconds
};

BenchmarkResult runBenchmark(const string& method, int width, int height, int maxIterations) {
    BenchmarkResult result;
    result.method = method;
    result.width = width;
    result.height = height;
    result.iterations = maxIterations;
    
    FIBITMAP* bitmap;
    
    auto start = high_resolution_clock::now();
    
    if (method == "Serial") {
        bitmap = renderSerial(width, height, maxIterations);
    } else if (method == "Parallel") {
        bitmap = renderParallel(width, height, maxIterations);
    } else if (method == "OpenCL") {
        bitmap = renderOpenCL(width, height, maxIterations);
    }
    
    auto end = high_resolution_clock::now();
    result.executionTime = duration_cast<milliseconds>(end - start).count();
    
    FreeImage_Unload(bitmap);
    
    return result;
}

int main() {
    vector<pair<int, int>> resolutions = {
        {1024, 768},
        {1920, 1080},
        {3840, 2160}
    };
    
    vector<int> iterations = {100, 500};
    vector<string> methods = {"Serial", "Parallel", "OpenCL"};
    
    vector<BenchmarkResult> results;
    
    cout << "Running Mandelbrot Set Rendering Benchmarks..." << endl;
    cout << "==============================================" << endl;
    
    for (const auto& resolution : resolutions) {
        for (int maxIter : iterations) {
            for (const auto& method : methods) {
                cout << "Benchmarking " << method << " at " << resolution.first << "x" << resolution.second 
                     << " with " << maxIter << " iterations... ";
                cout.flush();
                
                BenchmarkResult result = runBenchmark(method, resolution.first, resolution.second, maxIter);
                results.push_back(result);
                
                cout << "Done in " << result.executionTime << " ms" << endl;
            }
        }
    }
    
    // Print results table
    cout << "\nBenchmark Results:" << endl;
    cout << "=================" << endl;
    cout << left << setw(10) << "Method" 
         << right << setw(12) << "Resolution" 
         << right << setw(12) << "Iterations"
         << right << setw(15) << "Time (ms)"
         << right << setw(20) << "Speedup vs Serial" << endl;
    cout << string(69, '-') << endl;
    
    for (size_t i = 0; i < results.size(); i += methods.size()) {
        double serialTime = results[i].executionTime;
        
        for (size_t j = 0; j < methods.size(); j++) {
            const auto& result = results[i + j];
            double speedup = serialTime / result.executionTime;
            
            cout << left << setw(10) << result.method
                 << right << setw(5) << result.width << "x" << left << setw(5) << result.height
                 << right << setw(12) << result.iterations
                 << right << setw(15) << fixed << setprecision(2) << result.executionTime;
                 
            if (j == 0) {
                cout << right << setw(20) << "1.00x";
            } else {
                cout << right << setw(20) << fixed << setprecision(2) << speedup << "x";
            }
            cout << endl;
        }
        cout << string(69, '-') << endl;
    }
    
    return 0;
}