import custom_math_func
import _param.processing_param

#preping the data for use
def order(c):
    ordered=[]
    for i in range(len(c)):
        j=i+1
        #if at last point connect it to the first point
        if i == len(c)-1:
            j=0
        point1=tuple(c[i].flatten())
        point2=tuple(c[j].flatten())
        #make a line from point pair
        line=(point1,point2)
        #make sure that lines flow in the positive x-direction
        if point1[0]>point2[0]:
            line=(point2,point1)
        ordered.append(line)
    ordered=tuple(ordered)
    return ordered


def path_detection(contours,draw_q=None):
    deg_thresh=param.parallel_deg_thresh
    #process all contours
    for c in contours:
        #initialize & optain variables
        c=order(c)
        path1,path2=((0,0),(0,0)),((0,0),(0,0))
        len1,len2=0,0
        #find parallel line pairs
        for l1 in range(len(c)):
            deg1 = custom_math_func.deg(c[l1])
            for l2 in range(l1+1,len(c)):
                deg2 = custom_math_func.deg(c[l2])
                if deg1+deg_thresh > deg2 and deg2 > deg1-deg_thresh:
                    #find the path between parallel lines
                    current_path=custom_math_func.avg_line(c[l1],c[l2])
                    lenp=custom_math_func.length(current_path)
                    # choose the two longest detected paths
                    if lenp > len2:
                        if lenp > len1:
                            len2 = len1
                            path2 = path1
                            len1=lenp
                            path1=current_path
                        else:
                            len2=lenp
                            path2=current_path

        # add to draw que
        if draw_q != None:
            L1={'p1':path1[0],'p2':path1[1],'color':(255,0,100)}
            draw_q['lines'].append(L1)
            L2={'p1':path2[0],'p2':path2[1],'color':(255,0,100)}
            draw_q['lines'].append(L2)
