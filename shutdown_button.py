#! /usr/bin/python3
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

# credits to # scruss: https://github.com/scruss/shutdown_button
# example gpiozero code that could be used to have a reboot
#  and a shutdown function on one GPIO button
# scruss - 2017-10

use_button=23

from gpiozero import Button
from signal import pause
from subprocess import check_call
import RGBled as LED
import shutdown_reboot as shutboot

held_for=0.0

def rls():
    global held_for
    if held_for > 3.0:  # if button is helded for more than 3 seconds -> Shutdown: useful to disconnect the pi
        LED.shutdown_led()
        shutboot.shutdown_pi()
        check_call(['/sbin/poweroff'])
    elif held_for > 0.5: # if helded for more than 0.5 seconds and less than 3- > reboot: useful if there any abnormal code error
        LED.reboot_led()
        shutboot.reboot_pi()
        check_call(['/sbin/reboot'])
    else:
        held_for = 0.0

def hld():
    # callback for when button is held
    #  is called every hold_time seconds
    global held_for
    # need to use max() as held_time resets to zero on last callback
    held_for = max(held_for, button.held_time + button.hold_time)
button=Button(use_button, hold_time=1.0, hold_repeat=True)
button.when_held = hld
button.when_released = rls

pause() # wait forever
