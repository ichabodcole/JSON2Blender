#
# Converters
#
class Converter(object):
  def __init__(self, arg):
    pass

  def convert(self):
    pass

class PropertyConvert(Converter):
  def __init__(self):
    self.property_converters = {}

  def add_converter(self, key, converter):
    if key not in self.property_converters:
      self.property_converters[key] = converter

  def convert(self, converter_key):
    property_converter = self.property_converters[converter_key]
    converted_property = property_converter(prop_val)
    return converted_property

class LocationConverter(Converter):
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


class RotationConverter(Converter):
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