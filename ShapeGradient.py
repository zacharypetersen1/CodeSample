from PIL import Image
from sys import argv

if len(argv) != 3:
	print("usage: python ShapeGradient.py <inputFileName> <outputFileName>")
	exit(1)
	
scriptName, inputName, outputName = argv

# Try to load input image
try:
	inputImage = Image.open(inputName)
except IOError:
	print("Image named: '%s' could not be found" % inputName)
	exit(2)
	
# Create a copy of img that will be manipulated
outputImage = inputImage.copy()

# Data structures for search
visited = {}
queue = []
draw = []
maxDepth = 0

# Find starting points for search (i.e. pure blue pixels)
for x in range(0, inputImage.size[0]):
	for y in range(0, inputImage.size[1]):
		r, g, b, a = inputImage.getpixel((x,y))
		if b == 255 and g == 0 and r == 0 and a == 255:
			visited[(x, y)] = True
			queue.append((x, y, 0))

# Check if pixel needs to be explored
def tryVisit(pixData):
	global maxDepth
	x, y, depth = pixData
	r, g, b, a = inputImage.getpixel((x,y))
	# Only need to visit pixel if it has not been visited and is not transparent
	if not ((x,y) in visited) and a > 0:
		if depth > maxDepth:
			maxDepth = depth
		visited[(x, y)] = True
		queue.append((x, y, depth))

# Explores pixel and expands search outwards
def explore(pixData):
	x, y, depth = pixData
	tryVisit((x+1, y, depth+1))
	tryVisit((x-1, y, depth+1))
	tryVisit((x, y+1, depth+1))
	tryVisit((x, y-1, depth+1))
	r, g, b, a = inputImage.getpixel((x,y))
	draw.append((x, y, depth, a))

# Run search
while len(queue) > 0:
	explore(queue[0])
	queue.pop(0)

# Draw Gradient based on depth
for pixData in draw:
	x, y, depth, a = pixData
	col = int( (depth/maxDepth) * 255 )
	outputImage.putpixel((x, y), (col, col, col, a))

# Save output image
saveName = "%s.png" % outputName		
outputImage.save(saveName)