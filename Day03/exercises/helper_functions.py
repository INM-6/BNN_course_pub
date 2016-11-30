# -*- coding: utf-8 -*-
import nest
import nest.raster_plot
import numpy as np

def load_spikedata_from_file(spikefile):
    """
    Loads spike data from spikefile and returns it as a numpy array

    Directly borrowed and trimmed from existing method in nest.raster_plot
    
    Returns:
        data    data is a matrix such that
                    data[:,0] is a vector of all gids and
                    data[:,1] a vector with the corresponding time stamps.
    """
    #try:
    if True:
        if nest.is_sequencetype(spikefile):
            data = None
            for f in fname:
                if data == None:
                    print "Using loadtxt"
                    data = np.loadtxt(f)
                else:
                    print "Using concatenate"
                    data = np.concatenate((data, np.loadtxt(f)))
        else:
            print "Loading spike data for file: %s"%spikefile
            data = np.loadtxt(spikefile)
        return data
    #except:
        print "Error with loading spike data for file: %s"%spikefile
        return None


def get_latencies(data,gids,times):
    """
    Params:
        data        data is a matrix such that
                    data[:,0] is a vector of all gids and
                    data[:,1] a vector with the corresponding time stamps.
        gids        list of global ids that we will extract events for
        times       time is a list with at most two entries such that
                    time=[t_max] extracts all events with t< t_max
                    time=[t_min, t_max] extracts all events with t_min <= t < t_max

    
    Returns:
        gids        a list gids of all neurons that spiked during this time 
        latencies   a list containing the corresponding latencies 
    """
    
    try:
        subset_events = nest.raster_plot.extract_events(data,time=times,sel=gids)
        firsts = {}
        for i in range(len(subset_events)):
            if firsts.has_key(subset_events[i][0]):
                continue
            firsts[subset_events[i][0]] = subset_events[i][1]
    except:
        print "Error with extracting latencies"
        return None,None

    latency_gids = firsts.keys() # node ids that have appeared
    latencies = [firsts[d] for d in latency_gids]
    latency_gids = [int(g) for g in latency_gids]
    
    return latency_gids,latencies


def plot_Vm_traces(senders=None,times=None,potentials=None):
    """
    Plot the membrane potential traces
    
    Parameters
    ----------
    
    senders    - array - sender ids from multimeter.
    times      - array - sampling times from multimeter.
    potentials - array - membrane potential values from multimeter.
    """
    pass


