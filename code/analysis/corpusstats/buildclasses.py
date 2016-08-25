#encoding: utf-8
import sys,codecs
f=codecs.open(sys.argv[1],'r','utf-8')
lns=f.readlines()[:-2]
f.close()
chunks=[ln.split('\t') for ln in lns]
print "#encoding: utf-8"
print "classes = {"
for chnk in chunks:
    print unicode.format(u"'{0}','o',", chnk[0], encoding='utf-8')
print "}"
