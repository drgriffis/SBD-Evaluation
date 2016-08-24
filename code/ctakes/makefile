DATA=../../data
BNC=${DATA}/bnc
I2B2=${DATA}/i2b2
GENIA=${DATA}/genia
SWB=${DATA}/swb
CTAKES=java  \
		-cp $$CTAKES_HOME/resources:$$CTAKES_HOME/lib/* \
		-Dlog4j.configuration=file:$$CTAKES_HOME/config/log4j.xml \
		-Xms512M \
		-Xmx3g \
		org.apache.ctakes.core.cpe.CmdLineCpeRunner

help:
	@echo 'bnc    run cTAKES on BNC corpus and extract sentence boundaries'
	@echo 'i2b2   run cTAKES on i2b2 corpus and extract sentence boundaries'
	@echo 'genia  run cTAKES on GENIA corpus and extract sentence boundaries'
	@echo 'swb    run cTAKES on Switchboard corpus and extract sentence boundaries'

bnc:
	@${CTAKES} config-bnc.xml
	@bash extractbounds.sh ${BNC}/ctakes/output ${BNC}/ctakes/bounds

i2b2:
	@${CTAKES} config-i2b2.xml
	@bash extractbounds.sh ${I2B2}/ctakes/output ${I2B2}/ctakes/bounds

genia:
	@${CTAKES} config-genia.xml
	@bash extractbounds.sh ${GENIA}/ctakes/output ${GENIA}/ctakes/bounds

swb:
	@${CTAKES} config-swb.xml
	@bash extractbounds.sh ${SWB}/ctakes/output ${SWB}/ctakes/bounds
