from .interface_script import interface_script_parse
from .util import util_attach_log
from .util import util_get_basedir
from .util import util_read_file
from .util import util_time_logger as logger

import os
import sys
from types import SimpleNamespace as Ns

BASEDIR = util_get_basedir()

DIR_DESIGN = os.path.join(BASEDIR, 'design')

class Load:
    '''
    Represents what is transmitted through a link between ports. Some examples:
    power_12v, oil, torque_to_150nm.
    '''

    def __init__(self, load_h):
        self.load_h = load_h


class Qual:
    '''
    A quality that can be attached to a node.
    '''

    def __init__(self, k, v):
        self.k = k
        self.v = v


class Site:

    def __init__(self, site_h):
        self.site_h = site_h

        self.d_node = {}


class Node:

    def __init__(self, node_h):
        self.node_h = node_h

        self.d_port = {}

    def add_qual(self, k, v):
        if k in self.d_tqual:
            raise Exception(f'Dupe tqual for key {k}')
        self.d_tqual = Tqual(k=k, v=v)

    def add_port(self, port_h, cs_h, load_h):
        if port_h in self.d_port:
            raise Exception(f'Dupe port for key {k}')
        ns_port = Ns()
        ns_port.cs_h = cs_h
        ns_port.load_h = load_h
        self.d_port[port_h] = ns_port


class Plan:

    def __init__(self, plan_h, floor_site_h):
        self.plan_h = plan_h
        self.floor_site_h = floor_site_h
            # This is the 'floor' site_h, and is relevant within
            # plan scopes. When the user specifies the default through
            # use of a period, it will use this site.


class Design:

    def __init__(self, logger, dir_design, design_h):
        self.logger = logger
        self.dir_design = dir_design
        self.design_h = design_h

        util_attach_log(self)

        self.d_cs = {}
        self.d_compat = {}
        self.d_load = {}
        self.d_site = {}
        self.d_plan = {}

    def add_compat(self, x_cs_h, y_cs_h):
        # xxx do an alphabetical order test here to make sure that x is
        # less-than-or-equal-to y in alphabetical ordering. Throw an exception
        # if they are not.

        for cs_h in (x_cs_h, y_cs_h):
            if cs_h not in self.d_cs:
                raise Exception(f'Unknown connection-standard {cs_h}')
        del cs_h

        def ensure(cs_h):
            if cs_h not in self.d_compat:
                self.d_compat[cs_h] = set()

        ensure(x_cs_h)
        self.d_compat[x_cs_h].add(y_cs_h)

        ensure(y_cs_h)
        self.d_compat[y_cs_h].add(x_cs_h)


