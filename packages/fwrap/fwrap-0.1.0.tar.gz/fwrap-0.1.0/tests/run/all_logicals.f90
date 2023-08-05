      subroutine log_default(i1,i2,i3)
      implicit none
      logical, intent(in) :: i1
      logical, intent(inout) :: i2
      logical, intent(out) :: i3
      i2 = .false. .and. i1
      i3 = .false.
      end subroutine
      subroutine log_x_len(i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15)
      implicit none
      logical*1, intent(in) :: i4
      logical*1, intent(inout) :: i5
      logical*1, intent(out) :: i6
      logical*2, intent(in) :: i7
      logical*2, intent(inout) :: i8
      logical*2, intent(out) :: i9
      logical*4, intent(in) :: i10
      logical*4, intent(inout) :: i11
      logical*4, intent(out) :: i12
      logical*8, intent(in) :: i13
      logical*8, intent(inout) :: i14
      logical*8, intent(out) :: i15

      i5= .false. .and. i4
      i6= .false. .and. i7
      i8= .false.
      i9= .false. .and. i10
      i11= .false.
      i12= .false.
      i14= .false. .and. i13
      i15= .false.

      end subroutine
      subroutine log_kind_x(i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12)
      implicit none
      logical(kind=1), intent(in) :: i1
      logical(kind=1), intent(inout) :: i2
      logical(kind=1), intent(out) :: i3
      logical(kind=2), intent(in) :: i4
      logical(kind=2), intent(inout) :: i5
      logical(kind=2), intent(out) :: i6
      logical(kind=4), intent(in) :: i7
      logical(kind=4), intent(inout) :: i8
      logical(kind=4), intent(out) :: i9
      logical(kind=8), intent(in) :: i10
      logical(kind=8), intent(inout) :: i11
      logical(kind=8), intent(out) :: i12

      i2= .false. .and. i1
      i3= .false.
      i5= .false. .and. i4
      i6= .false.
      i8= .false. .and. i7
      i9= .false.
      i11= .false. .and. i10
      i12= .false.

      end subroutine
      ! subroutine log_kind_call(i1,i2,i3,i4,i5,i6)
      ! implicit none
      ! logical(kind=kind(.true.)), intent(in) :: i1
      ! logical(kind=kind(.true.)), intent(inout) :: i2
      ! logical(kind=kind(.true.)), intent(out) :: i3
      ! logical(kind=kind(0)), intent(in) :: i4
      ! logical(kind=kind(0)), intent(inout) :: i5
      ! logical(kind=kind(0)), intent(out) :: i6

      ! i2= .false. .and. i1
      ! i3= .false.
      ! i5= .false. .and. i4
      ! i6= .false.

      ! end subroutine
      ! subroutine log_sik_call(i1,i2,i3,i4,i5,i6,i7,i8,i9)
      ! implicit none
      ! logical(kind=selected_int_kind(1)), intent(in) :: i1
      ! logical(kind=selected_int_kind(1)), intent(inout) :: i2
      ! logical(kind=selected_int_kind(1)), intent(out) :: i3
      ! logical(kind=selected_int_kind(5)), intent(in) :: i4
      ! logical(kind=selected_int_kind(5)), intent(inout) :: i5
      ! logical(kind=selected_int_kind(5)), intent(out) :: i6
      ! logical(kind=selected_int_kind(10)), intent(in) :: i7
      ! logical(kind=selected_int_kind(10)), intent(inout) :: i8
      ! logical(kind=selected_int_kind(10)), intent(out) :: i9

      ! i2= .false. .and. i1
      ! i3= .false.
      ! i5= .false. .and. i4
      ! i6= .false.
      ! i8= .false. .and. i7
      ! i9= .false.

      ! end subroutine
