# Clinical-SBD
Virtual environment for replicating experiments from Griffis et al., "A Quantitative and Qualitative Evaluation of Sentence Boundary Detection for the Clinical Domain" (2016)

## Data

### i2b2

1. Sign up for i2b2 data access [here](https://www.i2b2.org/NLP/DataSets/Register.php) (requires submitting a signed Data Use Agreement)
2. After your data access is approved and you have a working login, go to [the download page](https://www.i2b2.org/NLP/DataSets/Download.php) and download the files labeled "Concept assertion relation training data" and "Test data" from the 2010 Relations Challenge
3. Place the two downloaded .tar.gz files in the `data/i2b2` directory
4. Execute the following commands to unpack the data:

        cd data/
        make i2b2

### GENIA

1. The GENIA data files are automatically sourced, in XML format, from [the Treebank portion of the GENIA project](http://www.geniaproject.org/genia-corpus/treebank).
2. Execute the following commands to unpack the data:

        cd data/
        make genia
