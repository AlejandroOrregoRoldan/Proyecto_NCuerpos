CXX = g++
CXXFLAGS = -Wall -O3
LDFLAGS = -lm

all: bin/sequential bin/parallel_ipc

bin/sequential: src/sequential.cpp
	$(CXX) $(CXXFLAGS) src/sequential.cpp -o bin/sequential $(LDFLAGS)

bin/parallel_ipc: src/parallel_ipc.cpp
	$(CXX) $(CXXFLAGS) src/parallel_ipc.cpp -o bin/parallel_ipc $(LDFLAGS)

clean:
	rm -f bin/sequential bin/parallel_ipc