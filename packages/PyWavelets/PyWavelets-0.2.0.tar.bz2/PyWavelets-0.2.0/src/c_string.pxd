# Copyright (c) 2006-2010 Filip Wasilewski <http://filipwasilewski.pl/>
# See COPYING for license details.

# $Id: c_string.pxd 154 2010-03-13 13:18:59Z filipw $

cdef extern from "string.h":
	ctypedef long size_t
	void *memcpy(void *dst,void *src,size_t len)
	void *memmove(void *dst,void *src,size_t len)
	char *strdup(char *)
