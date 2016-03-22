# SBD-Evaluation
Virtual environment for replicating experiments from the paper "[A Quantitative and Qualitative Evaluation of Sentence Boundary Detection for the Clinical Domain](http://web.cse.ohio-state.edu/~griffisd/papers/2016-AMIA-CRI.pdf)," appearing at AMIA CRI 2016.  [[Conference Slides](http://web.cse.ohio-state.edu/~griffisd/presentations/2016-AMIA-CRI.pdf)]

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

## Toolkits

### [cTAKES](http://ctakes.apache.org/)

Version 3.2.2 of Apache cTAKES automatically installs in `install/ctakes`.  The sentence chunking experiments use three components:

1. `FilesInDirectoryCollectionReader` - Handles iterating over files in a directory.
2. `ChunkerAggregate` - Part of the core pipeline; handles chunking text (sentence segmentation, phrase segmentation, POS tagging, etc.)
3. `FileWriterCasConsumer` - Handles writing CAS results to XML files

Configuration files for using cTAKES on each corpus are located in `code/ctakes`.  To process each corpus, execute the following commands:

        cd code/ctakes
        make [i2b2|ctakes|genia|swb]

This will run cTAKES and extract detected sentence boundaries from the output: bounds are written to `data/[CORPUS]/ctakes/bounds`.
