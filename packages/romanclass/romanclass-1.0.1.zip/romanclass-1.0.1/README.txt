Documentation is found in the file "roman.odt" in open document text format.  You can read or edit it with OpenOffice.org writer.
For those who have not yet installed openoffice.org, use "roman.pdf".

Because the documentation requires accurate rendering of rare unicode character graphics, it really cannot be done in a .txt file.

Installation uses the usual Python method:

>cd your-unzipped-directory
>python setup.py install

C:>c:\python27\python.exe
Python 2.7 (r27:82525, Jul  4 2010, 09:01:59) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import romanclass as roman
>>> r = roman.Roman(123)
>>> print(r)
CXXIII
>>> roman.test()
The longest number between Nulla and  Roman(4006)
was "MMMDCCCLXXXVIII" which is "3888" in Arabic
5000 ROMAN NUMERAL FIVE THOUSAND 5000.0
unicode= \u2181
10000 ROMAN NUMERAL TEN THOUSAND 10000.0
unicode= \u2182
50000 ROMAN NUMERAL FIFTY THOUSAND 50000.0
unicode= \u2187
100000 ROMAN NUMERAL ONE HUNDRED THOUSAND 100000.0
unicode= \u2188
>>> exit()

