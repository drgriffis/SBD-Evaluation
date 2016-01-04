'''
Script to convert a GENIA Treebank XML file to plaintext and extract its sentence boundaries.

Usage: plaintext.py XMLFILE OUTFILE BOUNDSFILE
'''
import sys
import xml.dom.minidom as dom

def getAbstract(trgd):
    """Traverse the document tree to get to the abstract
    """
    doctype = trgd.firstChild
    stylesheet = doctype.nextSibling
    annotation = stylesheet.nextSibling
    pubmedArticleSet = annotation.firstChild
    pubmedArticle = pubmedArticleSet.firstChild
    medlineCitation = pubmedArticle.firstChild
    PMID = medlineCitation.firstChild
    article = PMID.nextSibling
    articleTitle = article.firstChild
    abstract = articleTitle.nextSibling
    return abstract

def abstractToSentences(abstract):
    """Convert an abstract DOM object to plaintext; returns plaintext and list of sentence bounds
    """
    sentences = handleSentence(abstract.firstChild.firstChild, [])
    bounds = calculateBounds(sentences)
    return ' '.join(sentences), bounds

def calculateBounds(sentences):
    """Given a list of sentence strings, calculate their bounds as character offsets from 0
    """
    curbound, bounds = 0, []
    for s in sentences:
        bounds.append((curbound, curbound + len(s)))
        curbound += len(s) + 1
    commabounds = [','.join((str(b) for b in bnds)) for bnds in bounds]
    strbounds = '\n'.join(commabounds)
    return strbounds

def handleSentence(sentence, sentenceList):
    """Recursively walk through DOM sibling elements to extract sentences
    """
    if sentence == None:
        return sentenceList
    else:
        sentenceList.append(''.join(handleSentenceChild(sentence.firstChild, [])))
        return handleSentence(sentence.nextSibling, sentenceList)

def handleSentenceChild(child, tokenList):
    """Recursively walk the given DOM object to extract all tokens in it
    """
    if child == None:
        return tokenList
    elif child.localName == u'cons':
        tokenList = handleSentenceChild(child.firstChild, tokenList)
        return handleSentenceChild(child.nextSibling, tokenList)
    elif child.localName == u'tok':
        tokenList.append(child.firstChild.nodeValue)
        return handleSentenceChild(child.nextSibling, tokenList)
    elif child.nodeValue == u' ':
        tokenList.append(' ')
        return handleSentenceChild(child.nextSibling, tokenList)
    else:
        raise Exception("Unknown element:" + child.localName)

def dump(fname, contents):
    """Write ASCII-formatted data to file
    """
    f = open(fname, 'w')
    f.write(contents)
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: plaintext.py XMLFILE OUTFILE BOUNDSFILE")
        exit(1)

    trg=sys.argv[1]
    out=sys.argv[2]
    bnds=sys.argv[3]

    trgd = dom.parse(trg)
    abstract = getAbstract(trgd)

    plaintext, bounds = abstractToSentences(abstract)
    dump(out, plaintext)
    dump(bnds, bounds)
