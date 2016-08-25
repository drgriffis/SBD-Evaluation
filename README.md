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

### [Switchboard (PTB 3 release)](https://catalog.ldc.upenn.edu/LDC99T42)

1. Sign up for an account with the Linguistic Data Consortium [here](https://catalog.ldc.upenn.edu/signup)
  > Note that this requires being part an institution with LDC access.
2. If necessary, request access to [Treebank 3](https://catalog.ldc.upenn.edu/LDC99T42), then download it.
3. Copy the `LDC99T42.tgz` file to the `data/swb` directory
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
        make [i2b2|bnc|genia|swb]

This will run cTAKES and extract detected sentence boundaries from the output: bounds are written to `data/[CORPUS]/ctakes-output/bounds`.

### [Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP)

Version 3.5.2 of the Stanford CoreNLP suite and version 3.5.2 of the Stanford Parser automatically install in `install/stanford-corenlp`.

Code for executing Stanford CoreNLP on each corpus is located in `code/stanford-corenlp`.  To process each corpus, execute the following commands:
  
        cd code/stanford-corenlp
        make [i2b2|bnc|genia|swb]

This will run Stanford CoreNLP and extract detected sentence boundaries from the output, with some cleaning.  Bounds are written to `data/[CORPUS]/stanford-output/bounds/clean/fixed`.

### [Splitta](https://code.google.com/archive/p/splitta/)

Version 1.03 of the Splitta sentence segmenter automatically installs in `install/splitta`.

Scripts for executing Splitta on each corpus are located in `code/splitta`.  To process each corpus, execute the following commands:
  
        cd code/splitta
        make [i2b2|bnc|genia|swb]

This will run Splitta and extract detected sentence boundaries from the output.  Bounds are written to `data/[CORPUS]/splitta-output/[nb|svm]/bounds`.
(BNC bounds require further adjustment and are placed in `bounds/fixed`.)

### [LingPipe](http://alias-i.com/lingpipe)

Version 4.1.0 of the LingPipe Core software is present in `install/lingpipe` by default.

If the `.jar` file is missing, please go to [alias-i.com](http://alias-i.com/lingpipe/web/download.html) to download it (the AGPL version).

Code for executing LingPipe on each corpus is located in `code/lingpipe`.  To process each corpus, execute the following commands:
  
        cd code/lingpipe
        make [i2b2|bnc|genia|swb]

This will run LingPipe and extract detected sentence boundaries from the output, with some cleaning.  Bounds are written to `data/[CORPUS]/lingpipe-output/[ie|me]/bounds/clean`. (i2b2 bounds require further adjustment and are placed in `bounds/clean/fixed`.)
