#! -*- coding: utf-8 -*-
"""
Simple digraph implementation
"""


class Digraph(object):

    def __init__(self):
        self._nodes = set()
        self._edges = {}
        self._node_options = {}

    def add_node(self, node, **kwargs):
        self._nodes.add(node)
        self._node_options[node] = kwargs

    def add_nodes(self, *nodes):
        for node in nodes: self.add_node(node)

    def nodes(self):
        return self._nodes

    def add_edge(self, src, dst):
        if src not in self._edges:
            self._edges[src] = set()
        self._edges[src].add(dst)

    def add_edges(self, *edges):
        for src, dst in edges: self.add_edge(src, dst)

    def edges(self):
        ret = set()
        for src, dst_set in self._edges.iteritems():
            for dst in dst_set:
                ret.add( (src, dst) )
        return ret

    def incidents(self, node):
        return self._edges.get(node, set())

    def node_options(self, node):
        return self._node_options[node]


def accessibility(graph):
    access = {}
    for node in graph.nodes():
        incheck = set([node,]) # nodes which are currently in check
        accessible = set([node,]) # set of accessible nodes
        def _check_access(element):
            """ get a list of accessible nodes, exclude the node itself """
            incheck.add(element)
            if element in access:
                return access[element]
            # else check recursively
            ret = graph.incidents(element).copy()
            for i in graph.incidents(element):
                if i not in incheck:
                    ret.update(_check_access(i))
            return ret
        accessible.update(_check_access(node))
        access[node] = accessible
    return access
