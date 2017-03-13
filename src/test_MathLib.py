from MathLib import toVector, toValue
vec = (toVector(1.0,2,3))
print(vec)
a,b,c = toValue(vec)
print(a,b,c)
print(type(a))