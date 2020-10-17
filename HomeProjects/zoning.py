import random
from itertools import combinations_with_replacement, permutations


class Zoner:
    def __init__(self):
        self.min = [-20., -20., -20.]
        self.max = [20., 20., 20.]
        self.n = 4
        self.centroid = [0., 0., 0.]
        self.step = [0., 0., 0.]

    def get_steps(self, i):
        step = (self.max[i] - self.min[i]) / float(self.n)
        return step, [self.min[i] + x * step for x in range(0, self.n+1)]

    def get_zones(self, n):
        self.n = n
        self.step[0], self.xsteps = self.get_steps(0)
        self.step[1], self.ysteps = self.get_steps(1)
        self.step[2], self.zsteps = self.get_steps(2)
        print(self.step[0], self.xsteps)
        print(self.step[1], self.ysteps)
        print(self.step[2], self.zsteps)
        return

    def get_point_coord(self, i, div=10.):
        ii = random.randrange(int(self.min[i] * div), int(self.max[i] * div))
        return float(ii) / div

    def generate_points(self, num, div=10.):
        points = []
        for i in range(num):
            pnt = [self.get_point_coord(0, div), self.get_point_coord(1, div), self.get_point_coord(2, div)]
            points.append(pnt)
            # print("[{:.2f}\t{:.2f}\t{:.2f}]".format(pnt[0], pnt[1], pnt[2]))
        return points

    def get_coord_zone(self, point, i):
        return int(abs((point[i] - self.min[i]) // self.step[i]))

    def get_point_zone(self, point):
        xz = self.get_coord_zone(point, 0)
        yz = self.get_coord_zone(point, 1)
        zz = self.get_coord_zone(point, 2)
        return [xz+1, yz+1, zz+1]

    def count_xyz_zones(self, points, n):
        counts = {
            "x": [0 for i in range(n)],
            "y": [0 for i in range(n)],
            "z": [0 for i in range(n)]
            }
        for point in points:
            print(point)
            for i, axis in enumerate(["x", "y", "z"]):
                z = self.get_coord_zone(point, i)
                counts[axis][z] += 1
        print(counts)

    def get_point_distance_n5(self, point):
        zone = self.get_point_zone(point)
        print(zone, zone.count(3), zone.count(2) + zone.count(4), zone.count(1) + zone.count(5))
        if [3, 3, 3] == zone:
            return 0
        elif zone.count(3) == 2 and zone.count(2) + zone.count(4) == 1:
            return 1
        elif zone.count(3) == 1 and zone.count(2) + zone.count(4) == 2:
            return 1
        elif zone.count(2) + zone.count(4) == 3:
            return 2
        elif zone.count(2) + zone.count(4) == 1 and zone.count(1) + zone.count(5) == 1 and zone.count(3) == 1:
            return 3
        elif zone.count(2) + zone.count(4) == 2 and zone.count(1) + zone.count(5) == 1:
            return 4
        elif zone.count(2) + zone.count(4) == 1 and zone.count(1) + zone.count(5) == 2:
            return 4
        elif zone.count(1) + zone.count(5) == 3:
            return 5

    def zone_freqs_dict(self, n):
        combos = list(combinations_with_replacement([x + 1 for x in range(n)], 3))
        zone_freqs = dict()
        for i, c in enumerate(combos):
            zone_freqs[c] = {
                "cnt": 0,
                "sum": 0.,
                "avg": 0.
            }
        return zone_freqs

    def distance(self, p1):
        import math
        centroid = self.centroid
        # print(p1, centroid)
        return math.sqrt(((p1[0] - centroid[0]) ** 2) + ((p1[1] - centroid[1]) ** 2) + ((p1[2] - centroid[2]) ** 2))

    def get_point_dist_many(self, points, zone_freqs):
        for point in points:
            zone = self.get_point_zone(point)
            combos = list(set(permutations(zone, 3)))
            # print(combos)
            for combo in combos:
                if combo in zone_freqs.keys():
                    zone_freqs[combo]['cnt'] += 1
                    zone_freqs[combo]['sum'] += self.distance(point)
                    zone_freqs[combo]['combo'] = combo
                    # print(' - {} {:.2f}, {}'.format(point, self.distance(point), combo))

    def get_point_zones(self, points):
        for point in points:
            zone = self.get_point_distance_n5(point)
            print("Zone: {}, point: [{:.2f}\t{:.2f}\t{:.2f}]".format(zone, point[0], point[1], point[2]))


def get_zone_frequencies(zf):
    fin = []
    for k, v in zf.items():
        if v['cnt'] > 0:
            v['avg'] = v['sum'] / v['cnt']
            # print('Frequency: {} {} {:.2f}'.format(k, v['cnt'], v['sum']/v['cnt']))
        fin.append(v)

    for v in sorted(fin, key=lambda i: i['avg']):
        print('Frequency: {} {:.2f}'.format(v['combo'], v['avg']))


zn = Zoner()
np = 5
zn.get_zones(np)
zn.count_xyz_zones(zn.generate_points(5, 1.), np)
# zn.get_point_dist_many(zn.generate_points(10000), zf)
# zf = zn.zone_freqs_dict(4)
