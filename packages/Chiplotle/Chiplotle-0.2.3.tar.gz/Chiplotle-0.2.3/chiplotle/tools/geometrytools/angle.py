from __future__ import division
import numpy
import math

def angle(vect1, vect2):
   '''Returns the angle between two vectors.'''
   
   vect1_norm = numpy.linalg.norm(vect1)
   vect2_norm = numpy.linalg.norm(vect2)
   if vect1_norm == 0 or vect2_norm == 0:
      raise ValueError('vect1 and vect2 must have norm > 0.')

   vect1 = numpy.array(vect1, dtype=float)
   vect2 = numpy.array(vect2, dtype=float)
   correlation = numpy.sum(vect1 * vect2) 
   cos = correlation / (vect1_norm * vect2_norm)
   return math.acos(cos)


