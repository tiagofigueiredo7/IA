from classes.Cidade import Cidade
from classes.Hora import Hora

# Algoritmo de Procura em Profundidade (DFS)
def DFS(cidade: Cidade, inicio, fim, path, visited):
    visited.add(inicio)
    if inicio == fim:
        path.append(inicio)
        return path
    
    for local,_ in cidade.get_vizinhos(inicio):
        if local not in visited and DFS(cidade, local, fim, path, visited):
            path.insert(0, inicio)
            cidade.add_to_cache(inicio,fim,path)
            return path
    return None


def DFS_tipo(cidade: Cidade, inicio, tipo, path, visited):
    visited.add(inicio)    
    if cidade.get_local(inicio).getTipo() == tipo:
        path.append(inicio)
        return path
    
    for local,_ in cidade.get_vizinhos(inicio):
        if local not in visited and DFS_tipo(cidade, local, tipo, path, visited):
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
                    cidade.add_to_cache(inicio,fim,path)
                    return path
                elif local not in queue:
                    queue.append(local)
    return None


def BFS_tipo(cidade: Cidade, inicio, tipo):
    if cidade.get_local(inicio).getTipo() == tipo:
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
                if cidade.get_local(local).getTipo() == tipo:
                    path = [local]
                    while local != inicio:
                        local = parents[local]
                        path.insert(0,local)
                    return path
                elif local not in queue:
                    queue.append(local)
    return None

# Algoritmo de Procura A*
def aStar(cidade: Cidade, inicio, fim, h: Hora): 
    queue = set()
    queue.add(inicio)
    visited = set()
    cost = {inicio : 0}
    parents={inicio: inicio}

    while len(queue) > 0:
        n = None
        for q in queue:
            if n == None or cost[q] + cidade.get_transito(q,h) < cost[n] + cidade.get_transito(n,h):
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

    if parents.get(fim) is not None:
        path = []
        n = fim

        while parents[n] != n:
            path.append(n)
            n = parents[n]

        path.append(inicio)
        path.reverse()
        cidade.add_to_cache(inicio,fim,path)
        return path
    return None


def aStar_tipo(cidade: Cidade, inicio, tipo, autonomia, h: Hora):
    queue = set()
    queue.add(inicio)
    visited = set()
    cost = {inicio : 0}
    parents = {inicio: inicio}

    while len(queue) > 0:
        n = None

        for q in queue:
            if n is None or cost[q] + cidade.get_transito(q,h) < cost[n] + cidade.get_transito(n,h):
                n = q

        if cidade.get_local(n).getTipo() == tipo and cost[n] <= autonomia:
            path = []
            curr = n
            while parents[curr] != curr:
                path.append(curr)
                curr = parents[curr]
            path.append(inicio)
            path.reverse()
            return path

        queue.remove(n)
        visited.add(n)

        for v, d in cidade.get_vizinhos(n):
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

    return None

# Algoritmo de Procura Gulosa (Greedy)
def greedy(cidade: Cidade, inicio, fim, h: Hora): 
    queue = set()
    queue.add(inicio)
    visited = set()
    parents={inicio: inicio}

    while len(queue) > 0:
        n = None
        for q in queue:
            if n == None or cidade.get_transito(q,h) < cidade.get_transito(n,h):
                n = q 
        
        queue.remove(n)
        visited.add(n)
        
        for v,_ in cidade.get_vizinhos(n):
            if v not in queue and v not in visited:
                queue.add(v)
                parents[v] = n

    if parents.get(fim) is not None:
        path = []
        n = fim

        while parents[n] != n:
            path.append(n)
            n = parents[n]

        path.append(inicio)
        path.reverse()
        cidade.add_to_cache(inicio,fim,path)
        return path
    return None


def greedy_tipo(cidade: Cidade, inicio, tipo, h: Hora):
    queue = set()
    queue.add(inicio)
    visited = set()
    parents = {inicio: inicio}

    while len(queue) > 0:
        n = None

        for q in queue:
            if n is None or cidade.get_transito(q,h) < cidade.get_transito(n,h):
                n = q

        if cidade.get_local(n).getTipo() == tipo:
            path = []
            curr = n
            while parents[curr] != curr:
                path.append(curr)
                curr = parents[curr]
            path.append(inicio)
            path.reverse()
            return path

        queue.remove(n)
        visited.add(n)

        for v, _ in cidade.get_vizinhos(n):
            if v not in queue and v not in visited:
                queue.add(v)
                parents[v] = n

    return None