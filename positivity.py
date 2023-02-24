import numpy as np
import networkx as nx


def create_causal_graph():
    G = nx.DiGraph()
    G.add_node(0, name="entry")
    G.add_node(1, name="create A")
    G.add_node(2, name="edit A")
    G.add_node(3, name="delete A")
    G.add_node(4, name="create B")
    G.add_node(5, name="edit B")
    G.add_node(6, name="delete B")
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(0, 4)
    G.add_edge(4, 5)
    G.add_edge(4, 6)
    # subax = plt.subplot(121)
    # nx.draw(G, with_labels=True, font_weight='bold')
    # plt.show()
    return G


def confounder_selection():
    cg = create_causal_graph()
    num_t = 10
    num_m = len(cg.nodes)
    w = weak_positivity_validation(num_t, num_m)
    confounder_set_list = dict()
    for i in range(num_m):
        visited = [False] * num_m
        visited[i] = True
        confounder_set = []
        initial_set = cg.pred[i]
        stack = list(initial_set)
        while len(stack) != 0:
            j = stack.pop()
            if not visited[j]:
                visited[j] = True
                if w[i, j]:
                    confounder_set.append(j)
                else:
                    for n in cg.pred[j]:
                        stack.append(n)
        confounder_set_list[i] = confounder_set
    print(confounder_set_list)


def weak_positivity_validation(num_t, num_m):
    """
    :param num_t: the number of test cases
    :param num_m: the number of methods
    :return: weak positivity table
    """

    method_coverage_table = np.random.randint(0, 2, (num_m, num_t))
    weak_positivity_table = np.zeros((num_m, num_m))

    for i in range(num_m):
        for j in range(i + 1, num_m):
            flag = False
            p11 = False
            p10 = False
            p01 = False
            p00 = False
            for k in range(num_t):
                if method_coverage_table[i, k] == 1 and method_coverage_table[j, k] == 1:
                    p11 = True
                if method_coverage_table[i, k] == 1 and method_coverage_table[j, k] == 0:
                    p10 = True
                if method_coverage_table[i, k] == 0 and method_coverage_table[j, k] == 1:
                    p01 = True
                if method_coverage_table[i, k] == 0 and method_coverage_table[j, k] == 0:
                    p00 = True
                if p11 and p10 and p01 and p00:
                    flag = True
                    break
            weak_positivity_table[i, j] = flag
            weak_positivity_table[j, i] = flag
    return weak_positivity_table


if __name__ == '__main__':
    confounder_selection()
    # print(w)
    # g = CausalGraph()
