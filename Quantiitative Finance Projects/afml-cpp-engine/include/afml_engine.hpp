#ifndef AFML_ENGINE_HPP
#define AFML_ENGINE_HPP

#include <vector>
#include <cmath>
#include <algorithm>
#include <functional>
#include <array>

/**
 * HFT-GRADE AFML ENGINE
 * Refactor: Added Fixed-Width Window Fractional Differentiation (Ch. 5)
 */

struct Tick {
    uint64_t timestamp;
    double price;
    double volume;
};

/**
 * Fractional Differentiation Engine (FFD)
 * Stationarizes a price series while maintaining maximum memory.
 * Weights are pre-computed at compile-time/construction.
 */
template<size_t WindowSize = 256>
class FracDiffEngine {
public:
    explicit FracDiffEngine(double d) : d_(d), head_(0), count_(0) {
        compute_weights();
    }

    /**
     * Hot Path: Updates the window and returns the differentiated value.
     * Complexity: O(WindowSize) per tick.
     */
    double update(double price) {
        // Store price in circular buffer
        prices_[head_] = price;
        head_ = (head_ + 1) % WindowSize;
        if (count_ < WindowSize) count_++;

        if (count_ < WindowSize) return 0.0; // Wait for buffer to fill

        double result = 0.0;
        size_t curr = (head_ + WindowSize - 1) % WindowSize; // Start at latest price
        
        // Apply dot product of weights and historical prices
        for (size_t i = 0; i < WindowSize; ++i) {
            result += weights_[i] * prices_[curr];
            curr = (curr + WindowSize - 1) % WindowSize; // Move backwards in time
        }
        return result;
    }

private:
    void compute_weights() {
        weights_[0] = 1.0;
        for (size_t k = 1; k < WindowSize; ++k) {
            weights_[k] = weights_[k - 1] * (d_ - static_cast<double>(k) + 1.0) / static_cast<double>(k) * -1.0;
        }
    }

    double d_;
    std::array<double, WindowSize> weights_;
    std::array<double, WindowSize> prices_;
    size_t head_;
    size_t count_;
};

class CusumFilter {
public:
    explicit CusumFilter(double threshold) : threshold_(threshold), s_pos_(0.0), s_neg_(0.0) {}
    inline bool update(double diff) {
        s_pos_ = std::max(0.0, s_pos_ + diff);
        s_neg_ = std::min(0.0, s_neg_ + diff);
        if (s_pos_ > threshold_) { s_pos_ = 0.0; return true; }
        if (s_neg_ < -threshold_) { s_neg_ = 0.0; return true; }
        return false;
    }
private:
    double threshold_, s_pos_, s_neg_;
};

template<size_t MaxPositions = 1024>
class TripleBarrierEngine {
public:
    struct BarrierConfig { double pt_multiplier; double sl_multiplier; uint64_t expiration_ns; };
    using LabelCallback = std::function<void(uint64_t, int)>;

    TripleBarrierEngine(BarrierConfig config, double vol_estimate, LabelCallback cb) 
        : config_(config), vol_(vol_estimate), on_label_(cb), head_(0), tail_(0), count_(0) {}

    void on_tick(const Tick& tick) {
        if (count_ < MaxPositions) {
            auto& pos = buffer_[tail_];
            pos.entry_price = tick.price;
            pos.tp_price = tick.price * (1.0 + config_.pt_multiplier * vol_);
            pos.sl_price = tick.price * (1.0 - config_.sl_multiplier * vol_);
            pos.expiry_time = tick.timestamp + config_.expiration_ns;
            pos.active = true;
            tail_ = (tail_ + 1) % MaxPositions;
            count_++;
        }

        size_t current = head_;
        for (size_t i = 0; i < count_; ++i) {
            auto& pos = buffer_[current];
            if (pos.active) {
                int sign = 0; bool closed = false;
                if (tick.price >= pos.tp_price) { sign = 1; closed = true; }
                else if (tick.price <= pos.sl_price) { sign = -1; closed = true; }
                else if (tick.timestamp >= pos.expiry_time) { sign = 0; closed = true; }
                if (closed) { if (on_label_) on_label_(tick.timestamp, sign); pos.active = false; }
            }
            if (current == head_ && !pos.active) { head_ = (head_ + 1) % MaxPositions; count_--; }
            current = (current + 1) % MaxPositions;
        }
    }

private:
    struct ActivePosition { double entry_price, tp_price, sl_price; uint64_t expiry_time; bool active = false; };
    std::array<ActivePosition, MaxPositions> buffer_;
    BarrierConfig config_; double vol_; LabelCallback on_label_;
    size_t head_, tail_, count_;
};

#endif