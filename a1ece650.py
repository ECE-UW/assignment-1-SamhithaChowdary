import re
import sys

'''Please don't consider adjacent point cases'''

'''Output Code'''
def main(output):
    V = output['V']
    E = output['E']
    print 'V={'

    for V_key in V:
        print "%s:(%.2f,%.2f)" % (V_key, V[V_key][0], V[V_key][1])
    print '}'
    print ' '
    print 'E={'

    for i in range(len(E)):
        if (i < len(E) - 1):
            print "<" + str(E[i][0]) + "," + str(E[i][1]) + ">,"
        else:
            print "<" + str(E[i][0]) + "," + str(E[i][1]) + ">"
    print '}'

''' Intersection '''
def intersection(t1, t2, t3, t4):
    temperory_list = [t1, t2, t3, t4]
    temperory_set = set(temperory_list)
    if (len(temperory_set) == 2):
        return "same"
    elif (len(temperory_set) == 3):
        temperory_crossing = 0
        for elem in temperory_list:
            if (temperory_list.count(elem) == 2):
                temperory_crossing = elem
        temperory_set.remove(temperory_crossing)
        temperory_V_list = list(temperory_set)

        if (temperory_V_list[0][0] <= temperory_crossing[0] <= temperory_V_list[1][0]
            or temperory_V_list[1][0] <= temperory_crossing[0] <= temperory_V_list[0][0]
            or temperory_V_list[0][1] <= temperory_crossing[1] <= temperory_V_list[1][1]
            or temperory_V_list[1][1] <= temperory_crossing[1] <= temperory_V_list[0][1]):
            returnx = temperory_crossing[0]
            returny = temperory_crossing[1]
            return (returnx, returny)
        else:
            return "same intersection pt"
    else:
        if (t1[0] == t2[0] != t3[0] == t4[0]):
            return 0
        elif (t1[0] == t2[0] == t3[0] == t4[0]):
            if (t1[1] < t3[1] < t2[1] or t2[1] < t3[1] < t1[1] or t1[1] < t4[1] < t2[1] or t2[1] < t4[1] < t1[1]):
                return "same intersection pt"
            else:
                return 0
        elif (t1[0] == t2[0]):
            returnx = t1[0]
            c = (t3[1] - t4[1]) / (t3[0] - t4[0])
            d = t3[1] - (t3[1] - t4[1]) / (t3[0] - t4[0]) * t3[0]
            returny = c * returnx + d


        elif (t3[0] == t4[0]):
            returnx = t3[0]
            a = (t1[1] - t2[1]) / (t1[0] - t2[0])
            b = t1[1] - (t1[1] - t2[1]) / (t1[0] - t2[0]) * t1[0]
            returny = a * returnx + b

        else:
            a = (t1[1] - t2[1]) / (t1[0] - t2[0])
            b = t1[1] - (t1[1] - t2[1]) / (t1[0] - t2[0]) * t1[0]
            c = (t3[1] - t4[1]) / (t3[0] - t4[0])
            d = t3[1] - (t3[1] - t4[1]) / (t3[0] - t4[0]) * t3[0]
            if (a - c == 0):
                if ((t3[1] == a * t3[0] + b and t1[1] < t3[1] < t2[1])
                    or (t3[1] == a * t3[0] + b and t2[1] < t3[1] < t1[1])
                    or (t3[1] == a * t3[0] + b and t1[1] < t4[1] < t2[1])
                    or (t3[1] == a * t3[0] + b and t2[1] < t4[1] < t1[1])):
                    return "same intersection pt"
                else:
                    return 0

            else:
                returnx = (d - b) / (a - c)
                returny = (a * d - c * b) / (a - c)

        if ((returnx > t1[0] and returnx > t2[0])
            or (returnx < t1[0] and returnx < t2[0])
            or (returnx > t3[0] and returnx > t4[0])
            or (returnx < t3[0] and returnx < t4[0])
            or (returny > t1[1] and returny > t2[1])
            or (returny < t1[1] and returny < t2[1])
            or (returny > t3[1] and returny > t4[1])
            or (returny < t3[1] and returny < t4[1])):
            return 0
        else:
            return (returnx, returny)

'''Checking duplicate values'''
def streetchecker(output, streetname, streetline):
    S = output['S']
    s_input = []

    for i in range(0, len(streetline) - 1, 2):
        s_input.append((float(streetline[i]), float(streetline[i + 1])))

    for i in range(len(s_input) - 1):
        if (s_input[i] == s_input[i + 1]):
            return "same_nxt_pt"

    for i in range(len(s_input) - 1):
        j = i + 1

        while (j < (len(s_input) - 1)):
            x = intersection(s_input[i], s_input[i + 1], s_input[j], s_input[j + 1])
            if (x == "same intersection pt"):
                return "cover_itself"
            elif (x != 0 and x not in s_input):
                return "cover_itself"

            j = j + 1

    for i in range(len(s_input) - 1):
        for S_key in S:
            if (S_key != streetname):
                for j in range(len(S[S_key]) - 1):
                    x = intersection(s_input[i], s_input[i + 1], S[S_key][j], S[S_key][j + 1])
                    if (x == "same intersection pt"):
                        return "cover_other"


