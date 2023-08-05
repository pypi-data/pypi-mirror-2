The Philosophy behind Woven
===========================
*Here I try to explain the why and the how for Woven.*

**Developers are driven to create new django apps and sites for profit, pleasure or madness and sometimes all three**

but...

**Packaging and deployment of virtual servers is dull**

**Django packaging and deployment is awkward and dull**

**Packaging and deployment and configuration of Django on virtual servers is an awkward dull dark art**

**Because packaging, deployment and configuration is so boring I tend to forget the detail between projects and end up having the re-learn the same processes over and over**

**I want to reclaim my time spent re-learning packaging, deployment and configuration and invest it in actual development.**


The cycle of life
-----------------

A typical django development cycle goes something like this::

    **hack** using the tool of choice on the machine of choice
    **test**
    **package** using setuptools, distribute, or leave unpackaged in version control
    **deploy** to cloud using rsync, version control, or other tool
    
In any python project there are five layers of dependencies and packaging to consider in the development cycle. Roughly speaking in descending order of api stability at any point in time they are::

    The **os layer** - msi,dmg,rpm,deb being the main ones
    The **standard Python** installation and version - usually cpython but also jython, ironpython, pypy etc
    Third party python **packaged libraries** - Usually from Pypi as zip, eggs, tgz etc
    Any unpacked **source repositories** - git, hg, bzr, svn
    Your **project** 
    
Mix development cycle in the blender with dependencies and the weaknesses become apparent::

    development environment != server environment
    dependency combinations multiply possible failures
    packaging process can introduce errors

Lets look at those weakneses.
    
The os environment
------------------
    
Modern operating system packaging systems do a pretty good job of trying maintain equivalent stable environments between systems. Woven uses Ubuntu because the server os is a nice lightweight server os that is both common in the cloud, updated twice a year, and can be commercial or free. For non-python dependencies, you can strike a reasonable balance between stability and currency of package versions. The point of woven is that it should be simple to re-deploy a project onto a new version of ubuntu without massive upgrade drama. Long term support versions are great for stability when development has slowed but not for ongoing agile development when you want to be at the cutting if not bleeding edge.

Defeating dependency depression
-------------------------------
    
The typical solution is to use some kind of continuous integration tool such as buildbot, hudson, or bitten which help manage dependency and packaging issues. In the cloud however we can control the server environment, so continuous integration is a tactical nuclear weapon in the small skirmish that is packaging.

The other solution to the problem is something like Google App Engine, a tightly controlled environment with versioned api, and an attractive deployment tool. Of course if you don't like their packaged python library you can upload your own if it's pure python or go f**k yourself. Don't get me wrong, I can see GAE being really attractive solution when they release their SQL option.

Woven uses the standard Ubuntu debian packages for the os, python installation, and any python package you consider won't change between Ubuntu versions. For the rpoject environment it uses Virtualenv and pip to deploy a new environment for each significant version of your project. This makes it trivial to experiment with different versions of python libaries, and work from specific revisions in source repositories without locking you in to a specific api combination.

Package this!
-------------

Probably if you surveyed developer habits, a setup.py is the last thing that ever gets considered if at all because traditionally it was a pretty arcane and badly documented process that doesn't add much value if you are never going to distribute your package beyond a host server. Additionally it was easy to miss files or package them incorrectly, so you then need to run your tests on the final package adding a layer of complexity. This is changing.

Woven takes the pragmatic approach that the standard python distutils packaging is a good thing and getting better but not quite ready for the cloud, and doesn't pass the *so simple you'd be stupid not to do it for every project* test by itself. Probably the combination of ``distribute`` and ``nosetests`` would come mighty close but neither is stdlib at this time. So for the moment Woven makes you use a nominal setup.py but doesn't use any potential distribution you might create from it. To do that it would need to test the package in the cloud and woven doesn't do that ... yet.

Maybe one day you'll be able to ``python setup.py install --host=hostname``, but until that day you need additional tools for deployment. 

Deployment Alternatives
-----------------------

The alternative to Pip, Virtualenv would be buildout and it'

