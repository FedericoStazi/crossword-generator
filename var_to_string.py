#return the not prefix if b is 1
def nt(b):
    return "-" if b else ""

#create the c variable as a string
def c(i, j, s, b=0):
    return nt(b)+"c_"+str(i)+"_"+str(j)+"_"+s

#create the h variable as a string
def h(i, j, w, b=0):
    return nt(b)+"h_"+str(i)+"_"+str(j)+"_"+str(w)

#create the H variable as a string
def H(i, j, b=0):
    return nt(b)+"H_"+str(i)+"_"+str(j)

#create the v variable as a string
def v(i, j, w, b=0):
    return nt(b)+"v_"+str(i)+"_"+str(j)+"_"+str(w)

#create the V variable as a string
def V(i, j, b=0):
    return nt(b)+"V_"+str(i)+"_"+str(j)
