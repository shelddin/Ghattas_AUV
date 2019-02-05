import cv2
import numpy as np
from param import task_pts


def pnp(frame,bbox, world_pts):
    img_pts=np.array(
    [(bbox.x, bbox.y),
    (bbox.x, bbox.y+bbox.h),
    (bbox.x/2, bbox.y/2),
    (bbox.x+bbox.w, bbox.y),
    (bbox.x+bbox.w, bbox.y+bbox.h)], dtype='double')
    for i in range(5):
        cv2.circle(frame, tuple(img_pts[i]), 3, [255,255,255], -1)
        cv2.putText(frame, str(i), tuple(img_pts[i]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,150,30], 2)

#    world_pts= task_pts
    #np.array(
#    [(0,0,0),
#    (0,10,0),
#    (2.5,5,0),
#    (5,0,0),
#    (5,10,0)], dtype='double')
    size = (1920,1080)#frame.shape()
    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix=np.array(
    [[focal_length,0,center[0]],
    [0,focal_length,center[1]],
    [0,0,1]], dtype='double'
    )
    dist_coeffs=np.zeros((4,1))
    (success, rotation_vector, translation_vector) = cv2.solvePnP(world_pts, img_pts, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    print "Rotation Vector:\n {0}".format(rotation_vector)
    print "Translation Vector:\n {0}".format(translation_vector)
    cv2.putText(frame,"Rotation Vector:\n {0}".format(rotation_vector),(100,100),cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,150,30], 2)
    cv2.putText(frame,"Translation Vector:\n {0}".format(translation_vector),(100,200),cv2.FONT_HERSHEY_SIMPLEX, 0.5, [255,150,30], 2)

    (projected_z_2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 5.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    (projected_y_2D, jacobian) = cv2.projectPoints(np.array([(0.0, 5.0, 0.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)
    (projected_x_2D, jacobian) = cv2.projectPoints(np.array([(5.0, 0.0, 0.0)]), rotation_vector, translation_vector, camera_matrix, dist_coeffs)

    p = ( int(img_pts[0][0]), int(img_pts[0][1]))
    pz = ( int(projected_z_2D[0][0][0]), int(projected_z_2D[0][0][1]))
    py = ( int(projected_y_2D[0][0][0]), int(projected_y_2D[0][0][1]))
    px = ( int(projected_x_2D[0][0][0]), int(projected_x_2D[0][0][1]))

    cv2.line(frame, p, pz, (255,0,0), 2)
    cv2.line(frame, p, py, (0,255,0), 2)
    cv2.line(frame, p, px, (0,0,255), 2)
    cv2.imshow('prespective',frame)
    #out.write(frame)
    return success, rotation_vector, translation_vector
