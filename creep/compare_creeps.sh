echo "======"
echo "SiO2":
python fit_lz.py 50ns_sio2.dat $(ls -v SiO2_data/log.creep* | head -n 50)
echo "======"
echo "Passivated"
python fit_lz.py 50ns_passivated.dat $(ls -v passivated_data/log.creep_passivated*)
echo "======"
echo "Water"
python fit_lz.py 50ns_water.dat $(ls -v water_data/log.creep_water*)
echo "======"
