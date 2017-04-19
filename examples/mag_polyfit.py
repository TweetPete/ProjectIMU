from numpy.polynomial.polynomial import polyfit
from numpy import array 

x = array([1507.2, 18897.5, 45857.5])
y = array([-0.07067138, 6.17437722, 6.26229508])

coef = polyfit(y,x,1)
print(coef)
print(-0.07067138*4952.83270677+1671.82206381 )
