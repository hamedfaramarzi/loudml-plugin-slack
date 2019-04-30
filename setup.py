#!/usr/bin/env python3

"""
Setup slack plugin for LoudML
"""

from setuptools import setup

setup(
    name='loudml-plugin-slack',

    version='1.5.0',

    description="Slack plug-in for LoudML.",

    py_modules = [
        'loudml_plugin_slack',
    ],

    install_requires=[
        'loudml',
        'slacker',
    ],

    entry_points={
        'loudml.plugins': [
            # Register here your plug-in class.
            'slack=loudml_plugin_slack:SlackPlugin',
        ],
        'loudml.hooks': [
            # Register here your hooks.
            'slack=loudml_plugin_slack:SlackHook',
        ],
    },
)
