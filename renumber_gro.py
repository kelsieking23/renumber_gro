import argparse

def renumberGro(m, f):
    res_ids = getReferenceResidues(m)
    f = open(f, 'r')
    contents = f.readlines()
    f.close()
    k = 0
    i = 0
    index = -1
    new_contents = []
    for line in contents:
        if k != 2:
            k += 1
            new_contents.append(line)
            continue
        if line == contents[-1]:
            new_contents.append(line)
            break
        res_id = line.strip().split()[0]
        if res_id in res_ids:
            new_contents.append(line)
            continue
        if i == len(res_ids):
            i = 0
            index = 0
        parts = line.split()
        parts[0] = res_ids[index]
        format = '{:>8s}{:>7s}{:5s}{:>8s}{:>8s}{:>8s}\n'.format(*parts)
        new_contents.append(format)
        i += 1
        index += 1
    return new_contents

def getReferenceResidues(m):
    f = open(m, 'r')
    contents = f.readlines()
    f.close()

    i = 0
    res_ids = []
    for line in contents:
        if i != 2:
            i += 1
            continue
        if line == contents[-1]:
            break
        res_id = line.strip().split()[0]
        res_ids.append(res_id)
    return res_ids
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', required=True, help='The output of gmx insert-molecules (.gro) (the .gro file with multiple peptides)')
    parser.add_argument('-m', required=True, help='File (.gro) of the monomer inserted into the multi-peptide system')
    parser.add_argument('-o', required=True, default='renumber.gro', help='Path to renumbered output (.gro)')

    args = parser.parse_args()

    f = args.f
    m = args.m
    o = args.o

    renumbered = renumberGro(m, f)
    f = open(o, 'w')
    for line in renumbered:
        f.write(line)
    f.close()
    print('Wrote {}'.format(o))