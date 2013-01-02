# JSON2Blender v0.1
#
# Author: Cole Reed
# Email: info@auralgrey.com
# https://github.com/ichabodcole
#
# Please report issues at https://github.com/ichabodcole/AE2JSON
#
# Copyright (c) 2012 Cole Reed. All rights reserved.   
#
# Description:
# A script to convert AE2JSON encoded After Effects project data to Blender
#
# TODO (this is the short list)
#    Add comments
#    Add more import types

"""
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, 
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR 
OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os

import bpy
from math import radians

import json

directory = os.path.dirname(bpy.data.filepath)
if directory not in sys.path:
   sys.path.append(directory)

import data_parser

filename = "AE2JSON_Comp1.json"
full_path = directory + "/" +filename 
json_str = open(full_path).read()
json_data = json.loads(json_str)

data_parser = DataParser(json_data)
parsed_data = data_parser.parse()

#data_parser = AEProjectParser(json_data)
#data_parser.add_layer_parser('Null', NullLayerParser)
#data_parser.add_layer_parser('Camera', CameraLayerParser)
#parsed_data = data_parser.parse()
#import pprint
#pp = pprint.PrettyPrinter(indent = 4, depth = 5, width=120)
#pp.pprint(parsed_data)

class Main(object):
  def __init__(self, data_parser):
    self.data_parser = data_parser

  def run(self):
    self.data_parser.parse()

  def create_objects(self):
    pass

  def set_parents(self):
    pass