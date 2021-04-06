
class Graph:
    class Node:
        def __init__(self, n=''):
            self.name = n
            self.edges = list()

        def to_string(self):
            strepr = self.name
            strepr += ' [ '
            strepr += ', '.join([e.name for e in self.edges])
            strepr += ' ] '
            return strepr

    def __init__(self):
        self.nodes = dict()

    def assert_node(self, n):
        if n not in self.nodes.keys():
            raise Exception(f'No node named {n}')

    def add_node(self, name):
        if self.nodes and name in self.nodes.keys():
            return
        self.nodes[name] = Graph.Node(name)

    def add_edge(self, from_n, to_n):
        self.assert_node(from_n)
        self.assert_node(to_n)
        from_node = self.nodes[from_n]
        to_node = self.nodes[to_n]
        from_node.edges.append(to_node)

    def depth_first_traverse(self, n):
        root = self.nodes[n]

        self.depth_first_low(root, list())
        return

    def depth_first_low(self, node, visited):
        print(node.name)
        visited.append(node.name)
        for e in node.edges:
            if e.name not in visited:
                self.depth_first_low(e, visited)
        return

    def breadth_first_traverse(self, n):
        root = self.nodes[n]
        self.breadth_first_low([root], list())
        return

    def breadth_first_low(self, to_visit: list, visited: list):
        if len(to_visit) == 0:
            return
        root = to_visit.pop(0)
        print(root.name)
        visited.append(root.name)
        for e in root.edges:
            if e.name not in visited:
                to_visit.append(e)
        self.breadth_first_low(to_visit, visited)
        return

    def has_cycle(self):
        all_nodes = list()
        [all_nodes.add(e) for e in self.nodes]
        visited, visiting = set(), set()
        while all_nodes:
            current = all_nodes[0]
            if self.has_cycle(current, all_nodes, visiting, visited):
                return True
        return False

    def has_cycle(self, node, all_nodes, visiting, visited):
        all_nodes.remove(node)
        visiting.add(node.name)
        for n in node.edges:
            if n.name in visited:
                continue
            if n.name in visiting:
                return True
            if self.has_cycle(n, all_nodes, visiting, visited):
                return True
        visiting.remove(node.name)
        visited.add(node.name)
        return False

    def __str__(self):
        strepr = ''
        for k, v in self.nodes.items():
            strepr += v.to_string() + '\n'
        return strepr

    @classmethod
    def graph_test(cls):
        g = Graph()
        g.add_node('a')
        g.add_node('b')
        g.add_node('c')
        g.add_node('d')
        g.add_edge('a', 'b')
        g.add_edge('a', 'c')
        g.add_edge('b', 'd')
        g.add_edge('d', 'c')
        # print(g.to_string())
        g.breadth_first_traverse('a')
        return

    @classmethod
    def graph_test_1(cls):
        g = Graph()
        [g.add_node(n) for n in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']]
        [g.add_edge('a', a) for a in ['b', 'c', 'd']]
        [g.add_edge('c', a) for a in ['e', 'f']]
        [g.add_edge('b', a) for a in ['g']]
        [g.add_edge('e', a) for a in ['h', 'i']]
        [g.add_edge('i', a) for a in ['j']]
        print(str(g))
        g.depth_first_traverse('a')


Graph.graph_test_1()

