help:
	@echo 'bnc    run Splitta on BNC corpus and extract sentence boundaries'
	@echo 'i2b2   run Splitta on i2b2 corpus and extract sentence boundaries'
	@echo 'genia  run Splitta on GENIA corpus and extract sentence boundaries'
	@echo 'swb    run Splitta on Switchboard corpus and extract sentence boundaries'

bnc:
	@echo 'RUNNING WITH SVM MODEL'
	@bash splittabnc.sh -m svm
	@echo
	@echo 'RUNNING WITH NAIVE BAYES MODEL'
	@bash splittabnc.sh -m nb
i2b2:
	@echo 'RUNNING WITH SVM MODEL'
	@bash splittai2b2.sh -m svm
	@echo
	@echo 'RUNNING WITH NAIVE BAYES MODEL'
	@bash splittai2b2.sh -m nb
genia:
	@echo 'RUNNING WITH SVM MODEL'
	@bash splittagenia.sh -m svm
	@echo
	@echo 'RUNNING WITH NAIVE BAYES MODEL'
	@bash splittagenia.sh -m nb
swb:
	@echo 'RUNNING WITH SVM MODEL'
	@bash splittaswb.sh -m svm
	@echo
	@echo 'RUNNING WITH NAIVE BAYES MODEL'
	@bash splittaswb.sh -m nb
