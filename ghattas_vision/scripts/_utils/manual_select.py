import cv2



def manual_select(k,tasks, frame):
    if k==ord('g'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks.gate.detected(frame, (x,y,w,h))

    elif k==ord('t'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks.torpedo.detected(frame, (x,y,w,h))

    elif k==ord('p'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks.path.detected(frame, (x,y,w,h))

    elif k==ord('b'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks.bouy.detected(frame, (x,y,w,h))

    elif k==ord('d'):
        (x,y,w,h) = cv2.selectROI('frame', frame)
        tasks.dropper.detected(frame, (x,y,w,h))
