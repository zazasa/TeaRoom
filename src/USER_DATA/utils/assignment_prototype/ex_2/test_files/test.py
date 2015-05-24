#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 17:34:56
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 20:24:21

# add external folder to import path
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from user_files.escape_velocity import escape_velocity


class Planet(object):
    def __init__(self, name, mass, radius, velocity):
        super(Planet, self).__init__()
        self.name = name
        self.mass = mass
        self.radius = radius
        self.velocity = velocity

PLANETS = [
    Planet('Mercury', 3.3 * (10 ** 23), 2440, 4435),
    Planet('Hearth', 6.0 * (10 ** 24), 6378, 11200),
    Planet('Jupiter', 1.9 * (10 ** 27), 71492, 59600)]


for planet in PLANETS:
    try:
        v = escape_velocity(planet.mass, planet.radius)
        err = abs(1 - v / planet.velocity)
        assert err < 0.05
    except:
        print 'Fails to calculate for planet: %s, result: %s' % (planet.name, v)
        sys.exit(0)

print 'Nice job.'
