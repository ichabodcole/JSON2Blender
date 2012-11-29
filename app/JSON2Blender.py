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


class Main(object):
  def __init__(self, data_parser):
    self.data_parser = data_parser

  def run(self):
    self.data_parser.parse()

  def create_objects(self):
    pass

  def set_parents(self):
    pass

#
# Data Parsers
#
class AbstractParser(object):
  def __init__(self, data):
    self.in_data = data
    self.out_data = {}

  def parse(self):
    pass



class AfterEffectsParser(AbstractParser):
  def __init__(self, data):
    super(AfterEffectsParser, self).__init__(data)

    self.object_parsers = {}
    print("AfterEffectsParser : Constructor")

  def parse(self):
    project_settings = self.in_data['projectSettings']
    self.out_data['project_settings'] = self.__parse_project_settings(project_settings)

    comps = self.in_data['compositions']
    self.out_data['scenes'] = self.__parse_comps(comps)

  def add_object_parser(self, key, parser_class):
    if key not in self.object_parsers:
      self.object_parsers[key] = parser_class   


  def __parse_project_settings(self, project_settings):
    return project_settings

  def __parse_comps(self, comps):
    comp_list = []
    for comp in comps:
      comp_list.append(self.__parse_comp(comp))
    return comp_list

  def __parse_comp(self, comp):
    comp_settings = comp['compSettings']
    settings = self.__parse_comp_settings(comp_settings)
    #
    layers = comp['layers']
    objects = self.__parse_comp_layers(layers)
    data = {'settings': settings, 'objects': objects}
    return data

  def __parse_comp_settings(self, comp_settings):
    return comp_settings

  def __parse_comp_layers(self, layers):
    layer_list = []
    for layer in layers:
      layer_type = layer['layerType']
      if layer_type in self.object_parsers:
        layer_list.append(self.__parse_comp_layer(layer_type, layer))
    return layer_list

  def __parse_comp_layer(self, layer_type, layer):
        obj = self.object_parsers[layer_type](layer)
        return obj.parse()


#
#
#
class BaseObjectParser(AbstractParser):
  def __init__(self, objData):
    super(BaseObjectParser, self).__init__(objData)
    print("BaseObject Parser")

  def parse(self):
    self.__parse_meta_info()
    self.__parse_transform_data()
    return self.out_data

  def __parse_meta_info(self):
    self.out_data['object_type'] = self.in_data['layerType']
    self.out_data['name']        = self.in_data['name']
    self.out_data['parent']      = self.in_data['parent']

  def __parse_transform_data(self, transforms):
    transforms = self.in_data['transform']
    self.__parse_location(transforms)
    self.__parse_rotation(transforms)

  def __parse_location(self, transforms):
    location = transforms['position']
    location_data = {}
    location_data['data_path'] = 'location'
    location_data['index'] = -1 
    location_list = []

    location_list.append(self.__create_time_value_pair_list(location))

    location_data['keyframe_values'] = location_list
    self.out_data['location'] = location_data

  def __parse_rotation(self, transforms):
    rotation_x = transforms['xRotation']
    # ZY gets flipped
    rotation_y = transforms['zRotation']
    rotation_z = transforms['yRotation']

    self.out_data['rotation_x'] = rotation_x
    self.out_data['rotation_y'] = rotation_y
    self.out_data['rotation_z'] = rotation_z
    
  def __create_time_value_dict_list(self, time_value_list):
    time_value_pair_list = []
    for time_value in time_value_list:
      time_value_pair_list.append(self.__create_time_value_dict(time_value))
    return time_value_pair_list

  def __create_time_value_dict(self, time_value):
      time_value_dict = {}
      time_value_dict['time']  = val[0] # time in seconds
      time_value_dict['value'] = val[1] # an xyz array
      return time_value_dict
    

class NullParser(BaseObjectParser):
  def __init__(self, objData):
    super(NullParser, self).__init__(objData)
    print("Null Parser")


