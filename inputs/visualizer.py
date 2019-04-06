import matplotlib.pyplot as plt
import sys 

if __name__=='__main__':
	name = sys.argv[1]
	target = name + ".png"

	print ("Visualize %s to %s" % (name, target))

	data = [ float(l) for l in open(name, "r") if not l.startswith("#")]
	xs = [ i for i in range(0, len(data))]

	plt.plot(xs, data)
	plt.savefig(target)
