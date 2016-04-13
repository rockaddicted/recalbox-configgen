#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import ConfigParser
import recalboxFiles

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import settings.unixSettings as unixSettings
import recalboxFiles


reicastMapping = { 'a' :             {'button': 'btn_b'},
                   'b' :             {'button': 'btn_a'},
                   'x' :             {'button': 'btn_y'},
                   'y' :             {'button': 'btn_x'},
                   'start' :         {'button': 'btn_start'},
                   'hotkey' :        {'button': 'btn_escape'},
                   'pageup' :        {'axis': 'axis_trigget_left',  'button': 'btn_trigget_left'},
                   'pagedown' :      {'axis': 'axis_trigget_right', 'button': 'btn_trigget_right'},
                   'joystick1left' : {'axis': 'axis_x'},
                   'joystick1up' :   {'axis': 'axis_y'},
                   # The DPAD can be an axis (for gpio sticks for example) or a hat
                   'left' :          {'hat': 'axis_dpad1_x', 'axis': 'axis_x'},
                   'up' :            {'hat': 'axis_dpad1_y', 'axis': 'axis_y'}
}

sections = { 'emulator' : ['mapping_name', 'btn_escape'],
             'dreamcast' : ['btn_a', 'btn_b', 'btn_x', 'btn_y', 'btn_start', 'axis_x', 'axis_y', 'axis_trigget_left', 'axis_trigget_right'],
             'compat' : ['axis_dpad1_x', 'axis_dpad1_y', 'btn_trigger_left', 'btn_trigger_right']

}


# Create the controller configuration file
# returns its name
def generateControllerConfig(controller):
	# Set config file name
    configFileName = "{}/controllerP{}.cfg".format(recalboxFiles.reicastCustom,controller.player)
    Config = ConfigParser.ConfigParser()
    #~ cfgfile = open(recalboxFiles.reicastCustom + '/mappings/' + configFileName,'w+')
    cfgfile = open(configFileName,'w+')
    
    # create ini sections
    for section in sections:
        Config.add_section(section)

    # Add controller name
    Config.set("emulator", "mapping_name", controller.realName)
    
    # Parse controller inputs
    for index in controller.inputs:
		input = controller.inputs[index]
		if input.name not in reicastMapping:
			continue
		var = reicastMapping[input.name][input.type]
		for i in sections:
			if var in sections[i]:
				section = i
				break
		
		# Sadly, we don't get the right axis code for Y hats. So, dirty hack time
		code = input.code
		if input.type == 'hat':
		    if input.name == 'up':
    			code = int(input.code) + 1
		    else:
    			code = input.code
		
		Config.set(section, var, code)

    Config.write(cfgfile)
    cfgfile.close()
    return configFileName

