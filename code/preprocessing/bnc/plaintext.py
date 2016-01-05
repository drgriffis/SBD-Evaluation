'''
Script for extracting plaintext and sentence boundaries from BNC XML files.

For more detailed analysis, plaintext and sentence bound filenames are prefixed with the domain of the source text (e.g. "ACPROSE" => Academic Prose, "FICTION" => Fiction, etc.).

Due to differing handling of whitespace by different toolkits, two different kinds of bounds are generated:
    strict      do not include whitespace between sentences
    permissive  do include whitepsace between sentences
'''
import sys
import os
import codecs
import xml.dom.minidom as dom

def dump(fname, contents):
    f = codecs.open(fname, 'w', 'utf-8')
    f.write(contents)
    f.close()

def processDoc(text):
    pe = PlaintextExtractor()
    return pe.processText(text)

def getTextAndType(trgd):
    bncDoc = trgd.firstChild
    teiHeader = bncDoc.firstChild
    text = teiHeader.nextSibling
    while text.localName == None:
        text = text.nextSibling
    return text, text.getAttribute('type')

def boundsToCSV(bounds):
    csv = []
    for boundPair in bounds:
        line = []
        for b in boundPair: line.append(str(b))
        csv.append(','.join(line))
    return '\n'.join(csv)

def processText(text):
    allTokens, bounds = processNode(text, []), []
    return ''.join(allTokens), boundsToCSV(bounds)

class PlaintextExtractor:

    def processText(self, text):
        self.tokenList = []
        self.permissiveBoundsList = []
        self.strictBoundsList = []
        self.curStart, self.curEnd = 0, 0
        #self.processNode(text)
        self.processNodes(text)
        return ''.join(self.tokenList),\
               boundsToCSV(self.permissiveBoundsList),\
               boundsToCSV(self.strictBoundsList)

    def processNodes(self, startNode):
        nodeStack = [startNode]
        while len(nodeStack) > 0:
            node = nodeStack.pop(-1)
            # if empty, ignore
            if node == None:
                pass
            # if it's a word or punctuation, add the token
            elif node.localName == 'w' or node.localName == 'c':
                try:
                    text = node.firstChild.nodeValue
                    self.tokenList.append(text)
                    self.curEnd += len(text)
                    nodeStack.append(node.nextSibling)
                except AttributeError, e:
                    #print node.attributes.items()
                    #print node.firstChild
                    #exit(1)
                    pass
            # add two line breaks for a header or a div
            elif node.localName == 'head' or node.localName == 'div':
                # recursively process all contents
                self.processNodes(node.firstChild)
                # add two line breaks
                self.tokenList.append('\n\n')
                # update most recent bounds to reflect line breaks
                (start, end) = self.permissiveBoundsList[-1]
                self.permissiveBoundsList[-1] = (start, end + 2)
                self.curStart += 2; self.curEnd += 2
                # move on to next section
                nodeStack.append(node.nextSibling)
            # add one line break for a paragraph or an utterance switch
            elif node.localName == 'p' or node.localName == 'u':
                # process all child sentences (recursively)
                self.processNodes(node.firstChild)
                # add a line break
                self.tokenList.append('\n')
                # update most recent bounds to reflect line break
                if len(self.permissiveBoundsList) > 0:
                    (start, end) = self.permissiveBoundsList[-1]
                    self.permissiveBoundsList[-1] = (start, end + 1)
                self.curStart += 1; self.curEnd += 1
                # move to next paragraph/utterance
                nodeStack.append(node.nextSibling)
            # add a space after sentence breaks
            elif node.localName == 's':
                # recursively process this sentence
                self.processNodes(node.firstChild)
                # separate with single space
                self.tokenList.append(' ')
                # bounds
                self.permissiveBoundsList.append((self.curStart, self.curEnd))
                self.strictBoundsList.append((self.curStart, self.curEnd))
                self.curStart = self.curEnd + 1; self.curEnd += 1
                # move to next sentence
                nodeStack.append(node.nextSibling)
            # depth-first process straight through any other nodes
            else:
                self.processNodes(node.firstChild)
                nodeStack.append(node.nextSibling)

    def processNode(self, node):
        if node == None:
            pass
        # if it's a word or punctuation, add the token
        elif node.localName == 'w' or node.localName == 'c':
            try:
                text = node.firstChild.nodeValue
                self.tokenList.append(text)
                self.curEnd += len(text)
                self.processNode(node.nextSibling)
            except AttributeError, e:
                #print node.attributes.items()
                #print node.firstChild
                #exit(1)
                pass
        # add two line breaks for a header or a div
        elif node.localName == 'head' or node.localName == 'div':
            # process all contents
            self.processNode(node.firstChild)
            # add two line breaks
            self.tokenList.append('\n\n')
            # update most recent bounds to reflect line breaks
            (start, end) = self.permissiveBoundsList[-1]
            self.permissiveBoundsList[-1] = (start, end + 2)
            self.curStart += 2; self.curEnd += 2
            # move on to next section
            self.processNode(node.nextSibling)
        # add one line break for a paragraph or an utterance switch
        elif node.localName == 'p' or node.localName == 'u':
            # process all child sentences
            self.processNode(node.firstChild)
            # add a line break
            self.tokenList.append('\n')
            # update most recent bounds to reflect line break
            (start, end) = self.permissiveBoundsList[-1]
            self.permissiveBoundsList[-1] = (start, end + 1)
            self.curStart += 1; self.curEnd += 1
            # move to next paragraph/utterance
            self.processNode(node.nextSibling)
        # add a space after sentence breaks
        elif node.localName == 's':
            # process this sentence
            self.processNode(node.firstChild)
            # separate with single space
            self.tokenList.append(' ')
            # bounds
            self.permissiveBoundsList.append((self.curStart, self.curEnd))
            self.strictBoundsList.append((self.curStart, self.curEnd))
            self.curStart = self.curEnd + 1; self.curEnd += 1
            # move to next sentence
            self.processNode(node.nextSibling)
        # depth-first process straight through any other nodes
        else:
            self.processNode(node.firstChild)
            self.processNode(node.nextSibling)

if __name__ == '__main__':
    # check for correct arguments
    if len(sys.argv) < 4:
        print str.format('Usage: python {0} XMLFILE PLAINTEXT BOUNDS', __file__)
        exit()

    # fetch and parse the XML doc to get its doctype
    doc = sys.argv[1]
    trgd = dom.parse(doc)
    text, doctype = getTextAndType(trgd)

    # format names for processed files
    plainname = str.format(sys.argv[2], doctype)
    sBoundsname = str.format(sys.argv[3], doctype, 'strict')
    pBoundsname = str.format(sys.argv[3], doctype, 'permissive')

    # check if processed files exists first
    if os.path.exists(plainname) and os.path.exists(sBoundsname) and os.path.exists(pBoundsname):
        sys.exit(2)

    # if not, try to convert to plaintext
    try:
        plaintext, permissiveBounds, strictBounds = processDoc(text)
        dump(plainname, plaintext)
        dump(pBoundsname, permissiveBounds)
        dump(sBoundsname, strictBounds)
    except RuntimeError, e:
        sys.stderr.write(str.format("Runtime exception on {0}\n", doc))
        sys.stderr.write(str.format(">>>{0}\n", e.message))
        sys.exit(1)

    # signal success
    sys.exit(0)
