Binstr - A collection of utility functions for creating and operating on
         strings of binary digits. It is compatible with Python versions >2.6
         including 3.x.
         It is useful to use these functions to make small bugs in your code
         easier to find since all inputs are checked thoroughly for errors
         using assertions.

PyPI may not always have the latest version.
The latest version can always be found on the GitHub page (https://github.com/DavidMcEwan/binstr).

Includes:
    b_and()         - Perform a bitwise AND
    b_or()          - Perform a bitwise OR
    b_xor()         - Perform a bitwise XOR
    b_nand()        - Perform a bitwise NAND
    b_nor()         - Perform a bitwise NOR
    b_nxor()        - Perform a bitwise NXOR
    b_not()         - Perform a bitwise NOT (inversion)
    
    b_land()        - Perform a logical AND
    b_lor()         - Perform a logical OR
    b_lxor()        - Perform a logical XOR
    b_lnand()       - Perform a logical NAND
    b_lnor()        - Perform a logical NOR
    b_lnxor()       - Perform a logical NXOR
    
    int_to_b()      - Convert a positive integer to a sting of binary.
                      e.g. int_to_b(5) -> '00000101'
    frac_to_b()     - Convert a positive fraction to a string of binary.
                      e.g. frac_to_b(0.5) -> '10000000'
    str_to_b()      - Convert an ASCII string of characters to a string of binary.
                      e.g. str_to_b('abc') -> '011000010110001001100011' 
    bytes_to_b()    - Convert an byte sequence to a string of binary.
                      In Python 2.x this is the same as str_to_b().
    baseX_to_b()    - Convert from another base (4, 8, 16, 32 or 64) to binary coding.
    
    b_to_int()      - Convert from base2 binary coding to an integer.
    b_to_frac()      - Convert from base2 binary coding to an float less than 1.0.
    b_to_str()      - Convert from binary coding to a string of ASCII characters.
    b_to_bytes()    - Convert from binary coding to a byte sequence.
                      In Python 2.x this is the same as b_to_str().
    b_to_baseX()    - Convert from binary coding to another base (4, 8, 16, 32 or 64).
    
    b_bin_to_gray() - Convert binary code into gray code
    b_gray_to_bin() - Convert gray code into binary code
    
    b_add()         - Perform an ADD operation
    b_mul()         - Perform a MUL operation (multiply)
    
    b_blockify()    - Separate a string of binary into blocks
    b_validate()    - Validate that a given string contains only 0s and 1s

int_to_b() is a lot more flexible than the built in bin() function although
bin() is used internally. It allows you to force a width, change what bits are
chopped off, change the alignment and change the bit endianness.

The bit endianness is particularly useful for creating binary shuffles.
E.g. For creating the binary shuffle for a 256 sample FFT this can be done in a few lines.

from math import log
length = 256
shuffle = [int( int_to_b(i, width=int(log(length, 2)), endian='little') , 2)
           for i in range(length)]


str_to_b() is also very flexible and can be used to simulate the voltage levels
in serial communication.
E.g. To simulate a standard RS232 port with a "8E1" configuration sending the
data "Hello World!" this can be done simply.

data = str_to_b('Hello World!', endian='little', char_width=8, parity='sE', suffix='1')

Note that data is usually sent out LSB first. The char_width argument is shown
for clarity but is 8 by default. The suffix argument is used to add one stop bit.


-------------------------------------------------------------------------------
Installation
-------------------------------------------------------------------------------
extract the contents of the tarball:
cd to this directory (where README.txt and setup.py are) then run:

python setup.py install

Note: This may need to be run with root (admin) priviliges.


-------------------------------------------------------------------------------
Dev Notes
-------------------------------------------------------------------------------
This is just a list of things which have been considered while developing binstr,
just in case anybody is interested.

Binstr may work on versions of Python before 2.6 with some slight and fairly obvious
modifications (obvious when you run it) it. This is not really a big priority
of mine but I'll try not to break backward compatiblity when possible. No promises.

Rejected funtions include:
    deblockify - Use str().replace()
    b_to_file - Use file().write(b_to_bytes(<b_string>), 'wb')
    file_to_b - Use bytes_to_b(open(<path>, 'rb').read())
    b_log, b_exp, etc... - Use the proper math functions
    b_sub - Use b_add() with b_not for Two's compliment representaion.
    b_div - Use b_mul with inverse
    b_rotl, b_rotr - Use Python slices
    b_reverse - Use <string>[::-1] E.g. '0101'[::-1] returns '1010'

Stuff on my TODO list for next version include:
    1. Make some of the functions a bit more efficient by using map(), reduce() and filter().
       None of the functions have been written with speed as a top priority so some are pretty
       poor in terms of efficiency.
    
    2. Add functions for other binary encodings apart from standard base2 and Gray.
       These would (maybe) include signed/unsigned exponential, signed/unsigned interleaved
       exponential, Fibonacci, Rice, Golomb, Levenshtein, and Huffman coding.
       I'm not quite sure what else should be added like that just now.
    
    3. Add Two's Compliment function and One's(?).
       I know it's so trivial I could just put it in now but
       it seems nicer to leave it till version 1.4.

If anybody has any tips, advice or general abuse concerning Binstr then please feel
free to send me an email or even get on GitHub and contribute.

