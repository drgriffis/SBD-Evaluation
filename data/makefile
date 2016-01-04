DATA=$(shell pwd)
PREPROCESSING=${DATA}/../code/preprocessing
I2B2=${DATA}/i2b2
GENIA=${DATA}/genia

.PHONY: help i2b2 genia clean

help:
	@echo "i2b2    load i2b2 data into correct location"
	@echo "genia   load GENIA data into correct location and extract plaintext"
	@echo "clean   remove all data"

clean:
	@echo "Removing i2b2 data..."
	@rm -rf ${I2B2}/tmp
	@rm -f ${I2B2}/plaintext/*
	@echo "Removing GENIA data..."
	@rm -rf ${GENIA}/GENIA_treebank_v1
	@rm -f ${GENIA}/plaintext/*
	@rm -f ${GENIA}/bounds/*

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
		echo "i2b2 data unpacked to ${I2B2}/plaintext"; \
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
