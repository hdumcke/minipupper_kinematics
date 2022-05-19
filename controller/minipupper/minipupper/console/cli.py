# -*- coding: utf-8 -*-
import logging

import click
import daiquiri
import daiquiri.formatter
from minipupper import CONF

logger = daiquiri.getLogger(__name__)


@click.group()
def minipupper():
    """Minipupper development environment."""
    pass


@minipupper.command()
@click.option('--loops', '-l', default=1, type=click.INT, help='How many cycles to execute.')
@click.option('--time', '-t', default=1, type=click.FLOAT, help='Time to execute a single cycle in sec.')
@click.option('--debug', '-d', default=False, type=click.BOOL, help='Set debug mode.')
def execute(loops, time, debug):
    """
    Ececute cycles read from files.

    \b
    loops  How many cycles to execute. Default is 1
    time   Time to execute a single cycle in sec. Default is 1 sec
    """

    CONF.minipupper.debug = debug
    daiquiri.setup(level=logging.DEBUG if CONF.minipupper.debug else logging.INFO, outputs=('stdout',))
    logger.info("Configuration file: %s" % CONF.config_file)

    from minipupper.executor.joints import Reader, Servos

    reader = Reader()
    reader.read()
    num_steps = reader.get_max_steps()
    step_duration = time / num_steps
    logger.info("number of steps: %d" % num_steps)
    logger.info("duration per step: %.2f [msec]" % (step_duration*1000))
    logger.info("number of cycles: %d" % loops)
    logger.info("total duration: %.2f [sec]" % (time*loops))
    servos = Servos(reader.get_angles())
    servos.execute_loops(loops, step_duration, num_steps)


@minipupper.command()
@click.option('--loops', '-l', default=5, type=click.INT, help='How many cycles to execute.')
@click.option('--number_of_points', '-n', default=10, type=click.INT, help='How many points in a phase.')
@click.option('--velocity_adapt', '-v', default=4, type=click.INT, help='How to adapt velocity at the end of a phase.')
@click.option('--time', '-t', default=0.1, type=click.FLOAT, help='Time to execute a single cycle in sec.')
@click.option('--step_length', '-s', default=0.04, type=click.FLOAT, help='Length of a step.')
@click.option('--step_height', '-h', default=0.01, type=click.FLOAT, help='Height of a step.')
@click.option('--rotate', '-r', default='none', type=click.STRING, help='Set rotation left/right/none.')
@click.option('--forward', '-f', default=True, type=click.BOOL, help='Forward direction.')
@click.option('--debug', '-d', default=False, type=click.BOOL, help='Set debug mode.')
def walk(loops, time, debug, step_length, step_height, velocity_adapt, number_of_points, rotate, forward):
    """
    Let minipupper walk

    \b
    loops              How many cycles to execute. Default is 5
    time               Time to execute a single cycle in sec. Default is 0.1 sec
    number_of_points   Number of points on the trajectory that will be actuated, Default is 10
    step_length        Length of a step, default is 0.04
    step_height        Heigth of a step, default is 0.01
    rotate             Rotation (left/right) default is none
    forward            Forward direction, default is True
    debug              Turn debug logging on, default is false
    """

    CONF.minipupper.debug = debug
    daiquiri.setup(level=logging.DEBUG if CONF.minipupper.debug else logging.INFO, outputs=('stdout',))
    logger.info("Configuration file: %s" % CONF.config_file)

    from minipupper.executor.joints import Servos
    from minipupper.executor.gaits import GaitController
    import numpy as np

    theta = -3*np.pi/4
    gamma = np.pi/2
    gc = GaitController(step_length, step_height, velocity_adapt, number_of_points, theta, gamma)
    num_steps = len(gc.get_trajectory()[0])
    angles = np.zeros([4, 3, num_steps])
    angles[0][1:3, :] = gc.get_leg_servo_positions(shift=True).T
    angles[1][1:3, :] = gc.get_leg_servo_positions(shift=False).T
    angles[3][1:3, :] = gc.get_leg_servo_positions(shift=True).T
    angles[2][1:3, :] = gc.get_leg_servo_positions(shift=False).T
    if rotate[0] == 'l':
        angles[0][1:3, :] = np.flip(gc.get_leg_servo_positions(shift=True).T, axis=1)
    if rotate[0] == 'r':
        angles[1][1:3, :] = np.flip(gc.get_leg_servo_positions(shift=False).T, axis=1)
    if not forward:
        angles = np.flip(angles, axis=2)
    step_duration = time / num_steps
    logger.info("number of steps: %d" % num_steps)
    logger.info("duration per step: %.2f [msec]" % (step_duration*1000))
    logger.info("total duration: %.2f [sec]" % (time*loops))
    servos = Servos(angles)
    servos.execute_loops(loops, step_duration, num_steps)