class DesignIHandler:

    def __init__(self, logger, dir_design, design_h):
        self.logger = logger
        self.dir_design = dir_design
        self.design_h = design_h

        util_attach_log(self)

        self.design = Design(
            logger=self.logger,
            dir_design=self.dir_design,
            design_h=design_h)

        self.active_site = None
        self.active_node = None
        self.active_plan = None

    def on_include(self, relpath):
        '''
        Use the current handler to parse another file that is within the same
        directory.
        '''
        xxx

    def on_resource(self, resource_h, mime_type, path):
        xxx

    def on_cs(self, cs_h):
        if not cs_h.startswith('cs_'):
            raise Exception("Connection standard names must start cs_")

        ns_cs = Ns()
        self.design.d_cs[cs_h] = ns_cs

    def on_compat(self, x_cs_h, y_cs_h):
        self.design.add_compat(
            x_cs_h=x_cs_h,
            y_cs_h=y_cs_h)

    def on_load(self, load_h):
        load = Load(
            load_h=load_h)
        self.design.d_load[load_h] = load

    def on_ps(self, ps_h, manufacturer, code, description):
        '''
        Part specification.
        '''
        xxx

    def on_site(self, site_h):
        if self.active_site != None:
            raise Exception('You cannot nest sites.')
        if site_h in self.design.d_site:
            raise Exception(f'Dupe site {site_h}')

        site = Site(
            site_h=site_h)
        self.design.d_site[site_h] = site
        self.active_site = site

    def on_node(self, node_h):
        if self.active_site == None:
            raise Exception('Nodes must be defined within sites.')
        if self.active_node != None:
            raise Exception('You cannot nest nodes.')

        node = Node(
            node_h=node_h)
        self.active_site.d_node[node_h] = node
        self.active_node = node

    def on_qual(self, k, v):
        if self.active_node == None:
            raise Exception('Message qual is only valid within a node scope')
        if k in self.active_node.d_qual:
            raise Exception(f'Dupe qual {k}')
        self.active_node.add_tqual(
            k=k,
            v=v)

    def on_port(self, port_h, cs_h, load_h):
        if self.active_node == None:
            raise Exception('Message port is only valid within a node scope')
        if port_h in self.active_node.d_port:
            raise Exception(f'Dupe port_h {port_h}')
        if cs_h not in self.design.d_cs:
            raise Exception(f'Unknown connection standard (cs) {cs_h}')

        self.active_node.add_port(
            port_h=port_h,
            cs_h=cs_h,
            load_h=load_h)

    def on_to(self, portref):
        '''
        Links the port that is currently in scope to this other port.
        '''
        xxx

    def on_node_x(self):
        if self.active_node == None:
            raise Exception('There is no node scope open.')

        self.active_node = None

    def on_site_x(self):
        if self.active_site == None:
            raise Exception('There is no site scope open.')
        if self.active_node != None:
            raise Exception('There is a node scope that is not closed.')

        self.active_site = None

    def on_plan(self, plan_h, floor_site_h):
        print(f'xxx plan {plan_h}')

        if self.active_plan != None:
            raise Exception('Plans cannot be nested')
        if plan_h in self.design.d_plan:
            raise Exception(f'Dupe plan_h {plan_h}')

        plan = Plan(
            plan_h=plan_h,
            floor_site_h=floor_site_h)
        self.design.d_plan[plan_h] = plan
        self.active_plan = plan

    def on_move(self, src_siteref, node_h, dst_site_h):
        xxx

    def on_mall(self, src_siteref, node_h, dst_site_h):
        xxx

    def on_set_load(self, portref, load_h):
        """
        Modify a qual against a node
        """
        xxx

    def on_set_qual(self, noderef, k, v):
        """
        Modify a qual against a node
        """
        xxx

    def on_link(self, x_portref, y_portref):
        xxx

    def on_unlink(self, x_portref, y_portref):
        xxx

    def on_check_free(self, node_h):
        '''
        Check that a node is not linked.
        '''
        xxx

    def on_check_flush(self, node_h):
        '''
        Check that a node is fully-connected.
        '''
        xxx

    def on_check_here(self, node_h):
        '''
        Assert that a part is in the current site.
        '''
        xxx

    def on_check_empty(self):
        '''
        Assert that the current site is empty. This can be useful to do this
        once you have tranferred all the goods out to other sites, the confirm
        you have nothing left.
        '''
        xxx

    def on_check_build(self, noderef, design_i, design_site_h, design_node_h):
        '''
        Compare the graph of the item in node_h in the scope of the current
        site to design_i/design_site_h/design_node_h.

        This will start out by comparing that the type of the two things are
        equivalent. Then, it will recursively follow the graph of all the
        things that connect to the nodes to check that there relations are
        equivalent. It has an internal cache to avoid getting lost in cycles.

        This should not only output true-or-false. It should make a reasonable
        effort to capture the places where the graphs are inconsistent, and to
        present this information to the user that ran the program.
        '''
        xxx

    def on_plan_x(self):
        self.active_plan = None


class Folio:

    def __init__(self):
        self.lst_design = []

    def add_design(self, design):
        assert type(design) == Design
        self.lst_design.append(design)

    def __repr__(self):
        sb = ['Folio {']
        for design in self.lst_design:
            sb.append(f'    {design.design_h}')
        sb.append('}')
        return '\n'.join(sb)


def main():
    if len(sys.argv) == 1:
        lst_design_filename = os.listdir(DIR_DESIGN)
    else:
        lst_design_filename = sys.argv[1:]

    folio = Folio()

    for fname in lst_design_filename:
        if fname.startswith('.'): continue

        print(f'// {fname}')

        path_design = os.path.join(DIR_DESIGN, fname)
        if not os.path.exists(path_design):
            raise Exception(f'No design file {path_design}')

        if fname.endswith('.design_i'):
            design_h = '.'.join(fname.split('.')[:-1])
        else:
            design_h = fname

        data_i= util_read_file(path_design)
        handler = DesignIHandler(
            logger=logger,
            dir_design=DIR_DESIGN,
            design_h=design_h)
        interface_script_parse(
            data_i=data_i,
            handler=handler)

        folio.add_design(
            design=handler.design)

    # xxx
    print()
    print()
    print()
    print(folio)

if __name__ == '__main__':
    main()
