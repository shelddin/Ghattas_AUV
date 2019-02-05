import cv2

#draw all givin shapes in draw que using basic cv2 drawing functions
def draw_shapes(frame, draw_q):

    for L in draw_q['lines']:
        cv2.line(frame,L['p1'],L['p2'],L['color'],2)

    for C in draw_q['circle']:
        cv2.circle(frame, C['center'], C['radius'], C['color'], -1)

    for R in draw_q['rectangle']:
        cv2.rectangle(frame, R['p1'],R['p2'], R['color'], 1)

    for Co in draw_q['contour']:
        cv2.drawContours(frame,Co['cont'],-1,Co['color'],1)

    for T in draw_q['text']:
        cv2.putText(frame, T['text'], T['p'],cv2.FONT_HERSHEY_SIMPLEX, 0.5, T['color'], 2)
