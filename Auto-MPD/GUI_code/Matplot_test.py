from tkinter import *
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import nibabel as nib
import numpy as np
from scipy.ndimage import rotate
import pydicom
import glob
import os

# plot function is created for
# plotting the graph in
# tkinter window

def plot():
	path = '../images/BBox4Tumor_PreT_Raw_10099473.nii.gz'
	mask = nib.load(path).get_fdata()
	x,y,z = mask.shape
	# the figure that will contain the plot
	fig = Figure()

	plot1 = fig.subplots()
    
	# plotting the graph
	plot1.imshow(np.fliplr(rotate(mask[:,:,61], -90)),cmap='gray')

	canvas = FigureCanvasTkAgg(fig,master = window)
	canvas.draw()

	canvas.get_tk_widget().pack()

# the main Tkinter window
window = Tk()

# setting the title
window.title('Plotting in Tkinter')

# dimensions of the main window
window.geometry("500x500")

# button that displays the plot
plot_button = Button(master = window,
					command = plot,
					height = 2,
					width = 10,
					text = "Plot")

# place the button
# in main window
plot_button.pack()

# run the gui
window.mainloop()