class CameraParser(AbstractParser):
  def __init__(self, objData):
    super(CameraParser, self).__init__(objData)
    print("Camera Parser")

#
#
#
class PropertyLookup(object):
  def __init__(self):
    self.property_table = {}

  def add_property(self, key, data_path, args={'index':-1}):
    ref = self.property_table[key] = {}
    ref['data_path'] = data_path
    ref['index']     = args['index']

  def get_property(self, key):
    if ref_name in self.property_table:
      return self.property_table[key]


#
# Converters
#
class AbstractConverter(object):
  def __init__(self, arg):
    pass

  def convert(self):
    pass

class LocationConverter(AbstractConverter):
  def __init__(self, arg):
    super(Converter, self).__init__(arg)
    self.scaleFactor = 0.01

  def convert(self, locData):
    pass

  def __flip_zy():
    #Flip the ZY coordinates
    location[1], location[2] = location[2], -location[1]

  def __scale_units():
    #Scale down the dimensions to a resonable size
    location = [x * self.scaleFactor for x in location]
    pass

  def __offset():
    # Adjust the object position to compensate for After Effects Top Left corner coordinate  system
    location[0], location[1] = (location[0]-(self.compSettings['width']/2)), (location[1]-(self.compSettings['height']/2))

class RotationConverter(AbstractConverter):
  def __init__(self, arg):
    super(Converter, self).__init__(arg)

  def convert(self, locData):
    pass

  def __toRadians():
    #rotation = radians(rotation)
    pass

class xRotConverter(RotationConverter):
  def __init__(self, arg):
    super(Converter, self).__init__(arg)

  def convert(self, locData):
    pass

  def __offset():
    #rotation += 90
    pass

class yRotConverter(RotationConverter):
  def __init__(self, arg):
    super(Converter, self).__init__(arg)

  def convert(self, locData):
    pass

  def __flip_zy():
    pass

class yRotConverter(RotationConverter):
  def __init__(self, arg):
    super(Converter, self).__init__(arg)

  def convert(self, locData):
    pass

  def __flip_zy():
    pass

#
#
#
class PropertySetter(object):
  def __init__(self, propertyLookup, converterFactory, frameCalculator):
    self.frameCalc = frameCalculator

  def set_property(self, blenderObj, propertyName, propValues):
    self.blenderObj = blenderObj
    self.propertyName = propertyName
    self.propValues = propValues

    if (self.__has_keyframes()):
      self.__set_prop_keyframed()
    else:
      self.__set_prop_static()
    pass

  def __has_keyframes(self):
    numProperties = len(self.propValues)
    if(numProperties < 2 and numProperties != 0):
      return False
    #if there is more than 1 value the property has keyframes
    return True

  def __set_prop_static(self):
    propVal = self.propValues[0][1]
    self.__set_prop(propVal)
    

  def __set_prop_keyframed(self):
    for propVal in self.propValues:
      time = propVal[0]
      propVal = propVal[1]
      frame = self.frameCalc.timeToFrame(time)
      self.__set_prop(propVal, frame)

  def __set_prop(self, propVal, frame=-1):
    propData = propertyLookup.prop(self.propertyName)
    dataPath = propData.dataPath
    index    = propData.index

    self.blenderObj[dataPath] = self.Converter(self.propName, propVal)

    if(frame != -1):
      self.blenderObj.keyframe_insert(data_path=dataPath, frame=frame, index=index)

#
#
#
class FrameCalculator(object):
  def __init__(self, frameDuration):
    self.frameDuration = frameDuration

  def timeToFrame(self, time):
    frame = round(time / self.frameDuration)
    return frame

##
filename = "AE2JSON_Comp1.json"
directory = os.path.dirname(bpy.data.filepath)
full_path = directory + "/" +filename 
json_str = open(full_path).read()
json_data = json.loads(json_str)


data_parser = AfterEffectsParser(json_data)
data_parser.add_object_parser('Null', NullParser)
data_parser.add_object_parser('Camera', CameraParser)

data_converter(parsed_data)
data_converter.convert();

