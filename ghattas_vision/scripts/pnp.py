import cv2
import numpy as np

def npn(target):
    img_pts=target.img_pts
    world_pts=target.world_pts
    camera_matrix=np.array(
    [,0,],
    [,0,],
    [0,0,1], dtype='double'
    )
    dist_coeffs=np.zeros((4,1))
    (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.CV_ITERATIVE)

    print "Rotation Vector:\n {0}".format(rotation_vector)
    print "Translation Vector:\n {0}".format(translation_vector)

#    (projected_point_2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
