# Clinical-SBD
Virtual environment for replicating experiments from Griffis et al., "A Quantitative and Qualitative Evaluation of Sentence Boundary Detection for the Clinical Domain" (2016)

## Data

### [BNC](http://www.natcorp.ox.ac.uk/)

1. Sign up for dataset access via the [Oxford Text Archive](http://ota.ox.ac.uk/scripts/download.php?otaid=2554)
2. You will receive an email with a download link.
3. Click the link to download the `2554.zip` file, and save it to `data/bnc`.
4. Execute the following commands to unpack the data:

        cd data/
        make bnc

   > Note that the plaintext extraction process for BNC takes several hours.

### [Switchboard](https://catalog.ldc.upenn.edu/LDC97S62)

1. Sign up for an account with the Linguistic Data Consortium [here](https://catalog.ldc.upenn.edu/signup)
  > Note that this requires being part an institution with LDC access.
2. ??? **PENDING**
3. Copy the .tar.gz file to the `data/swb` directory
4. Execute the following commands to unpack the data:

        cd data/
        make swb

### [i2b2 2010 Clinical Dataset](https://www.i2b2.org/NLP/Relations/)

1. Sign up for i2b2 data access [here](https://www.i2b2.org/NLP/DataSets/Register.php) (requires submitting a signed Data Use Agreement)
2. After your data access is approved and you have a working login, go to [the download page](https://www.i2b2.org/NLP/DataSets/Download.php) and download the files labeled "Concept assertion relation training data" and "Test data" from the 2010 Relations Challenge
3. Place the two downloaded .tar.gz files in the `data/i2b2` directory
4. Execute the following commands to unpack the data:

        cd data/
        make i2b2

### [GENIA](http://www.geniaproject.org/)

1. The GENIA data files are automatically sourced, in XML format, from [the Treebank portion of the GENIA project](http://www.geniaproject.org/genia-corpus/treebank).
2. Execute the following commands to unpack the data:

        cd data/
        make genia
