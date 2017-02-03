# Automatic Edit Extraction

This directory contains the minimal amount of code needed to use the automatic edit extraction algorithm described in:

> Mariano Felice, Christopher Bryant, and Ted Briscoe. 2016. [**Automatic extraction of learner errors in esl sentences using linguistically enhanced alignments**](http://aclweb.org/anthology/C/C16/C16-1079.pdf). In Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics: Technical Papers. Osaka, Japan.

If you make use of this code, please cite the above paper.

# Overview

The main aim of this code is to take a parallel original and corrected text file (1 sentence per line) and convert it into M2 format, where the edits that transform the former into the latter have been made explicit.

## Example:  
Original: &emsp;&emsp;&emsp; This are gramamtical sentence .  
Corrected: &emsp;&emsp; This is a grammatical sentence .  
Output M2: &emsp;&nbsp;&nbsp; S This are gramamtical sentence .  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; A 1 2|||NA|||is|||REQUIRED|||-NONE-|||0  
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; A 2 2|||NA|||a|||REQUIRED|||-NONE-|||0  	
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; A 2 3|||NA|||grammatical|||REQUIRED|||-NONE-|||0  

In M2 format, the first line preceded by S contains the original tokenized source sentence.  
All subsequent lines preceded by A indicate an edit Annotation made to that source sentence.  
The first field denotes the start and end token offsets of the edit in the source sentence, the second field denotes the error type for the edit (not available in automatic alignment) and the third field contains the tokenized correction string. The next two fields are included for historical reasons, while the last field indicates the id of the annotator.

# Pre-requisites

Although the code was written for Python 3.4, we have also tested it in Python 2.7. It may work in other versions too.

Regardless of which version of Python you use, you will also need to download spaCy: [https://spacy.io/](https://spacy.io/)  
Instructions on how to install it are here: [https://spacy.io/docs/usage/](https://spacy.io/docs/usage/)

The following will install spaCy for Python3:  
`pip3 install -U spacy`  
`python3 -m spacy.en.download all --force`  

# Usage

`parallel_to_m2.py` is the main script. Running `python3 parallel_to_m2.py -h` displays the following help message:

```
usage: parallel_to_m2.py [-h] [options] -orig ORIG -cor COR -out OUT

Convert parallel original and corrected text files (1 sentence per line) into M2 format.
The default uses Damerau-Levenshtein and merging rules and assumes tokenized text.

optional arguments:
  -h, --help    show this help message and exit
  -orig ORIG    The path to the original text file.
  -cor COR      The path to the corrected text file.
  -out OUT      The full filename of where you want the output m2 file saved.
  -tok          Use this flag if the parallel sentences are untokenized.
  -lev          Align texts using standard Levenshtein rather than our linguistically 
                enhanced Damerau-Levenshtein distance.
  -merge MERGE  Choose a merging strategy for an automatic alignment.
                all-split: Merge nothing; e.g. MSSDI -> M, S, S, D, I
                all-merge: Merge adjacent non-matches; e.g. MSSDI -> M, SSDI
                all-equal: Merge adjacent same-type non-matches; e.g. MSSDI -> M, SS, D, I
                rules: Use our own rule-based merging strategy (default)
```

Included in this distribution is an example original and corrected text file and expected m2 output file.  
These shall be used to demonstrate sample usage below.

By default, the script uses the best Damerau-Levenshtein + rules strategy described in the COLING paper. As such, the following command should produce a file called `out_test.m2` in the test directory, which should be identical to `expected_test.m2`.

`python3 parallel_to_m2.py -orig test/orig_test -cor -test/cor_test -out test/out_test.m2`

If you want to do the alignment using other options, you can use the `-lev` flag to perform a standard Levenshtein and/or the `-merge MERGE` flag to choose a different merging strategy. For example, the following command will align the input files using levenshtein without merging anything.

`python3 parallel_to_m2.py -orig test/orig_test -cor -test/cor_test -out test/lev_all-split.m2 -lev -merge all-split`

## Note
The speed of the alignment depends on the options and size of the input parallel files. Additionally, attempting to align sentences that are very different takes longer. In the default setting, the program processes roughly 1000 sentence per minute. 

# MIT License

Copyright (c) 2017 chrisjbryant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Contact

If you have any questions, suggestions or bug reports, you can contact the authors at:  
mariano dot felice at cl.cam.ac.uk  
christopher dot bryant at cl.cam.ac.uk  


