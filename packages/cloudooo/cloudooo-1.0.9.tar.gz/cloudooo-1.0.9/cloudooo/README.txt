Install Cloudooo
================
  
  $ python2.6 setup.py install
  
  Warnings:
      - you must have installed setuptools>=0.6c11 in this python.

Install Dependencies in Mandriva
================================
  
  $ urpmi xvfb # System Dependencies

Install OpenOffice.org
======================

  Was used for testing the package's official openoffice.org. Follow these steps to install:
  
  Download Package from the official site
  ---------------------------------------
  
  x86_32
  ----
    $ wget http://download.services.openoffice.org/files/stable/3.2.0/OOo_3.2.0_LinuxIntel_install_wJRE_en-US.tar.gz
  
  x86_64
  ------
    $ wget http://download.services.openoffice.org/files/stable/3.2.0/OOo_3.2.0_LinuxX86-64_install_wJRE_en-US.tar.gz

  Unpack the tar.gz and Install
  -----------------------------
    $ tar zxvf OOo_3.2.0_LinuxX86-64_install_wJRE_en-US.tar.gz
    $ cd OOO320_m12_native_packed-1_en-US.9483/RPMS
    $ rpm -i *.rpm # install all packages together
    
    The instalation is in /opt

Create Configuration File
=========================
  
  The configuration file is used to start the application using paster.
  $ cp ./cloudooo/samples/samples.conf . # Copy to current folder

  The next step is define some attributes in cloudooo.conf:
    - working_path - folder to run the application. This folder need be created.
    - uno_path - full path to UNO library;
    - soffice_binary_path - full path to soffice.bin;

Run Application
===============

  $ paster serve ./cloudooo.conf

  or run as a daemon:
  
  $ paster serve ./cloudoo.conf --daemon
  

Stop Application
===============

  $ kill -1 PASTER_PID

  Warning: always use SIGHUP because only with this signal all processes are
stopped correctly.

Cloudooo Description
=====================

- XMLRPC + WSGI will be one bridge for easy access OpenOffice.org. This will implement one XMLRPC server into WSGI (Paster).

- PyUno is used to connect to OpenOffice.org stated with open socket. The features will be handled all by pyuno.

- Xvfb is used to run Openoffice.org. This is controlled by Daemon(cloudooo).

- Only a process will have access to OpenOffice.org by time.

- All clients receive the same object(proxy) when connects with XMLRPC Server.

Xvfb and OpenOffice

 - configure and start Xvfb;
    - Use a single Xvfb;
    - the xvfb will be started with the XMLRPC Server;
	- When start the Daemon(cloudooo), it configures Xvfb, next opens the openoffice(with pyuno) and start XMLRPC Server; 
 - control Xvfb;
 - start openoffice;
   - Pyuno start the openoffice processes and the communication is through sockets;
   - Openoffice processes run in brackground and in virtual display;
 - control openoffice;
   - The socket can't lose the connection, if this occurs should kill the process and submit again the file;

XMLRPC Server - XMLRPC + WSGI
-----------------------------

  - Send document to openoffice and return the document converted with metadata;
      - XMLRPC receives a file and connects to a openoffice by pyuno;
      - The pyuno opens a new openoffice, write, add metadata and returns the document edited or converted to xmlrpc and it return the document to the user;
      - When finalize the use of openoffice, should make sure that it was finalized;
  - Export to another format;
  - Invite document and return metadata only;
  - Edit metadata of the document;
  - Problems and possible solution
     - OpenOffice is stalled;
       - finalize the process, start openoffice and submit the document again(without restart the cloudooo);
     - Openoffice is crashed;
       - finalize the process, verify if all the process was killed, start openoffice and submit the document again(without restart the cloudooo)
     - OpenOffice received the document and stalled;
       - if openoffice isn't responding, kill the process and start
     - The document that was sent is corrupt;
       - write in log the error and verify that the process aren't in memory
