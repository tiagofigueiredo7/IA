from classes.Cidade import Cidade

# Algoritmo de Procura em Profundidade (DFS)
def DFS(cidade: Cidade, inicio, fim, path, visited):
    visited.add(inicio)
    if inicio == fim:
        path.append(inicio)
        return path
    
    for local,_ in cidade.get_vizinhos(inicio):
        if local not in visited and DFS(cidade, local, fim, path, visited):
            path.insert(0, inicio)
            return path
    return None


# Algoritmo de Procura em Largura (BFS)
def BFS(cidade: Cidade, inicio, fim):
    if inicio == fim:
        return [inicio]
    
    visitados = set()
    visitados.add(inicio)
    queue = [inicio]
    parents = {}

    for n in queue:
        for local,_ in cidade.get_vizinhos(n):
            if local not in visitados:
                visitados.add(local)
                parents[local] = n
                if local == fim:
                    path = [local]
                    while local != inicio:
                        local = parents[local]
                        path.insert(0,local)
                    return path
                elif local not in queue:
                    queue.append(local)
    print("não encontrei!!!")
    return None


# Algoritmo de Procura A*
def aStar(cidade: Cidade, start, end): 
    queue = set()
    queue.add(start)
    visited = set()
    cost = {start : 0}
    parents={start: start}

    while len(queue) > 0:
        n = None
        for q in queue:
            if n == None or cost[q] + cidade.get_transito(q) < cost[n] + cidade.get_transito(n):
                n = q 
        
        queue.remove(n)
        visited.add(n)
        
        for v,d in cidade.get_vizinhos(n):
            if v not in queue and v not in visited:
                queue.add(v)
                parents[v] = n
                cost[v] = cost[n] + d
            
            elif cost[v] > cost[n] + d:
                parents[v] = n
                cost[v] = cost[n] + d

                if v in visited: 
                    visited.remove(v)
                    queue.add(v)

    if parents.get(end) is not None:
        path = []
        n = end

        while parents[n] != n:
            path.append(n)
            n = parents[n]

        path.append(start)
        path.reverse()
        return path
    return None


# Algoritmo de Procura Gulosa (Greedy)
def greedy(cidade: Cidade, start, end): 
    queue = set()
    queue.add(start)
    visited = set()
    parents={start: start}

    while len(queue) > 0:
        n = None
        for q in queue:
            if n == None or cidade.get_transito(q) < cidade.get_transito(n):
                n = q 
        
        queue.remove(n)
        visited.add(n)
        
        for v,_ in cidade.get_vizinhos(n):
            if v not in queue and v not in visited:
                queue.add(v)
                parents[v] = n

    if parents.get(end) is not None:
        path = []
        n = end

        while parents[n] != n:
            path.append(n)
            n = parents[n]

        path.append(start)
        path.reverse()
        return path
    return None


## adicionar mais?