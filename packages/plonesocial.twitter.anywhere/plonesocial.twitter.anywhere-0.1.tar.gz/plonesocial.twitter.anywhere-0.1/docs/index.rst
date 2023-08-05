.. plonesocial.auth.rpx documentation master file, created by sphinx-quickstart on Tue Oct 13 16:00:50 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. image:: screens/plone_overview.png
   :width: 700px

Twitter @Anywhere for Plone
===========================


``plonesocial.twitter.anywhere`` is an addon for Plone which integrates `Twitter @Anywhere <http://dev.twitter.com/anywhere>`_ into your Plone site. 

It provides the auto linking and hovercard features which you can enable and disable as well as two portlets, one for displaying a Follow button and another one with a customizable tweetbox. More functionality might be added in the future.

Tutorial
========

Install `plonesocial.twitter.anywhere` in Plone
***********************************************

Look for your `buildout.cfg` and search for the following line::

    [buildout]
    ...
    
    eggs =
        ...
    
Add a new indented line to it like this::

    eggs = 
        ...
        plonesocial.twitter.anywhere
        
and rerun buildout::

    bin/buildout -vv
    
(or without `-vv` in case you don't need the additional debug output).

Then restart your Plone site.

Go to "Site Setup" and then to "Add-on Products" and install it.

    

Creating an application at Twitter
**********************************

For using `Twitter @Anywhere <http://dev.twitter.com/anywhere>`_ you first need to generate an API key which means registering an application on Twitter.

For this go to the `Twitter @Anywhere Application Registration screen <http://dev.twitter.com/anywhere/apps/new>`_ and enter the following details:

 * A name for the application (free to choose)
 * The location of your Plone site. This cannot be `localhost` but needs to be a real domain. Give the path to your Plone root.
 * Enter your own Organization 
 * Enter a callback URL. This is not really needed but simply give the URL to your Plone site root (like above) and e.g. add ``/@@anywhere_callback`` (nothing is there at the moment though).
 * optionally you can upload an icon for your application
 * Make sure you selected "Read & Write" as the default access type.
 
Here is how it looks like:

.. image:: screens/2_anywhere_registration.png
   :width: 600px

After submitting the form you have to agree to the Terms of Service and then you will see the following screen:

.. image:: screens/3_anywhere_after_registration.png
   :width: 600px

You can either copy your API key out of the JavaScript call or you can go to "View your Applications" and click on your application to get the app screen:

.. image:: screens/4_anywhere_apikey.png
   :width: 600px

Copy the API key into your clipboard.


Configuring your Plone site
***************************

Now go to your Plone site and choose ``Site Admin`` in the ``Admin`` menu (as it's called in Plone 4, otherwise click on ``Plone Setup`` in Plone 3). You should see the ``Twitter @Anywhere Configuration`` link which you should click.

.. image:: screens/5_plone_setup.png
   :width: 600px

Now enter your API key and select if you want auto linking of ``@username`` links or if you want the hovercard effect on them.

Submit the form.

Now ``Twitter @Anywhere`` is configured for your Plone site. You can now start adding portlets.


The Twitter @Anywhere portlets
******************************

``plonesocial.twitter.anywhere`` provides two portlets:

.. image:: screens/6_portlet_overview.png
   :width: 300px



The Twitter Follow portlet
--------------------------

This portlet simply prints a "Follow @username on Twitte" button where you can configure which username to use. You can of course use multiple portlets of this type on one Plone site.

This is how the portlet looks:

.. image:: screens/7_follow_portlet.png
   :width: 300px




The Tweetbox portlet
--------------------

.. image:: screens/8_tweetbox.png
   :width: 300px


The Tweetbox portlet provides a box for sending out tweets. Those will be posted to the timeline of the user using the tweetbox.

You can configure the following settings per box:

 * Box ``width`` and ``height`` depend on your Plone theme. The defaults should work well in the Plone 4 theme.
 * The ``Label`` setting defines the title above the box. An empty field will produce the default label.
 * The ``Contents`` settings holds a default text which is put into the tweetbox. E.g. you could put "RT @username " there or add some default hashtags.
 * The ``Counter`` settings defines if the character counter is displayed. 




Credits
=======

* Christian Scholz (cs@comlounge.net)

Development was sponsored by `COM.lounge GmbH <http://comlounge.net/>`_.

Source Code
===========

The source code is available at http://bitbucket.org/mrtopf/plonesocial.twitter.anywhere/

Python Package
==============

The package can be found at http://pypi.python.org/pypi/plonesocial.twitter.anywhere/

License
=======

**MIT License**

Copyright (c) 2010 COM.lounge GmbH

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


