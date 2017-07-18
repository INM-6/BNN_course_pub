import numpy as np
import random as rand
import pylab as pl
import nest
import nest.topology as topo

"""
Setting up NEST
"""
nest.ResetKernel()
np.random.seed()
rndSeeds = np.random.randint(0, 1000, 2)
rngSeeds = [rndSeeds[0]]
grngSeed = rndSeeds[1]
dt = .1
nest.SetStatus([0], {"resolution"        : dt,
                     "rng_seeds"         : rngSeeds,
                     "grng_seed"         : grngSeed})

"""
Simulation parameters
"""
simtime = 10000.
wuptime = 200.


"""
You may want to use these variables to alternate between the different 
configurations. You need long simualtions to stimate correlation coefficients
properly.
"""
gauss_ex = False
gauss_in = False


"""
Network parameters
"""
order   = 1000
ne      = 4 * order
ni      = 1 * order
epsilon = .1
je      = .1
g       = 10
ji      = -g * je
delay   = 1.5

#topology parameters
extentX = 1.
extentY = 1.
wrapped = True

#layer parameters
layer_dict = {"extent"      : [extentX, extentY],
              "edge_wrap"   : wrapped}

#connection parameters

"""
Write your code here
--------------------

Write the dictionaries that you will use to connect the neurons locally. You can
use one dictionary for both populations if you wish. Remember that your choice 
of parameters has to match the description given in the exercise sheet. Number
of connections have to be roughly the same as in the random case. Use the
function FindConnections() to find out whether you are making the same number of
connections or not.
"""

condict_ex = {}

condict_in = {}

"""
Neuron parameters
"""
neuron_model= "iaf_psc_alpha"
tauSynEx    = .5
tauSynIn    = .5
tauMem      = 20.
theta       = 20.
reset       = .0
neuron_params= {"C_m"       : 1.,
                "tau_m"     : tauMem,
                "tau_syn_ex": tauSynEx,
                "tau_syn_in": tauSynIn,
                "t_ref"     : 2.,
                "E_L"       : .0,
                "V_m"       : .0,
                "V_reset"   : reset,
                "V_th"      : theta}


nest.CopyModel("iaf_psc_alpha", "exc", params=neuron_params)
nest.CopyModel("iaf_psc_alpha", "inh", params=neuron_params)

"""
Part a:
Create layers

The following code distributes the neurons randomly across the layer.
"""

ex_pos = [[np.random.uniform(-extentX / 2., extentX / 2.),\
           np.random.uniform(-extentY / 2., extentY / 2.)] for j in xrange(ne)]
layer_dict.update({"positions": ex_pos,"elements":"exc"})
in_pos = [[np.random.uniform(-extentX / 2., extentX / 2.),\
           np.random.uniform(-extentY / 2., extentY / 2.)] for j in xrange(ni)]
layer_dict.update({"positions": in_pos, "elements":"inh"})


"""
Write your code here
--------------------
Create a layer of inhibitory neurons and another of excitatory neurons. Use
the funcion topo.CreateLayer() for that.
"""


"""
Part b:
Connect the layers
"""

"""
Write your code here
--------------------

Connect the layers (EE,EI,IE,II). Write your code in such a way that you can 
easily switch between random and local connectivity.
"""

"""
External input
"""
ext_rate=7.8
ext = nest.Create("poisson_generator",params={"rate":ext_rate*1e3})

"""
Recorders
"""
recorder_params    ={"start"        : wuptime,
                      "to_file"     : False,
                      "to_memory"   : True}
sd = nest.Create("spike_detector", params=recorder_params)
vm = nest.Create("voltmeter", params=recorder_params)

"""
Connect external drive
"""
nest.Connect(ext, inhNeurons + excNeurons, "all_to_all",
             syn_spec={"weight":je, "delay":1.})
             

"""
Connect to recorders
"""
nest.Connect(excNeurons, sd,"all_to_all",
             syn_spec={"weight":1.0, "delay":1.0})
            
nest.DivergentConnect(vm, excNeurons, "all_to_all",
             syn_spec={"weight":1.0, "delay":1.0})
             


"""
Part b cont:
Plot the network
"""

"""
Write your code here
--------------------

Plot the network connectivity. Re-use the function provided in 
exercise 2.
"""

"""
Simulate
"""
nest.Simulate(wuptime + simtime)

"""
Get data from recorders
"""
data_sd = nest.GetStatus(sd, "events")[0]
s_sd,t_sd = data_sd["senders"], data_sd["times"]

data_v = nest.GetStatus(vm, "events")[0]
s_v,t_v,p_v = np.array(data_v["senders"]), np.array(data_v["times"]), np.array(data_v["V_m"])

"""
Part c:
Analyse the data
"""

"""
Write your code here
--------------------

Plot the spiking activity and the PSTH. Re-use the code that you implemented in 
previous exercises.
"""



def get_ccs(times, senders, n_sample=1000, bin_size=5.):
    unique_ids = np.unique(senders)
    bins= np.arange(wuptime, simtime + wuptime + bin_size, bin_size)
    cc = np.zeros(n_sample)
    for i in xrange(n_sample):
        sp1, sp2 = rand.sample(unique_ids, 2)
        psth1 = np.histogram(times[senders == sp1], bins)[0]
        psth2 = np.histogram(times[senders == sp2], bins)[0]
        cc[i] = np.corrcoef(psth1, psth2)[0][1]
    return cc


"""
Write your code here
--------------------

Plot the distribution of correlation coefficients. Use the function pl.hist().
"""
pl.xlabel("correlation coefficient", fontsize=30)
pl.ylabel("counts", fontsize=30)
pl.show()

