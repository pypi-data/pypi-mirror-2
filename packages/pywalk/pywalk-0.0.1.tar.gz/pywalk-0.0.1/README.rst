\# Pywalk

Pywalk is a python module written for traversing trees built of
dictionaries, lists and tuples in a breadth-first manner.

This module is still under development. If you're used to mature,
polished python libraries you may want to avoid pywalk. Additionally, it
has only been tested against Python 2.7.1+ (what happens to be what's on
my computer) so it may not work as expected in Python 3.x. However, if
you're a more adventurous developer with an urge (or need) for
manipulating nested data structures, this just might be the library for
you!

Pywalk is a spiritual port of
[js-traverse](https://github.com/substack/js-traverse), in that it's
meant to solve similar problems.

\#\# How It Works:

\`walk(tree)\` returns a decorator that applies a callback to each node
in the tree, in a breadth-first manner. For example:

> tree = {'a': 1, 'b': [9, 9, 6, 7, 6]}
>
> print("Tree before: "+repr(tree))
>
> @walk(tree) def that\_aint\_my\_zip\_code(node): if node.value == [9,
> 9, 6, 7, 6] : node.set([9, 9, 7, 7, 5])
>
> print("Tree after: "+repr(tree))

\#\# Installation:

If you download this project, you should be able to install it by
running

> sudo python setup.py install

Or, once it's on pypi:

> sudo pip install pywalk

but that might be a while.

\#\# Methods for \`node\` in the callback:

The object passed to the callback has a bunch of attributes which are
hopefully useful:

-   \`node.value\` is the value of the node itself.
-   \`node.path\` is a list of indices used to get to the given node.
    Ex: The \`node.path\` for the 7 in the previous example is, \`['b',
    3]\`.
-   \`node.key\` is basically \`node.path[-1]\`.
-   \`node.level\` is basically \`len(node.path)\`.
-   \`node.is\_root\` is True if the node is the root node, and
    otherwise False.
-   \`node.is\_leaf\` is True if the node has no children (ie, is not a
    dict, list or tuple), and False otherwise.
-   \`node.set(v)\` changes the value of the current node to value (v).
-   [unimplemented] \`node.del\` should probably delete the node and the
    associated branch from the tree.
-   [unimplemented] \`node.parent\` should return the parent \`node\`
    object.

\#\# Tests:

Not much for tests right now, but if you want to run them (it) anyway,
try:

> nosetests test/\*

The one test right now parallels an example used in js-traverse.

\#\# Developers! Developers! Developers!

If you're a python fan and like what you see (or don't quite like what
you see), I heartily invite you to dig in, fork it up and [git push it
good](https://twitter.com/\#!/maraksquires/status/71911996051824640).

\#\# License:

MIT.
