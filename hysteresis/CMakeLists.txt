cmake_minimum_required(VERSION 3.9)

project(hysteresis)

find_package(MPI REQUIRED)

cmake_host_system_information(RESULT host QUERY HOSTNAME)

set(GPUS "1" CACHE STRING "GPUs on bigfacet")

if(host MATCHES "hp")
    set(lmpcmd ${MPIEXEC} lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "bigfacet")
    set(lmpcmd ${MPIEXEC} -n ${GPUS} /lammps/lammps_kokkos2/src/lmp_kokkos_cuda_mpi -k on g ${GPUS} -sf kk -pk kokkos newton on neigh half binsize 7.5 -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "smaug")
    set(lmpcmd ${MPIEXEC} ~/lammps/build/lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
elseif(host MATCHES "ifi.uio.no")
    set(lmpcmd ${MPIEXEC} -np 32 lmp -var INDIR ${CMAKE_CURRENT_SOURCE_DIR} -var OUTDIR ${CMAKE_CURRENT_BINARY_DIR})
else()
    message(SEND_ERROR "hostname not recognised")
endif()

message(STATUS "Selected LAMMPs command: ${lmpcmd}")

add_custom_target(hysteresis ALL DEPENDS dump.hysteresis.bin)
add_custom_command(
    OUTPUT dump.hysteresis.bin
    COMMAND ${lmpcmd} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.hysteresis
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/in.hysteresis restart.system
)
add_custom_command(
    OUTPUT restart.system
    COMMAND ${lmpcmd} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.make_system
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/in.make_system ${CMAKE_CURRENT_SOURCE_DIR}/in.common_variables ${CMAKE_CURRENT_SOURCE_DIR}/in.common_regions restart.amorphous
)
add_custom_command(
    OUTPUT restart.amorphous
    COMMAND ${lmpcmd} -in ${CMAKE_CURRENT_SOURCE_DIR}/in.make_amorphous
    DEPENDS  ${CMAKE_CURRENT_SOURCE_DIR}/in.make_amorphous ${CMAKE_CURRENT_SOURCE_DIR}/in.common_variables ${CMAKE_CURRENT_SOURCE_DIR}/in.potential ${CMAKE_CURRENT_SOURCE_DIR}/betacristobalite.data
)
