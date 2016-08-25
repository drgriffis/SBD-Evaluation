'''
Methods for analysing average sentence length in a corpus and determining the frequency of sentence-terminal characters.
'''

import sys, os
import codecs
import optparse

def readCSV(content, sep=','):
    lns = content.strip().split('\n')
    lns = [[int(c) for c in row.split(sep)] for row in lns]
    return lns

def load(fname, useUtf8=False):
    if useUtf8:
        f = codecs.open(fname, 'r', 'utf-8')
    else:
        f = open(fname, 'r')
    c = f.read()
    f.close()
    return c

def laxincrement(dct, key, inc=1):
    if dct.has_key(key):
        dct[key] += inc
    else:
        dct[key] = inc

def getSentenceEndings(content, bounds):
    ends = {}
    for [start, end] in bounds:
        sentence = content[start:end].strip()
        if len(sentence) > 0:
            laxincrement(ends, sentence[-1])
    return ends

def getSentenceNumTokens(content, bounds):
    numTokens = 0
    sentCount = 0
    for [start, end] in bounds:
        sentence = content[start:end].strip()
        if len(sentence) > 0:
            numTokens += len(sentence.split())
            sentCount += 1
    return numTokens, sentCount

def analyzeCorpusSentEnds(corpus):
    corpusEnds = {}
    for [fl, bndsf] in corpus:
        content = load(fl)
        bnds = readCSV(load(bndsf))
        ends = getSentenceEndings(content, bnds)
        for endchr in ends.keys():
            laxincrement(corpusEnds, endchr, ends[endchr])
    return corpusEnds

def analyzeCorpusSentLen(corpus):
    globalNumTokens, globalSentCount = 0, 0
    for [fl, bndsf] in corpus:
        content = load(fl)
        bnds = readCSV(load(bndsf))
        numTokens, sentCount = getSentenceNumTokens(content, bnds)
        globalNumTokens += numTokens
        globalSentCount += sentCount
    return float(globalNumTokens)/globalSentCount

def getCorpus(txtdir, bndsdir, txtend, bndsend, prefix=""):
    corpus = []
    for f in os.listdir(txtdir):
        if os.path.isfile(os.path.join(txtdir, f)):
            text = os.path.join(txtdir, f)
            bnds = os.path.join(bndsdir, prefix + f[:-len(txtend)]+bndsend)
            corpus.append([text, bnds])
    return corpus

def cli():
    parser = optparse.OptionParser(usage='Usage: %prog -t TEXTDIR -b BOUNDSDIR -e TEXTEND -E BOUNDSEND')
    parser.add_option('-t', '--textdir', dest='textdir',
        help='directory with plaintext files')
    parser.add_option('-b', '--boundsdir', dest='boundsdir',
        help='directory with bounds files')
    parser.add_option('-e', '--textend', dest='textend',
        help='file extension of plaintext files')
    parser.add_option('-E', '--boundsend', dest='boundsend',
        help='file extension of bounds files')
    parser.add_option('-a', '--analysis', dest='atype',
        help='ends or len')
    (options, args) = parser.parse_args()
    if not options.textdir or not options.boundsdir or not options.textend or not options.boundsend or not options.atype or not options.atype in ['ends','len']:
        parser.print_help()
        exit()
    return options.textdir, options.boundsdir, options.textend, options.boundsend, options.atype

if __name__ == '__main__':
    txtd, bndsd, txte, bndse, atype = cli()
    corpus = getCorpus(txtd, bndsd, txte, bndse)

    if atype == 'ends':
        corpusEnds = analyzeCorpusSentEnds(corpus)

        sm = 0
        for key in corpusEnds.keys():
            print str.format("{0}\t{1}", key.encode('utf-8'), corpusEnds[key])
            sm += corpusEnds[key]
        print '-----------\nTotal sentences: ', sm
    else:
        avgLen = analyzeCorpusSentLen(corpus)
        print avgLen
