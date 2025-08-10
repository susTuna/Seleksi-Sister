#include "utils/imageutil.hpp"

using namespace std;

vector<Color> createPalette(int size) {
    vector<Color> palette(size);
    for (int i = 0; i < size; ++i) {
        palette[i] = {
            (BYTE)(255 * (double)i / size),
            (BYTE)(255 * (double)i / size),
            (BYTE)(255 - 255 * (double)i / size)
        };
    }
    return palette;
}

bool saveImage(const FREE_IMAGE_FORMAT format, FIBITMAP* bitmap, const string& filename) {
    if (format == FIF_UNKNOWN) throw runtime_error("Unknown image format");
    else if (!bitmap) throw runtime_error("Bitmap is null");
    else if (!FreeImage_Save(format, bitmap, filename.c_str())) {
        FreeImage_Unload(bitmap);
        throw runtime_error("Failed to save image: " + filename);
    }
    FreeImage_Unload(bitmap);
    return true;
}

FIBITMAP* renderTile(int tile_x_index, int tile_y_index,
                int tile_width, int tile_height,
                int image_width, int image_height,
                int maxIterations) {
    FIBITMAP* bitmap = FreeImage_Allocate(tile_width, tile_height, 24);
    if (!bitmap) throw runtime_error("Failed to allocate image bitmap");

    auto palette = createPalette(maxIterations);
    
    for (int y = 0; y < tile_height; ++y) {
        for (int x = 0; x < tile_width; ++x) {
            int global_x = tile_x_index * tile_width + x;
            int global_y = tile_y_index * tile_height + y;

            double real = MIN_REAL + (static_cast<double>(global_x) / image_width) * (MAX_REAL - MIN_REAL);
            double imag = MIN_IMAG + (static_cast<double>(global_y) / image_height) * (MAX_IMAG - MIN_IMAG);

            complex<double> c(real, imag);
            MandelbrotResult result = calculateMandelbrot(c, maxIterations);
            RGBQUAD color;
            if (result.iterations != maxIterations) {
                color.rgbRed = palette[result.iterations % maxIterations].r;
                color.rgbGreen = palette[result.iterations % maxIterations].g;
                color.rgbBlue = palette[result.iterations % maxIterations].b;
                FreeImage_SetPixelColor(bitmap, x, y, &color);
            }
        }
    }
    return bitmap;
}

void renderSerial(int width, int height, int maxIterations,
                  const string& filename, FREE_IMAGE_FORMAT format) {
    FIBITMAP* bitmap = FreeImage_Allocate(width, height, 24);
    if (!bitmap) throw runtime_error("Failed to allocate image bitmap");

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            double real = MIN_REAL + (static_cast<double>(x) / width) * (MAX_REAL - MIN_REAL);
            double imag = MIN_IMAG + (static_cast<double>(y) / height) * (MAX_IMAG - MIN_IMAG);
            complex<double> c(real, imag);
            MandelbrotResult result = calculateMandelbrot(c, maxIterations);
            RGBQUAD color;
            if (result.iterations != maxIterations) {
                color.rgbRed = (BYTE)(255 * result.iterations / maxIterations);
                color.rgbGreen = (BYTE)(255 * result.iterations / maxIterations);
                color.rgbBlue = (BYTE)(255 - 255 * result.iterations / maxIterations);
                FreeImage_SetPixelColor(bitmap, x, y, &color);
            }
        }
    }
    saveImage(format, bitmap, filename);
}

void renderParallel(int width, int height, int maxIterations,
                    const string& filename, FREE_IMAGE_FORMAT format) {
    int num_tiles_x = ceil(static_cast<double>(width) / TILE_WIDTH);
    int num_tiles_y = ceil(static_cast<double>(height) / TILE_HEIGHT);

    vector<future<FIBITMAP*>> futures;
    for (int tile_y = 0; tile_y < num_tiles_y; ++tile_y) {
        for (int tile_x = 0; tile_x < num_tiles_x; ++tile_x) {
            futures.emplace_back(async(launch::async,renderTile, 
                tile_x, tile_y, 
                TILE_WIDTH, TILE_HEIGHT, 
                width, height, 
                maxIterations));
        }
    }

    FIBITMAP* final_bitmap = FreeImage_Allocate(width, height, 24);
    if (!final_bitmap) throw runtime_error("Failed to allocate final image bitmap");

    for (int tile_y = 0; tile_y < num_tiles_y; ++tile_y) {
        for (int tile_x = 0; tile_x < num_tiles_x; ++tile_x) {
            FIBITMAP* tile_bitmap = futures[tile_y * num_tiles_x + tile_x].get();
            if (!tile_bitmap) {
                cerr << "Failed to retreive bitmap." << endl;
                continue;
            }
            FreeImage_Paste(final_bitmap, tile_bitmap, tile_x * TILE_WIDTH, tile_y * TILE_HEIGHT, 255);
            FreeImage_Unload(tile_bitmap);
        }
    }
    saveImage(format, final_bitmap, filename);
}