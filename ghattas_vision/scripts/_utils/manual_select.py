import cv2



def manual_select(k,tasks, frame):
    if k==ord('g'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks['gate']._detected(frame, (x,y,w,h))

    elif k==ord('t'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks['torpedo']._detected(frame, (x,y,w,h))

    elif k==ord('p'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks['path']._detected(frame, (x,y,w,h))

    elif k==ord('b'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks['bouy']._detected(frame, (x,y,w,h))

    elif k==ord('d'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks['dropper']._detected(frame, (x,y,w,h))
