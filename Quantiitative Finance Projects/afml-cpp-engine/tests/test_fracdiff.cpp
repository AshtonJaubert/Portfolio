#include <iostream>
#include <cassert>
#include <cmath>
#include "afml_engine.hpp"

/**
 * Testing Fractional Differentiation Correctness
 */

void test_fracdiff_logic() {
    std::cout << "Testing Fractional Differentiation (d=1.0)... ";
    
    // d=1.0 is just a first-difference: Price(t) - Price(t-1)
    FracDiffEngine<2> engine(1.0);
    
    engine.update(100.0); // Fill buffer
    double diff = engine.update(105.0);
    
    // Expecting 105 - 100 = 5.0
    assert(std::abs(diff - 5.0) < 1e-6);
    std::cout << "PASSED" << std::endl;
}

void test_fracdiff_d0() {
    std::cout << "Testing Fractional Differentiation (d=0.0)... ";
    
    // d=0.0 should return the original series (no change)
    FracDiffEngine<5> engine(0.0);
    
    engine.update(100.0);
    engine.update(100.0);
    engine.update(100.0);
    engine.update(100.0);
    double val = engine.update(110.0);
    
    assert(std::abs(val - 110.0) < 1e-6);
    std::cout << "PASSED" << std::endl;
}

int main() {
    test_fracdiff_logic();
    test_fracdiff_d0();
    return 0;
}