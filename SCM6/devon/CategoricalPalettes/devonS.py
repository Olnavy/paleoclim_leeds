# 
#         devonS
#                   www.fabiocrameri.ch/colourmaps
from matplotlib.colors import LinearSegmentedColormap      
      
cm_data = [[0.17103, 0.1004, 0.29978],      
           [0.97357, 0.97102, 0.9946],      
           [0.46541, 0.54531, 0.85481],      
           [0.15721, 0.33688, 0.55],      
           [0.77788, 0.75776, 0.95431],      
           [0.67022, 0.65223, 0.9289],      
           [0.15947, 0.21408, 0.41376],      
           [0.24355, 0.43562, 0.72126],      
           [0.87576, 0.86438, 0.97448],      
           [0.18662, 0.38871, 0.63374],      
           [0.5826, 0.59942, 0.89939],      
           [0.92433, 0.91729, 0.9845],      
           [0.82797, 0.81233, 0.96463],      
           [0.34009, 0.48804, 0.7967],      
           [0.16605, 0.15887, 0.35797],      
           [0.73094, 0.70728, 0.94445],      
           [0.153, 0.27597, 0.47721],      
           [0.40285, 0.51731, 0.8284],      
           [0.70354, 0.68012, 0.93806],      
           [0.16908, 0.12989, 0.32874],      
           [0.21086, 0.41176, 0.67765],      
           [0.15595, 0.24449, 0.44456],      
           [0.80281, 0.78492, 0.95945],      
           [0.52572, 0.57232, 0.87823],      
           [0.63338, 0.62739, 0.9172],      
           [0.1679, 0.36299, 0.58894],      
           [0.15267, 0.30853, 0.51375],      
           [0.28309, 0.45897, 0.75842],      
           [0.16264, 0.1881, 0.3875],      
           [0.95053, 0.94585, 0.98989],      
           [0.90157, 0.89249, 0.97981],      
           [0.85336, 0.83998, 0.96987],      
           [0.75303, 0.7308, 0.94915],      
           [0.15431, 0.26008, 0.46054],      
           [0.17023, 0.11524, 0.31422],      
           [0.22582, 0.42338, 0.69948],      
           [0.71771, 0.69377, 0.94147],      
           [0.60899, 0.61329, 0.90881],      
           [0.49589, 0.55887, 0.8668],      
           [0.37122, 0.50278, 0.81336],      
           [0.17653, 0.37638, 0.61145],      
           [0.55471, 0.58579, 0.88913],      
           [0.81537, 0.79859, 0.96203],      
           [0.79032, 0.77131, 0.95687],      
           [0.43435, 0.53148, 0.84211],      
           [0.84064, 0.82612, 0.96725],      
           [0.68789, 0.66628, 0.93396],      
           [0.16439, 0.17341, 0.37268],      
           [0.31037, 0.47331, 0.77832],      
           [0.15232, 0.29214, 0.49486],      
           [0.16765, 0.14438, 0.34332],      
           [0.15768, 0.22918, 0.42901],      
           [0.19798, 0.40036, 0.65577],      
           [0.88864, 0.8784, 0.97714],      
           [0.76546, 0.74426, 0.95174],      
           [0.93741, 0.93154, 0.98719],      
           [0.65537, 0.64159, 0.92436],      
           [0.16105, 0.34846, 0.56651],      
           [0.96369, 0.96022, 0.99259],      
           [0.9113, 0.9031, 0.98181],      
           [0.15456, 0.32486, 0.53399],      
           [0.16131, 0.19914, 0.3987],      
           [0.86294, 0.85041, 0.97184],      
           [0.74366, 0.72073, 0.94718],      
           [0.25915, 0.4453, 0.73742],      
           [0.59601, 0.60632, 0.90422],      
           [0.72441, 0.70054, 0.943],      
           [0.75925, 0.73752, 0.95045],      
           [0.64469, 0.63449, 0.92093],      
           [0.77167, 0.75101, 0.95302],      
           [0.20423, 0.40606, 0.66671],      
           [0.51089, 0.5656, 0.87258],      
           [0.16353, 0.18072, 0.38008],      
           [0.16837, 0.13713, 0.33601],      
           [0.95711, 0.95303, 0.99124],      
           [0.16426, 0.35588, 0.57769],      
           [0.56881, 0.59258, 0.89435],      
           [0.93087, 0.92441, 0.98584],      
           [0.1551, 0.25226, 0.45249],      
           [0.1536, 0.26797, 0.46878],      
           [0.21803, 0.41753, 0.68857],      
           [0.8951, 0.88544, 0.97847],      
           [0.27068, 0.45204, 0.74803],      
           [0.17202, 0.36982, 0.60021],      
           [0.1586, 0.2216, 0.42135],      
           [0.32497, 0.48065, 0.78772],      
           [0.29635, 0.46607, 0.76854],      
           [0.16036, 0.20662, 0.40621],      
           [0.41863, 0.52444, 0.8354],      
           [0.16689, 0.1516, 0.35064],      
           [0.71077, 0.68697, 0.93983],      
           [0.17068, 0.10786, 0.30699],      
           [0.69594, 0.67324, 0.93611],      
           [0.8343, 0.81921, 0.96594],      
           [0.1814, 0.38265, 0.62262],      
           [0.48073, 0.55212, 0.86088],      
           [0.67933, 0.65928, 0.93157],      
           [0.1652, 0.16612, 0.36531],      
           [0.54033, 0.57904, 0.88375],      
           [0.79656, 0.77811, 0.95816]]      
      
devonS_map = LinearSegmentedColormap.from_list('devonS', cm_data)      
# For use of "viscm view"      
test_cm = devonS_map      
      
if __name__ == "__main__":      
    import matplotlib.pyplot as plt      
    import numpy as np      
      
    try:      
        from viscm import viscm      
        viscm(devonS_map)      
    except ImportError:      
        print("viscm not found, falling back on simple display")      
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',      
                   cmap=devonS_map)      
    plt.show()      