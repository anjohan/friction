import sys
from fit_lz import lz_analysis, find_data
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt


R = 8.31

T = np.array([400, 450, 500, 550], dtype=np.float64)
tc = np.zeros_like(T)
V0 = np.zeros_like(T)

Vs = []


def V0simple(T, V):
    return V * np.exp(-E_tc / (R * T))


for i, temp in enumerate(T):
    output = f"quartz_infinite_T{temp:.0f}.dat"
    inputs = [
        f"quartz_infinite_temp_data/log.creep_T{temp:.0f}_{i}" for i in range(1, 51)
    ]
    tc[i], tc_sigma, h0, h0_sigma, V0[i], V0_sigma = lz_analysis(output, inputs)

print(V0)
a, b = np.polyfit(1 / (R * T), np.log(V0), 1)
np.savetxt(
    "/home/anders/master/data/creep/V0.dat",
    np.column_stack((1 / (R * T), V0, np.exp(b + a / (R * T)))),
)

print("E_tc = ", a)
sys.exit()

h0s, BQs, tcs = np.zeros((3, 4))
for j, temp in enumerate(T):
    output = f"quartz_infinite_T{temp}.dat"
    inputs = [
        f"quartz_infinite_temp_data/log.creep_T{temp:.0f}_{i}" for i in range(1, 51)
    ]
    datas = map(find_data, inputs)

    t = []
    lz = []

    for data in datas:
        t += data["Step"]
        lz += data["Lz"]

    dt = 0.5e-6 if ("water" in inputs[0] or "passivated" in inputs[0]) else 2e-6

    t = np.asarray(t) * dt
    lz = np.asarray(lz)
    N = len(t)
    window_length = N // 40 + (N // 40) % 2 + 1
    lz_smooth = savgol_filter(lz, window_length, 3)
    lz = lz_smooth

    d = 55

    def h_predict(t, h0, BQ, tc):
        return h0 * (1 - R * temp / BQ * np.log(1 + t / tc))

    p, cov = curve_fit(h_predict, t, lz, maxfev=10000)
    h0, BQ, tc = p

    h0s[j] = h0
    BQs[j] = BQ
    tcs[j] = tc

    h_fit = h_predict(t, h0, BQ, tc)

    plt.plot(t, lz, label=f"T = {temp}, data")
    plt.plot(t, h_fit, label=f"T = {temp}, fit")


"""
    E_tc = 35e3

    def hsimple(t, tc, V, h0):
        return h0 - V * np.exp(-E_tc / (R * temp)) * tc * np.log(1 + t / tc)

    # dhdt = (lz[1:] - lz[:-1]) / dt
    # t = t[:-1] + 0.5 * dt

    p, cov = curve_fit(hsimple, t, lz, maxfev=10000, p0=[2.0, 100.0, 150.3])
    tc, V, h0 = p
    tc_sigma, V_sigma, h0_sigma = np.sqrt([cov[i, i] for i in range(3)])
    print("T: ", temp, "tc: ", tc, "V: ", V, "h0: ", h0)
    print("Uncertainty:", "T: ", "tc: ", tc_sigma, "V: ", V_sigma, "h0: ", h0_sigma)

    Vs.append(V)

    lz_fit = hsimple(t, tc, V, h0)
    plt.plot(t, lz, label=f"T = {temp}, results")
    plt.plot(t, lz_fit, label=f"T = {temp}, fit")
"""

print("T: ", T)
print("h0: ", h0s)
print("BQ: ", BQs)
print("tc: ", tcs)

print(R * T * d / BQs)


plt.legend()
plt.show()

plt.figure()
plt.plot(T, BQs)
plt.show()


"""
def expfit(T, C, E):
    return C * np.exp(-E / (R * T))


Vs = np.array(Vs)
p, cov = curve_fit(expfit, T, Vs)
true_V, deltaE = p

print("New V: ", true_V)
print("New activation energy: ", E_tc + deltaE)

plt.plot(1 / T, np.log(Vs), label="data")
plt.plot(1 / T, np.log(expfit(T, true_V, deltaE)), label="fit")
plt.legend()
plt.show()

print(T, tc, V0)
p, c = curve_fit(V0simple, T, V0)
print(p)
V = p[0]


# plt.plot(1 / T, np.log(V0))
# plt.plot(1 / T, np.log(V0simple(T, V)))
# plt.show()

a, b = np.polyfit(1 / (R * T), np.log(tc), deg=1)
E_tc = a
print("E_tc: ", E_tc)
a, b = np.polyfit(1 / (R * T), np.log(V0), deg=1)


def logV0_prediction(T, C, Q, B0):
    return C - Q / (R * T) * (1 - B0 * np.exp(-0.0006 * T))


def V0_prediction(T, V, Q, B0):
    return V * np.exp(-Q / (R * T) * (1 - B0 * np.exp(-0.0006 * T)))


params, cov = curve_fit(V0_prediction, T, V0, maxfev=10000)

V, Q, B0 = params
Qfit = Q

B = B0 * np.exp(-0.0006 * T)

print(E_tc, Q)
d = 80

tc_estimate = T * d / (B * Q * V0)


print("Q: ", Qfit)
print("T: ", T)
print("B: ", B)
print("E_tc: ", E_tc)

plt.subplots(2, 1)
plt.subplot(2, 1, 1)
plt.plot(T, V0, label="results")
plt.plot(T, V0_prediction(T, V, Qfit, B0), label="prediction")
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
"""
