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