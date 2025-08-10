CXX = g++
MINGW =  x86_64-w64-mingw32
CXXFLAGS = -Wall -Wextra -O2 -std=c++17 -I ./src/header/
LDFLAGS = -lfreeimage -lOpenCL
LWINDOWS = -IL./src/lib/
SRC = src/algorithm/mandelbrot.cpp src/gpuaccel/gpuaccel.cpp src/imageutil/imageutil.cpp
MAIN = src/main.cpp
BENCH = src/benchmark.cpp
BIN = ./bin

BM = Benchmark
EXEC = MandelbrotOfMadness

windows:
	mkdir -p $(BIN) 
	$(MINGW)-$(CXX) $(CXXFLAGS) -o $(BIN)/$(EXEC).exe $(MAIN) $(SRC) $(LWINDOWS) $(LDFLAGS)

linux: 
	mkdir -p $(BIN)
	$(CXX) $(CXXFLAGS) -o $(BIN)/$(EXEC) $(MAIN) $(SRC) $(LDFLAGS)

windows-bench:
	mkdir -p $(BIN)
	$(MINGW)-$(CXX) $(CXXFLAGS) -o $(BIN)/$(BM).exe $(BENCH) $(SRC) $(LWINDOWS) $(LDFLAGS)

linux-bench:
	mkdir -p $(BIN)
	$(CXX) $(CXXFLAGS) -o $(BIN)/$(BM) $(BENCH) $(SRC) $(LDFLAGS)

build: windows linux

benchmark: windows-bench linux-bench

clean:
	rm -rf $(BIN)/*.exe
	rm -rf $(BIN)/$(LINUX)

all: build benchmark