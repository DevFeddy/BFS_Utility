# Register
- can be initialized (optional) with a list containing initial values for register where the first element is c(1)
- access with [], c(0) = reg[0] etc

# RAM_Interpreter 
- initialize with string of code and an object of registers
- execute with .execute(), Parameters:
    - show (bool): if True, shows value of register after every command (default: False)
    - timeout (int): if non-negative, lines of code that will be executed before the programm stops (default: -1)
