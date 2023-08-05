# Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
# See COPYING for license details.

# $Id: c_math.pxd 154 2010-03-13 13:18:59Z filipw $

cdef extern from "math.h":
    double sqrt (double x)
    double exp (double x)
    double pow (double x, double y)
