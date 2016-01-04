I2B2=i2b2

.PHONY: help i2b2

help:
	@echo "i2b2    load i2b2 data into correct location"
	@echo "clean   remove all data"

clean:
	@echo "Removing i2b2 data..."
	@rm -rf i2b2/tmp
	@rm -f i2b2/plaintext/*

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
