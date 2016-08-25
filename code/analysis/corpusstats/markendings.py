#encoding: utf-8
import calculatestats as cs
import optparse, os, codecs
from i2b2classes import classes as i2b2classes

def writeCSV(data, sep=','):
    output = [[str(c) for c in row] for row in data]
    output = [sep.join(row) for row in output]
    return '\n'.join(output)

def dump(fname, content):
    f = codecs.open(fname, 'w', 'utf-8')
    f.write(content)
    f.close()

def markEndings(content, bounds, classes):
    marked = []
    for [start, end] in bounds:
        sentence = content[start:end].strip()
        if len(sentence) > 0:
            endgrp = classes[sentence[-1]]
        else:
            endgrp = 'N'
        marked.append([start, end, endgrp])
    return marked

def markCorpusEndings(corpus, classes, useUtf8):
    for [fl, bndsf, mrkdf] in corpus:
        content = cs.load(fl, useUtf8)
        try:
            bnds = cs.readCSV(cs.load(bndsf))
            marked = markEndings(content, bnds, classes)
        except ValueError, e:
            marked = []
        dump(mrkdf, writeCSV(marked))

def cli():
    parser = optparse.OptionParser(usage='Usage: %prog -t TEXTDIR -b BOUNDSDIR -m MARKEDDIR -e TEXTEND -E BOUNDSEND -M MARKEDEND')
    parser.add_option('-t', '--textdir', dest='textdir',
        help='directory with plaintext files')
    parser.add_option('-b', '--boundsdir', dest='boundsdir',
        help='directory with bounds files')
    parser.add_option('-e', '--textend', dest='textend',
        help='file extension of plaintext files')
    parser.add_option('-E', '--boundsend', dest='boundsend',
        help='file extension of bounds files')
    parser.add_option('-m', '--markeddir', dest='markeddir',
        help='directory to put marked files in')
    parser.add_option('-M', '--markedend', dest='markedend',
        help='file extension of marked files')
    parser.add_option('-p', '--prefix', dest='prefix',
        default="", help='prefix of bounds files')
    parser.add_option('-u', '--useUtf8', dest='useUtf8',
        help='help here', action='store_true', default=False)
    (options, args) = parser.parse_args()
    if not options.textdir or not options.boundsdir or not options.markeddir or not options.textend or not options.boundsend or not options.markedend:
        parser.print_help()
        exit()
    return options.textdir, options.boundsdir, options.markeddir, options.textend, options.boundsend, options.markedend, options.prefix, options.useUtf8

if __name__ == '__main__':
    txtd, bndsd, mrkd, txte, bndse, mrke, prefix, useUtf8 = cli()
    corpus = cs.getCorpus(txtd, bndsd, txte, bndse, prefix)
    newcorpus = []
    for [txt, bnds] in corpus:
        markedf = os.path.join(mrkd, os.path.basename(bnds)[:-len(bndse)]+mrke)
        newcorpus.append([txt,bnds,markedf])
    markCorpusEndings(newcorpus, i2b2classes, useUtf8)
