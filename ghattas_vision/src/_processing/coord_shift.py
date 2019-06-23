



def coord_shift(pts,x_shift,y_shift):
	shift_pts=[]
	for pt in pts:
		shift_pt = (pt[0]-x_shift,y_shift-pt[1])
		shift_pts.append(shift_pt)

	return shift_pts
