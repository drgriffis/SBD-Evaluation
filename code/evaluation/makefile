JAVAC_CP="../jars/commons-io-2.4.jar:../jars/opencsv-2.3.jar"
JAVA_CP="bin:${JAVAC_CP}"
EXEC=java -cp "bin:jars/commons-io-2.4.jar:jars/commons-lang3-3.4.jar:jars/opencsv-2.3.jar:jars/lingpipe-4.1.0.jar:jars/stanford-corenlp-3.5.2-models.jar:jars/stanford-corenlp-3.5.2.jar:jars/stanford-parser-3.5.2-models.jar:jars/stanford-parser.jar"
DATAROOT=../../data
RESROOT=${DATAROOT}/results
RES_HEADERS="Toolkit,Precision,Recall,F-Score"

### Main targets ####################

i2b2: evcompile
	@echo ${RES_HEADERS} > ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=ctakes   TK_SUFFIX=.txt.xml.bounds >> ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=splitta  TK_SUFFIX=.txt.bounds  MODEL=nb/ >> ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=splitta  TK_SUFFIX=.txt.bounds  MODEL=svm/ >> ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=lingpipe TK_SUFFIX=.csv  OPT=clean/fixed/  MODEL=ie/ >> ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=lingpipe TK_SUFFIX=.csv  OPT=clean/fixed/  MODEL=me/ >> ${RESROOT}/i2b2.csv
	@make -s i2b2_tk TK=stanford TK_SUFFIX=.csv  OPT=clean/fixed/ >> ${RESROOT}/i2b2.csv

genia: evcompile
	@echo ${RES_HEADERS} > ${RESROOT}/genia.csv
	@make -s genia_tk TK=ctakes   TK_SUFFIX=.xml.txt.xml.bounds >> ${RESROOT}/genia.csv
	@make -s genia_tk TK=splitta  TK_SUFFIX=.xml.txt.bounds  MODEL=nb/ >> ${RESROOT}/genia.csv
	@make -s genia_tk TK=splitta  TK_SUFFIX=.xml.txt.bounds  MODEL=svm/ >> ${RESROOT}/genia.csv
	@make -s genia_tk TK=lingpipe TK_SUFFIX=.xml.csv  OPT=clean/  MODEL=ie/ >> ${RESROOT}/genia.csv
	@make -s genia_tk TK=lingpipe TK_SUFFIX=.xml.csv  OPT=clean/  MODEL=me/ >> ${RESROOT}/genia.csv
	@make -s genia_tk TK=stanford TK_SUFFIX=.xml.csv  OPT=clean/fixed/ >> ${RESROOT}/genia.csv

bnc: evcompile
	@echo ${RES_HEADERS} > ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=ctakes   TK_SUFFIX=.xml.txt.xml.bounds  LVL=strict >> ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=splitta  TK_SUFFIX=.xml.txt.bounds  MODEL=nb/  OPT=fixed/  LVL=strict >> ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=splitta  TK_SUFFIX=.xml.txt.bounds  MODEL=svm/  LVL=permissive >> ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=lingpipe TK_SUFFIX=.xml.csv  MODEL=ie/  OPT=clean/  LVL=strict >> ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=lingpipe TK_SUFFIX=.xml.csv  MODEL=me/  OPT=clean/  LVL=strict >> ${RESROOT}/bnc.csv
	@make -s bnc_tk TK=stanford TK_SUFFIX=.xml.csv  OPT=clean/fixed/  LVL=permissive >> ${RESROOT}/bnc.csv

swb: evcompile
	@echo ${RES_HEADERS} > ${RESROOT}/swb.csv
	@make -s swb_tk TK=ctakes   TK_SUFFIX=.prd.txt.xml.bounds >> ${RESROOT}/swb.csv
	@make -s swb_tk TK=splitta  TK_SUFFIX=.prd.txt.bounds  MODEL=nb/ >> ${RESROOT}/swb.csv
	@make -s swb_tk TK=splitta  TK_SUFFIX=.prd.txt.bounds  MODEL=svm/ >> ${RESROOT}/swb.csv
	@make -s swb_tk TK=lingpipe TK_SUFFIX=.prd.csv  OPT=clean/  MODEL=ie/ >> ${RESROOT}/swb.csv
	@make -s swb_tk TK=lingpipe TK_SUFFIX=.prd.csv  OPT=clean/  MODEL=me/ >> ${RESROOT}/swb.csv
	@make -s swb_tk TK=stanford TK_SUFFIX=.prd.csv  OPT=clean/fixed/ >> ${RESROOT}/swb.csv


### Compilation target ##############

evcompile:
	@set -e; \
	if [ ! -d bin ]; then \
		mkdir bin; \
	fi; \
	javac -d bin -cp ${JAVAC_CP} src/SegmentationEvaluator.java


### Execution targets ###############

genia_tk:
	@set -e; \
	java -cp ${JAVA_CP} SegmentationEvaluator \
		${DATAROOT}/genia/bounds \
		${DATAROOT}/genia/${TK}-output/${MODEL}bounds/${OPT} \
		.xml.bounds \
		${TK_SUFFIX} \
	| tr '\n' ':' \
	| awk -F ':' '{ print "${TK}${MODEL}," $$2 "," $$4 "," $$6 }';

swb_tk:
	@set -e; \
	java -cp ${JAVA_CP} SegmentationEvaluator \
		${DATAROOT}/swb/bounds \
		${DATAROOT}/swb/${TK}-output/${MODEL}bounds/${OPT} \
		.prd.txt.bounds \
		${TK_SUFFIX} \
	| tr '\n' ':' \
	| awk -F ':' '{ print "${TK}${MODEL}," $$2 "," $$4 "," $$6 }';

bnc_tk:
	@set -e; \
	java -cp ${JAVA_CP} SegmentationEvaluator \
		${DATAROOT}/bnc/bounds \
		${DATAROOT}/bnc/${TK}-output/${MODEL}bounds/${OPT} \
		.xml.txt.bounds.${LVL} \
		${TK_SUFFIX} \
	| tr '\n' ':' \
	| awk -F ':' '{ print "${TK}${MODEL}," $$2 "," $$4 "," $$6 }';

i2b2_tk:
	@set -e; \
	java -cp ${JAVA_CP} SegmentationEvaluator \
		${DATAROOT}/i2b2/bounds/clean \
		${DATAROOT}/i2b2/${TK}-output/${MODEL}bounds/${OPT} \
		.csv \
		${TK_SUFFIX} \
	| tr '\n' ':' \
	| awk -F ':' '{ print "${TK}${MODEL}," $$2 "," $$4 "," $$6 }';

i2b2-specialist:
	make i2b2 TK=specialist SEARCH=.csv REPL=.txt.sentences.bounds
genia-specialist:
	make genia TK=specialist SEARCH=.xml.bounds REPL=.xml.txt.sentences.bounds
bnc-specialist:
	make bnc TK=specialist SEARCH=.xml.txt.bounds.permissive REPL=.xml.txt.bounds.superfixed LVL=permissive OPT=superfixed/
swb-specialist:
	make swb TK=specialist SEARCH=.prd.txt.bounds REPL=.prd.txt.sentences.bounds
