Change log
==========


v1.0 *[2010-07-31]*
----

  * Justified columns.
    _(Contributed by Steve Losh.)_

  * Output is indented to line up with the prompt. For example, if the prompt
    string is "<code>&gt;&nbsp;</code>", the output will be indented by two
    spaces. _(Contributed by Liam Cooke with a bug fix from Adam Lloyd.)_

  * Bug fixed: exception raised when `see()` has nothing to display.


v0.5.4 *[2009-07-23]*
----

  * Bug fixed: Calling `see()` first with no arguments would return nothing.


v0.5.3 *[2009-04-12]*
----

  * New project homepage: http://inky.github.com/see/

  * Results are spaced out more, and line up with the default interpreter prompt.
    For example:

        >>> see(int, pattern='h*')
            hash()    help()    hex()

  * Unary operator symbols changed from `+@` and `-@` to `+obj` and `-obj`
    respectively.

  * Running `see.py` as a script will show documentation, equivalent
    to `help(see)`.

  * If you want to be lazy, you can '`from see import *`', and only `see()`
    will be imported.

  * Bug fixed: `see()` output could be modified, but would still print
    the original results. The output list now acts like a tuple.

  * Revised code documentation and examples.


v0.5.2 *[2009-03-16]*
------

  * Calling `see()` without arguments shows local variables.
    _(Contributed by Charlie Nolan.)_


v0.5.1 *[2009-03-13]*
------

  * Filename pattern matching is now the default. For example:

        > see('', '.is*')
          .isalnum()   .isalpha()   .isdigit()   .islower()   .isspace()
          .istitle()   .isupper()

    Regular expression matching can still be done, using the `r` argument.

  * Two bugs fixed for Python 3.0:

      * After the first `see()` call, subsequent calls would give no
        output for some objects.

      * Regular expression and filename pattern matching would also result
        in nothing being output.


v0.5 *[2009-03-07]*
----

  * Now returns a list-like object, for iterating through the results, while
    still showing the human-readable output when run interactively.
    _(Contributed by [Bob Farrell][bobf].)_


  * Optional `regex` and `fn` arguments, for regular expression and filename
    pattern matching, respectively.
    _(Contributed by [Ed Page][epage].)_


v0.4.1 *[2009-02-23]*
------

  * New attributes: `str()` and `repr()`.
    _(`str()` contributed by [Guff][guff].)_


v0.4 *[2009-02-19]*
----

  * For Python 3.0, new attributes are included, and deprecated attributes
    are no longer shown.
    _(Contributed by Gabriel Genellina.)_

  * AttributeError with Django class attributes fixed.
    _(Contributed by [jdunck][jdunck].)_

  * The correct symbols are now shown for objects implementing
    `__divmod__`, `__floordiv__` and `__cmp__`.
    _(Contributed by Gabriel Genellina.)_

  * (Pseudo-)static variables moved outside the `see()` function.
    This may or may not be more efficient.

  * If the object has a docstring set, 'help()' is shown in the list
    instead of '?'.
    _(Suggested by [edcrypt][edcrypt].)_

  * Instructions added for using this with iPython.
    _(Contributed by [Baishampayan Ghose][ghoseb].)_


v0.3.1 *[2009-02-18]*
------

  * Added symbols for binary arithmetic operations using reflected
    (swapped) operands.

  * 'with' and 'reversed()' symbols added.


v0.3 *[2009-02-18]*
----

  * Rudimentary Python 3.0 support, using suggestions from
    [CommodoreGuff][CommodoreGuff].

  * Created a _setup.py_ installation script.

  * Change an outdated documentation link in the _README_ file.
    _(Suggested by [Ian Gowen][igowen].)_


v0.2 *[2009-02-17]*
----

  * Special attribute symbols reordered.

  * Unary addition and subtraction changed to `+@` and `-@` respectively.

  * Added '.*' symbol for the `__getattr__` attribute.

  * `help()` documentation added.


v0.1 *[2009-02-16]*
----

  * Original.


[bobf]: http://github.com/bobf
[CommodoreGuff]: http://www.reddit.com/user/CommodoreGuff/
[edcrypt]: http://github.com/edcrypt
[epage]: http://github.com/epage
[ghoseb]: http://github.com/ghoseb
[guff]: http://github.com/Guff
[igowen]: http://ian.gowen.cc/
[jdunck]: http://github.com/jdunck
