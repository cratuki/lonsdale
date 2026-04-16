import difflib
import os
import time

def util_attach_log(ob):
    lst = []
    for c in ob.__class__.__name__:
        o = ord(c)
        if 65 <= o <= 90:
            # capitalise
            if lst: lst.append('_')
            lst.append(chr(o+32))
        else:
            lst.append(c)
    cname = ''.join(lst)
    def log(msg=''):
        ob.logger(f'[{cname}] {msg}')
    ob.log = log

def util_diff(str1, str2):
    """Return a diff of two strings using difflib"""
    d = difflib.Differ()
    diff = d.compare(str1.splitlines(), str2.splitlines())
    return '\n'.join(diff)

def util_font_stencil_print(stencil):
    for row in stencil:
        print(''.join(row))
    print()

def util_font_stencil_from_itch_io_json_format_unstable(d, width):
    #
    # Note that I am in the habit of hacking this function up for specific
    # font conversions. Hence "unstable". Do not use this function in codebase
    # code. It is intended only to assist converting sourced json fonts into
    # stencil format as I get them. Avoid lasting dependence on this function.
    #
    d_stencil = {}
    for (c, lst) in d.items():
        # Create an empty grid
        grid = []
        for i in range(len(lst)):
            grid.append(list('.'*width))
        # Apply the definition to our grid
        for (row_idx, n) in enumerate(lst):
            row = grid[row_idx]
            col_idx = 1
            def check(b):
                if n & b:
                    try:
                        row[col_idx] = 'w'
                    except:
                        print(c)
                        raise
            check(0b00000001); col_idx += 1;
            check(0b00000010); col_idx += 1;
            check(0b00000100); col_idx += 1;
            check(0b00001000); col_idx += 1;
            check(0b00010000); col_idx += 1;
            check(0b00100000); col_idx += 1;
            check(0b01000000); col_idx += 1;

        # get rid of the left-most column
        for (row_idx, n) in enumerate(lst):
            row = grid[row_idx]
            row.reverse()
            row.pop()
            row.reverse()
        d_stencil[c] = grid
    return d_stencil

def util_get_basedir():
    dir_wimbers = os.path.dirname(os.path.realpath(__file__))
    return os.path.dirname(dir_wimbers)

def util_hexdump(bb, start_addr=0x0, length=16):
    # Adapteed from, https://gist.github.com/sbz/1080258
    FILTER = ''.join([(len(repr(chr(x))) == 3) and chr(x) or '.' for x in range(256)])
    lines = []
    for c in range(0, len(bb), length):
        bb_win = bb[c:c+length]
        try:
            chars = bb_win.decode('utf8')
            hex = ' '.join(["%02x"%ord(x) for x in chars])
            printable = ''.join(["%s" % ((ord(x) <= 127 and FILTER[ord(x)]) or '.') for x in chars])
        except:
            hex = ' '.join(["%02x"%b for b in bb_win])
            printable = ''.join([".." for x in bb_win])
        lines.append("%04x  %-*s  %s" % (c+start_addr, length*3, hex, printable))
    return '\n'.join(lines)

def util_load(fname):
    with open(fname) as fp:
        data = fp.read()
    return data

def util_logger(m=''):
    print(m)

def util_read_file(path):
    with open(path) as fp:
        data = fp.read()
    return data

def util_time_logger(m=''):
    t = time.strftime('%Y%m%d %H%M%S')
    for line in m.split('\n'):
        print(f'{t} {line}')
    
