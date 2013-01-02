#
# Data Parsers
#
class Parser(object):
  def __init__(self, data):
    self.in_data = data
    self.out_data = {}

  def parse(self):
    pass

#project_settings
#scenes
# objects
#   object properties

class ProjectParser(Parser):
  def __init__(self, data, comp_parser):
    super(ProjectParser, self).__init__(data)

    self.layer_parsers = {}
    print("ProjectParser : Constructor")

  def parse(self):
    project_settings = self.in_data['projectSettings']
    self.out_data['project_settings'] = self.__parse_project_settings(project_settings)

    comps = self.in_data['compositions']
    self.out_data['scenes'] = self.__parse_comps(comps)
    return self.out_data

  def add_layer_parser(self, key, parser_class):
    if key not in self.layer_parsers:
      self.layer_parsers[key] = parser_class

  def __parse_project_settings(self, project_settings):
    return project_settings

  def __parse_comps(self, comps):
    comp_list = []
    for comp in comps:
      comp_list.append(self.__parse_comp(comp))
    return comp_list

  def __parse_comp_settings(self, comp_settings):
    return comp_settings


#
#
#
class CompositionParser(Parser):
  def __init__(self, comp_data, layer_parser):
    super(Parser, self).__init__(comp_data)

  def parse(self):
    comp_settings = comp['compSettings']
    settings = self.__parse_comp_settings(comp_settings)
    #
    layers = comp['layers']
    objects = self.__parse_comp_layers(layers)
    data = {'settings': settings, 'objects': objects}
    return data

  def __parse_comp_layers(self, layers):
    layer_list = []
    for layer in layers:
      layer_type = layer['layerType']
      if layer_type in self.layer_parsers:
        layer_list.append(self.__parse_comp_layer(layer_type, layer))
    return layer_list

  def __parse_comp_layer(self, layer_type, layer):
        obj = self.layer_parsers[layer_type](layer)
        return obj.parse()

#
#
#
class LayerParser(Parser):
  def __init__(self, layer_data):
    super(LayerParser, self).__init__(layer_data)
    print("Layer Parser")

  def parse(self):
    self.__parse_meta_info()
    self.__parse_transform_data()
    self.__parse_instance_data()
    return self.out_data

  def __parse_meta_info(self):
    self.out_data['object_type'] = self.in_data['layerType']
    self.out_data['name']        = self.in_data['name']
    self.out_data['parent']      = self.__parent_check(self.in_data['parent'])

  def __parent_check(self, parent_data):
    if parent_data == 0:
      parent_data = False

    return parent_data

  def __type_converter(self):
    pass

  def __parse_instance_data(self):
    print("Not instituted in LayerParser")

  def __parse_transform_data(self):
    transforms = self.in_data['transform']
    self.out_data['location']   = self.__parse_property('location', transforms['position'])
    self.out_data['rotation_x'] = self.__parse_property('rotation_euler', transforms['xRotation'], 0)
    self.out_data['rotation_y'] = self.__parse_property('rotation_euler', transforms['yRotation'], 1)
    self.out_data['rotation_z'] = self.__parse_property('rotation_euler', transforms['zRotation'], 2)
    self.__flip_rotation_yz_axis(self.out_data['rotation_y'], self.out_data['rotation_z'])

  def __parse_property(self, data_path, property_value_list, index=-1):
    property_data = {}
    property_data['data_path'] = data_path
    property_data['index'] = index
    property_data['keyframe_values'] = self.__create_time_value_dict_list(property_value_list)
    return property_data
    
  def __create_time_value_dict_list(self, time_value_list):
    time_value_pair_list = []
    for time_value in time_value_list:
      time_value_pair_list.append(self.__create_time_value_dict(time_value))
    return time_value_pair_list

  def __create_time_value_dict(self, time_value):
      time_value_dict = {}
      time_value_dict['time']  = time_value[0] # the time value
      time_value_dict['value'] = time_value[1] # the prop value at the above time
      return time_value_dict

  def __flip_rotation_yz_axis(self, rotation_y_list, rotation_z_list):
    self.out_data['rotation_y'] = rotation_z_list
    self.out_data['rotation_z'] = rotation_y_list
    

class PropertyParser(Parser):
  def __init__(self, property_data):
    super(PropertyParser, self).__init__(property_data)

  def parse(self):
    pass


class NullLayerParser(LayerParser):
  def __init__(self, objData):
    super(NullLayerParser, self).__init__(objData)
    print("Null Parser")
 
  def __parse_instance_data(self):
    print("Null has no extra instance data at this time")


class CameraLayerParser(LayerParser):
  def __init__(self, objData):
    super(CameraLayerParser, self).__init__(objData)
    print("Camera Parser")

  def __parse_instance_data(self):
    print("Camera has no extra instance data at this time")
    