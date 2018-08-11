cmake_minimum_required(VERSION 3.7)

project(hysteresis)

find_package(MPI REQUIRED)

cmake_host_system_information(RESULT host QUERY HOSTNAME)

set(GPUS "1" CACHE STRING "GPUs on bigfacet")

if(host MATCHES "hp")
    set(lmpcmd ${MPIEXEC} lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "bigfacet")
    set(lmpcmd ${MPIEXEC} -n ${GPUS} /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g ${GPUS} -sf kk -pk kokkos newton on neigh half binsize 7.5 -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
    set(lmpcmd_one ${MPIEXEC} -n 1 /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g 1 -sf kk -pk kokkos newton on neigh half binsize 7.5 -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "smaug")
    set(lmpcmd ${MPIEXEC} ~/lammps/build/lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
    set(lmpcmd_one ${MPIEXEC} -n 1 ~/lammps/build/lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "ifi.uio.no")
    set(lmpcmd ${MPIEXEC} -np 32 lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
    set(lmpcmd_one ${MPIEXEC} -np 1 lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "compute-") # abel
    set(lmpcmd mpirun lmp_intel_cpu_intelmpi -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
    set(lmpcmd_one mpirun -n 1 lmp_intel_cpu_intelmpi -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
else()
    message(SEND_ERROR "hostname not recognised")
endif()

message(STATUS "Selected LAMMPs command: ${lmpcmd}")

foreach(suffix SiO2)
add_custom_target(hysteresis_${suffix} ALL DEPENDS dump.hysteresis_${suffix}.bin)
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/dump.hysteresis_${suffix}.bin
    COMMAND ${lmpcmd} -var SUFFIX ${suffix} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.hysteresis
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/in.hysteresis ${CMAKE_CURRENT_BINARY_DIR}/data.system_${suffix}
)
endforeach(suffix)
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/data.system_SiO2
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_BINARY_DIR}/data.system ${CMAKE_CURRENT_BINARY_DIR}/data.system_SiO2
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/data.system
)
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/restart.system ${CMAKE_CURRENT_BINARY_DIR}/data.system
    COMMAND ${lmpcmd} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.make_system
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/in.make_system ${CMAKE_CURRENT_SOURCE_DIR}/in.common_variables ${CMAKE_CURRENT_SOURCE_DIR}/in.common_regions ${CMAKE_CURRENT_BINARY_DIR}/restart.amorphous
)
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/restart.amorphous
    COMMAND ${lmpcmd} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.make_amorphous
    DEPENDS  ${CMAKE_CURRENT_SOURCE_DIR}/in.make_amorphous ${CMAKE_CURRENT_SOURCE_DIR}/in.common_variables ${CMAKE_CURRENT_SOURCE_DIR}/data.betacristobalite
)
