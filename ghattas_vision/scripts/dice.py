from sklearn.cluster import KMeans
from collections import Counter
import custom_math_func


def kme(centroids,draw_q=None):
    #initialize & optain variables
    numbers=['1','2','5','6']
    kmeans = KMeans(n_clusters=4, random_state=0 , n_init=10, max_iter=300).fit(centroids)
    count = Counter(kmeans.labels_)


    for y in range(4):
        # default vlue if number is not recognized n=0
        n='0'
        N=numbers.copy()

        # dice number recognition rules
        if '1' in N or '2' in N:
            if '1' in N:
                if count[y] > 3:
                    N.remove('1')
                if count[y] < 4 and count[y]%2==1:
                    n='1'
            if '2' in N:
                if count[y] > 6:
                    N.remove('2')
                if count[y] < 7 and count[y]%2==0:
                    n='2'
            if count[y] == 2:
                lab=kmeans.labels_
                l=[]
                for z in range(len(lab)):
                    if lab[z]==y:
                        l.append(centroids[z])
                ldeg=custom_math_func.deg(l)
                if ldeg <15 or ldeg > -15 or ldeg>75 or ldeg<-75:
                    n='1'
                else:
                    n='2'
                if '1' not in N:
                    n='2'
                if '2' not in N:
                    n='1'
        if '5' in N:
            if count[y] < 5:
                N.remove('5')
            if count[y]%5 == 0:
                n='5'
        if '6' in N:
            if count[y] < 6:
                N.remove('6')
            if count[y]%6 == 0:
                n='6'
        if len(N)==1:
            n = N[0]


        # remove already detected dice numbers from consideration
        try:
            numbers.remove(n)
        except:
            pass

        # add to draw que
        if draw_q != None:
            k = kmeans.cluster_centers_[y]
            kX=int(k[0])
            kY=int(k[1])
            C={'center':(kX,kY),'radius':5,'color':(0, 255, 255)}
            draw_q['circle'].append(C)
            T={'text':n,'p':(kX - 20, kY - 20),'color':(0, 255, 255)}
            draw_q['text'].append(T)
