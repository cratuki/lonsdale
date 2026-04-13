#
# This is fork of the interface script library to support async interaction
# (Original: github.com/cratuki/interface_script_py)
#

import asyncio
import inspect


# --------------------------------------------------------
#   common
# --------------------------------------------------------
def parse_line_to_tokens(line):
    '''
    Tokenises a line.
    
    Respects quotation mark boundaries that indicate strings containing
    spaces, or escapted quotation marks.

    Respects comments, denoted by a hash symbol that is not inside of a quoted
    block.
    '''
    tokens = []
    acc = []
    def esc_append(c):
        if c == '\n':
            pass
        else:
            acc.append(c)
    mode_normal   = 0
    mode_squotes  = 1
    mode_dquotes  = 2
    mode_escape_n = 3 # escape, normal mode
    mode_escape_s = 4 # escape, single-quote mode
    mode_escape_d = 5 # escape, double-quote mode
    var_mode = [mode_normal]
    def set_mode(m):
        var_mode[0] = m
    def mode():
        return var_mode[0]
    def spin(force=False):
        s = ''.join(acc).strip()
        if force or s: tokens.append(s)
        while acc: acc.pop()
        var_mode[0] = mode_normal
    for c in line.strip():
        if mode() == mode_escape_n:
            esc_append(c)
            set_mode(mode_normal)
        elif mode() == mode_escape_s:
            esc_append(c)
            set_mode(mode_squotes)
        elif mode() == mode_escape_d:
            esc_append(c)
            set_mode(mode_dquotes)
        elif mode() == mode_normal:
            if c == '\\':
                set_mode(mode_escape_n)
            elif c == ' ':
                # end of word
                spin()
            elif c == '#':
                # comment
                spin()
                break
            elif c == '"':
                # enter double quotes
                spin()
                set_mode(mode_dquotes)
            elif c == "'":
                # enter single quotes
                spin()
                set_mode(mode_squotes)
            else:
                acc.append(c)
        elif mode() == mode_squotes:
            if c == '\\':
                set_mode(mode_escape_s)
            elif c == "'":
                # exit single quotes
                spin(True)
            else:
                acc.append(c)
        elif mode() == mode_dquotes:
            if c == '\\':
                set_mode(mode_escape_d)
            elif c == '"':
                # exit double quotes
                spin(True)
            else:
                acc.append(c)
        else:
            raise Exception('Should not get here [%s]'%mode())
    if mode() != mode_normal:
        raise Exception("invalid line. [%s]"%(line))
    spin()
    return tokens


# --------------------------------------------------------
#   async
# --------------------------------------------------------
class LineFinderAsync:
    "At the end of a line, this triggers a callback."

    async def init(self, cb_line):
        self.cb_line = cb_line
        self.sb = []

    async def accept(self, c):
        if c == '\n':
            line = ''.join(self.sb).strip()
            await self.cb_line(line)
            self.sb = []
        else:
            self.sb.append(c)


class SignalConsumerAsync(object):

    def __init__(self, handler):
        self.handler = handler

    def on_interface(self, iname, vfields):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            s = ', '.join(['self', *vfields])
            raise Exception('no handler %s(%s)'%(method_name, s))
        method = getattr(self.handler, method_name)
        argspec = list(inspect.signature(method).parameters.keys())
        if argspec != vfields and not (len(argspec) == 1 and argspec[0] == 'kwargs'):
            raise Exception('inconsistent spec for %s iscript:%s method:%s'%(
                iname, str(vfields), str(argspec)))

    async def on_signal(self, iname, kwargs):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            raise Exception('no handler [%s]'%method_name)
        member = getattr(self.handler, method_name)

        await member(**kwargs)


class InterfaceScriptParserAsync:

    async def init(self, handler):
        self.handler = handler

        self.signal_consumer = SignalConsumerAsync(
            handler=self.handler)
        # on_interface(iname, vfields) -> None
        self.cb_interface = self.signal_consumer.on_interface
        # on_signal(iname, values) -> None
        self.cb_signal = self.signal_consumer.on_signal

        self.finder = LineFinderAsync()
        await self.finder.init(self._on_line)

        self.interfaces = {}

    async def parse(self, s):
        for c in s:
            await self.finder.accept(c)

    async def _on_line(self, line):
        tokens = parse_line_to_tokens(line)
        if not tokens:
            return
        if tokens[0] == 'i':
            self._handle_interface(tokens)
        else:
            if tokens[0] == '.':
                tokens = tokens[1:]
            await self._handle_signal(tokens)

    def _handle_interface(self, tokens):
        if len(tokens) < 2:
            raise Exception("Invalid vdef %s"%str(tokens))
        iname = tokens[1]
        vfields = tokens[2:]
        if iname in self.interfaces:
            # it's fine to have multiple definitions, but they must
            # be consistent.
            current = self.interfaces[iname]
            if vfields != current:
                m = "inconsistent vdefs %s %s"%(
                    str(current),
                    str(vfields))
                raise Exception(m)
        else:
            self.interfaces[iname] = vfields
            self.cb_interface(iname, vfields)

    async def _handle_signal(self, tokens):
        iname = tokens[0]
        if iname not in self.interfaces:
            raise Exception("no interface defined for %s"%iname)
        vfields = self.interfaces[iname]
        values = tokens[1:]
        if len(vfields) != len(values):
            raise Exception("wrong number of args. i %s %s. got %s"%(
                iname, str(vfields), str(values)))

        kwargs = {}
        for (idx, vfield) in enumerate(vfields):
            kwargs[vfield] = values[idx]

        await self.cb_signal(iname, kwargs)


