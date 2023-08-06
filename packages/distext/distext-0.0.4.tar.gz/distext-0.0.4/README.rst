Some useful distutils/setuptools/distribute extensions to deal with our needs @
Silveregg.

The main features are:

    - support for arbitrary and customizable installation of data files, ala
      autoconf. For example, you can set a file to be installed in $sysconfdir, which
      will expand to /etc by default, but can be customized from the command
      line. Only sysconfdir, bin and libdir are supported for now.
    - optionally generate a python module which contains the aforementioned
      paths so that they can be retrieved at runtime
    - option to install init scripts, optionally from templates using install
      variables (think init scripts which need to know where other bits are
      installed). The templating format is Jinja2.
    - basic code to write hg revision in a version file
