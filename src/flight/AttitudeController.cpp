// AttitudeController.cpp
// Quaternion PID controller for satellite attitude holding (±0.1 deg per axis)
// SentinelHunter Flight Core

#include <iostream>
#include <array>
#include <cmath>
#include <fstream>

/**
 * @brief Normalize a quaternion (4D vector)
 */
std::array<double, 4> normalize(const std::array<double, 4>& q) {
    double norm = std::sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3]);
    std::array<double, 4> out = q;
    for (int i = 0; i < 4; ++i) out[i] /= norm;
    return out;
}

/**
 * @brief Compute quaternion error (q_err = q_target * q_current^-1)
 * For minimal demo, assume q_current is close to q_target and use difference.
 */
std::array<double, 4> quat_error(const std::array<double, 4>& q_target, const std::array<double, 4>& q_current) {
    std::array<double, 4> err;
    for (int i = 0; i < 4; ++i) err[i] = q_target[i] - q_current[i];
    return normalize(err);
}

/**
 * @brief AttitudeController implements a quaternion PID controller for attitude stabilization.
 */
class AttitudeController {
public:
    AttitudeController() : kp(1.0), ki(0.0), kd(0.0), prev_error{0,0,0,0} {
        error = {0, 0, 0, 0};
        integral = {0, 0, 0, 0};
        derivative = {0, 0, 0, 0};
    }
    void setGains(double p, double i, double d) {
        kp = p; ki = i; kd = d;
    }
    std::array<double, 4> update(const std::array<double, 4>& q_target, const std::array<double, 4>& q_current) {
        error = quat_error(q_target, q_current);
        for (int i = 0; i < 4; ++i) {
            integral[i] += error[i];
            derivative[i] = error[i] - prev_error[i];
            prev_error[i] = error[i];
        }
        std::array<double, 4> output;
        for (int i = 0; i < 4; ++i) {
            output[i] = kp * error[i] + ki * integral[i] + kd * derivative[i];
        }
        return output;
    }
    void actuate(const std::array<double, 4>& control) {
        std::cout << "Simulated actuator command: ";
        for (auto v : control) std::cout << v << " ";
        std::cout << std::endl;
    }
    void output_telemetry(const std::array<double, 4>& q_current, const std::array<double, 4>& control) {
        std::ofstream out("telemetry.csv", std::ios::app);
        out << q_current[0] << ',' << q_current[1] << ',' << q_current[2] << ',' << q_current[3] << ',';
        out << control[0] << ',' << control[1] << ',' << control[2] << ',' << control[3] << '\n';
        out.close();
    }
private:
    double kp, ki, kd;
    std::array<double, 4> error, integral, derivative, prev_error;
};

int main() {
    AttitudeController ctrl;
    ctrl.setGains(1.0, 0.1, 0.01);
    std::array<double, 4> q_target = {1, 0, 0, 0};
    std::array<double, 4> q_current = {0.99, 0.01, 0, 0};
    auto output = ctrl.update(q_target, q_current);
    ctrl.actuate(output);
    ctrl.output_telemetry(q_current, output);
    return 0;
}
