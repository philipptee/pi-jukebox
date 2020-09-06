#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gpiozero import Button
from gpiozero import DigitalOutputDevice
from gpiozero import LED
import os
import subprocess
import sys
import time

_SHUTDOWN_BUTTON_HOLD_TIME_SECS = 2.0
_DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'phoniebox.conf')

class ShutdownDeamon():
    def __init__(self, phoniebox_service_name):
      self._shut_down_triggered = False
      self._phoniebox_service_name = phoniebox_service_name
      self._cut_power_out = DigitalOutputDevice(pin=4, initial_value=True)
      self._status_led = LED(27, initial_value=True)
      # The shutdown button has two functions:
      #   1. on short press the phoniebox client is restarted.
      #   2. on long press the box is shut down.
      self._shut_down_btn =  Button(17, hold_repeat=True, hold_time=0.3, pull_up=True)
      self._shut_down_btn.when_held = self.shutdown_btn_held  
      self._shut_down_btn.when_released = self.shutdown_btn_released
      self._signal()
  
    def _signal(self):
        self._status_led.off()
        time.sleep(0.3)
        self._status_led.on()
    
    def shutdown_btn_held(self):
      if self._shut_down_btn.held_time >= _SHUTDOWN_BUTTON_HOLD_TIME_SECS:
        self._shut_down_triggered = True
        self.shut_down()

    def shutdown_btn_released(self):
      if not self._shut_down_triggered:
        self.restart_phoniebox_deamon()

    def restart_phoniebox_deamon(self):
      print("Restarting phoniebox")
      self._status_led.off()
      time.sleep(0.3)
      self._status_led.on()
      subprocess.call("sudo systemctl restart %s" % self._phoniebox_service_name, shell=True)

    def shut_down(self):
      print("Perform shut down.")
      for _ in range(3):
        self._status_led.off()
        time.sleep(0.3)
        self._status_led.on()
        time.sleep(0.3)
      self._status_led.off()
      self._cut_power_out.off()
      subprocess.call("sudo shutdown -h now", shell=True)

    def run(self):
      while True:
        time.sleep(10.0)


if __name__ == "__main__":
#config_file_path = _DEFAULT_CONFIG_PATH
#  if len(sys.argv) <= 1:
#    print("missing argument 1: phoniebox service name.")
#    sys.exit(-1)
#  if len(sys.argv) >= 3:
#    config_file_path = sys.argv[2]
#  phoniebox_service_name = sys.argv[1]
  # TODO read the config
  daemon = ShutdownDeamon(phoniebox_service_name="phoniebox-py")
  daemon.run()  # blocking