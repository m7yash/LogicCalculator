# Logic Calculator

Program that computes propositions and generates truth tables! Developed by Yash Mishra.

<img width="1324" alt="image" src="https://user-images.githubusercontent.com/61370209/176289701-23bfbd85-d42a-4a80-98b8-d84ea2ddbf19.png">

## How to Use:
- On this repository's main page, click 'Code' and then click 'Download ZIP'
- Use command line to run ```python3 Main.py``` in the downloaded folder
  - Your program result will be printed to the terminal screen and also to ```output.txt```
  - Change the window size of ```output.txt``` if lines are pushed together

## Notes:
- This version is still under testing
  - If you discover a bug, let me know! Email me at m7yash@cs.washington.edu
- If you request a complex computation, the printing in the terminal may be unreliable, so see ```output.txt``` instead (and adjust the window size so that the lines are not pushed together)
- To compute something such as ```(p&q)->r```, you have to first compute ```p&q```. If that is saved in column 4 of the table (the first three columns would be taken by ```p```, ```q```, and ```r``` respectively), then you have to do then ```4->r``` to get ```(p&q)->r``` in column 5 of the table.
  - I coded it this way because it basically forces "showing work" in between steps. It will also be easier to understand how the final result was computed. This tool is likely to be used for learning and/or checking work, and when we do these computations by hand, we generally write out columns for intermediate steps. So, this will make it easier to catch mistakes in hand-written truth tables.
  - In the future, I will add an option to do computations directly.

## Background:
- I originally created this program for fun while taking CSE 311 (Foundations of Computing I) when we learned propositional logic. I found it tiring to draw out long truth tables so I wanted to have my computer do it for me! I shared it with some classmates as well and we were able to use it to get a better understanding of propositional logic.
- The original program was in Java, and it was written poorly from a coding standpoint because I had finished all of it in two days. The code is in ```OldVersion.java``` and is located in the ```old``` folder.
- I am always looking to improve as a programmer, so I decided to completely redo the program at the start of the summer (and switch to Python). I made many new changes:
  - Program-related
    - No limit of 10 computations! User can now compute as many propositions as they would like thanks to improved input handling!
    - More efficient storage of T/F values since the table is made of ```bool```s instead of strings
    - The algorithm to generate all T/F value combinations in a particular pattern is now more understandable and concise
    - Inputting propositions and calculated propositions is significantly easier
    - There is now strict input validation
  - Printing
    - User can decide whether results are printed as 1/0 or T/F
    - Column spacing is now done automatically and is based on the length of the longest computation
    - Terminal text now has many colors to make entering input and reading output easier
    - Output is now also logged to a file
  - Code Style
    - More understandable code
    - Comments to clarify code
    - Fixed typos
    - Better instructions and examples for user
  - Other
    - User can see how long the program takes to do all the computations (in milliseconds)
    - The table now has column numbers above the propositions

## Plans for the future:
- Use Regular Expressions for input validation
- Add an option to allow for direct computations
- Further improve code quality
