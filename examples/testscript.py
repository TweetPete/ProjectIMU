from math import sqrt
from numpy import rad2deg
from Settings import g
ax = -0.108225710
ay = -0.022668240
az = -9.763507613
s_ax = 0.128801
s_ay = 0.095893
s_az = 0.145545

mx = 12.1699268074
my = -14.7826727401
s_mx = 0.225350
s_my = 0.079485

s_phi_2 = (az/(ay**2+az**2))**2 * s_ay**2 + (-ay/(az**2+ay**2))**2 * s_az**2
s_phi = sqrt(s_phi_2)

s_theta_2= (1/(g*sqrt(1-(ax**2/g**2))))**2 * s_ax**2
s_theta = sqrt(s_theta_2)

s_psi_2 = (mx/(my**2+mx**2))**2 * s_my**2 + (-my/(mx**2+my**2))**2 * s_mx**2
s_psi = sqrt(s_psi_2)

print((s_phi))
print((s_theta))
print((s_psi))