#convert cnf to dimacs format
def parse(cnf):

    var_list = map((lambda s : s.replace('-', '')),(' '.join(cnf)).split(' '))
    var_names = {}

    curr_var = 0

    for v in var_list:
        if v not in var_names:
            curr_var += 1
            var_names[v] = curr_var

    result = "p cnf "+str(curr_var)+" "+str(len(cnf))+"\n"

    for line in cnf:
        for v in line.split(' '):
            if v[0] == '-':
                result += '-'+str(var_names[v[1:]])+' '
            else:
                result += str(var_names[v])+' '
        result += '0\n'

    return result, var_names