'''First Validation'''


def add(output, streetname, streetline):
    s = output['S']
    V = output['V']
    E = output['E']
    s[streetname] = []

    for i in range(0, len(streetline) - 1, 2):
        s[streetname].append((float(streetline[i]), float(streetline[i + 1])))

    E_crossing_set = set()

    for E_elem in E:
        E_crossing_set.add((V[E_elem[0]], V[E_elem[1]]))

    V_near_crossing_set = set()

    comp = []

    for s_key1 in s:
        for s_key2 in s:
            if (s_key1 != s_key2 and set([s_key1, s_key2]) not in comp):
                comp.append(set([s_key1, s_key2]))
                i = 0
                j = 0
                while (i < len(s[s_key1]) - 1):
                    while (j < len(s[s_key2]) - 1):
                        V_interx = intersection(s[s_key1][i], s[s_key1][i + 1], s[s_key2][j], s[s_key2][j + 1])
                        if (V_interx != 0 and V_interx != "same intersection pt"):
                            V_near_crossing_set.update(
                                [s[s_key1][i], s[s_key1][i + 1], s[s_key2][j], s[s_key2][j + 1], V_interx])
                            if (V_interx not in s[s_key1] and V_interx not in s[s_key2]):
                                E_crossing_set.update(
                                    [(s[s_key1][i], V_interx), (V_interx, s[s_key1][i + 1]),
                                     (s[s_key2][j], V_interx), (V_interx, s[s_key2][j + 1])])
                                if ((s[s_key1][i], s[s_key1][i + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[s_key1][i], s[s_key1][i + 1]))
                                if ((s[s_key2][j], s[s_key2][j + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[s_key2][j], s[s_key2][j + 1]))
                                s[s_key1].insert(i + 1, V_interx)
                                s[s_key2].insert(j + 1, V_interx)
                                j = j + 1

                            elif (V_interx in s[s_key1] and V_interx not in s[s_key2]):
                                E_crossing_set.update([(s[s_key2][j], V_interx), (V_interx, s[s_key2][j + 1])])
                                if ((s[s_key2][j], s[s_key2][j + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[s_key2][j], s[s_key2][j + 1]))
                                s[s_key2].insert(j + 1, V_interx)
                                j = j + 1

                            elif (V_interx in s[s_key2] and V_interx not in s[s_key1]):
                                E_crossing_set.update(
                                    [(s[s_key1][i], V_interx), (V_interx, s[s_key1][i + 1])])
                                if ((s[s_key1][i], s[s_key1][i + 1]) in E_crossing_set):
                                    E_crossing_set.remove((s[s_key1][i], s[s_key1][i + 1]))
                                s[s_key1].insert(i + 1, V_interx)

                                j = j + 1

                            elif (V_interx in s[s_key1] and V_interx in s[s_key2]):
                                E_crossing_set.update(
                                    [(s[s_key1][i], s[s_key1][i + 1]), (s[s_key2][j], s[s_key2][j + 1])])
                        j = j + 1
                    j = 0
                    i = i + 1

    if (len(V) == 0):
        V_new_list = list(V_near_crossing_set)
        count = 0

    else:
        V_values_set = set(V.values())
        V_new_set = V_near_crossing_set - V_values_set
        V_new_list = list(V_new_set)
        V_key_list = V.keys()
        count = V_key_list[len(V_key_list) - 1]

    for V_elem in V_new_list:
        count = count + 1
        V[count] = V_elem

    E_list = list(E_crossing_set)
    E = []

    for E_elem in E_list:
        for V_key in V:
            if (E_elem[0] == V[V_key]):
                t1 = V_key
            if (E_elem[1] == V[V_key]):
                t2 = V_key
        E.append((t1, t2))

    output['S'] = s
    output['V'] = V
    output['E'] = E

    return output
'''Second Validation'''
def delete(output, streetname):
    S = output['S']
    V = output['V']
    E = output['E']
    s = S[streetname]
    V_id_du = {}
    V_id_1 = []
    V_id_3_4 = []
    V_id_2_m4 = []
    s_V_id = []
    V_del_set = set()

    for E_elem in E:
        if (E_elem[0] not in V_id_du.keys()):
            V_id_du[E_elem[0]] = 1

        else:
            V_id_du[E_elem[0]] = V_id_du[E_elem[0]] + 1

        if (E_elem[1] not in V_id_du.keys()):
            V_id_du[E_elem[1]] = 1

        else:
            V_id_du[E_elem[1]] = V_id_du[E_elem[1]] + 1

    for V_id_du_key in V_id_du:
        if (V_id_du[V_id_du_key] == 1):
            V_id_1.append(V_id_du_key)

        elif (3 <= V_id_du[V_id_du_key] <= 4):
            V_id_3_4.append(V_id_du_key)

        else:
            V_id_2_m4.append(V_id_du_key)

    for i in range(len(s)):

        for V_key in V:
            if (s[i] == V[V_key]):
                s_V_id.append(V_key)

    for i in range(len(s_V_id)):
        if (i != len(s_V_id) - 1):
            if ((s_V_id[i], s_V_id[i + 1]) in E):
                E.remove((s_V_id[i], s_V_id[i + 1]))
            elif ((s_V_id[i + 1], s_V_id[i]) in E):
                E.remove((s_V_id[i + 1], s_V_id[i]))
        if (s_V_id[i] in V_id_1):
            del V[s_V_id[i]]
        elif (s_V_id[i] in V_id_3_4):
            merge = {0: 0, 1: 0}
            E_output = E[:]
            for E_elem in E:
                if (s_V_id[i] == E_elem[0]):
                    merge[1] = E_elem[1]
                elif (s_V_id[i] == E_elem[1]):
                    merge[0] = E_elem[0]
                if ((s_V_id[i], merge[1]) in E_output):
                    E_output.remove((s_V_id[i], merge[1]))
                elif ((merge[0], s_V_id[i]) in E_output):
                    E_output.remove((merge[0], s_V_id[i]))

            E = E_output[:]
            E.append((merge[0], merge[1]))
            V_del_set.add(V[s_V_id[i]])
            del V[s_V_id[i]]


    E_output = E[:]
    for elem in E:
        if (elem[0] in V_id_1 and elem[1] in V_id_1):
            E_output.remove(elem);
            del V[elem[0]]
            del V[elem[1]]
    E = E_output[:]
    del S[streetname]
    for S_key in S:
        for elem in S[S_key]:
            if (elem in V_del_set):
                S[S_key].remove(elem)

    output['V'] = S
    output['V'] = V
    output['E'] = E

    return output


output = {'V': {}, 'E': [], 'S': {}}


'''RegularGX'''
while (1):
    S = output['S']
    try:
        input_x = raw_input()
    except EOFError:
        break

    x = re.match(r'^\s*(\w)\s*"(.*)"(.*)$', input_x)
    x_g = re.match(r'^\s*(g)\s*$', input_x)

    if x:
        cmd = x.group(1)
        scmd = re.match(r'[acrg]$', cmd)
        if not scmd:
            sys.stderr.write("Error: input does not start with 'a' or 'c' or 'r' or 'g' \n")
            continue
        if (cmd == 'a' or cmd == 'c' or cmd == 'r'):
            streetname = re.match(r'^\s*$', x.group(2))
            if streetname:
                sys.stderr.write("Error: street name is null \n")
                continue
            if (cmd == 'a' and (x.group(2) in S.keys())):
                sys.stderr.write("Error: 'a' specified for a street that already exists \n")
                continue

            if (cmd == 'c' and (x.group(2) not in S.keys())):
                sys.stderr.write("Error: 'c' specified for a street that does not exist \n")
                continue

            if (cmd == 'r' and (x.group(2) not in S.keys())):
                sys.stderr.write("Error: 'r' specified for a street that does not exist \n")
                continue

        if (cmd == 'a' or cmd == 'c'):
            streetline = re.match(r'(\s*\(\s*-?\d+\s*,\s*-?\d+\s*\)\s*)*$', x.group(3))

            if streetline:
                p = re.compile(r'-?\d+')
                streetline_list = p.findall(x.group(3))
                if (len(streetline_list) == 0):
                    sys.stderr.write("Error: Incomplete coordinates for \"" + x.group(2) + "\"\n")
                    continue
                if (len(streetline_list) == 2):
                    sys.stderr.write("Error: Incomplete coordinates for \"" + x.group(2) + "\"\n")
                    continue

                check = streetchecker(output, x.group(2), streetline_list)
                if (check == "same_nxt_pt"):
                    sys.stderr.write("Error: two neighboring point in \"" + x.group(2) + "\" are same ,can not be made into a segment \n")
                    continue

                if (check == "cover_itself"):
                    sys.stderr.write("Error: the part of \"" + x.group(2) + "\" covers another part of itself \n")
                    continue

                if (check == "cover_other"):
                    sys.stderr.write(
                        "Error: the part of \"" + x.group(2) + "\" covers another part of other streets \n")
                    continue

            else:
                sys.stderr.write("Error: Incomplete coordinates for \"" + x.group(2) + "\"\n")
                continue

        if (cmd == 'r'):
            streetline = re.match(r'^\s*$', x.group(3))
            if not streetline:
                sys.stderr.write("Error: 'r' specified for a street that defines coordinates again \n")
                continue

        if (cmd == 'a'):
            output = add(output, x.group(2), streetline_list)

        elif (cmd == 'c'):
            output = delete(output, x.group(2))
            output = add(output, x.group(2), streetline_list)

        elif (cmd == 'r'):
            output = delete(output, x.group(2))

    elif x_g:
        main(output)

    else:
        sys.stderr.write("Error: input is not valid \n")
