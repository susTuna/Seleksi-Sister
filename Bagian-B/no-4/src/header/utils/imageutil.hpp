#ifndef __IMAGEUTIL_HPP__
#define __IMAGEUTIL_HPP__

#include <string>
#include "algorithm/mandelbrot.hpp"
#include <FreeImage.h>
#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <cmath>

typedef struct Color {
    BYTE r, g, b;
};

void renderSerial(int width, int height, int maxIterations,
                  const std::string& filename);

void renderParallel(int width, int height, int maxIterations,
                    const std::string& filename);

void renderTile(int tile_x_index, int tile_y_index,
                int tile_width, int tile_height,
                int image_width, int image_height,
                int maxIterations, const std::string& filename);

std::vector<Color> createPalette(int size);

#endif // __IMAGEUTIL_HPP__