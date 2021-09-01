import pygame

# size
BLOCK_SIZE = 20
BLOCK_FRAME = 5
TOTAL_BLOCK_SIZE = BLOCK_SIZE + BLOCK_FRAME
WIDTH = 28
HEIGHT = 20
TOTAL_WIDTH = WIDTH * TOTAL_BLOCK_SIZE
TOTAL_HEIGHT = HEIGHT * TOTAL_BLOCK_SIZE
# colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (125, 125, 125)

diagonal = True


def click_to_loc(click_loc: (int, int)):
    click_loc = click_loc[0] // TOTAL_BLOCK_SIZE, click_loc[1] // TOTAL_BLOCK_SIZE
    click_loc = click_loc[0] * TOTAL_BLOCK_SIZE, click_loc[1] * TOTAL_BLOCK_SIZE
    click_loc = click_loc[0] + TOTAL_BLOCK_SIZE // 2, click_loc[1] + TOTAL_BLOCK_SIZE // 2
    return click_loc


def get_neighbors(pos: (int, int)):
    res = []
    y = pos[1]
    if 0 < (x := pos[0] + TOTAL_BLOCK_SIZE) < TOTAL_WIDTH:
        y = pos[1]
        res.append((x, y))
        if diagonal and 0 < (y := pos[1] + TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
            res.append((x, y))
        if diagonal and 0 < (y := pos[1] - TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
            res.append((x, y))
    if 0 < (x := pos[0] - TOTAL_BLOCK_SIZE) < TOTAL_WIDTH:
        y = pos[1]
        res.append((x, y))
        if diagonal and 0 < (y := pos[1] + TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
            res.append((x, y))
        if diagonal and 0 < (y := pos[1] - TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
            res.append((x, y))
    x = pos[0]
    if 0 < (y := pos[1] + TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
        res.append((x, y))
    if 0 < (y := pos[1] - TOTAL_BLOCK_SIZE) < TOTAL_HEIGHT:
        res.append((x, y))
    return res


def euclidean_distance(point1: (int, int), point2: (int, int)):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5


def A_star(end, start, walls):
    visited = set()
    backtrack = dict()
    to_check = [start]
    distance = {start: 0}
    weight = TOTAL_BLOCK_SIZE//2
    while len(to_check) != 0:
        current = to_check[0]
        if end == current:
            return visited, backtrack
        visited.add(current)
        for node in get_neighbors(current):
            if node in visited or node in walls:
                continue
            if node not in distance:
                distance[node] = float("inf")
            if distance[current] + weight < distance[node]:
                distance[node] = distance[current] + weight
                backtrack[node] = current
            if node not in to_check:
                to_check.append(node)
        to_check.remove(current)
        to_check.sort(key=lambda x:  distance[x] + euclidean_distance(x, end))
    return visited, backtrack


def display_loop(display):
    running = True
    start = click_to_loc((0, 0))
    end = click_to_loc((TOTAL_WIDTH - 1, TOTAL_HEIGHT - 1))
    mode = 's'
    walls = set()
    visited, backtrack = A_star(end, start, walls)
    change = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                mode = event.unicode
                print(f"mode : {mode}")
                if mode == 'r':
                    start = click_to_loc((0, 0))
                    end = click_to_loc((TOTAL_WIDTH - 1, TOTAL_HEIGHT - 1))
                    mode = 's'
                    walls = set()
                elif mode == 'd':
                    global diagonal
                    diagonal = not diagonal
                visited, backtrack = A_star(end, start, walls)
                change = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                loc = click_to_loc(pygame.mouse.get_pos())
                if mode == 's':
                    start = loc
                elif mode == 'e':
                    end = loc
                elif mode == 'w':
                    if loc in walls:
                        walls.remove(loc)
                    else:
                        walls.add(loc)

                visited, backtrack = A_star(end, start, walls)
                change = True
        if not change:
            continue
        display.fill(BLACK)
        for i in range(TOTAL_BLOCK_SIZE // 2, TOTAL_WIDTH, TOTAL_BLOCK_SIZE):
            for j in range(TOTAL_BLOCK_SIZE // 2, TOTAL_HEIGHT, TOTAL_BLOCK_SIZE):
                color = BLUE
                if (i, j) in visited:
                    color = RED
                if (i, j) in walls:
                    color = GREY
                if (i, j) == start:
                    color = YELLOW
                if (i, j) == end:
                    color = GREEN
                pygame.draw.rect(display, color, (i - BLOCK_SIZE // 2, j - BLOCK_SIZE // 2, BLOCK_SIZE, BLOCK_SIZE))
        if end in backtrack:
            node = end
            while node != start:
                pygame.draw.line(display, (255, 255, 255), node, backtrack[node], 3)
                node = backtrack[node]
        pygame.display.flip()
        change = False


def main():
    pygame.init()
    display = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
    pygame.display.set_caption('A star algorithm grid')
    display_loop(display)
    pygame.quit()


if __name__ == '__main__':
    main()
