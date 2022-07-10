import math

JSON_FILE = 'resources/nodes_full.json'

# ROADM parameters
DINAMIC_SWITCHING_MATRIX = False    # This means that a ROADM can't do a switching operation on a channel without
                                    # disturbing the neighbouring ones. Dinamic switching matrix is intended in the
                                    # sense that the switching matrices of the nodes are dinamically modified throughout
                                    # the simulation.
DEFAULT_TRANSCEIVER = "shannon"   # Possible values: "fixed_rate", "flex_rate" and "shannon"
# Signal Parameters
DEFAULT_SIGNAL_POWER = 1
NUM_CHANNELS = 10
CHANNELS_SPACING = 50e9
SYMBOL_RATE = 32e9
NOISE_BANDWIDTH = 12.5e9
BIT_ERROR_RATE = 1e-3
# Amplifiers Parameters
DISTANCE_BETWEEN_AMP = 80000   # expressed in m
AMPLIFIERS_GAIN = 16    # (expressed in dB)
AMPLIFIERS_NOISE_FIGURE = 3    # (expressed in dB)
# Fiber Parameters
FIBER_ALPHA = 0.0002/(20*math.log(math.e, 10))   # Line Loss
FIBER_BETA = 2.13e-26                            # Line Chromatic Dispersion (Beta is the propagation constant)
FIBER_GAMMA = 1.27e-3                            # Line Non-Linearity
