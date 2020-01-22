program remove_drift
    use mod_lammps_reader
    use iso_fortran_env, only: dp => real64

    implicit none

    type(lammps_reader) :: reader

    integer :: step, dstep = 100000, u, i, j

    logical, dimension(:), allocatable :: is_interesting
    integer(int64) :: num_interesting, num_atoms
    integer, dimension(:), allocatable :: interesting_idx

    character(len=:), allocatable :: filename

    real(dp) :: xmin, ymin, zmin, lx, ly, lz, xmid, ymid, zmid, celldim(3), origin(3)
    real(dp) :: masses(3) = [28.0d0, 16.0d0, 1.0d0], cm0(3), cm(3), interesting_mass, dcm(3)

    if (this_image() /= 1) goto 10

    filename = "/home/anders/data/dump.creep_water_T500.0.bin"
    call reader%open_file(filename)
    call reader%read_step()
    call get_cell
    call reader%sort_by_property(1)

    num_atoms = size(reader%values, 2)

    write(*,*) reader%header%num_atoms, num_atoms, shape(reader%values)
    allocate(is_interesting(num_atoms))


    is_interesting = .false.
    interesting_mass = 0.0d0
    cm0 = 0

    do i = 1, num_atoms
        associate(x => reader%values(3,i), &
                  y => reader%values(4,i), &
                  z => reader%values(5,i), &
                  typ => reader%values(2,i))
            if ((z-zmin)/lz < 0.9 .and. (z-zmin)/lz > 0.65 .and. &
                sqrt(((x - xmid)/lx)**2 + ((y - ymid)/ly)**2) < 0.2) then
                is_interesting(i) = .true.
                interesting_mass = interesting_mass + masses(nint(typ))
                cm0 = cm0 + masses(nint(typ))*[x,y,z]
            end if
        end associate
    end do

    cm0 = cm0/interesting_mass
    num_interesting = count(is_interesting)
    interesting_idx = pack([(i, i = 1, num_atoms)], is_interesting)

    write(*,*) num_interesting, size(interesting_idx), interesting_mass
    write(*,*) cm0

    10 continue

    call co_broadcast(num_interesting, 1)
    call co_broadcast(interesting_mass, 1)
    call co_broadcast(cm0, 1)

    if (this_image() /= 1) allocate(interesting_idx(num_interesting))

    call co_broadcast(interesting_idx, 1)

    step = dstep*(this_image() - 1)

    steps: do
        call reader%open_file("/home/anders/data/dump.creep_water_T500.*.bin", step)
        if (.not. reader%has_next_step) exit steps

        call reader%read_step
        call get_cell
        call reader%sort_by_property(1)

        cm = 0
        do i = 1, num_interesting
            associate(typ => reader%values(2,interesting_idx(i)), &
                      r => reader%values(3:5, interesting_idx(i)))
                  cm = cm + masses(nint(typ))*r
            end associate
        end do
        cm = cm/interesting_mass

        dcm = cm - cm0
        write(*,*) this_image(), step, dcm

        do i = 1, num_atoms
            associate(r => reader%values(3:5, i))
                r = r - dcm
                where (r < origin)
                    r = r + celldim
                else where(r - origin > celldim)
                    r = r - celldim
                end where
            end associate
        end do

        open(newunit=u, file=replace_asterisk_with_step("/home/anders/data/dump.water_T500_nodrift.*.bin",step), &
             access="stream", action="write")
        call reader%write_to_file(u)
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

            celldim= [lx, ly, lz]
            origin = [xmin, ymin, zmin]

            xmid = xmin + 0.5d0*lx
            ymid = ymin + 0.5d0*ly
            zmid = zmin + 0.5d0*lz

            ! write(*,*) "Cell origin:",  xmin, ymin, zmin
            ! write(*,*) "Cell centre:", xmid, ymid, zmid
            ! write(*,*) "Cell size:", lx, ly, lz
        end subroutine
end program
