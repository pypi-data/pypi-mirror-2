README.txt(v1.0.0)


PACKAGE NAME:
    Genome Relative Abundance using Mixture Model thoery (GRAMMy)
    Currently the package works for Linux platforms.
    It might be work for OS X and Windows (not tested).

DEPENDENCY:
    Python(>=2.5)
        download @ http://www.python.org/
    Numpy(>=1.0)
        download @ http://www.scipy.org/
    Scipy(>=0.6)
        download @ http://www.scipy.org/
    Biopython(>=1.0)
        download @ http://biopython.org/

FILES:
    LICENSE.txt
    README.txt
    INSTALL.txt
    MANIFEST.in
    setup.py
    grammy/
    doc/
    test/
    scripts/

INSTALL:
    Refer to INSTALL.txt

EXECUTABLES:
    scripts/grammy-gdt.py
    scripts/grammy-rdt.py
    scripts/grammy-pre.py
    scripts/grammy-em.py
    scripts/grammy-post.py

USAGE:
    (i) Above executables will be available from your python scripts directory.
    	Use '-h' to read individual script usage.
    (ii) A pre-structured genome and taxon directory if required for grammy-gdt.py;
    	An example is available as the grefs.tgz file.
    	The file can be downloaded from http://meta.usc.edu/softs/grammy/grefs.tgz
    (iii) A test example is available at 'test/test.sh' and explained there.

DOCUMENTATION:
    (i) developement information of grammy sub modules, e.g. grammy.gemlib model,
    	can be found by issuing "pydoc grammy.gemlib" command on command line. 
    (ii) information of how to use this package for analysis data by examples can
    	be found in documentation in "doc" subdirectory


