def distance(A, B, get_children, insert_cost, remove_cost, update_cost,
             return_operations=False):
    A, B = AnnotatedTree(A, get_children), AnnotatedTree(B, get_children)
    size_a = len(A.nodes)
    size_b = len(B.nodes)
    treedists = zeros((size_a, size_b), float)
    operations = [[[] for _ in range(size_b)] for _ in range(size_a)]

    def treedist(i, j):
        Al = A.lmds
        Bl = B.lmds
        An = A.nodes
        Bn = B.nodes

        m = i - Al[i] + 2
        n = j - Bl[j] + 2
        fd = zeros((m,n), float)
        partial_ops = [[[] for _ in range(n)] for _ in range(m)]

        ioff = Al[i] - 1
        joff = Bl[j] - 1

        for x in range(1, m):
            node = An[x+ioff]
            fd[x][0] = fd[x-1][0] + remove_cost(node)
            op = Operation(REMOVE, node)
            partial_ops[x][0] = partial_ops[x-1][0] + [op]
        for y in range(1, n):
            node = Bn[y+joff]
            fd[0][y] = fd[0][y-1] + insert_cost(node)
            op = Operation(INSERT, arg2=node)
            partial_ops[0][y] = partial_ops[0][y-1] + [op]

        for x in range(1, m):
            for y in range(1, n):
                node1 = An[x+ioff]
                node2 = Bn[y+joff]
                # only need to check if x is an ancestor of i
                # and y is an ancestor of j
                if Al[i] == Al[x+ioff] and Bl[j] == Bl[y+joff]:
                    costs = [fd[x-1][y] + remove_cost(node1),
                             fd[x][y-1] + insert_cost(node2),
                             fd[x-1][y-1] + update_cost(node1, node2)]
                    fd[x][y] = min(costs)
                    min_index = costs.index(fd[x][y])

                    if min_index == 0:
                        op = Operation(REMOVE, node1)
                        partial_ops[x][y] = partial_ops[x-1][y] + [op]
                    elif min_index == 1:
                        op = Operation(INSERT, arg2=node2)
                        partial_ops[x][y] = partial_ops[x][y - 1] + [op]
                    else:
                        op_type = MATCH if fd[x][y] == fd[x-1][y-1] else UPDATE
                        op = Operation(op_type, node1, node2)
                        partial_ops[x][y] = partial_ops[x - 1][y - 1] + [op]

                    operations[x + ioff][y + joff] = partial_ops[x][y]
                    treedists[x+ioff][y+joff] = fd[x][y]
                else:
                    p = Al[x+ioff]-1-ioff
                    q = Bl[y+joff]-1-joff
                    costs = [fd[x-1][y] + remove_cost(node1),
                             fd[x][y-1] + insert_cost(node2),
                             fd[p][q] + treedists[x+ioff][y+joff]]
                    fd[x][y] = min(costs)
                    min_index = costs.index(fd[x][y])
                    if min_index == 0:
                        op = Operation(REMOVE, node1)
                        partial_ops[x][y] = partial_ops[x-1][y] + [op]
                    elif min_index == 1:
                        op = Operation(INSERT, arg2=node2)
                        partial_ops[x][y] = partial_ops[x][y-1] + [op]
                    else:
                        partial_ops[x][y] = partial_ops[p][q] + \
                            operations[x+ioff][y+joff]

    for i in A.keyroots:
        for j in B.keyroots:
            treedist(i, j)

    if return_operations:
        return treedists[-1][-1], operations[-1][-1]
    else:
        return treedists[-1][-1]