echo "=========="
for T in $(seq 400 50 550); do
    echo $T
    python fit_lz.py quartz_T${T}.dat $(ls -v quartz_temp_data/log.creep_T${T}_*)
    echo "=========="
done