# --------------------------------------------------------
#   sync
# --------------------------------------------------------
class LineFinderSync:
    "At the end of a line, this triggers a callback."

    def init(self, cb_line):
        self.cb_line = cb_line
        self.sb = []

    def accept(self, c):
        if c == '\n':
            line = ''.join(self.sb).strip()
            self.cb_line(line)
            self.sb = []
        else:
            self.sb.append(c)


class SignalConsumerSync(object):

    def __init__(self, handler):
        self.handler = handler

    def on_interface(self, iname, vfields):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            s = ', '.join(['self', *vfields])
            raise Exception('no handler %s(%s)'%(method_name, s))
        method = getattr(self.handler, method_name)
        argspec = list(inspect.signature(method).parameters.keys())
        if argspec != vfields and not (len(argspec) == 1 and argspec[0] == 'kwargs'):
            raise Exception('inconsistent spec for %s iscript:%s method:%s'%(
                iname, str(vfields), str(argspec)))

    def on_signal(self, iname, kwargs):
        method_name = 'on_%s'%iname
        if method_name not in dir(self.handler):
            raise Exception('no handler [%s]'%method_name)
        member = getattr(self.handler, method_name)

        member(**kwargs)


class InterfaceScriptParserSync:

    def init(self, handler):
        self.handler = handler

        self.signal_consumer = SignalConsumerSync(
            handler=self.handler)
        # on_interface(iname, vfields) -> None
        self.cb_interface = self.signal_consumer.on_interface
        # on_signal(iname, values) -> None
        self.cb_signal = self.signal_consumer.on_signal

        self.finder = LineFinderSync()
        self.finder.init(self._on_line)

        self.interfaces = {}

    def parse(self, s):
        for c in s:
            self.finder.accept(c)

    def _on_line(self, line):
        try:
            tokens = parse_line_to_tokens(line)
            if not tokens:
                return
            if tokens[0] == 'i':
                self._handle_interface(tokens)
            else:
                if tokens[0] == '.':
                    tokens = tokens[1:]
                self._handle_signal(tokens)
        except:
            print(line)
            raise

    def _handle_interface(self, tokens):
        if len(tokens) < 2:
            raise Exception("Invalid vdef %s"%str(tokens))
        iname = tokens[1]
        vfields = tokens[2:]
        if iname in self.interfaces:
            # it's fine to have multiple definitions, but they must
            # be consistent.
            current = self.interfaces[iname]
            if vfields != current:
                m = "inconsistent vdefs %s %s"%(
                    str(current),
                    str(vfields))
                raise Exception(m)
        else:
            self.interfaces[iname] = vfields
            self.cb_interface(iname, vfields)

    def _handle_signal(self, tokens):
        iname = tokens[0]
        if iname not in self.interfaces:
            raise Exception("no interface defined for %s"%iname)
        vfields = self.interfaces[iname]
        values = tokens[1:]
        if len(vfields) != len(values):
            raise Exception("wrong number of args. i %s %s. got %s"%(
                iname, str(vfields), str(values)))

        kwargs = {}
        for (idx, vfield) in enumerate(vfields):
            kwargs[vfield] = values[idx]

        self.cb_signal(iname, kwargs)


# --------------------------------------------------------
#   api
# --------------------------------------------------------
async def interface_script_parser_async_new(handler):
    isp = InterfaceScriptParserAsync()
    await isp.init(handler=handler)
    return isp

def interface_script_parser_sync_new(handler):
    isp = InterfaceScriptParserSync()
    isp.init(handler=handler)
    return isp

def interface_script_parse(data_i, handler):
    parser = interface_script_parser_sync_new(
        handler=handler)
    parser.parse(
        s=data_i)
