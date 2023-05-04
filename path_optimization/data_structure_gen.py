import utm

diction = {}

def list(filename: str, latlon: bool):
    temp_list = []
    file = open(filename)
    for line in file:
        a,x,y,z = line.split(',')
        if latlon == True:
            temp_list.append((z.strip(),float(y),float(x)))
        else:
            temp_list.append(tuple(z,utm.from_latlon(float(y),float(x))[:2]))
    return temp_list

def dictionary(filename: str, latlon: bool):
    temp_dict = {}
    file = open(filename)
    for line in file:
        a,x,y,z = line.split(',')
        if latlon == True:
            temp_dict[z.strip()] = (float(y),float(x))
        else:
            temp_dict[z.strip()] = tuple(utm.from_latlon(float(y),float(x))[:2])
    return temp_dict