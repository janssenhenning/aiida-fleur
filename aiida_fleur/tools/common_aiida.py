# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c), Forschungszentrum Jülich GmbH, IAS-1/PGI-1, Germany.         #
#                All rights reserved.                                         #
# This file is part of the AiiDA-FLEUR package.                               #
#                                                                             #
# The code is hosted on GitHub at https://github.com/JuDFTteam/aiida-fleur    #
# For further information on the license, see the LICENSE.txt file            #
# For further information please visit http://www.flapw.de or                 #
# http://aiida-fleur.readthedocs.io/en/develop/                               #
###############################################################################
"""
In here we put all things util (methods, code snipets) that are often useful, but not yet in AiiDA
itself.
So far it contains:

export_extras
import_extras
delete_nodes (FIXME)
delete_trash (FIXME)
create_group

"""
# TODO import, export of descriptions, and labels...?
from __future__ import absolute_import
from __future__ import print_function
import json
import six
from six.moves import input as input_six

from aiida.orm import load_node
from aiida.orm.querybuilder import QueryBuilder
from aiida.orm import Group, Node
from aiida.common.exceptions import NotExistent


def export_extras(nodes, filename='node_extras.txt'):
    """
    Writes uuids and extras of given nodes to a json-file.
    This is useful for import/export because currently extras are lost.
    Therefore this can be used to save and restore the extras via
    :func:`~aiida_fleur.tools.common_aiida.import_extras`.

    :param: nodes: list of AiiDA nodes, pks, or uuids
    :param: filename, string where to store the file and its name

    example use:
    .. code-block:: python

        node_list = [120,121,123,46]
        export_extras(node_list)

    """

    outdict = {}
    for node in nodes:
        if not isinstance(node, Node):  # pk or uuid
            node = load_node(node)

        uuid = node.uuid
        extras_dict = node.extras
        outdict[uuid] = extras_dict

    json.dump(outdict, open(filename, 'w'), sort_keys=True, indent=4, separators=(',', ': '))


def import_extras(filename):
    """
    Reads in node uuids and extras from a file (most probably generated by
    :func:`~aiida_fleur.tools.common_aiida.export_extras`) and applies them to nodes in the DB.

    This is useful for import/export because currently extras are lost.
    Therefore this can be used to save and restore the extras on the nodes.

    :param: filename, string what file to read from (has to be json format)

    example use:
    import_extras('node_extras.txt')
    """

    all_extras = {}

    try:
        all_extras = json.load(open(filename))
    except json.JSONDecodeError:
        print('The file has to be loadable by json. i.e json format (which it is not).')

    for uuid, extras in six.iteritems(all_extras):

        try:
            node = load_node(uuid)
        except NotExistent:
            # Does not exists
            print(('node with uuid {} does not exist in DB'.format(uuid)))
            node = None
            continue
        if isinstance(node, Node):
            node.set_extra_many(extras)
        else:
            print('node is not instance of an AiiDA node')
        #print(extras)


