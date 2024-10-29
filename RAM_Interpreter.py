from typing import Any, MutableSequence

class Register(MutableSequence):

    l: list
    constant: int

    def __init__(self, l = None) -> None:
        self.l = [0] + l
    

    def __getitem__(self, ind: int) -> int:
        if ind < 0:
            return self.constant
        if ind >= len(self.l):
            return 0
        return self.l[ind]
    
    def __setitem__(self, ind: int, value: Any) -> None:
        if ind < 0:
            self.constant = value
            return
        dif = ind - len(self.l)
        if dif >= 0:
            self.l += dif*[0]
            self.l.append(value)
        else:
            self.l[ind] = value
    
    def __delitem__(self, ind: int) -> None:
        if ind < len(self.l):
            self.l[ind] = 0
    
    def __len__(self) -> int:
        return len(self.l)
    
    def insert(self, index: int, value: Any) -> None:
        raise ValueError()
    
    def print(self):
        print(self.l)


class RAM_Interpreter:
    
    cmd: list[str]
    args: Register
    counter: int
    end: bool

    def __init__(self, cmds: str, args: Register) -> None:
        self.cmd = [self.init_cmd(c) for c in cmds.split('\n') if self.init_cmd(c) != None]
        self.args = args
        self.counter = 1
        self.end = False
    
    def init_cmd(self, cmd: str):
        cmd = cmd.lower()
        cmd = cmd.strip()
        if cmd.startswith('if'):
            arg = cmd.split()[-1]
            mode = cmd.split()[1]
            mode = mode.removeprefix('c(0)')
            comp = mode[-1]
            mode = mode.removesuffix(comp)
            cmd = f"ifs {mode} {comp} {arg}"
        if cmd == '':
            return None
        return cmd

    def execute(self, show = False, timeout = -1):
        while not self.end and timeout != 0:
            self.call(self.cmd[self.counter - 1])
            timeout -= 1
            if (show):
                self.args.print()
                print(f'Counter: {self.counter} --> Next: {self.cmd[self.counter - 1]}')
    
    def call(self, func: str):
        if func == 'end':
            self.end = True
            return
        if func.startswith('if'):
            cmd, op, comp, arg = func.split()
            arg = int(arg)
            comp = int(comp)
            self.ifs(op, comp, arg)
            return
        
        cmd, arg = func.split()
        pre = ''
        cs = cmd.split('-')
        arg = int(arg)
        if len(cs) > 1:
            pre = cs[0]
            cmd = cs[1]
            if pre.lower() == 'c':
                self.cfun(arg, self.get_function(cmd))
            if pre.lower() == 'ind':
                self.ind(arg, self.get_function(cmd))
        else:
            self.get_function(cmd)(arg)

    
    def get_function(self, func: str):
        return getattr(self, func)

    def ifs(self, op, comp, arg):
        v = self.args[0]
        def do():
            self.goto(arg)
            raise ValueError()
        
        try:
            match(op):
                case '=':
                    if v == comp: do()
                case '<':
                    if v < comp: do()
                case '>':
                    if v > comp: do()
                case '<=':
                    if v <= comp: do()
                case '>=':
                    if v >= comp: do()
            self.counter += 1
        except ValueError:
            pass

    def goto(self, numb):
        self.counter = numb

    def ind(self, numb, fun):
        n = self.args[numb]
        fun(n)

    def cfun(self, numb, fun):
        if fun == self.store:
            raise ValueError("NO such thing as c-store")
        self.args[-1] = numb
        fun(-1) 

    def load(self, numb):
        self.args[0] = self.args[numb]
        self.counter += 1
    
    def store(self, numb):
        self.args[numb] = self.args[0]
        self.counter += 1
    
    def add(self, numb):
        self.args[0] += self.args[numb]
        self.counter += 1
    
    def sub(self, numb):
        self.args[0] = max(self.args[0] - self.args[numb], 0)
        self.counter += 1
    
    def mult(self, numb):
        self.args[0] *= self.args[numb]
        self.counter += 1
    
    def div(self, numb):
        self.args[0] //= self.args[numb]
        self.counter += 1
