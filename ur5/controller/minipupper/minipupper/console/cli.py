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
def execute(loops, time):
    """
    Ececute cycles read from files.

    \b
    loops  How many cycles to execute. Default is 1
    time   Time to execute a single cycle in sec. Default is 1 sec
    """

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
