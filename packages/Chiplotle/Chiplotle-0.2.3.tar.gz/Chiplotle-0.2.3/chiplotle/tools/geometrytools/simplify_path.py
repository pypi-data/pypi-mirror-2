import numpy
from chiplotle.tools.geometrytools.angle import angle

def simplify_path(path, threshold):
   '''Removes points in a path that are along a (almost) straight line.
   
   - `path`: a list or numpy array of 2-d absolute coordinate values. 
   - `threshod`: the angle value above which points in the path will be 
      preserved.
   '''
   if threshold < 0:
      raise ValueError('threshold must be >= 0.')
   if threshold == 0:
      return numpy.array(path)

   path = numpy.array(path)
   path_diff = numpy.diff(path, axis=0) 
   angles = [ ]
   ## get angles between relative vector regments...
   for x, y in zip(path_diff[0:-1], path_diff[1:]):
      ## if vectors have no length, skip.
      if (numpy.sum(x) == 0 or numpy.sum(y) == 0):
         ang = 0
      else:
         ang = angle(x, y)
      angles.append(ang)
   angles_diff = numpy.abs(numpy.diff(angles))
   indxs = angles_diff >= threshold
   ## make sure the first and last points are always added...
   ## lost one in path_diff, one in for loop, and one in angles_diff
   significant_indxs = numpy.concatenate([[True], indxs, [True, True]])
   return path[significant_indxs]
         


