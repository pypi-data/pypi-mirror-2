===========
Podcaster
===========

Converts a Youtube / Dailymotion RSS feed to an iTunes podcast.

And it's powered by the wonderful Nagare_ framework ! 

Installation
================

- Note that the Nagare_ framework needs `Python Stackless`_ in order to run
- Using `easy_install` : easy_install podcaster

Launch the application
==========================

- Launch `podcaster` using the command : nagare-admin serve podcaster

Basic Usage
=================

By default, your `Podcaster` application will be accessible using your favorite
web browser at the address : http://localhost:8080/podcaster

Select the platform, fill in the YouTube/Dailymotion username of the person you
want to subscribe, choose the video resolution, and submit the form.

Subscribe to a new iTunes' podcast using the generated URL and that's it !

Notes
=======

This application is still at a beta stage, but feel free to give me feedback if
you liked this app.

Why this app ?
================

I don't like watching videos using my web browser, opening multiple tabs,
waiting for the player to preload data before being able to watch the video
(YouTube is very slow with my internet provider).
I don't like useless comments, unrelated informations, etc. I want to watch my
videos, and that's all !

Some podcasts are available on iTunes but the resolution is sometimes too low
for my 21'+ screen ;)

So I let iTunes do the job for me when I'm away.

.. _Nagare: http://www.nagare.org
.. _`Python Stackless`: http://www.stackless.com