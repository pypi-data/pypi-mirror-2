Python wrapper for the Poker Sleuth Scriptable Equity Calculator
================================================================

This module provides a Python interface to the `Poker Sleuth`__
`scriptable Texas Hold'em Equity Calculator`__.  Tell it what hands
your opponents may have, and it calculates your odds of winning at the
showdown if no one folds.

For example, to compute the odds of winning when you have a pair of
Jacks, your opponent has the Ace and 5 of diamonds, and the board
cards are the 3 of diamonds, 5 of clubs, and 9 of diamonds:

::

    >>> import pokersleuth
    >>> pokersleuth.calculate_equity('3d5c9d', ('JJ', 'Ad5d')
    [0.48225, 0.51775]

The module can also be used directly from the command line:

::

    python -m pokersleuth 3d5c9d JJ Ad5d

__ http://pokersleuth.com/
__ http://pokersleuth.com/poker-equity-calculator.shtml
