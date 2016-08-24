import sys
import codecs
import optparse

def cli():
    parser = optparse.OptionParser(usage='Usage: %prog -t TYPE -f INFILE -o OUTFILE -s SLICESFILE')
    parser.add_option('-t', '--type', dest='proctype',
        help='pre or post')
    parser.add_option('-f', '--input-file', dest='infname',
        help='name of BNC data file to fix')
    parser.add_option('-o', '--output-file', dest='outfname',
        help='where to save reformatted BNC text')
    parser.add_option('-s', '--slices-file', dest='slicesfname',
        help='where to save slice information')
    (options, args) = parser.parse_args()
    if not options.proctype or not options.infname or not options.outfname or not options.slicesfname:
        parser.print_help()
        exit()
    return options.proctype, options.infname, options.outfname, options.slicesfname

def dump(fname, content):
    f = codecs.open(fname, 'w', 'utf-8')
    f.write(content)
    f.close()

def load(fname):
    f = codecs.open(fname, 'r', 'utf-8')
    c = f.read()
    f.close()
    return c

def fromCSV(text):
    lns = text.strip().split('\n')
    try:
        lns = [ln.split(',') for ln in lns]
        return [[int(ln[0]),int(ln[1])] for ln in lns]
    except ValueError, e:
        return []

def toCSV(data):
    return '\n'.join([','.join([str(c) for c in row]) for row in data])

def flatten(bnds):
    flat = []
    for bnd in bnds:
        flat.extend(bnd)
    return flat

def deflatten(flatBnds):
    bnds, bnd = [], []
    isEnd = False
    for flat in flatBnds:
        bnd.append(flat)
        if not isEnd: isEnd = True
        else:
            bnds.append(bnd)
            bnd = []
            isEnd = False
    return bnds

def removeMultiNewlines(inf, outf, slcf):
    c = load(inf)

    output = []
    slices = []
    threshold, seen = 0, 0
    slicing = False
    for i in range(len(c)):
        char = c[i]
        if char != '\n':
            if slicing:
                numSliced = seen-threshold
                slices.append(((i-numSliced), numSliced))
                slicing = False
            seen = 0
            output.append(char)
        else:
            seen += 1
            if seen <= threshold:
                output.append(char)
            else:
                slicing = True
    if slicing:
        numSliced = seen-threshold
        slices.append(((i-numSliced), numSliced))

    dump(outf, ''.join(output))
    dump(slcf, toCSV(slices))

def reinstateMultiNewlines(inf, outf, slcf):
    bnds = fromCSV(load(inf))
    slices = fromCSV(load(slcf))

    slicesIx = 0
    offset = 0
    bndsIx = 0
    newBnds = []
    for bnd in flatten(bnds):
        #print str.format("Bound: {0}\tCorrected: {1}\tSlice: {2}\tGreater: {3}", bnd, bnd+offset+1, slices[slicesIx][0], bnd+offset+1 >= slices[slicesIx][0])
        while (slicesIx < len(slices)
            and (bnd+offset+1 >= slices[slicesIx][0]
                 or bnd+offset+2 == slices[slicesIx][0])):
            if bnd+offset+2 == slices[slicesIx][0]:
                offset += slices[slicesIx][1] + 1
            else:
                offset += slices[slicesIx][1]
            slicesIx += 1
        bnd += offset
        newBnds.append(bnd)
    newBnds = deflatten(newBnds)

    dump(outf, toCSV(newBnds))

if __name__ == '__main__':
    ptype, infname, outfname, slicesfname = cli()
    if ptype == 'pre':
        removeMultiNewlines(infname, outfname, slicesfname)
    elif ptype == 'post':
        reinstateMultiNewlines(infname, outfname, slicesfname)
