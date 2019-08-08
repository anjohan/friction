from scipy.optimize import curve_fit
from pylab import *

R = 8.31

T = array([400, 450, 500, 550])
tc = array([4.66, 2.4, 0.96, 0.23])
V0 = array([0.11, 0.27, 0.72, 2.59])

a, b = polyfit(1 / T, log(tc), deg=1)
E_tc = R * a
a, b = polyfit(1 / T, log(V0), deg=1)


def logV0_prediction(T, C, Q, B0):
    return C - Q / (R * T) * (1 - B0 * exp(-0.0006 * T))


params, cov = curve_fit(logV0_prediction, T, log(V0), maxfev=10000)

C, Q, B0 = params
Qfit = Q

B = B0 * exp(-0.0006 * T)
Q = E_tc / (1 - B)

print(E_tc, Q, B)
d = 80

tc_estimate = R * T * d / (B * Q * V0)


print("Q: ", Qfit)
print("T: ", T)
print("B: ", B)
print("E_tc: ", E_tc)

subplots(2, 1)
subplot(2, 1, 1)
plot(T, V0, label="results")
plot(T, exp(logV0_prediction(T, C, Qfit, B0)), label="prediction")
legend()
xlabel("T")
ylabel("V0")
title("V0, comparison of measurement and fit")

subplot(2, 1, 2)
plot(T, tc, label="results")
plot(T, tc_estimate, label="prediction")
xlabel("T")
ylabel("tc")
legend()
title("tc, comparison of measurement and prediction")

tight_layout()
show()
