import distutils.core
import os.path

if __name__ == '__main__':
    # List the source files from the CDF v2.5 distribution.
    # CDF stands for Common Data Format.  The source code
    # included below is part of the NASA Goddard Space Flight
    # Center (GSFC)'s package.  To the best of my knowledge it
    # is unmodified from the original sources.
    #
    # NSSDC Common Data Format (CDF)
    # (C) Copyright 1990-1995 NASA/GSFC
    # National Space Science Data Center
    # NASA/Goddard Space Flight Center
    # Greenbelt, Maryland 20771 USA
    # (DECnet   -- NCF::CDFSUPPORT)
    # (Internet -- CDFSUPPORT@NSSDCA.GSFC.NASA.GOV)
    # 
    # The use and distribution of this software is limited by
    # the CDF copyright, which states that the software may be
    # copied or redistributed as long as it is not sold for
    # profit, although it can be incorporated into another
    # substantive product with or without modifications for
    # profit or non-profit.  If the software is modified, it
    # must include the following notices:
    #   - The software is not the original.
    #   - Change history.
    # Consult the CDF documentation for more information.
    #
    # The NASA GSFC CDF software is referred to be a variety of names
    # throughout the documentation, but in the context of this Python
    # package it includes any C source or header file in the "src"
    # directory.  
    #
    # Note that the Python package you are examining right now is
    # not the CDF package released by Goddard but does incorporate
    # substantial portions of the Goddard software.  To use the
    # Python package in any meaningful way is to use the Goddard
    # CDF library.  Likewise, to distribute or incorporate the
    # Python package is to distribute of incorporate the CDF
    # library.  The copyright applied to the Python package may
    # be different than the copyright applied to the CDF library.
    # It is your responsibility to ensure that you are in compliance
    # with copyright law.
    cdf25_distribution_sources = [
        'src/cdflib.c', 'src/cdfcre.c', 'src/cdfope.c',
        'src/cdfclo.c', 'src/cdfmisc1.c', 'src/cdfdel.c',
        'src/cdfsel.c', 'src/cdfcon.c', 'src/cdfget.c',
        'src/cdfmisc2.c', 'src/cdfread.c', 'src/cdfwrite.c',
        'src/cdfhyper.c', 'src/epochuf.c', 'src/dirutils.c',
        'src/cdfput1.c', 'src/cdfput2.c', 'src/cdf_c_if.c',
        'src/cdf_f_if.c', 'src/cdf_i_if.c', 'src/cdftext.c',
        'src/cdfed.c', 'src/cdfstr.c', 'src/cdfvalid.c',
        'src/cdfmem.c', 'src/vstream.c', 'src/epochu.c']
    # End of NASA GSFC CDF library source files.

    # Define a C extension.
    internal = distutils.core.Extension('cdf.internal',
        sources = [
            # The core code for the Python extension
            'cdf25internalmodule.c'] \
            # The unadulterated source code from the CDF v2.5 distribution.
            # While the Python extension itself is not part of the CDF v2.5
            # distribution, it incorporates significant portions of the
            # code from the distribution.  Any use you make of the Python
            # extensions is likely to be subject to the licensing and
            # copyright restrictions of both the Python extension and the
            # CDF v2.5 distribution.
            + cdf25_distribution_sources,
        libraries = ['m'])

    # Define a Python extension module.  This is a lot easier to
    # do than a C extension module because Python has a lot more
    # insight into the workings of Python than it does C.
    pythonic = [
        'cdf.pythonic.interface',
        'cdf.pythonic.attribute',
        'cdf.pythonic.entry']

    # Define another Python extension
    standard = ['cdf.standard']

    data_dir = os.path.expanduser('~/cdf/')
    data_files = [
        # Documentation
        (data_dir,
            ['README',
            'cdf25crm.ps',
            'cdf25ug.ps',
            'numpybook.pdf']),
        # Functional tests
        (os.path.join(data_dir, 'tests/pythonic'),
            ['tests/pythonic/makervar.py',
            'tests/pythonic/makezvar.py',
            'tests/pythonic/makegattr.py']),
        # Examples
        (os.path.join(data_dir, 'examples/internal'),
            ['examples/internal/list-cdf.py',
            'examples/internal/copy-cdf.py',
            'examples/internal/new-cdf.py',
            'examples/internal/test.cdf']),
        (os.path.join(data_dir, 'examples/pythonic'),
            ['examples/pythonic/list-cdf.py',
            'examples/pythonic/copy-cdf.py',
            'examples/pythonic/new-cdf.py',
            'examples/pythonic/csv2cdf.py',
            'examples/pythonic/test.csv',
            'examples/pythonic/test.cdf'])]

    # Invoke the setup code, which will (depending on the command line
    # arguments) build, install, or otherwise tinker with this package
    # on this system.
    distutils.core.setup(
        name = 'CDF',
        version = '0.1',
        description = 'This package handles files in Common Data Format v2.5',
        author = 'Matt Born',
        author_email = 'mattborn@ssl.berkeley.edu',
        url = 'http://efw.ssl.berkeley.edu/packages/cdf',
        classifiers = ['Development Status :: 2 - Pre-Alpha', 
            'Intended Audience :: Science/Research',
            'License :: Public Domain',
            'Topic :: Scientific/Engineering :: Astronomy'],
        ext_modules = [internal],
        py_modules = standard + pythonic,
        requires = ['numpy'],
        # Include some non-source files.  These files are for reference,
        # and will not be compiled.
        data_files = data_files)

    stat = os.stat(os.path.expanduser('~'))
    uid = stat.st_uid
    gid = stat.st_gid
    for (dir, files) in [(data_dir, [])] + data_files:
        os.chown(dir, uid, gid)
        for file in files:
            path = os.path.join(dir, os.path.basename(file))
            os.chown(path, uid, gid)
