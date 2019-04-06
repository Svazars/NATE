import numpy as np


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

# input sum_sin
#===========================================================================

def toPrices1(ys): # 1 ... 101
	ys = ys + abs(min(ys))
	ys = 100.0 * (ys / max(ys))	
	ys = 1.0 + np.ceil(ys)
	return ys

def sum_sin(size):
	noise = np.random.uniform(-1.5, 1.5, size)
	xs = np.linspace(0.0, 40.0, size)
	ys = (3.0 * np.array(np.sin(xs))) + (2.0 * np.array(np.sin(xs / 5.0)))
	ys = ys + smooth(noise, 5)
	return ys  
#===========================================================================

# input shapes
#===========================================================================
def toPrices2(ys):
	return np.ceil(ys)

def hatShape(size):
	part1 = np.array([ x for x in range(0, size/2)])
	part2 = np.array([ size/2 - x for x in range(0, size/2 + 1)])
	xs = np.concatenate((np.zeros((size/10)), part1, part2, np.zeros((size/10))), axis=0)
	xs = (np.array(xs / np.max(xs)) * 100.0) + 50.0
	noise = np.random.uniform(-5, 5, len(xs))
	return xs + smooth(noise, 5)

def vShape(size):
	part1 = np.array([ x for x in range(0, size/2)])
	part2 = np.array([ size/2 - x for x in range(0, size/2 + 1)])
	xs = -np.concatenate((np.zeros((size/10)), part1, part2, np.zeros((size/10))), axis=0)
	xs = (np.array(xs / np.max(np.abs(xs))) * 100.0) + 150.0
	noise = np.random.uniform(-5, 5, len(xs))
	return xs + smooth(noise, 5)

def imbHat(size):
	part1 = np.array([ x for x in range(0, size/2)])
	part2 = np.array([ size/2 - 0.5*x for x in range(0, size/2 + 1)])
	xs = np.concatenate((np.zeros((size/10)), part1, part2, np.ones(size/10) * 100.0), axis=0)
	xs = (np.array(xs / np.max(xs)) * 100.0) + 50.0
	noise = np.random.uniform(-5, 5, len(xs))
	return xs + smooth(noise, 5)

def zigzag(size):
	part1 = np.array([ x for x in range(0, size/2)])
	part2 = np.array([ size/2 - 2.0*x for x in range(0, size/2 + 1)])
	part3 = np.array([ -size/2 + x for x in range(0, size/2 + 1)])
	xs = np.concatenate((np.zeros((size/10)), part1, part2, part3, np.zeros((size/10))), axis=0)
	xs = (np.array(xs / np.max(xs)) * 117.0) + 133.0
	noise = np.random.uniform(-5, 5, len(xs))
	return xs + smooth(noise, 5)

def imbzigzag(size):
	part1 = np.array([ -x for x in range(0, size/2)])
	part2 = np.array([ -size/2 + 4.0*x for x in range(0, size/2 + 1)])
	part3 = np.array([ 3*size/2 - x for x in range(0, size/2 + 1)])
	xs = np.concatenate((np.zeros((size/10)), part1, part2, part3), axis=0)
	xs = (np.array(xs / np.max(xs)) * 66.0) + 100.0
	noise = np.random.uniform(-7, 4, len(xs))
	return xs + smooth(noise, 9)
#===========================================================================	

if __name__=='__main__':

	name = "sample.txt"

	print("Generate to file <%s>" % name)

	converter = toPrices2
	dataGen = imbzigzag
	size = 500

	data = converter(dataGen(size))
	f = open(name, "w")
	for e in data:
		f.write("%d\n" % e)
	f.close()

	print("Done %d points" % size)

