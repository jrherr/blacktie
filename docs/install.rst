Installation
============

Requirements
------------

The following python modules must be installed for blacktie to function properly: ::

  Mako>=0.7.3
  PyYAML>=3.10
    
The following modules will provide useful but optional functionality: ::

  pprocess>=0.5



Installing the latest version from the git repository
-----------------------------------------------------
.. Note:: Git is a **very** useful tool to have installed and to know how to use.  `Learn more here <http://git-scm.com/>`_ and `try it out here <http://try.github.com/>`_.

Clone the repo::
    
  $ git clone git://github.com/xguse/blacktie.git
    
Install with any unmet requirements using ``pip``: ::
  
  $ [sudo] pip install -r blacktie/requirements.txt blacktie

Install using standard ``setup.py`` script: ::
  
  $ cd blacktie
  $ [sudo] python setup.py install

Installing without using ``git`` for the download
---------------------------------------------------------
After installing the requirements: ::

  $ wget https://github.com/xguse/blacktie/archive/master.zip
  $ unzip master.zip
  $ cd blacktie-master
  $ [sudo] python setup.py install
