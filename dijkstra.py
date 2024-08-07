import heapq

def dijkstra_path(graph, start, end):
    n = len(graph)
    distances = [float('inf')] * n
    previous_nodes = [None] * n
    distances[start] = 0
    priority_queue = [(0, start)]  # (distância, vértice)
    
    while priority_queue:
        current_distance, u = heapq.heappop(priority_queue)
        
        if u == end:
            break
        
        if current_distance > distances[u]:
            continue
        
        for v, weight in enumerate(graph[u]):
            if weight > 0:  # Verifica se há uma aresta
                distance = current_distance + weight
                if distance < distances[v]:
                    distances[v] = distance
                    previous_nodes[v] = u
                    heapq.heappush(priority_queue, (distance, v))
    
    # Reconstruir o caminho
    path = []
    if distances[end] < float('inf'):
        while end is not None:
            path.append(end)
            end = previous_nodes[end]
        path.reverse()
    
    return distances[path[-1]], path if path else (float('inf'), [])

