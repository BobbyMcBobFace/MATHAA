# Introduction

A dumpster for my math aa :0

Dont expect any good repo practises this is literally a dumping ground

## Files

[LaTeXTOASCII.py](/LaTeXTOASCII/LaTeXTOASCII.py) -- Takes in _expressions.txt_ with LaTeX equations as input and outputs ASCII equations. -- useful for converting LaTeX eqn's from desmos into plaintext

Requirements:

- expressions.txt containing LaTeX equations see [expressions.txt.sample](/LaTeXTOASCII/expressions.txt.sample)
- pylatexenc `pip install pylatexenc`

[CONVERTERv0.py](/CONVERTER/CONVERTERv0.py) -- takes in _input.txt_ with ASCII equations and filters out implicit equations into _badeqn.txt_ and the rest into _goodeqn.txt_

[CONVERTERv1.py](/CONVERTER/CONVERTERv1.py) -- takes in _input.txt_ with ASCII equations and converts explicit equations into a list of TI-BASIC [piecewise(](http://tibasicdev.wikidot.com/piecewise) --- right now a manual transfer to the graphing calculator

[CONVERTERv2.py](/CONVERTER/CONVERTERv2.py) -- takes in _input.txt_ with ASCII equations and converts explicit equations into a collection of TI-BASIC .txt files. It can be run through a TI-BASIC Compiler.

## Roadmap

- [x]  Add conversion support to ti-basic piecewise( and etc for non-implicit graphs in [CONVERTERv0.py](/CONVERTER/CONVERTERv0.py)
- [x]  Add support to fully produce a complete .8xp file that can be uploaded to the calculator to run
- [ ] Add support for the rest of the graphs.

For now check out <https://tiny.cc/mathprojconverter/> by my senior although it is not as robust

## Failures

Failed stuff can be found [here](/failed%20stuff/) (warning messy)

_Licensed under the MIT License_
<sub><sup>might switch to the wtfpl soon</sup></sub>
