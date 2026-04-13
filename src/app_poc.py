from .interface_script import interface_script_parse
from .util import util_attach_log
from .util import util_get_basedir
from .util import util_read_file
from .util import util_time_logger as logger

import os
import sys

BASEDIR = util_get_basedir()

DIR_DESIGN = os.path.join(BASEDIR, 'design')


class Design:

    def __init__(self, logger):
        self.logger = logger

        util_attach_log(self)


class Site:

    def __init__(self):
        xxx


class DesignIHandler:

    def __init__(self, logger):
        self.logger = logger

        util_attach_log(self)

        self.design = Design(
            logger=self.logger)

        self.active_site = None

    def on_resource(self, resource_h, mime_type, path):
        xxx

    def on_load(self, load_h):
        xxx

    def on_connection_standard(self, cs_h):
        xxx

    def on_connection_bridge(self, cs_h_a, cs_h_b):
        xxx

    def on_type_qual(self, k, v):
        xxx

    def on_type_port(self, tport_h):
        xxx

    def on_type_create(self, type_h):
        xxx

    def on_rqual(self, k, v):
        xxx

    def on_rneed(self, node_type_h):
        xxx

    def on_rsend(self, node_type_h):
        xxx

    def on_recipe(self, recipe_h):
        xxx

    def on_site(self, site_h):
        xxx

    def on_qual(self, k, v):
        xxx

    def on_port(self, port_h, cs_h, load_h):
        xxx

    def on_node(self, node_h, node_type_h):
        xxx

    def on_to(self, port_h):
        '''
        Links the port that is currently in scope to this other port.
        '''
        xxx

    def on_credit(self, site_h, node_h):
        xxx

    def on_debit(self, site_h, node_h):
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

    def on_check_build(self, our_node_h, design_i, design_site_h, design_node_h):
        '''
        Compare the graph of the item in node_h in the scope of the current
        site to design_i/design_site_h/design_node_h.

        It will start out by comparing that the type of the two things are
        equivalent. Then, it will recursively follow the graph of all the
        things that connect to the nodes to check that there relations are
        equivalent. It has an internal cache to avoid getting lost in cycles.
        '''
        xxx

    def on_site_x(self):
        xxx

    def on_cing(self, node_h):
        xxx

    def on_cout(self, type_h, node_h):
        xxx

    def on_cook(self, loc_h, recipe_h):
        xxx


class Folio:

    def __init__(self):
        self.lst_design = []

    def add_design(self, design):
        assert type(design) == Design
        self.lst_design.append(design)

    def __repr__(self):
        return '[Folio.__repr__]'


def main():
    if len(sys.argv) == 1:
        lst_design_filename = os.listdir(DIR_DESIGN)
    else:
        lst_design_filename = sys.argv[1:]

    folio = Folio()

    for fname in lst_design_filename:
        if fname.startswith('.'): continue
        path_design = os.path.join(DIR_DESIGN, fname)
        if not os.path.exists(path_design):
            raise Exception(f'No design file {path_design}')

        data_i= util_read_file(path_design)
        handler = DesignIHandler(
            logger=logger)
        interface_script_parse(
            data_i=data_i,
            handler=handler)

        folio.add_design(
            design=handler.design)

    interface_script_parse(
        data_i=data_i,
        handler=handler)

    print(folio)

if __name__ == '__main__':
    main()
