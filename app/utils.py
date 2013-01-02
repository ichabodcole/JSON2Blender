#
#
#
class FrameCalculator(object):
  def __init__(self, frameDuration):
    self.frameDuration = frameDuration

  def timeToFrame(self, time):
    frame = round(time / self.frameDuration)
    return frame