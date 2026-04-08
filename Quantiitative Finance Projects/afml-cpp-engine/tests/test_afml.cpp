#include <iostream>
#include <cassert>
#include "afml_engine.hpp"

void test_cusum() {
    CusumFilter filter(10.0);
    assert(filter.update(11.0) == true);
    std::cout << "CUSUM: PASSED" << std::endl;
}

void test_barriers() {
    int result = -999;
    auto cb = [&](uint64_t ts, int label) { (void)ts; result = label; };
    
    // Test with a smaller buffer size to ensure template works
    TripleBarrierEngine<16> engine({2.0, 1.0, 1000}, 0.01, cb);

    engine.on_tick({100, 100.0, 1.0}); 
    engine.on_tick({200, 98.0, 1.0});  
    assert(result == -1);
    std::cout << "Barrier: PASSED" << std::endl;
}

int main() {
    test_cusum();
    test_barriers();
    return 0;
}