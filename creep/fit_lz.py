import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.signal import savgol_filter
from scipy.optimize import curve_fit
from logplotter import find_data

R = 8.31  # J/mol/K
T = 500  # K


def lz_analysis(output_file, input_files):

    datas = map(find_data, input_files)

    t = []
    lz = []

    for data in datas:
        t += data["Step"]
        lz += data["Lz"]

    dt = (
        0.5e-6
        if ("water" in input_files[0] or "passivated" in input_files[0])
        else 2e-6
    )

    t = np.asarray(t) * dt
    lz = np.asarray(lz)

    # plt.plot(t, lz)
    # plt.show()
    # sys.exit()

    N = len(t)
    window_length = N // 40 + (N // 40) % 2 + 1
    lz_smooth = savgol_filter(lz, window_length, 3)

    # t, lz = np.loadtxt("data/lz.dat", unpack=True)

    t = t[:: len(t) // 1000]
    lz = lz[:: len(lz) // 1000]
    lz_smooth = lz_smooth[:: len(lz_smooth) // 1000]

    def prediction(t, tc, h0, V0):
        return h0 - tc * V0 * np.log(1 + t / tc)

    def t_predict(h, tc, h0, V0):
        return tc * (np.exp((h0 - h) / (V0 * tc)) - 1)

    # parameters, covariances = curve_fit(
    #     t_predict, lz, t, maxfev=10000, p0=[0.1, 120.0, 1.0]
    # )

    parameters, covariances = curve_fit(prediction, t, lz_smooth, maxfev=10000)

    # parameters, covariances = curve_fit(
    #     prediction, t, lz_smooth, bounds=(0.0001, (10, 150, 30)), maxfev=10000, method="trf"
    # )

    tc, h0, V0 = parameters
    uncertainty = np.sqrt(np.diag(covariances))

    lz_predict = prediction(t, tc, h0, V0)

    if __name__ == "__main__":
        plt.plot(t, lz, label="raw data")
        plt.plot(t, lz_smooth, label="smooth")
        plt.plot(t, lz_predict, label="$h_0 - C\cdot\log(1+t/t_c)$")
        plt.legend()
        plt.xlabel("$t$ [ns]")
        plt.ylabel("$L_z$ [Å]")
        plt.savefig(output_file[:-4] + "_lz.png")

        print(f"tc = {tc} +- {uncertainty[0]}")
        print(f"h0 = {h0} +- {uncertainty[1]}")
        print(f"V0 = {V0} +- {uncertainty[2]}")

    np.savetxt(
        output_file,
        np.column_stack((t, lz, lz_predict, lz_smooth)),
    )

    return tc, uncertainty[0], h0, uncertainty[1], V0, uncertainty[2]


if __name__ == "__main__":
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    lz_analysis(output_file, input_files)
