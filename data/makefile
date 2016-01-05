DATA=$(shell pwd)
CODE=${DATA}/../code
PREPROCESSING=${CODE}/preprocessing
I2B2=${DATA}/i2b2
GENIA=${DATA}/genia
BNC=${DATA}/bnc

.PHONY: help i2b2 genia bnc clean

help:
	@echo "i2b2    load i2b2 data into correct location"
	@echo "genia   load GENIA data into correct location and extract plaintext"
	@echo "bnc     load BNC data into correct location and extract plaintext"
	@echo "clean   remove all data"

clean:
	@echo "Removing i2b2 data..."
	@rm -rf ${I2B2}/tmp
	@rm -f ${I2B2}/plaintext/*
	@rm -f ${I2B2}/bounds/*
	@echo "Removing GENIA data..."
	@rm -rf ${GENIA}/GENIA_treebank_v1
	@rm -f ${GENIA}/plaintext/*
	@rm -f ${GENIA}/bounds/*
	@echo "Removing BNC data..."
	@rm -rf ${BNC}/2554
	@rm -f ${BNC}/plaintext/*
	@rm -f ${BNC}/bounds/*

i2b2:
	@cd ${I2B2} && \
	TRAINING=concept_assertion_relation_training_data && \
	TEST=test_data && \
	if [ -e $${TRAINING}.tar.gz ] && [ -e $${TEST}.tar.gz ]; then \
		echo "Unpacking i2b2 data..." && \
		mkdir tmp && \
		cp $${TRAINING}.tar.gz tmp/ && \
		cp $${TEST}.tar.gz tmp/ && \
		cd tmp && \
		tar -xzf $${TRAINING}.tar.gz && \
		tar -xzf $${TEST}.tar.gz && \
		cp $${TRAINING}/beth/txt/* ../plaintext/ && \
		cp $${TRAINING}/partners/txt/* ../plaintext/ && \
		cp $${TEST}/* ../plaintext/ && \
		cd ../ && \
		rm -rf tmp && \
		echo "Calculating i2b2 sentence bounds..." && \
		javac -d ${PREPROCESSING}/i2b2/bin -cp "${CODE}/jars/commons-io-2.4.jar:${CODE}/jars/opencsv-2.3.jar" ${PREPROCESSING}/i2b2/*.java && \
		java -cp "${PREPROCESSING}/i2b2/bin:${CODE}/jars/commons-io-2.4.jar:${CODE}/jars/opencsv-2.3.jar" i2b2.ReferenceGenerator ${I2B2}/plaintext/ ${I2B2}/bounds/ && \
		echo "i2b2 data unpacked to:" && \
		echo "\tPlaintext files: ${I2B2}/plaintext" && \
		echo "\tSentence boundaries: ${I2B2}/bounds"; \
	else \
		echo "Missing required files:" && \
		if [ ! -e $${TRAINING}.tar.gz ]; then echo "\t${I2B2}/$${TRAINING}.tar.gz"; fi && \
		if [ ! -e $${TEST}.tar.gz ]; then echo "\t${I2B2}/$${TEST}.tar.gz"; fi \
	fi

genia:
	@cd ${GENIA} && \
	TREEBANK=GENIA_treebank_v1 && \
	if [ -e $${TREEBANK}.tar.gz ]; then \
		echo "Unpacking GENIA data...\n" && \
		if [ ! -d $${TREEBANK} ]; then \
			tar -xzf $${TREEBANK}.tar.gz; \
		fi && \
		cd ${PREPROCESSING}/genia && \
		bash extractplaintext.sh ${GENIA}/$${TREEBANK} ${GENIA}/plaintext ${GENIA}/bounds && \
		echo "\nGENIA data unpacked to:" && \
		echo "\tXML files: ${GENIA}/$${TREEBANK}" && \
		echo "\tPlaintext files: ${GENIA}/plaintext" && \
		echo "\tSentence boundaries: ${GENIA}/bounds"; \
	else \
		echo "Missing required file:" && \
		echo "\t${GENIA}/$${TREEBANK}.tar.gz"; \
	fi

bnc:
	@cd ${BNC} && \
	XML=2554 && \
	XMLPATH=$${XML}/download/Texts && \
	if [ -e $${XML}.zip ]; then \
		echo "Unpacking BNC data..." && \
		if [ ! -d $${XML} ]; then \
			unzip -q $${XML}.zip; \
		fi && \
		cd ${PREPROCESSING}/bnc && \
		bash getfilelist.sh ${BNC}/$${XMLPATH} filelist2.txt && \
		bash bncplaintext.sh ${BNC}/$${XMLPATH} filelist.txt ${BNC}/plaintext ${BNC}/bounds; \
	else \
		echo "Missing required files:" && \
		echo "\t${BNC}/$${XML}.zip"; \
	fi
