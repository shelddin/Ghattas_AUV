#1 iterate through the tracks list to find matching new point
#2 when a track and a new point are matched remove them
#3 repete the process with increasing minimum_dist threshold untill all tracks or points are matched
#4 calculate track age when age>150frames remove the oldest point
#5 when a track is lost for over 30frames drop the track
import custom_math_func

min_dist=[50,100,200,300,500]

def motion_tracking(draw,tracks,centers):

    new_tracks=[]

    for mdist in min_dist:
        if tracks and centers:
            for t in tracks:
                tp=t['lines']
                tp=tp[-1]
                tp=tp[1]
                for c in centers:
                    L=(tp,c)
                    delt=custom_math_func.length(L)
                    if delt < mdist:
                        t['lines'].append((tp,c))
                        t['lost']=0
                        new_tracks.append(t)
                        tracks.remove(t)
                        centers.remove(c)
                        break

    if centers:
        for c in centers:
            nt={'lines':[(c,c)],'age':0,'lost':0}
            new_tracks.append(nt)

    if tracks:
        for t in tracks:
            t['lost']=t['lost']+1
            if t['lost'] < 30:
                new_tracks.append(t)
            else:
                print('opps looks like we lost 1!!')

    if new_tracks:
        for t in new_tracks:
            t['age']=t['age']+1
            if t['age'] > 150:
                t['lines'].pop(0)
            for l in t['lines']:
                L={'p1':l[0],'p2':l[1],'color':(255,0,255)}
                draw['lines'].append(L)

    return new_tracks
