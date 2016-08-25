SHELL=bash
JAVAC_CP="../jars/commons-io-2.4.jar:../jars/commons-lang3-3.4.jar:../jars/opencsv-2.3.jar:../../install/lingpipe/lingpipe-4.1.0.jar"
JAVA_CP="bin:${JAVAC_CP}"
EXEC=java -cp ${JAVA_CP} -Xmx1g
DATAROOT=../../data
CLNQTS=../postprocessing/cleanquotes.sh

help:
	@echo 'bnc    run LingPipe on BNC corpus and extract sentence boundaries'
	@echo 'i2b2   run LingPipe on i2b2 corpus and extract sentence boundaries'
	@echo 'genia  run LingPipe on GENIA corpus and extract sentence boundaries'
	@echo 'swb    run LingPipe on Switchboard corpus and extract sentence boundaries'

### Main targets ###############

i2b2: tkcompile
	@set -e; \
	make i2b2_mdl MODEL=ie; \
	make i2b2_mdl MODEL=me

genia: tkcompile
	@set -e; \
	make genia_mdl MODEL=ie; \
	make genia_mdl MODEL=me

swb: tkcompile
	@set -e; \
	make swb_mdl MODEL=ie; \
	make swb_mdl MODEL=me

bnc: tkcompile
	@set -e; \
	make bnc_mdl MODEL=ie; \
	make bnc_mdl MODEL=me;


### Compile target #############

tkcompile:
	@if [ ! -d bin ]; then \
		mkdir bin; \
	fi; \
	javac -d bin -cp ${JAVAC_CP} src/LingPipeSegmenter.java


### Execution targets ##########

i2b2_mdl:
	@set -e; \
	if [ ! -d ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/clean/fixed ]; then \
		mkdir -p ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/clean/fixed; \
	fi; \
	${EXEC} LingPipeSegmenter \
		${DATAROOT}/i2b2/plaintext/ \
		${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/ \
		${MODEL}; \
	export PYTHONPATH=/vagrant/code:$${PYTHONPATH}; \
	bash ${CLNQTS} ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds csv ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/clean; \
	../postprocessing/i2b2/correctbounds -s ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/clean -d ${DATAROOT}/i2b2/lingpipe-output/${MODEL}/bounds/clean/fixed -t lingpipe

genia_mdl:
	@set -e; \
	if [ ! -d ${DATAROOT}/genia/lingpipe-output/${MODEL}/bounds/clean ]; then \
		mkdir -p ${DATAROOT}/genia/lingpipe-output/${MODEL}/bounds/clean; \
	fi; \
	${EXEC} LingPipeSegmenter \
		${DATAROOT}/genia/plaintext/ \
		${DATAROOT}/genia/lingpipe-output/${MODEL}/bounds/ \
		${MODEL}; \
	bash ${CLNQTS} ${DATAROOT}/genia/lingpipe-output/${MODEL}/bounds csv ${DATAROOT}/genia/lingpipe-output/${MODEL}/bounds/clean

swb_mdl:
	@set -e; \
	if [ ! -d ${DATAROOT}/swb/lingpipe-output/${MODEL}/bounds/clean ]; then \
		mkdir -p ${DATAROOT}/swb/lingpipe-output/${MODEL}/bounds/clean; \
	fi; \
	${EXEC} LingPipeSegmenter \
		${DATAROOT}/swb/plaintext/ \
		${DATAROOT}/swb/lingpipe-output/${MODEL}/bounds/ \
		${MODEL}; \
	bash ${CLNQTS} ${DATAROOT}/swb/lingpipe-output/${MODEL}/bounds csv ${DATAROOT}/swb/lingpipe-output/${MODEL}/bounds/clean

bnc_mdl:
	@set -e; \
	if [ ! -d ${DATAROOT}/bnc/lingpipe-output/${MODEL}/bounds/clean ]; then \
		mkdir -p ${DATAROOT}/bnc/lingpipe-output/${MODEL}/bounds/clean; \
	fi; \
	${EXEC} LingPipeSegmenter \
		${DATAROOT}/bnc/plaintext/ \
		${DATAROOT}/bnc/lingpipe-output/${MODEL}/bounds/ \
		${MODEL}; \
	bash ${CLNQTS} ${DATAROOT}/bnc/lingpipe-output/${MODEL}/bounds csv ${DATAROOT}/bnc/lingpipe-output/${MODEL}/bounds/clean
