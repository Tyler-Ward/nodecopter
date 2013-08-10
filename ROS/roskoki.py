#!/usr/bin/env python
from pykoki import PyKoki, Point2Di, Point2Df, CameraParams
import cv, cv2
import sys

import roslib
roslib.load_manifest('roskoki')
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class roskoki:

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image)

    cv.NamedWindow("Image window", 1)
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv(data, "bgr8")
    except CvBridgeError, e:
      print e

    koki = PyKoki()

    params = CameraParams(Point2Df( cv_image.width/2, cv_image.height/2 ),
                                      Point2Df(571, 571),
                                      Point2Di( cv_image.width, cv_image.height ))

    print koki.find_markers( cv_image, 0.1, params )

    cv.ShowImage("Image window", cv_image)
    cv.WaitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError, e:
      print e

def main(args):
  ic = roskoki()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print "Shutting down"
  cv.DestroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)


