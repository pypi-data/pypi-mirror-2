SUBROUTINE get_chi(chi_plus, chi_minus, h, kx, w, num_of_regions)
  IMPLICIT NONE
  INTEGER, PARAMETER :: wp = KIND(0.0D0)
  ! Number of regions, num_of_regions, equals $p+1$, where $p$ is the
  ! label for the 'reflected' half-space.  [see Fig. 1 in the paper]
  ! In the code below, we keep the same indexing as in our paper.
  INTEGER, INTENT(IN) :: num_of_regions
  COMPLEX(wp), INTENT(IN) :: h(0:num_of_regions-1)
  COMPLEX(wp), INTENT(IN) :: kx(0:num_of_regions-1)
  COMPLEX(wp), INTENT(IN) :: w(0:num_of_regions-1)
  COMPLEX(wp), INTENT(OUT) :: chi_plus(0:num_of_regions-1)
  COMPLEX(wp), INTENT(OUT) :: chi_minus(0:num_of_regions-1)

  COMPLEX(wp) :: denom, M(2,2), Mtmp(2,2)
  COMPLEX(wp) :: J = (0.0_wp, 1.0_wp)
  INTEGER:: i, p

  p = num_of_regions - 1

  ! [see (27) in the paper]
  M(1,1) = 0.5_wp * (1.0_wp + w(1)/w(2)) * EXP(-J*kx(1)*h(1))
  M(2,1) = 0.5_wp * (1.0_wp - w(1)/w(2)) * EXP(-J*kx(1)*h(1))
  M(1,2) = 0.5_wp * (1.0_wp - w(1)/w(2)) * EXP(J*kx(1)*h(1))
  M(2,2) = 0.5_wp * (1.0_wp + w(1)/w(2)) * EXP(J*kx(1)*h(1))
  DO i=2, p-1
     Mtmp(1,1) = 0.5_wp * (1.0_wp + w(i)/w(i+1)) * EXP(-J*kx(i)*h(i))
     Mtmp(2,1) = 0.5_wp * (1.0_wp - w(i)/w(i+1)) * EXP(-J*kx(i)*h(i))
     Mtmp(1,2) = 0.5_wp * (1.0_wp - w(i)/w(i+1)) * EXP(J*kx(i)*h(i))
     Mtmp(2,2) = 0.5_wp * (1.0_wp + w(i)/w(i+1)) * EXP(J*kx(i)*h(i))
     M = MATMUL(Mtmp, M)
  END DO

  denom = (w(1) + w(0))*M(1,1) + (w(1) - w(0))*M(1,2)

  ! [see (28a) in the paper]
  chi_plus(0) = 2.0_wp*w(1)/denom

  ! [see (28c) in the paper]
  chi_plus(1) = (w(1) + w(0))/denom

  ! Set the incident $\chi$ to one, i.e., $\chi^+_p = 1$.
  chi_plus(p) = 1.0_wp

  ! Set the reflected $\chi$ in the 'transmitted half-space to zero, 
  ! i.e., $\chi^-_0 = 0$ because there is no reflected wave in the 
  ! 'transmitted' half-space.
  chi_minus(0) = 0.0_wp 

  ! [see (28c) in the paper]
  chi_minus(1) = (w(1) - w(0))/denom

  ! [see (28b) in the paper]
  chi_minus(p) = ( (w(1) + w(0))*M(2,1) + (w(1) - w(0))*M(2,2) )/denom

  ! [see (28d) in the paper]
  DO i=1, p-2
     M(1,1) = 0.5_wp * (1.0_wp + w(i)/w(i+1)) * EXP(-J*kx(i)*h(i))
     M(2,1) = 0.5_wp * (1.0_wp - w(i)/w(i+1)) * EXP(-J*kx(i)*h(i))
     M(1,2) = 0.5_wp * (1.0_wp - w(i)/w(i+1)) * EXP(J*kx(i)*h(i))
     M(2,2) = 0.5_wp * (1.0_wp + w(i)/w(i+1)) * EXP(J*kx(i)*h(i))
     chi_plus(i+1) = M(1,1)*chi_plus(i) + M(1,2)*chi_minus(i)
     chi_minus(i+1) = M(2,1)*chi_plus(i) + M(2,2)*chi_minus(i)
  END DO

END SUBROUTINE get_chi
!---------------------------------------------------------------------------------------------------
SUBROUTINE cmplx_sqrt(kx, kxSquared, num_of_regions)
  IMPLICIT NONE
  INTEGER, PARAMETER :: wp = KIND(0.0D0)
  ! Number of regions, num_of_regions, equals $p+1$, where $p$ is the
  ! label for the 'reflected' half-space.  [see Fig. 1 in the paper]
  ! In the code below, we keep the same indexing as in our paper.
  INTEGER, INTENT(IN) :: num_of_regions
  COMPLEX(wp), INTENT(IN) :: kxSquared(0:num_of_regions-1)
  COMPLEX(wp), INTENT(OUT) :: kx(0:num_of_regions-1)

  ! [see (8) in the paper]
  kx = SQRT(kxSquared)
  WHERE ( AIMAG(kx) < 0 ) kx = -kx
END SUBROUTINE cmplx_sqrt
!---------------------------------------------------------------------------------------------------
