import numpy as np

#color thresholdes
color_thresh={}
color_thresh['black'] = np.array([[[0,0,0],[179,255,30]]])
color_thresh['red'] = np.array([[[0,5,5],[80,255,255]],[[150,5,5],[179,255,255]]])
color_thresh['green'] = np.array([[[45,100,100],[80,255,255]]])
color_thresh['orange'] = np.array([[[5,100,100],[20,255,255]]])
color_thresh['yellow'] = np.array([[[20,100,100],[30,255,255]]])

#size thresholds
def contour_min_size(key):
    contour_min_size_dict={}
    contour_min_size_dict.setdefault(key,500)
    contour_min_size_dict['black']=500
    return contour_min_size_dict[key]

kernel_size=(5,5)

parallel_deg_thresh=5
