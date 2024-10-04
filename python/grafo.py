import pygame
import networkx as nx
import sys
import random

# Initialize pygame
pygame.init()




# Set screen dimensions
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

# Set window title
pygame.display.set_caption("NetworkX Graph with Node Selection and Movement")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Create a networkx graph
G = nx.erdos_renyi_graph(20, 0.5)  # Random graph with 10 nodes and 50% edge probability
node_values = {node: random.randint(1, G.degree(node)) for node in G.nodes()}

list_node_values = list(node_values.values())
list_fixed_values = list(node_values.values())

# Get positions for the nodes using a spring layout
pos = nx.circular_layout(G)

# Scale the positions to fit on the pygame screen
scaled_pos = {}
for node, (x, y) in pos.items():
    scaled_x = screen_width // 2 + int(x * screen_width // 2) + 500
    scaled_y = screen_height // 4 + int(y * screen_height // 4) + 100
    scaled_pos[node] = [scaled_x, scaled_y]  # Store as mutable list for movement

# Initialize solution_variable (0 means unselected, 1 means selected)
solution_variable = [0] * len(G.nodes)

# Node radius and selection status
node_radius = 20
selected_node = None  # Keeps track of the node being dragged
hovered_node = None   # Keeps track of the node being hovered


def pablo_solution(nodes):
    list_neighbors_values = [[] for _ in range(len(nodes))]
  
    for node in nodes:
        neighbors = list(G.neighbors(node))
        for neighbor in neighbors:
            value = list_fixed_values[neighbor]
            list_neighbors_values[node].append(value)
    
    sum_list = [sum(value) for value in list_neighbors_values]
    for v in sum_list:
        print(f"value : {v}, index : {sum_list.index(v)}")


    min_pairs  = []
    copy_list = sum_list.copy()
    for v in sum_list:
        indexed_numbers = sorted(enumerate(copy_list), key=lambda x: x[1])
        min_values = indexed_numbers[:2]
        #index , value
        if len(min_values) > 0:
            print(min_values)
            min_pairs.append([min_values[0][0], min_values[1][0]])
        copy_list = copy_list[:-2]
    
    for pair in min_pairs:
        print(pair)



# Function to decrease the values of connected nodes by 1 if they are connected to a selected node
def decrease_connected_nodes(selected_nodes, degree_dict):
    for node in selected_nodes:
        # Get all connected neighbors
        neighbors = list(G.neighbors(node))
        for neighbor in neighbors:
            if degree_dict[neighbor] > 0 and solution_variable[neighbor] == 0:
                nn_neighbor = list(G.neighbors(neighbor))
                count = 0
                for nn in nn_neighbor:
                    if solution_variable[nn] == 1:
                        count += 1
                if list_fixed_values[neighbor] - count < 0:
                    degree_dict[neighbor] = 0
                else:
                    degree_dict[neighbor] = list_fixed_values[neighbor] - count
            
            if degree_dict[neighbor] == 0:
                solution_variable[neighbor] = 1


# Function to draw the table with buttons
def draw_table(screen, values1, values2):
    table_x = 20
    table_y = 20
    row_height = 30
    column_width = 100
    button_width = 80

    # Draw the table background
    pygame.draw.rect(screen, GRAY, (table_x - 5, table_y - 5, column_width * 2 + button_width + 15, len(values1) * row_height + 40))

    # Draw column headers
    font = pygame.font.SysFont(None, 24)
    header1 = font.render("V original", True, BLACK)
    header2 = font.render("V novo", True, BLACK)
    button_header = font.render("Select", True, BLACK)
    screen.blit(header1, (table_x, table_y))
    screen.blit(header2, (table_x + column_width, table_y))
    screen.blit(button_header, (table_x +50  +column_width + button_width // 2 - 20, table_y))

    # Draw each row with buttons
    for i, (val1, val2) in enumerate(zip(values1, values2)):
        text1 = font.render(f"{i}-> {val1}", True, BLACK)
        text2 = font.render(str(val2), True, BLACK)
        screen.blit(text1, (table_x, table_y + (i + 1) * row_height))
        screen.blit(text2, (table_x + column_width, table_y + (i + 1) * row_height))

        # Draw button for selecting the node
        button_rect = pygame.Rect(table_x + column_width + 40, table_y + (i + 1) * row_height, button_width, row_height - 5)
        pygame.draw.rect(screen, GREEN if solution_variable[i] == 1 else RED, button_rect)
        button_text = font.render("Select", True, BLACK)
        screen.blit(button_text, (button_rect.x + 5, button_rect.y + 5))


# Function to handle button click
def handle_button_click(mouse_pos, values):
    for i in range(len(values)):
        button_rect = pygame.Rect(20 + 105, 25 + (i + 1) * 30, 80, 25)
        if button_rect.collidepoint(mouse_pos):
            solution_variable[i] = 1  # Set the corresponding value in solution_variable to 1
            break


pablo_solution(G.nodes)
# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button down - check if a node was clicked
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Handle left button click for selection
            if event.button == 1:  # Left mouse button for selecting nodes
                for node, (x, y) in scaled_pos.items():
                    distance = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5
                    if distance < node_radius:
                        solution_variable[node] = 1 - solution_variable[node]  # Toggle between 0 and 1
                        break
            
            # Handle left button click for buttons in the table
            handle_button_click((mouse_x, mouse_y), list_fixed_values)

            # Handle right button click for moving nodes
            if event.button == 3:  # Right mouse button for moving nodes
                for node, (x, y) in scaled_pos.items():
                    distance = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5
                    if distance < node_radius:
                        selected_node = node
                        break

        # Mouse button up - stop dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                selected_node = None

        # Mouse motion - move the selected node with the right button
        elif event.type == pygame.MOUSEMOTION:
            if selected_node is not None:
                mouse_x, mouse_y = event.pos
                scaled_pos[selected_node] = [mouse_x, mouse_y]

            # Check if mouse is hovering over any node
            mouse_x, mouse_y = event.pos
            for node, (x, y) in scaled_pos.items():
                distance = ((x - mouse_x) ** 2 + (y - mouse_y) ** 2) ** 0.5
                if distance < node_radius:
                    hovered_node = node
                    break
            else:
                hovered_node = None  # Reset if not hovering over any node

        # Handle spacebar to decrease connected node values
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                selected_nodes = [node for node in G.nodes if solution_variable[node] == 1]
                if selected_nodes:
                    decrease_connected_nodes(selected_nodes, list_node_values)

    # Fill screen with white color
    screen.fill(WHITE)

    # Draw edges
    for edge in G.edges():
        node1, node2 = edge
        pygame.draw.line(screen, BLACK, scaled_pos[node1], scaled_pos[node2], 2)

    # Draw nodes
    for node, (x, y) in scaled_pos.items():
        color = GREEN if solution_variable[node] == 1 else RED
        pygame.draw.circle(screen, color, (x, y), node_radius)
        font = pygame.font.SysFont(None, 24)
        node_value = list_node_values[node]
        original_values = list_fixed_values[node]
        img = font.render(str(node_value), True, BLACK)
        screen.blit(img, (x - 10, y - 10))

    # Draw the table with the two lists
    draw_table(screen, list_fixed_values, list_node_values)

    


    # Display the hovered node ID on the right side of the screen
    if hovered_node is not None:
        font = pygame.font.SysFont(None, 24)
        hover_text = font.render(f"Node: {hovered_node}", True, BLACK)
        screen.blit(hover_text, (screen_width - 200, 20))  # Adjust position as needed

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
