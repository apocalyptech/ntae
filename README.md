Nine Inch Nails "Not The Actual Events" Variations Generator
============================================================

ABOUT
-----

The band Nine Inch Nails released an EP entitled "Not The Actual Events"
in late 2016, which included an optional "Physical Component" to be delivered
in 2017.  These started arriving in the mail on the week of Februrary 27, 2017.
It quickly became apparent that there were multiple variants of
many of the sheets contained inside, so this page is an attempt to lay
them all out in a big ol' index.

The script which generates this HTML is `generate.py`.  There's a bit of
information inside that script itself about what directories to process,
and some human-readable labels to use for everyting, but the utility mostly
just loops through the specified directories and discovers the image files
and source information itself, and generates thumbnails for use on the main
index page.  It then outputs an index.html with all the collated images,
inlining the thumbnails and linking to the full-size images.  The script
doesn't take any arguments - it's all just hardcoded.

If you want to contribute to this archive, it'd probably be easiest for you
to just contribute to the "Physical Component Variations" thread at ETS
over here: http://www.echoingthesound.org/community/threads/4430-Not-The-Actual-Events-Physical-Edition-variations/
I'll be watching that thread for updates at least for the next few weeks.
You're welcome to send me a pull request as well, of course, though I
suspect nobody would bother.  :)  See below for the general format the
data should take, though a brief glance inside the directories yourself
should make it pretty clear.

The index itself can been seen here: https://apocalyptech.com/ntae/

REQUIREMENTS
------------

`generate.py` is written in Python, and I believe it should work in
Python 2 or Python 3.  It's been most recently only tested against
Python 3.6, and earlier versions were being run against Python 2.7.
I'm afraid there are no unit tests on this.

Extra Python modules required:

* Jinja2
* PIL (if on Python 2), or Pillow (if on Python 3)

DATA FORMAT
-----------

I like this kind of script for web work because nearly all the data
necessary to recreate the index page is present right on the directory
structure itself - if you had the data but not the generator/index page
itself, it would be pretty trivial to code up a new one without really
missing anything.  It does mean that whenever new images are added, you've
got to re-run the generation script to output the HTML, but that does
also mean that you're not wasting CPU time dynamically generating it with
every page load, so that's nice.  Hosting it requires no programming
language like PHP or the like.

The image files themselves are expected to be of the form:

    `<identifier>_<side>_<other>.jpg`

`identifier` is an identifier defined in `generate.py`, and I tend to
use the background color of the sheet in question.  `side` should be
either `fr` for front, or `bk` for back.  `other` can be anything,
really, though I tend to just name them numerically starting with `01`.

So for instance, for "Branches/Bones", some of the filenames I've got
are:
    
    blue_bk_01.jpg
    blue_bk_02.jpg
    blue_fr_01.jpg
    blue_fr_02.jpg
    white_fr_01.jpg

Given that file set, the "blue" variant would have two front images
and two back images, whereas the "white" variant only has one front (and
no back images).  The english text shown on the index page itself is
currently defined in `generate.py` code:

    track01 = self.new_sheet('01_branches_bones', '01. Branches/Bones')
    track01.add_variant('blue', 'Blue with black text')
    track01.add_variant('white', 'White with black text')

Finally, I have attribution text files which allow me to link back to
where these files were found on the internet.  This should be named
as a text file with the same name as the image in question but with
`.txt` appended.  So for instance the attribution file for
`blue_bk_01.jpg` should be named `blue_bk_01.jpg.txt`.  The contents
of the file is something like:

    ets: https://echoingthesound.org/foo
    imgur: https://imgur.com/foo

The attribution code is pretty "stupid" and will just use whatever it
finds in the file like that, so "ets" will be what the first link shows
up as, and will be linked to the specified URL.  This is a bit inefficient
since in general multiple images will share the same source/attribution,
but at least the attribution file can be brought along with the filename
easily, if it's ever renamed or moved.

TODO
----

The directory-reading code is rather inefficient, and a bit stupid in
places, but given the size of the data set I haven't cared enough to make
it a bit more reasonable.  The attribution/source reading in particular
is quite stupid - when it finds a `.txt` file it'll just blindly assume
that it goes with the previously-seen image file, rather than actually
doublechecking the filename.  The matching will only actually work
properly so long as the filenames are set up rigorously enough that
there's no potential ambiguity.  Again, given the data size (and the
fact that I'm probably the only person who'll ever be adding more
images here), I haven't considered that a big enough deal to do anything
about.
