import math
import random
from matplotlib import pyplot as plt
from celluloid import Camera
from Point import Point
from Vector import Vector


fig = plt.figure()
camera = Camera(fig)


def init_points():
    points = []
    xs = [random.randint(0, 10) for _ in range(10)]
    ys = [random.randint(0, 10) for _ in range(10)]
    for i in range(len(xs)):
        x = Point(xs[i], ys[i])
        points.append(x)
    return points


def draw_point(point: Point):
    plt.scatter(point.x, point.y)


def draw_points(points: list):
    for i in range(len(points)):
        draw_point(points[i])


def init_vectors_of_moving(points: list):
    vectors = []
    xs = [random.randint(-1, 1) for _ in range(len(points))]
    ys = [random.randint(-1, 1) for _ in range(len(points))]
    for i in range(len(xs)):
        p = Point(xs[i], ys[i])
        while p.x == 0 and p.y == 0:
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
        vectors.append(p)
    return vectors


def opposite_vectors_of_moving(vectors: list):
    for i in range(len(vectors)):
        vectors[i] = Point(-vectors[i].x, -vectors[i].y)
    return vectors


def get_min_y(points: list):
    min_y = points[0].y
    for i in range(len(points)):
        if points[i].y < min_y:
            min_y = points[i].y
    return min_y


def cos(v1: Vector, v2: Vector):
    cos_value = (v1 * v2) / (v1.get_length() * v2.get_length())
    if cos_value > 1:
        return 1
    elif cos_value < -1:
        return -1
    else:
        return cos_value


def get_init_point(points: list):
    min_y = get_min_y(points)
    init_point = Point(-1, -1)
    for i in range(len(points)):
        if points[i].y == min_y:
            init_point = points[i]
    return init_point


def get_next_active_point(points: list, current_active_point: Point, convex_hull_points: list):
    if len(convex_hull_points) < 2:
        polar_axis = Vector(Point(0, 0), Point(1, 0))
    else:
        # в качестве полярной оси взяли последнюю добавленную сторону
        polar_axis = Vector(convex_hull_points[-2], convex_hull_points[-1])
    next_active_point = get_point_with_min_arc(points, current_active_point, polar_axis, convex_hull_points)
    return next_active_point


def get_point_with_min_arc(points: list, active_point: Point, polar_axis: Vector, convex_hull_points: list):
    min_arc = 2 * math.pi
    index = -1
    init_point = get_init_point(points)
    print(polar_axis.get_length())
    for i in range(len(points)):
        if len(convex_hull_points) == 1 and points[i].x == init_point.x and points[i].y == init_point.y:
            continue
        is_on_hull = False
        for j in range(1, len(convex_hull_points)):
            if points[i].x == convex_hull_points[j].x and points[i].y == convex_hull_points[j].y:
                is_on_hull = True
                break
        if is_on_hull:
            continue
        current_arc = math.acos(cos(Vector(active_point, points[i]), polar_axis))
        if min_arc > current_arc >= 0:
            min_arc = current_arc
            index = i
    return points[index]


# Jarvis algorithm
def build_convex_hull(points: list):
    init_point = get_init_point(points)
    active_point = init_point
    convex_hull_points = [active_point]

    while True:
        active_point = get_next_active_point(points, active_point, convex_hull_points)
        convex_hull_points.append(active_point)
        if init_point.x == convex_hull_points[-1].x and init_point.y == convex_hull_points[-1].y:
            break

    return convex_hull_points


def draw_convex_hull(convex_hull_points: list, color: str):
    for i in range(len(convex_hull_points) - 1):
        plt.plot([convex_hull_points[i].x, convex_hull_points[i + 1].x],
                 [convex_hull_points[i].y, convex_hull_points[i + 1].y], color=color)
    camera.snap()


def point_distance(p1: Point, p2: Point):
    return math.sqrt(abs((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y - p1.y)))


def det(a, b, c, d):
    return a * d - b * c

# вместо площади треугольника считаем площадь паралеллограмма через векторное произведение
def vector_product(p0: Point, p1: Point, p2: Point):
    return det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)


def findDiameter(points):
    k = len(points)
    i = 1
    d = 0
    while vector_product(points[k-1], points[0], points[i]) < vector_product(points[k-1], points[0], points[i + 1]):
        i += 1
    start = i
    j = 0
    while start < k:
        tmp = start
        while vector_product(points[j % k], points[(j + 1) % k], points[tmp % k]) <= vector_product(points[j % k], points[(j + 1) % k], points[(tmp + 1) % k]):
            tmp += 1
        end = tmp
        for l in range(start, end + 1):
            if point_distance(points[j % k], points[l % k]) > d:
                tmp1 = points[j % k]
                tmp2 = points[l % k]
                d = point_distance(points[j % k], points[l % k])
        start = end
        j += 1
    res = {'distance': d, 'points': [tmp1, tmp2]}
    return res


def draw_diameter(points: list):
    plt.plot([points[0].x, points[1].x],
             [points[0].y, points[1].y], "red")


def move(moving_points: list, vectors: list):
    for i in range(len(moving_points)):
        moving_points[i] = moving_points[i] + vectors[i]


def init_motion(points: list):
    vectors = init_vectors_of_moving(points)
    diameter_limit = 40

    i = 0
    while i < 70:
        # print(i)
        convex_hull_points = build_convex_hull(points)

        draw_points(points)
        draw_diameter(findDiameter(convex_hull_points)['points'])
        draw_convex_hull(convex_hull_points, "blue")

        if findDiameter(convex_hull_points)['distance'] >= diameter_limit:
            vectors = opposite_vectors_of_moving(vectors)

        move(points, vectors)
        i += 1


def init():
    points = init_points()
    init_motion(points)
    # draw_points(points)
    # convex_hull_points = build_convex_hull(points)
    # draw_convex_hull(convex_hull_points, "blue")
    # check(convex_hull_points)

    plt.grid(True)
    animation = camera.animate(blit=False, interval=300)
    animation.save("animation.gif")
    plt.show()


init()
