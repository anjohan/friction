program lz_analysis
    use mod_lammps_reader
    use iso_fortran_env, only: real64
    implicit none

    type(lammps_reader) :: reader

    integer :: step = 0, step_interval = 100000
    integer :: u

    real(real64) :: dt = 2.0D-6, zmin, zmax

    open(newunit=u, file="data/lz.dat", action="write")

    do
        call reader%open_file("data/dump.creep.*.bin", step)

        if (.not. reader%has_next_step) exit

        write(*,*) step

        zmin = reader%next_header%boundary(1,3)
        zmax = reader%next_header%boundary(2,3)

        write(u, *) dt*step, zmax - zmin

        step = step + step_interval
    end do

    close(u)
end program
