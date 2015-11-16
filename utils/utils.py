__author__ = 'Idan'

import numpy as np
from scipy.stats import mode
from scipy.special import erf,erfcinv

def parse_row(row , delim= ','):
    items = row.split(delim)

    res = {}


def get_mode_index(arr):
    '''
    :param array:
     a vector representing a slice of a histogram data, that has only one maxima
    :return:
    returns the exact index of the maxima in the array ( the numbuer of elements till the maxima )
    '''
    value, count = mode(arr)
    return np.where(arr == value.item())[0][0]
    # return np.where(arr == value.item())
    # arr[value]
    # arr[arr == value.item()][0]
    # np.argmax(arr)

def arg_jump(arr, tau = 2.2):
    '''

    :param arr: a slice of an array
    :return:
    the index of the first jump in continuicity
    val > mean + 2.2*std
    '''
    # return \
    cond = np.where(arr > (np.mean(arr) + tau * np.std(arr)))[0][0]
    if cond[0]: return None
    return  cond[0][0]  # reutrn the forst

def args_jump(arr, tau = 2.2):
    '''

    :param arr: a slice of an array
    :return:
    the index of the first jump in continuicity
    val > mean + 2.2*std
    '''
    # return \
    cond = np.where(arr > (np.mean(arr) + tau * np.std(arr)))[0][0]
    if cond[0]: return None
    return  cond[0] # reutrn the forst


def arg_fall(arr, tau = 2.2):
    '''

    :param arr: a slice of an array
    :return:
    the index of the first jump in continuicity
    val > mean + 2.2*std
    '''
    cond = np.where(arr < (np.mean(arr) - tau * np.std(arr)))[0][0]
    if cond[0]: return None
    return  cond[0][0]  # reutrn the forst

def get_error_f( z, inverse = False , stand = False ):
    '''
    :param z:
    P(|N|<x)=erf(x/sqrt(2)).
    z = ( x - mu) / std
    z can be 0.95 to 0.05
    tbd: at 0.5 should be 0.5?
    :return:
        2/sqrt(pi)*integral(exp(-t**2), t=0..z).

    '''
    if stand: z = ( (z - np.mean(z) ) / (np.std(z) * np.sqrt(2) ) )
    if inverse : return erfcinv(z)  # returns standardisized value
    return erf(z)  # returns probability


def get_zero_start_n_stop(value, time, th=0):
    cond = np.where(value == th)
    cond2 = [cond[i] and not cond[i-1] or cond[i-1] and not cond[i] for i in enumerate(cond)]
    if cond2[0]: cond2[0] = False
    dim = np.shape(time[cond2])[0]
    if dim % 2 : time = time [:-1]
    return np.reshape(time[cond2], dim / 2, 2)


def get_longer_then(time_pars,th):
    # np.where(time[:-1] - time[1:] )
    res=[]
    for pair in time_pars:
        if pair[1] - pair[0] >= th:
            res.append(pair)
    return res

# def get_conflicts



    # docking_time_samples = time[cond]

    # args_jump(docking_time_samples) #window??