'''
# uncommented this, since it is for sure out of date and dangerous to use
# for current version see aiida-core docs
def delete_nodes(pks_to_delete):
    """
    Delete a set of nodes. (From AiiDA cockbook)
    Note: TODO this has to be improved for workchain removal. (checkpoints and co)
    Also you will be backchecked.

    BE VERY CAREFUL!

    .. note::

        The script will also delete
        all children calculations generated from the specified nodes.

    :params pks_to_delete: a list of the PKs of the nodes to delete
    """
    # TODO: CHECK IF THIS IS UP TO DATE!
    from django.db import transaction
    from django.db.models import Q
    from aiida.backends.djsite.db import models

    # Delete also all children of the given calculations
    # Here I get a set of all pks to actually delete, including
    # all children nodes.
    all_pks_to_delete = set(pks_to_delete)
    for pk in pks_to_delete:
        all_pks_to_delete.update(
            models.DbNode.objects.filter(input_links__in=pks_to_delete).values_list('pk', flat=True))

    print(('I am going to delete {} nodes, including ALL THE CHILDREN'
           'of the nodes you specified. Do you want to continue? [y/N]'
           ''.format(len(all_pks_to_delete))))
    answer = input_six()

    if answer.strip().lower() == 'y':
        # Recover the list of folders to delete before actually deleting
        # the nodes.  I will delete the folders only later, so that if
        # there is a problem during the deletion of the nodes in
        # the DB, I don't delete the folders

        # There seem to be no folders in AiiDA 1.0
        #folders = [load_node(pk).folder for pk in all_pks_to_delete]

        with transaction.atomic():
            # Delete all links pointing to or from a given node
            models.DbLink.objects.filter(Q(input__in=all_pks_to_delete) | Q(output__in=all_pks_to_delete)).delete()
            # now delete nodes
            models.DbNode.objects.filter(pk__in=all_pks_to_delete).delete()

        # If we are here, we managed to delete the entries from the DB.
        # I can now delete the folders

        # There seem to be no folders in AiiDA 1.0
        # for f in folders:
        #     f.erase()


def delete_trash():
    """
    This method deletes all AiiDA nodes in the DB, which have a extra trash=True
    And all their children. Could be advanced to a garbage collector.

    Be careful to use it.
    """

    #query db for marked trash
    q = QueryBuilder()
    nodes_to_delete_pks = []

    q.append(Node, filters={'extras.trash': {'==': True}})

    res = q.all()
    for node in res:
        nodes_to_delete_pks.append(node[0].pk)
        print(('pk {}, extras {}'.format(node[0].pk, node[0].extras)))

    #Delete the trash nodes

    print(('deleting nodes {}'.format(nodes_to_delete_pks)))
    delete_nodes(nodes_to_delete_pks)

    return
'''


def create_group(name, nodes, description=None, add_if_exist=False):
    """
    Creates a group for a given node list.

    So far this is only an AiiDA verdi command.

    :params name: string name for the group
    :params nodes: list of AiiDA nodes, pks, or uuids
    :params description: optional string that will be stored as description for the group

    :returns: the group, AiiDa group

    Usage example:

    .. code-block:: python

        group_name = 'delta_structures_gustav'
        nodes_to_group_pks =[2142, 2084]
        create_group(group_name, nodes_to_group_pks,
                     description='delta structures added by hand. from Gustavs inpgen files')

    """
    #from aiida.common import NotExistent

    group, created = Group.objects.get_or_create(label=name)
    if created:
        print(('Group created with PK={} and name {}'.format(group.pk, group.label)))
    else:
        print(('Group with name {} and pk {} already exists.' ''.format(group.label, group.pk)))

        if add_if_exist:
            print('Adding nodes to the existing group {}'.format(group.label))
        else:
            print('Nodes were not added to the existing group {}'.format(group.label))
            return

    nodes2 = []
    for node in nodes:
        if not isinstance(node, Node):
            try:
                node = load_node(node)
            except NotExistent:
                print('Skipping {}, it does not exist in the DB'.format(node))
                continue
        nodes2.append(node)

    group.add_nodes(nodes2)
    print(('added nodes: {} to group {} {}'.format([x.pk for x in nodes2], group.label, group.pk)))

    if description:
        group.description = description

    return group


def get_nodes_from_group(group, return_format='uuid'):
    """
    Returns a list of pk or uuid of a nodes in a given group. Since 1.1.0, this function does
    not load a group using the label or any other identification. Use Group.objects.get(filter=ID) to
    pre-load this, available filters are: id, uuid, label, type_string, time, description, user_id.
    """

    if return_format == 'uuid':
        return [x.uuid for x in group.nodes]
    if return_format == 'pk':
        return [x.pk for x in group.nodes]
    else:
        raise ValueError("return_format should be 'uuid' or 'pk'.")
