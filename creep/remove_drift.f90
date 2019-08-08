program remove_drift
    use mod_lammps_reader
    use iso_fortran_env, only: dp => real64

    implicit none

    type(lammps_reader) :: reader

    integer :: step, dstep = 100000, u, i

    logical, dimension(:), allocatable :: is_interesting
    integer(int64) :: num_interesting, num_atoms
    integer, dimension(:), allocatable :: interesting_idx

    real(dp) :: xmin, ymin, zmin, lx, ly, lz, xmid, ymid, zmid

    call reader%open_file("water_data/dump.creep_water.0.bin")
    call reader%read_step
    call reader%sort_by_property(1)

    num_atoms = size(reader%values, 2)

    write(*,*) num_atoms, shape(reader%values)
    allocate(is_interesting(num_atoms))

    call get_cell

    is_interesting = .false.

    do i = 1, num_atoms
        associate(x => reader%values(3,i), &
                  y => reader%values(4,i), &
                  z => reader%values(5,i))
            if ((z-zmin)/lz < 0.9 .and. (z-zmin)/lz > 0.65 .and. sqrt(((x - xmin)/lx-0.5)**2 + ((y - ymin)/ly-0.5)**2) < 0.2) then
                is_interesting(i) = .true.
            end if
        end associate
    end do

    num_interesting = count(is_interesting)
    interesting_idx = pack([(i, i = 1, num_atoms)], is_interesting)

    write(*,*) num_interesting, size(interesting_idx)
    stop


    step = dstep*(this_image() - 1)

    steps: do
        call reader%open_file("water_data/dump.creep_water.*.bin", step)
        if (.not. reader%has_next_step) exit steps

        call reader%read_step

        open(newunit=u, file=replace_asterisk_with_step("water_data/dump.water_nodrift.*.bin",step), &
             access="stream", action="write")

        close(u)
        step = step + num_images()*dstep
    end do steps

    contains
        subroutine get_cell
            xmin = reader%header%boundary(1,1)
            ymin = reader%header%boundary(1,2)
            zmin = reader%header%boundary(1,3)

            lx = reader%header%boundary(2,1) - xmin
            ly = reader%header%boundary(2,2) - ymin
            lz = reader%header%boundary(2,3) - zmin

            xmid = xmin + 0.5d0*lx
            ymid = ymin + 0.5d0*ly
            zmid = zmin + 0.5d0*lz
        end subroutine
end program
