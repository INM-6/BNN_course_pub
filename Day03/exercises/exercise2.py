# -*- coding: utf-8 -*-
import pylab
import nest
import nest.topology as topp


"""
Network parameters
"""
rowcol = 40
extent = [1., 1.]
model = "iaf_neuron"

"""
Create connection dictionaries

Write your code here
--------------------

Implement different connectivity dictionaries using the indications given in the
exercise sheet. 
"""

CD1 = {}

CD2 = {}

"""
Create a layer, connect it using the given connectivity dictionary, plot the targets of
the center element and save to file.

cds      : a list of connection dictionaries
savename : name of the file to save the image to
"""

def plot_layer_targets(cds, savename):
    nest.ResetKernel()
    layer = topp.CreateLayer({"rows":rowcol, "columns":rowcol, 
                              "extent":extent, "elements":model})
    for cd in cds:
        topp.ConnectLayers(layer, layer, cd)
    
    ctr = topp.FindCenterElement(layer)
    fig = topp.PlotLayer(layer, nodesize=20)
    topp.PlotTargets(ctr,layer, fig=fig, tgt_color="red")
    
    pylab.savefig("%s.png"%savename)
    pylab.close()

plot_layer_targets([CD1], "cd1")
plot_layer_targets([CD2], "cd2")
