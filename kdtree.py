from math import floor
from random import randint

def generate_unique_points(count, xmin, ymin, xmax, ymax):
    points = []
    for i in range(count):
        points.append((random.randint(xmin, xmax), random.randint(ymin, ymax)))
    return list(set(points))

def median(nums):
    sorted_nums = sorted(nums)
    count = len(sorted_nums)
    if count % 2 == 0:
        return min(sorted_nums[count / 2 - 1], sorted_nums[count / 2])
    else:
        return sorted_nums[int(math.floor(count / 2))]

class KdTree:
    def __init__(self, points=[]):
        self.root = self._build_tree(points)

    def _build_tree(self, points, depth=0):
        dim = depth % len(points[0])
        left_pts, right_pts, split_pt = self._partition_points(points, dim)
        node = self._create_node(split_pt)
        if len(points) > 1:
            node["left"] = self._build_tree(left_pts, depth + 1)
            node["right"] = self._build_tree(right_pts, depth + 1)
        return node

    def _create_node(self, split_pt, left=None, right=None):
        node = {'split_point': split_pt,
                'left': left,
                'right': right}
        return node

    def _partition_points(self, points, dim):
        split_point = self._composite_median(points, dim)
        left_points = []
        right_points = []
        for point in points:
            comp = self._composite_compare(point, split_point, dim)
            if comp == -1 or comp == 0:
                left_points.append(point)
            elif comp == 1:
                right_points.append(point)

        return left_points, right_points, split_point

    def _composite_compare(self, pt1, pt2, dim):
        if pt1 == pt2:
            return 0

        curr_dim = dim
        dim_count = len(pt1)
        while 1:
            if pt1[curr_dim] == pt2[curr_dim]:
                curr_dim = curr_dim + 1 if curr_dim < dim_count - 1 else 0
            else:
                break
        return -1 if pt1[curr_dim] < pt2[curr_dim] else 1

    def _composite_median(self, points, dim):
        sorted_points = sorted(points, cmp=lambda pt1, pt2: self._composite_compare(pt1, pt2, dim))
        count = len(sorted_points)
        if count % 2 == 0:
            left_pt = sorted_points[count / 2 - 1]
            right_pt = sorted_points[count / 2]
            comp = self._composite_compare(left_pt, right_pt, dim)
            if comp == -1:
                return left_pt
            elif comp == 1:
                return right_pt
        else:
            return sorted_points[int(math.floor(count / 2))]

    def search_range(self, min_pt, max_pt):
        points = self._report_subtree(self.root, min_pt, max_pt)
        return points

    def _report_subtree(self, node, min_pt, max_pt, depth=0):
        if node["left"] == None and node["right"] == None:
            if self._point_in_range(node["split_point"], min_pt, max_pt):
                return [node["split_point"]]
            else:
                return []

        dim = depth % len(node["split_point"])

        min_comp = self._composite_compare(node["split_point"], min_pt, dim)
        left_pts = []
        if min_comp == 1 or min_comp == 0:
            left_pts = self._report_subtree(node["left"], min_pt, max_pt, depth + 1)

        max_comp = self._composite_compare(node["split_point"], max_pt, dim)
        right_pts = []
        if max_comp == -1:
            right_pts = self._report_subtree(node["right"], min_pt, max_pt, depth + 1)

        return left_pts + right_pts

    def _point_in_range(self, point, min_pt, max_pt):
        in_range = True
        for dim in range(len(max_pt)):
            if point[dim] < min_pt[dim] or point[dim] > max_pt[dim]:
                in_range = False
                break
        return in_range

def test1():
    points = [(0,),(2,),(4,),(6,),(8,)]
    kd_tree = KdTree(points)
    assert kd_tree.search_range((-1,), (9,)) == [(0,),(2,),(4,),(6,),(8,)]
    assert kd_tree.search_range((1,), (3,))  == [(2,)]
    assert kd_tree.search_range((5,), (7,))  == [(6,)]
    assert kd_tree.search_range((4,), (6,))  == [(4,), (6,)]
    assert kd_tree.search_range((0,), (2,))  == [(0,), (2,)]

def test2():
    points = generate_unique_points(1000, -100, -100, 100, 100)
    kd_tree = KdTree(points)
    results = kd_tree.search_range((-10, -10), (10, 10))
    assert all(map(lambda n: abs(n) <= 10, [n for pt in results for n in pt]))