Example usage:

from DataPrimitives import DataPrimitives

dp = DataPrimitives()

# Convert string to bits
string2bits    = dp.OS2BSP('abc') 
# string2bits  = 011000010110001001100011

# Convert bits to integer
bits2integer   = dp.BS2IP('011000010110001001100011')
# bits2integer = 6382179

# Convert integer string to string
integer2string = dp.I2OSP(6382179, 3)
# integer2string = abc

You may turn on the explanation mode by suppling a True argument to the main class. 

Example: 
        tutor = DataPrimitives(True)
        tutor.BS2OSP("011000010110001001100011")  

This will print out every transformation:
        Convert bit string 011000010110001001100011 to symbol octets
        Convert 8 bit string:01100001 to integer:
            bit num 7 is 0     sum is 0
            bit num 6 is 1     sum is 0 + 64(2**6) = 64
            bit num 5 is 1     sum is 64 + 32(2**5) = 96
            bit num 4 is 0     sum is 96
            bit num 3 is 0     sum is 96
            bit num 2 is 0     sum is 96
            bit num 1 is 0     sum is 96
            bit num 0 is 1     sum is 96 + 1(2**0) = 97
        Return: 97
            01100001 is decimal 97 = ascii symbol: a
        Convert 8 bit string:01100010 to integer:
            bit num 7 is 0     sum is 0
            bit num 6 is 1     sum is 0 + 64(2**6) = 64
            bit num 5 is 1     sum is 64 + 32(2**5) = 96
            bit num 4 is 0     sum is 96
            bit num 3 is 0     sum is 96
            bit num 2 is 0     sum is 96
            bit num 1 is 1     sum is 96 + 2(2**1) = 98
            bit num 0 is 0     sum is 98
        Return: 98
            01100010 is decimal 98 = ascii symbol: b
        Convert 8 bit string:01100011 to integer:
            bit num 7 is 0     sum is 0
            bit num 6 is 1     sum is 0 + 64(2**6) = 64
            bit num 5 is 1     sum is 64 + 32(2**5) = 96
            bit num 4 is 0     sum is 96
            bit num 3 is 0     sum is 96
            bit num 2 is 0     sum is 96
            bit num 1 is 1     sum is 96 + 2(2**1) = 98
            bit num 0 is 1     sum is 98 + 1(2**0) = 99
        Return: 99
            01100011 is decimal 99 = ascii symbol: c
        Retrun: abc
