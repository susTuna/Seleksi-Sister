#ifndef __IMAGEUTIL_HPP__
#define __IMAGEUTIL_HPP__

#include <string>
#include "algorithm/mandelbrot.hpp"
#include <FreeImage.h>
#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <future>
#include <cmath>

typedef struct Color {
    BYTE r, g, b;
};

#define TILE_WIDTH 1024 //px
#define TILE_HEIGHT 1024 //px

const long double MIN_REAL = -2.5;
const long double MAX_REAL = 1.0;
const long double MIN_IMAG = -1.5;
const long double MAX_IMAG = 1.5;

FIBITMAP* renderSerial(int width, int height, int maxIterations);

FIBITMAP* renderParallel(int width, int height, int maxIterations);

FIBITMAP* renderTile(int tile_x_index, int tile_y_index,
                int tile_width, int tile_height,
                int image_width, int image_height,
                int maxIterations);

std::vector<Color> createPalette(int size);

bool saveImage(const FREE_IMAGE_FORMAT format, FIBITMAP* bitmap, const std::string& filename);

#endif // __IMAGEUTIL_HPP__