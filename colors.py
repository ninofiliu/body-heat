import math

def mix(t, a, b):
	return [a + t * (b-a) for (a,b) in zip(a,b)]

def color_ramp(t, ramp):
	if (t<=0):
		return ramp[0]
	if (t>=1):
		return ramp[-1]
	n = len(ramp) - 1
	i = math.floor(t * n)
	u = (t * n) % 1
	return mix(u, ramp[i], ramp[i+1])
