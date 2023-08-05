Worm
~~~~

What came first, the worm or the fish__?

.. __: http://pypi.python.org/pypi/fish

Ever wanted to have animating worms for progress bars in your command-line
script?

Inspired by Ludvig Ericson, author of ``fish``, I present ``worm``. Thus
proving that I don't have better things to do with my time than to write
meaningless ASCII animation programs.

``worm``, the module that makes any program represent its
sluggishness to the console while churning away on some good 'ole data.

Usage? Simple enough:

>>> import worm
>>> while churning:
...     churn_churn()
...     worm.animate()

There is nothing more to say except:

    Possibilities are endless here, gentlemen:

        The only limit is yourself.

        http://zombo.com/

Note: unlike ``fish`` this progress bar is *awesome* and requires a UTF-8
terminal to work its *awesomeness* in.


History
~~~~~~~

0.3 - fix wrapping; make install work
0.2 - remove UTF8 usage 
0.1 - first release
