CXX = clang++
CXXFLAGS = -std=c++17 -Wall -Wextra -O3 -I./include

# Targets
ENGINE_BIN = afml_engine
TEST_BIN = test_suite
BENCH_BIN = bench_suite
FRAC_TEST = test_frac

all: $(ENGINE_BIN) $(TEST_BIN) $(BENCH_BIN) $(FRAC_TEST)

$(ENGINE_BIN): src/main.cpp include/afml_engine.hpp
	$(CXX) $(CXXFLAGS) src/main.cpp -o $(ENGINE_BIN)

$(TEST_BIN): tests/test_afml.cpp include/afml_engine.hpp
	$(CXX) $(CXXFLAGS) tests/test_afml.cpp -o $(TEST_BIN)

$(BENCH_BIN): benchmarks/bench_afml.cpp include/afml_engine.hpp
	$(CXX) $(CXXFLAGS) benchmarks/bench_afml.cpp -o $(BENCH_BIN)

$(FRAC_TEST): tests/test_fracdiff.cpp include/afml_engine.hpp
	$(CXX) $(CXXFLAGS) tests/test_fracdiff.cpp -o $(FRAC_TEST)

clean:
	rm -f $(ENGINE_BIN) $(TEST_BIN) $(BENCH_BIN) $(FRAC_TEST)

.PHONY: all clean