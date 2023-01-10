# Collatz-Cruncher
A program to test billions of numbers in an effort to find a number that disproves the Collatz Conjecture.

## Installing
Make sure you have [Python 3](https://python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed.\
Pip should automatically be installed alongside Python, but if you run the `CollatzCruncher.py` program and there are errors,\
try installing pip using the link above.\
The installer script (`install.py`) will automatically install dependencies `tqdm` and `colorama`.\
`git clone https://github.com/perspector/Collatz-Cruncher.git`
`python3 install.py`

## Running
`python3 CollatzCruncher.py`


## NOTE: Performance Fix
If your computer crashes, the program is killed, or becomes unresponsive, or you run out of RAM:
-  Change `power` variable in CollatzCruncher.py to something smaller (determines the amount of numbers that will be calculated at once)
-  Change `cooldown` variable in CollatzCruncher.py to something larger (determines the amount of time between calculating sets of numbers)


## Credits
Inspiration from [Veritasium: The Simplest Math Problem No One Can Solve - Collatz](https://www.youtube.com/watch?v=094y1Z2wpJg)
