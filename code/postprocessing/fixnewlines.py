import sys, codecs

def readCSV(content, sep=','):
    lns = content.strip().split('\n')
    if len(lns) > 1 or len(lns[0]) > 0:
        lns = [[int(c) for c in row.split(sep)] for row in lns]
    else:
        lns = []
    return lns

def load(fname, useUtf8=False):
    if useUtf8:
        f = codecs.open(fname, 'r', 'utf-8')
    else:
        f = open(fname, 'r')
    c = f.read()
    f.close()
    return c

def writeCSV(csv, sep=','):
    output = [[str(c) for c in row] for row in csv]
    output = [sep.join(row) for row in output]
    return '\n'.join(output)

def dump(fname, contents):
    f = open(fname, 'w')
    f.write(contents)
    f.close()

def getWhitespaceAdjust(sentence):
    nonln = sentence.replace('\n', ' ')
    numExtraSpaces, countingSpaces = 0, False
    for c in nonln:
        if c == ' ':
            if not countingSpaces: countingSpaces = True
            else: numExtraSpaces += 1
        else:
            countingSpaces = False
    return numExtraSpaces

def getWhitespaceAdjust2(sentence, isLast):
    if isLast:
        sentence = sentence.strip()
    nonln = sentence.replace('\n', ' ')
    #nonln = sentence.replace('\n', '')
    numExtraSpaces, countingSpaces = 0, False
    for c in nonln:
        if c == ' ':
            if not countingSpaces: countingSpaces = True
            else: numExtraSpaces += 1
        else:
            countingSpaces = False
    return numExtraSpaces

def getAdditionalWhitespaceAfter(text, endBnd):
    ix, ws, isWhitespace = 0, 0, True
    while isWhitespace:
        if (endBnd+ix) < len(text) and text[endBnd+ix] in [' ','\n']:
            ws += 1
            ix += 1
        else: isWhitespace = False
    if ws > 0: return ws - 1
    else: return ws

def getAdditionalWhitespaceAfter2(text, endBnd):
    ix, ws, isWhitespace = 0, 0, True
    while isWhitespace:
        if (endBnd+ix) < len(text) and text[endBnd+ix] in [' ','\n']:
            ws += 1
            ix += 1
        else: isWhitespace = False
    if ws == 0:
        while (endBnd+ix) < len(text) and not text[endBnd+ws] in [' ','\n']:
            ws -= 1
        return ws
    else:
        return ws - 1
    #if ws > 0: return ws - 1
    #else: return ws
    #return ws - 1

def correct(csv, text):
    outCSV = []
    offset=0
    for [start, end] in csv:
        nlAdjuster = 0
        sentence = text[start+offset:end+offset]
        newAdjust = getWhitespaceAdjust(sentence)
        while nlAdjuster < newAdjust:
            nlAdjuster = newAdjust
            sentence = text[start+offset:end+offset+nlAdjuster]
            newAdjust = getWhitespaceAdjust(sentence)
        extra = getAdditionalWhitespaceAfter(text,end+offset+nlAdjuster)
        print str.format(" Orig: [{0}, {1}]; Offset: {2}; Extra space in sent: {3}; New: [{4}, {5}]", start, end, offset, nlAdjuster+extra, start+offset, end+offset+nlAdjuster+extra)
        outCSV.append([start+offset,end+offset+nlAdjuster+extra])
        offset += nlAdjuster + extra
    return outCSV

def correct2(csv, text):
    outCSV = []
    offset=0
    prevEnd=-1
    for [start, end] in csv:
        offset -= (start - prevEnd - 1)
        #nlAdjuster = 0
        #sentence = text[start+offset:end+offset]
        #newAdjust = getWhitespaceAdjust2(sentence)
        nlAdjuster, newAdjust = -1, 0
        while nlAdjuster < newAdjust:
            nlAdjuster = newAdjust
            sentence = text[start+offset:end+offset+nlAdjuster]
            newAdjust = getWhitespaceAdjust2(sentence, end==csv[-1][1])
        extra = getAdditionalWhitespaceAfter2(text,end+offset+nlAdjuster)
        #print str.format(" Orig: [{0}, {1}]; Offset: {2}; Extra space in sent: {3}; New: [{4}, {5}]", start, end, offset, nlAdjuster+extra, start+offset, end+offset+nlAdjuster+extra)
        outCSV.append([start+offset,end+offset+nlAdjuster+extra])
        prevEnd = end
        offset += nlAdjuster + extra
    return outCSV

def correctwrapper(csvf, textf, useUtf8=False):
    '''Used in i2b2 correction
    '''
    text = load(textf, useUtf8=useUtf8)
    csv = readCSV(load(csvf))
    return correct2(csv, text)

if __name__ == '__main__':
    bndsf=sys.argv[1]
    plnf=sys.argv[2]
    outf=sys.argv[3]

    pln=load(plnf)
    bnds=readCSV(load(bndsf))

    newBnds = correct(bnds, pln)
    dump(outf, writeCSV(newBnds))
