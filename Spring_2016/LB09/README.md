**Speaker**: Leo Siqueira (RSMAS)

**Title**: Save time and $make reproducible research with GNU Make

**Where and when**: MSC 329, 12-1pm,  Wednesday, March 2, 2016

**Summary**:

A lot of the research described in recent papers is not actually reproducible. Why is it so hard for people who are (and will be) the leaders in the field to publish code that can be easily compiled and reproduced? Using Make doesn’t fundamentally change how you do something, but it encourages to you record each step in the process, enabling you (and your coworkers or reviewers) to reproduce the entire process later. Make is not merely a tool for building large binaries or libraries but is a machine-readable documentation that can save you time and make your workflow reproducible. Do your future self and coworkers a favor, and start using Make. Let the computer work for you!

**Technical Note**:
The makefile_basic folder already contains three figures, the data used to produce a paper as well as a text file and its bibliography. Please set the name of your latex compiler (pdflatex) inside the Makefile. For basic functionality type

make clean <br />
make paper <br />
make view <br />

For a full working version of this material, please make sure you have a latex compiler of your choice installed as well as the following python packages: numpy, matplotlib, pandas, and seaborn.