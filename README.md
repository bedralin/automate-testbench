automate-testbench
==================

In this repository, I am open-sourcing some of my code used to automate a certain test-bench. 
You may use these as examples to start your own fun automation of hardware. I noticed that 
there was not much information online about automating test-benches so I am giving you some 
sample code of what I have to get you started. I can not give you my full automation code, 
because this may be sensitive information which I am not allowed to give. Just keep in mind,
when writing your automation script, pay attention to the timing. So critical!

Shoutout to my buddy Harley Cumming for showing me the beauty of Computer Engineering!

In order for this to work, you must install the package called python-vxi11: 
- https://github.com/python-ivi/python-vxi11
- git clone https://github.com/python-ivi/python-vxi11
- sudo python setup.py install

You will also need to install PySerial:
- http://pyserial.sourceforge.net/
- sudo svn co http://svn.code.sf.net/p/pyserial/code/trunk/pyserial/
- cd pyserial
- sudo python setup.py install

Feel free to email me for any help:
- Bronson Edralin <bedralin@hawaii.edu>
- BS Electrical Engineering, May 2014
- MS Computer Engineering Graduate Student and Research Assistant
- Instrumentation Development Lab (IDL), Physics and Astronomy Department, University of Hawaii at Manoa
