SHELL=bash
JAVAC_CP="../jars/commons-io-2.4.jar:../jars/commons-lang3-3.4.jar:../jars/opencsv-2.3.jar:../../install/stanford-corenlp/stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2.jar:../../install/stanford-corenlp/stanford-corenlp-full-2015-04-20/stanford-corenlp-3.5.2-models.jar:../../install/stanford-corenlp/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar:../../install/stanford-corenlp/stanford-parser-full-2015-04-20/stanford-parser.jar"
JAVA_CP="bin:${JAVAC_CP}"
EXEC=export JAVA_HOME=$${JAVA8_HOME}; $${JAVA_HOME}/bin/java -cp ${JAVA_CP} -Xmx4g
DATAROOT=../../data
CLNQTS=../postprocessing/cleanquotes.sh
CLNSTFRD=../postprocessing/stanford-corenlp/correctbounds

help:
	@echo 'bnc    run Stanford CoreNLP on BNC corpus and extract sentence boundaries'
	@echo 'i2b2   run Stanford CoreNLP on i2b2 corpus and extract sentence boundaries'
	@echo 'genia  run Stanford CoreNLP on GENIA corpus and extract sentence boundaries'
	@echo 'swb    run Stanford CoreNLP on Switchboard corpus and extract sentence boundaries'

### Compile target #############

tkcompile:
	@if [ ! -d bin ]; then \
		mkdir bin; \
	fi; \
	export JAVA_HOME=$${JAVA8_HOME}; \
	$${JAVA_HOME}/bin/javac -d bin -cp ${JAVAC_CP} src/StanfordSegmenter.java


### Main targets ###############

i2b2: tkcompile
	@set -e; \
	if [ ! -d ${DATAROOT}/i2b2/stanford-output/bounds/clean/fixed ]; then \
		mkdir -p ${DATAROOT}/i2b2/stanford-output/bounds/clean/fixed; \
	fi; \
	${EXEC} StanfordSegmenter \
		${DATAROOT}/i2b2/plaintext/ \
		${DATAROOT}/i2b2/stanford-output/bounds/; \
	export PYTHONPATH=/vagrant/code:$${PYTHONPATH}; \
	bash ${CLNQTS} ${DATAROOT}/i2b2/stanford-output/bounds csv ${DATAROOT}/i2b2/stanford-output/bounds/clean; \
	../postprocessing/i2b2/correctbounds -s ${DATAROOT}/i2b2/stanford-output/bounds/clean -d ${DATAROOT}/i2b2/stanford-output/bounds/clean/fixed -t stanford

genia: tkcompile
	@set -e; \
	if [ ! -d ${DATAROOT}/genia/stanford-output/bounds/clean/fixed ]; then \
		mkdir -p ${DATAROOT}/genia/stanford-output/bounds/clean/fixed; \
	fi; \
	${EXEC} StanfordSegmenter \
		${DATAROOT}/genia/plaintext/ \
		${DATAROOT}/genia/stanford-output/bounds/; \
	bash ${CLNQTS} ${DATAROOT}/genia/stanford-output/bounds csv ${DATAROOT}/genia/stanford-output/bounds/clean; \
	${CLNSTFRD} ${DATAROOT}/genia/stanford-output/bounds/clean ${DATAROOT}/genia/stanford-output/bounds/clean/fixed

swb: tkcompile
	@set -e; \
	if [ ! -d ${DATAROOT}/swb/stanford-output/bounds/clean/fixed ]; then \
		mkdir -p ${DATAROOT}/swb/stanford-output/bounds/clean/fixed; \
	fi; \
	${EXEC} StanfordSegmenter \
		${DATAROOT}/swb/plaintext/ \
		${DATAROOT}/swb/stanford-output/bounds/; \
	bash ${CLNQTS} ${DATAROOT}/swb/stanford-output/bounds csv ${DATAROOT}/swb/stanford-output/bounds/clean; \
	${CLNSTFRD} ${DATAROOT}/swb/stanford-output/bounds/clean ${DATAROOT}/swb/stanford-output/bounds/clean/fixed

bnc: tkcompile
	@set -e; \
	if [ ! -d ${DATAROOT}/bnc/stanford-output/bounds/clean/fixed ]; then \
		mkdir -p ${DATAROOT}/bnc/stanford-output/bounds/clean/fixed; \
	fi; \
	${EXEC} StanfordSegmenter \
		${DATAROOT}/bnc/plaintext/ \
		${DATAROOT}/bnc/stanford-output/bounds/; \
	bash ${CLNQTS} ${DATAROOT}/bnc/stanford-output/bounds csv ${DATAROOT}/bnc/stanford-output/bounds/clean; \
	${CLNSTFRD} ${DATAROOT}/bnc/stanford-output/bounds/clean ${DATAROOT}/bnc/stanford-output/bounds/clean/fixed
