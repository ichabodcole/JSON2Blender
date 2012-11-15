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

import bpy
import os
import json
from math import radians

directory = os.path.dirname(bpy.data.filepath)
filename = "AE2JSON_Comp1.json"
fullpath = directory + "/" +filename

json_str = open(fullpath).read()
json_data = json.loads(json_str)




class Main():
  def __init__(self, json_data):
    self.json_data = json_data
    self.compSettings = json_data['compSettings']
    self.objectList = []

  def run(self):
    for data in self.json_data:
      obj = self.json_data[data]
      if(data == 'nulls'):
        for null in obj:
          nullObj = Null(self.compSettings, obj[null])




class BaseObject(object):
  def __init__(self, compSettings, objData):
    self.compSettings = compSettings
    self.objData = objData
    self.name = self.objData['name']
    self.__add_to_scene()
    self.__set_properties()

  def __set_property(self, propType, propList):
    numProperties = len(propList)
    if (numProperties < 2 and numProperties != 0):
      propVal = propList[0][1]
      self.__handle_prop(propType, propVal)
    else:
      for prop in propList:
        time = prop[0]
        propVal = prop[1]
        frameDuration = self.compSettings['frameDuration']
        frame = round(time / frameDuration)
        self.__handle_prop(propType, propVal, frame)

  def __handle_prop(self, propType, propVal, frame=-1):
    if(propType == 'location'):
      self.__set_location(propVal, frame)

    if(propType == 'xRotation' or propType == 'yRotation' or propType == 'zRotation'):  
      self.__set_rotation(propType, propVal, frame)

  def __get_location_data(self):
    location = self.objData['transform']['position']
    return location

  def __set_location(self, location, frame):
    # Adjust the object position to compensate for After Effects Top Left corner coordinate  system
    location[0], location[1] = (location[0]-(self.compSettings['width']/2)), (location[1]-(self.compSettings['height']/2))

    #Flip the ZY coordinates
    location[1], location[2] = location[2], -location[1]

    #Scale down the dimensions to a resonable size
    scaleFactor = 0.01
    location = [x * scaleFactor for x in location]

    # Set the objects position
    self.BO.location = location

    # Keyframe the position
    if(frame != -1):
      self.BO.keyframe_insert(data_path="location", frame=frame)

  def __get_rotation_data(self, rotationType):
    # Some After Effects objects do not have a rotation, 
    # so we must add a default if rotation does not exist.
    if(self.objData['transform'][rotationType]):
      rotation = self.objData['transform'][rotationType]
    else:
      rotation = [[0, 0]]
    return rotation

  def __set_rotation(self, axis, rotation, frame):
    # Correct for AE starting rotation
    if(axis == 'xRotation'):
      index = 0
      rotation += 90

    # Correct for AE's ZY coordinate flip
    if(axis == 'yRotation'):
      index = 2
      # Another coordinate fix
      rotation *= -1
    if(axis == 'zRotation'):
      index = 1

    # Convert degrees to radians
    rotation = radians(rotation)

    # Set the object's rotation
    self.BO.rotation_euler[index] = rotation

    # Keyframe the rotation
    if(frame != -1):
      self.BO.keyframe_insert(data_path="rotation_euler", frame=frame, index=index)
        
  def __set_properties(self):
    self.__set_property('location', self.__get_location_data())
    self.__set_property('xRotation', self.__get_rotation_data('xRotation'))
    self.__set_property('yRotation', self.__get_rotation_data('yRotation'))
    self.__set_property('zRotation', self.__get_rotation_data('zRotation'))

  # add the object type to the scene and create an instance variable reference for it.
  def __add_to_scene(self):
    bpy.ops.object.add(type='EMPTY')
    self.BO = bpy.context.object
    self.BO.name = self.name

class Null(BaseObject):
  def __init__(self, compSettings, objData):
    super(Null, self).__init__(compSettings, objData)


main = Main(json_data).run()