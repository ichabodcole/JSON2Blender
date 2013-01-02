#
#
#
class PropertySetter(object):
  def __init__(self, propertyLookup):
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
    dataPath = propData.dataPath
    index    = propData.index

    self.blenderObj[dataPath] = propVal

    if(frame != -1):
      self.blenderObj.keyframe_insert(data_path=dataPath, frame=frame, index=index)