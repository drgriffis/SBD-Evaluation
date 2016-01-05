'''
Script for parsing Penn Treebank-formatted (PRD) Switchboard files.

Uses NLTK to parse PTB formatting.
'''
import sys
import nltk.tree

def getTree(fname):
    """Parse the input filepath into a Tree object
    """
    f = open(fname,'r')
    allLns = f.readlines()
    f.close()

    treeLns = []
    for ln in allLns:
        if ln[0:2] != "*x": treeLns.append(ln)
    treeStr = ''.join(treeLns)
    treeStr = '(ROOT ' + treeStr + ')'
    return nltk.tree.Tree.fromstring(treeStr)

def getPlaintextAndBounds(t):
    """Given a Tree object, returns its plaintext and CSV sentence bounds
    """
    d = DialogueExtractor()
    utterances, bounds = d.pullText(t)
    # A/B: UTTERANCE
    #strUtterances = [str.format("{0}: {1}", u[0], u[1]) for u in utterances]
    # UTTERANCE ONLY
    strUtterances = [u[1] for u in utterances]

    strBounds = [','.join([str(b) for b in bnd]) for bnd in bounds]
    return '\n'.join(strUtterances), '\n'.join(strBounds)

def dump(fname, contents):
    f = open(fname, 'w')
    f.write(contents)
    f.close()

class DialogueExtractor:
    """Class for parsing PTB Switchboard tree
    """

    def __init__(self):
        self.se = SentenceExtractor()

    def pullText(self, t):
        self.text, self.bounds, self.curspeaker = [], [], '?'
        for i in range(len(t)):
            subtree = t[i][0]
            # CODE SpeakerA/B signifies speaker switch
            if subtree.label() == 'CODE':
                labl = subtree[0]
                if len(labl) > 7 and labl[0:7] == 'Speaker':
                    self.curspeaker = labl[7]
            else:
                self.text.append((self.curspeaker, self.se.pullText(subtree)))
        self.collapseUtterances()
        return self.text, self.bounds

    def collapseUtterances(self):
        utterances, utterance = [], []
        bounds, curStart = [], 0
        prevSpeaker = None
        for (speaker, chunk) in self.text:
            if speaker != prevSpeaker:
                if len(utterance) > 0:
                    utterances.append((prevSpeaker, ' '.join(utterance)))
                utterance = []
            utterance.append(chunk)
            prevSpeaker = speaker
            # add bounds of sentence
            bounds.append((curStart, curStart + len(chunk)))
            curStart += len(chunk) + 1
        # flush the last utterance
        if len(utterance) > 0:
            utterances.append((prevSpeaker, ' '.join(utterance)))
        self.text = utterances
        self.bounds = bounds

class SentenceExtractor:
    
    def pullText(self, s):
        self.firstToken = True
        self.tokens = []
        self.processTree(s)
        return ''.join(self.tokens)

    def processTree(self, t):
        if type(t) != type('abc'):
            for i in range(len(t)):
                self.processTree(t[i])
        # ignore non-text symbols
        elif not t[0] in '[]*+' and t != 'E_S' and t != 'N_S' and t != '0':
            if not self.firstToken and not t.strip() in '.,?!\'' and t.strip() != "'s":
                self.tokens.append(' ' + t)
            else:
                self.tokens.append(t)
                self.firstToken = False


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: plaintext PRDFILE PLNFILE BNDFILE\n")
        print("\tPRDFILE  .prd file to parse")
        print("\tPLNFILE  path to write plaintext file to")
        print("\tBNDFILE  path to write sentence bounds to")
        exit(1)
    inf = sys.argv[1]
    outf = sys.argv[2]
    bndf = sys.argv[3]
    t = getTree(inf)
    text, bounds = getPlaintextAndBounds(t)
    dump(outf, text)
    dump(bndf, bounds)
