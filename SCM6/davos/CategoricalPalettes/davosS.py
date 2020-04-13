# 
#         davosS
#                   www.fabiocrameri.ch/colourmaps
from matplotlib.colors import LinearSegmentedColormap      
      
cm_data = [[0, 0.019685, 0.29201],      
           [0.99123, 0.99027, 0.95718],      
           [0.40896, 0.54645, 0.58144],      
           [0.17713, 0.34467, 0.58337],      
           [0.6983, 0.75318, 0.56026],      
           [0.2941, 0.46407, 0.61562],      
           [0.076446, 0.18952, 0.46021],      
           [0.52777, 0.62551, 0.53686],      
           [0.9112, 0.92095, 0.75278],      
           [0.032137, 0.11127, 0.38047],      
           [0.60422, 0.68107, 0.53189],      
           [0.46433, 0.58253, 0.55775],      
           [0.23311, 0.40823, 0.61049],      
           [0.81025, 0.84085, 0.63691],      
           [0.12214, 0.26702, 0.52947],      
           [0.96506, 0.96546, 0.85817],      
           [0.3503, 0.50682, 0.60387],      
           [0.14883, 0.30685, 0.55945],      
           [0.011304, 0.069327, 0.33618],      
           [0.49509, 0.60303, 0.5462],      
           [0.98089, 0.97976, 0.90905],      
           [0.56362, 0.65108, 0.53132],      
           [0.86585, 0.88476, 0.69326],      
           [0.37973, 0.5271, 0.59346],      
           [0.26367, 0.43766, 0.61581],      
           [0.43459, 0.56313, 0.57033],      
           [0.097192, 0.22598, 0.49432],      
           [0.64497, 0.71199, 0.53977],      
           [0.053198, 0.14777, 0.4185],      
           [0.94103, 0.94521, 0.80357],      
           [0.75743, 0.79936, 0.59516],      
           [0.32425, 0.48781, 0.6109],      
           [0.20668, 0.37989, 0.60073],      
           [0.06489, 0.16864, 0.43966],      
           [0.44937, 0.57275, 0.56398],      
           [0.51112, 0.61395, 0.54116],      
           [0.83907, 0.86357, 0.66429],      
           [0.021233, 0.090352, 0.35838],      
           [0.58321, 0.66544, 0.53067],      
           [0.39435, 0.53685, 0.58759],      
           [0.1353, 0.28713, 0.54517],      
           [0.9866, 0.98537, 0.93338],      
           [0.47953, 0.5926, 0.55178],      
           [0.30924, 0.47623, 0.61375],      
           [0.97382, 0.97321, 0.88403],      
           [0.54521, 0.63783, 0.53348],      
           [0.24839, 0.42333, 0.61388],      
           [0.89001, 0.90397, 0.72299],      
           [0.27892, 0.45122, 0.61635],      
           [0.36505, 0.51712, 0.59892],      
           [0.67075, 0.73183, 0.54832],      
           [0.16281, 0.32604, 0.57221],      
           [0.10953, 0.2466, 0.51247],      
           [0.72736, 0.77583, 0.57587],      
           [0.19176, 0.36264, 0.59289],      
           [0.0023129, 0.047559, 0.314],      
           [0.95425, 0.95622, 0.83137],      
           [0.33546, 0.49612, 0.60817],      
           [0.7878, 0.82319, 0.61789],      
           [0.21795, 0.39233, 0.60552],      
           [0.088241, 0.21038, 0.48004],      
           [0.41992, 0.55359, 0.57672],      
           [0.041347, 0.12687, 0.39688],      
           [0.62684, 0.69816, 0.53539],      
           [0.92509, 0.93217, 0.77484],      
           [0.22553, 0.40038, 0.60821],      
           [0.3577, 0.51201, 0.60146],      
           [0.070681, 0.17908, 0.45002],      
           [0.44197, 0.56792, 0.56715],      
           [0.65764, 0.72171, 0.54364],      
           [0.16993, 0.33545, 0.57799],      
           [0.82487, 0.85237, 0.65035],      
           [0.02654, 0.10079, 0.36945],      
           [0.31676, 0.48209, 0.61244],      
           [0, 0.034324, 0.30295],      
           [0.18441, 0.35374, 0.58833],      
           [0.0066067, 0.058541, 0.32508],      
           [0.15579, 0.31652, 0.56602],      
           [0.12867, 0.27714, 0.53749],      
           [0.2865, 0.45772, 0.61613],      
           [0.19916, 0.37135, 0.59702],      
           [0.1158, 0.25686, 0.52112],      
           [0.59353, 0.67309, 0.53102],      
           [0.96967, 0.9695, 0.87121],      
           [0.97755, 0.97662, 0.89664],      
           [0.256, 0.43059, 0.61502],      
           [0.48726, 0.59776, 0.54894],      
           [0.40165, 0.54165, 0.58455],      
           [0.53639, 0.63156, 0.53503],      
           [0.30167, 0.47023, 0.61482],      
           [0.05913, 0.15821, 0.42915],      
           [0.50303, 0.60843, 0.5436],      
           [0.24073, 0.41588, 0.61238],      
           [0.01619, 0.079806, 0.3473],      
           [0.9839, 0.98267, 0.9213],      
           [0.51937, 0.61965, 0.53891],      
           [0.98903, 0.98789, 0.94534],      
           [0.85276, 0.87439, 0.67863],      
           [0.047327, 0.13734, 0.40774],      
           [0.71266, 0.76436, 0.5676]]      
      
davosS_map = LinearSegmentedColormap.from_list('davosS', cm_data)      
# For use of "viscm view"      
test_cm = davosS_map      
      
if __name__ == "__main__":      
    import matplotlib.pyplot as plt      
    import numpy as np      
      
    try:      
        from viscm import viscm      
        viscm(davosS_map)      
    except ImportError:      
        print("viscm not found, falling back on simple display")      
        plt.imshow(np.linspace(0, 100, 256)[None, :], aspect='auto',      
                   cmap=davosS_map)      
    plt.show()      