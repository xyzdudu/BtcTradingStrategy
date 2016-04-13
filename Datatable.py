from pychartdir import *

# The data for the line chart
# data0 = [42, 49, 33, 38, 64, 56, 29, 41, 44, 57, 59, 42]
# data1 = [65, 75, 47, 34, 42, 49, 73, 62, 90, 69, 66, 78]
# data2 = [36, 28, 25, 28, 38, 20, 22, 30, 25, 33, 30, 24]
# labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Create a XYChart object of size 1200 x 400 pixels
c = XYChart(1200, 400)

def draw(data,labels):
	# Set the plotarea at (30, 20) and of size 200 x 200 pixels
	c.setPlotArea(30, 20, 1150, 350)

	# Add a line chart layer using the given data
	c.addLineLayer(data)

	# Set the labels on the x axis.
	c.xAxis().setLabels(labels)

	# Display 1 out of 3 labels on the x-axis.
	c.xAxis().setLabelStep(3)

	# Output the chart
	c.makeChart("simpleline.png")