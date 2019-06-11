echo "=========="
for T in $(seq 400 50 550); do
    echo $T
    python fit_lz.py T${T}.dat $(ls -v temp_data/log.creep_T${T}_*)
    echo "=========="
done
