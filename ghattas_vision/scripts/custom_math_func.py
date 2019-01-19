import math

# a collection of usefull geometric functions

#given 2 lines calculate the average line inbetween them
def avg_line(L1,L2):
    x1 = int((L1[0][0]+L2[0][0])/2)
    y1 = int((L1[0][1]+L2[0][1])/2)
    x2 = int((L1[1][0]+L2[1][0])/2)
    y2 = int((L1[1][1]+L2[1][1])/2)
    return ((x1,y1),(x2,y2))

def length(L):
    return math.sqrt((L[0][0] - L[1][0])**2 + (L[0][1] - L[1][1])**2)

def slope(P1,P2):
    if P2[0] - P1[0] == 0:
        return 'vertical'
    return(P2[1] - P1[1]) / (P2[0] - P1[0])

def deg(L):
    m=slope(L[0],L[1])
    if m=='vertical':
        return 90
    return math.degrees(math.atan(m))
