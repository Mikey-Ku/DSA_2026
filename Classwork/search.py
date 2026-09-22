def bfs(graph, start_node):
    visited = set()
    queue = [start_node]
    visited.add(start_node)

    while queue:
        current = queue.pop(0)
        print(current, end=" ")

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return visited



def dfs(graph, start_node):
    visited = set()
    stack = [start_node]
    visited.add(start_node)

    while stack:
        current = stack.pop()
        print(current, end=" ")

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)

    return visited
