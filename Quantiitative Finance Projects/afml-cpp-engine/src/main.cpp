#include <iostream>
#include <chrono>
#include "afml_engine.hpp"

int main() {
    std::cout << "Starting Zero-Allocation AFML Engine Simulation..." << std::endl;

    auto logger = [](uint64_t ts, int label) {
        std::cout << "[Event] TS: " << ts << " | Label: " << label << std::endl;
    };

    TripleBarrierEngine<1024>::BarrierConfig config{2.0, 1.0, 1000000000}; 
    TripleBarrierEngine<1024> engine(config, 0.01, logger); // Note the <1024>
    CusumFilter filter(0.005);

    std::vector<Tick> ticks = {
        {1000, 100.0, 10},
        {2000, 100.5, 5},
        {3000, 102.1, 20}, 
        {4000, 99.0, 15}    
    };

    double last_price = ticks[0].price;
    for (const auto& t : ticks) {
        if (filter.update(t.price - last_price)) {
            engine.on_tick(t);
        }
        last_price = t.price;
    }

    return 0;
}