main = Main(data_parser)
main.run()

"""
class Main():
  def __init__(self, json_data):
    self.json_data = json_data
    #self.defaultComp = json_data['comps'][0]
    #self.compSettings = self.defaultComp['compSettings']
    #self.relationships = []


  def run(self):
    layers = self.defaultComp['layers']
    for layer in layers:  
      layerType = layer['layerType']

      if(layerType == 'Null'):
        obj = Empty(self.compSettings, layer)
      elif(layerType == 'Solid'):
        obj = Mesh(self.compSettings, layer)
      elif(layerType == 'Camera'):
        obj = Camera(self.compSettings, layer)
      
    #  self.check_for_parent(layer)
    #self.set_parents()

  def check_for_parent(self, child):
    if(child['parent'] != 0):
      self.add_to_relationships(child['parent'], child['name'])

  def add_to_relationships(self, parentName, childName):
    self.relationships.append({'parent': parentName, 'child': childName})

  def set_parents(self):
    print('set_parents')
    for relation in self.relationships:
      child  = bpy.data.objects[relation['child']]
      parent = bpy.data.objects[relation['parent']]

      pMat = parent.matrix_world.inverted()
      child.parent = parent
      child.matrix_parent_inverse = pMat

      # A second way to preform the above...
      #bpy.ops.object.select_all(action='DESELECT')
      #bpy.context.scene.objects.active = parent
      #child.select = True
      #bpy.ops.object.parent_set(type='OBJECT')
"""

"""

class BaseObject(object):
  def __init__(self, compSettings, objData):
    self.compSettings = compSettings
    self.objData = objData
    self.name    = self.objData['name']
    self.parent  = self.objData['parent']
    self.BO      = self.add_to_scene()
    self.BO.name = self.name
    self.BO.show_name = True
    self.set_properties()

  def __set_property(self, propType, propList):
    if self.__is_keyframed(propList):
      self.__set_prop_keyframed(propType, propList)
    else:
      self.__set_prop_static(propType, propList)
      
  def __is_keyframed(self, propList):
    numProperties = len(propList)
    if(numProperties < 2 and numProperties != 0):
      return False

    return True

  def __frame_duration(self):
    return self.compSettings['frameDuration']

  def __get_frame(self, time):
    frameDuration = self.__frame_duration()
    frame = round(time / frameDuration)
    return frame

  def __set_prop_static(self, propType, propList):
    propVal = propList[0][1]
    self.__handle_prop(propType, propVal)

  def __set_prop_keyframed(self, propType, propList):
    for prop in propList:
      #time = prop.time
      #value = prop.value
      time = prop[0]
      propVal = prop[1]
      frame = self.__get_frame(time)
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
        
  def set_properties(self):
    self.__set_property('location', self.__get_location_data())
    self.__set_property('xRotation', self.__get_rotation_data('xRotation'))
    self.__set_property('yRotation', self.__get_rotation_data('yRotation'))
    self.__set_property('zRotation', self.__get_rotation_data('zRotation'))

  # add the object type to the scene and create an instance variable reference for it.
  def add_to_scene(self):
    print("ObjectBase")
    bpy.ops.object.add(type='EMPTY')
    return bpy.context.object




class Empty(BaseObject):
  def __init__(self, compSettings, objData):
    super(Empty, self).__init__(compSettings, objData)

  def add_to_scene(self):
    print("add Empty")
    bpy.ops.object.add(type='EMPTY')
    return bpy.context.object


class Mesh(BaseObject):
  def __init__(self, compSettings, objData):
    super(Mesh, self).__init__(compSettings, objData)

  def add_to_scene(self):
    print("add Mesh")
    bpy.ops.object.add(type='MESH')
    return bpy.context.object


class Camera(BaseObject):
  def __init__(self, compSettings, objData):
    super(Camera, self).__init__(compSettings, objData)

  def add_to_scene(self):
    print("add Camera")
    bpy.ops.object.camera_add()
    return bpy.context.object
"""
