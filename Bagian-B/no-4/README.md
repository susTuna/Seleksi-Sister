# Mandelbrot Set Renderer

A high-performance Mandelbrot set fractal renderer implemented in C++ with support for serial, parallel (multi-threaded), and GPU-accelerated (OpenCL) rendering modes.

## Features

- **Multiple Rendering Modes:**
  - Serial (single-threaded) rendering
  - Parallel (multi-threaded) rendering  
  - OpenCL GPU acceleration
- **Flexible Output:** Support for PNG and BMP image formats
- **Performance Benchmarking:** Built-in benchmark suite to compare rendering methods
- **Cross-platform:** Windows and Linux support

## Dependencies

### Required Libraries
- **FreeImage** - Image loading, saving and manipulation library
- **OpenCL** - GPU acceleration support

### Installation

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install libfreeimage-dev opencl-headers ocl-icd-opencl-dev
```

#### Linux (Arch)
```bash
sudo pacman -S freeimage opencl-headers opencl-icd-loader
```

#### Windows
- Download FreeImage binaries from [FreeImage website](http://freeimage.sourceforge.net/)
- Install OpenCL SDK (usually comes with GPU drivers)

## Building

The project uses a Makefile with support for both Windows (MinGW) and Linux compilation.

### Linux
```bash
make linux
```

### Windows (using MinGW cross-compiler)
```bash
make windows
```

### Build Everything
```bash
make build
```

### Build Benchmarks
```bash
make benchmark
```

### Clean Build Files
```bash
make clean
```

## Usage

### Main Application
Run the compiled executable:

#### Linux
```bash
./bin/MandelbrotOfMadness
```

#### Windows
```bash
./bin/MandelbrotOfMadness.exe
```

The program will prompt you for:
1. Image resolution (width and height)
2. Rendering mode (1: Serial, 2: Parallel, 3: OpenCL)
3. Output filename with extension (.png or .bmp)

### Example Session
```
Set image resolution (e.g 1920 1080): 1920 1080
Rendering a 1920x1080px Mandelbrot set with 256 max iterations.
Choose a rendering mode:
1. Serial (single-threaded)
2. Parallel (multi-threaded)
3. OpenCL (GPU acceleration)
Enter your choice (1 - 3): 3
Choose an output filename (with extension): mandelbrot.png
Rendered using OpenCL.
Image saved as mandelbrot.png
```

### Benchmark Mode
Run the benchmark executable to compare performance across different rendering methods:

#### Linux
```bash
./bin/Benchmark
```

#### Windows
```bash
./bin/Benchmark.exe
```

The benchmark will automatically test all rendering modes at various resolutions and iteration counts, providing performance comparisons.

## Configuration

- **Max Iterations:** Currently set to 256 (defined in [`main.cpp`](no-4/src/main.cpp))
- **Supported Formats:** PNG (default) and BMP
- **Default Resolutions (Benchmark):** 1024x768, 1920x1080, 3840x2160

## Project Structure

```
no-4/
├── makefile                 # Build configuration
├── src/
│   ├── main.cpp            # Main application entry point
│   ├── benchmark.cpp       # Benchmark suite
│   ├── algorithm/          # Mandelbrot calculation algorithms
│   ├── gpuaccel/          # OpenCL GPU acceleration
│   ├── imageutil/         # Image utility functions
│   └── header/            # Header files
└── bin/                   # Compiled executables
```

## Performance

The OpenCL implementation provides significant speedup over serial rendering, especially for higher resolutions and iteration counts. Use the benchmark mode to measure performance on your specific hardware.

## Requirements

- C++17 compatible compiler
- OpenCL-capable GPU (for GPU acceleration mode)
- Sufficient RAM for high-resolution images