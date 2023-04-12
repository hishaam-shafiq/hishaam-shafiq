import heapq

#need to take into consideration time driving to pickup another load thats in another city. to account for this we 
#would just add nodes with zero profit and infinity time before with time between as well
def find_most_profitable_path(cities, edges, start_city, end_city, max_time):
    # Create an empty graph with cities as keys and empty lists as values
    graph = {city: [] for city in cities}
    
    # Add edges to the graph
    for city1, city2, profit, time, max_allowed_time in edges:
        graph[city1].append((city2, profit, time, max_allowed_time))
    
    # Call the modified Dijkstra's algorithm and get the most profitable path
    profit, time, path = dijkstra_modified(graph, start_city, end_city, max_time)
    
    return profit, time, path

def dijkstra_modified(graph, start, end, max_time):
    # Initialize a max_heap with the start city, 0 profit, and 0 time
    max_heap = [(-0, 0, start, [])]  # max_heap (negated profit, time, city, path)
    
    # Initialize the variable to store the most profitable path, time, and profit
    max_profit_path = (0, None, [])  # Store max profit path (profit, time, path)

    # Continue processing the heap until it is empty
    while max_heap:
        # Pop the path with the highest (negated) profit from the max_heap
        neg_profit, time, current_city, path = heapq.heappop(max_heap)
        
        # Get the actual profit by negating the neg_profit
        profit = -neg_profit

        # Check if the current_city is the end city
        if current_city == end:
            # If the current profit is greater than the max profit, update the max_profit_path
            if profit > max_profit_path[0]:
                max_profit_path = (profit, time, path + [current_city])

        # Iterate through the neighbors of the current city
        for neighbor, profit_edge, time_edge, max_allowed_time in graph[current_city]:
            # Check if the current time is within the allowed start limit for the path
            if time <= max_allowed_time:
                # If adding the neighbor's time doesn't exceed max_time, process this path
                new_time = time + time_edge
                
                # Add 8 to the new_time every time it goes up by 16 or more
                new_time += 8 if new_time // 16 > time // 16 else 0

                if new_time <= max_time:
                    new_profit = profit + profit_edge
                    new_path = path + [current_city]
                    
                    # Push the new path onto the max_heap with the profit negated
                    heapq.heappush(max_heap, (-new_profit, new_time, neighbor, new_path))

    # If no valid path is found, return 0 profit and a message indicating no path was found
    if max_profit_path[0] == 0:
        return 0, None, "No valid path found within the maximum time constraint."
    
    # Return the most profitable path, time, and profit
    return max_profit_path

cities = ["A", "B", "C", "D"]
edges = [
    ("A", "B", 10, 4, 8),
    ("A", "C", 5, 2, 3),
    ("B", "D", 20, 6, 12),
    ("C", "D", 15, 4, 5)
]
start_city = "A"
end_city = "D"
max_time = 12

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 30, 10, ['A', 'B', 'D']

cities = ["A", "B", "C", "D", "E"]
edges = [
    ("A", "B", 5, 2, 5),
    ("A", "C", 10, 4, 6),
    ("B", "D", 20, 8, 10),
    ("C", "D", 15, 6, 8),
    ("D", "E", 10, 4, 6),
    ("C", "E", 25, 8, 12)
]
start_city = "A"
end_city = "E"
max_time = 20

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 35, 18, ['A', 'C', 'E']

cities = ["A", "B", "C", "D", "E", "F"]
edges = [
    ("A", "B", 5, 2, 5),
    ("A", "C", 10, 4, 6),
    ("B", "D", 20, 8, 10),
    ("C", "D", 15, 6, 8),
    ("D", "E", 10, 4, 6),
    ("C", "E", 25, 8, 12),
    ("E", "F", 15, 4, 5)
]
start_city = "A"
end_city = "F"
max_time = 25

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 50, 22, ['A', 'C', 'E', 'F']


cities = ["A", "B", "C", "D", "E", "F", "G"]
edges = [
    ("A", "B", 5, 2, 5),
    ("A", "C", 10, 4, 6),
    ("B", "D", 20, 8, 10),
    ("C", "D", 15, 6, 8),
    ("D", "E", 10, 4, 6),
    ("C", "E", 25, 8, 12),
    ("E", "F", 15, 4, 20),
    ("F", "G", 5, 2, 30)
]
start_city = "A"
end_city = "G"
max_time = 30

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 55, 24, ['A', 'C', 'E', 'F', 'G']

cities = ["A", "B", "C", "D", "E", "F", "G"]
edges = [
    ("A", "B", 5, 2, 5),
    ("A", "C", 10, 4, 6),
    ("B", "D", 20, 8, 10),
    ("C", "D", 15, 6, 8),
    ("D", "E", 10, 4, 6),
    ("C", "E", 25, 8, 12),
    ("E", "F", 15, 4, 5),
    ("F", "G", 5, 2, 3)
]
start_city = "A"
end_city = "G"
max_time = 20

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 0, None, "No valid path found within the maximum time constraint."


cities = ["A", "B", "C", "D", "E", "G"]
edges = [
    ("A", "G", 20, 30, 5),
    ("A", "B", 10, 10, 10),
    ("B", "G", 1, 3, 15),
    ("B", "D", 3, 5, 15),
    ("G", "D", 30, 20, 14),
    ("D", "E", 10, 10, 100),
    ("E", "C", 10, 10, 100),
    ("C", "A", 10, 10, 100)
]
start_city = "A"
end_city = "A"
max_time = 200

profit, time, path = find_most_profitable_path(cities, edges, start_city, end_city, max_time)
print(profit, time, path)  # Expected output: 0, None, "No valid path found within the maximum time constraint."
