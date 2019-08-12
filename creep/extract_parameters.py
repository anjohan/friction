from fit_lz import lz_analysis
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


R = 8.31

T = np.array([400, 450, 500, 550], dtype=np.float64)
tc = np.zeros_like(T)
V0 = np.zeros_like(T)

for i, temp in enumerate(T):
    output = f"quartz_infinite_T{temp}.dat"
    inputs = [
        f"quartz_infinite_temp_data/log.creep_T{temp:.0f}_{i}" for i in range(1, 51)
    ]
    tc[i], tc_sigma, h0, h0_sigma, V0[i], V0_sigma = lz_analysis(output, inputs)

print(T, tc, V0)

a, b = np.polyfit(1 / T, np.log(tc), deg=1)
E_tc = R * a
a, b = np.polyfit(1 / T, np.log(V0), deg=1)


def logV0_prediction(T, C, Q, B0):
    return C - Q / (R * T) * (1 - B0 * np.exp(-0.0006 * T))


params, cov = curve_fit(logV0_prediction, T, np.log(V0), maxfev=10000)

C, Q, B0 = params
Qfit = Q

B = B0 * np.exp(-0.0006 * T)
Q = E_tc / (1 - B)

print(E_tc, Q, B)
d = 80

tc_estimate = T * d / (B * Q * V0)


print("Q: ", Qfit)
print("T: ", T)
print("B: ", B)
print("E_tc: ", E_tc)

plt.subplots(2, 1)
plt.subplot(2, 1, 1)
plt.plot(T, V0, label="results")
plt.plot(T, np.exp(logV0_prediction(T, C, Qfit, B0)), label="prediction")
plt.legend()
plt.xlabel("T")
plt.ylabel("V0")
plt.title("V0, comparison of measurement and fit")

plt.subplot(2, 1, 2)
plt.plot(T, tc, label="results")
plt.plot(T, tc_estimate, label="prediction")
plt.xlabel("T")
plt.ylabel("tc")
plt.legend()
plt.title("tc, comparison of measurement and prediction")

plt.tight_layout()
plt.show()
