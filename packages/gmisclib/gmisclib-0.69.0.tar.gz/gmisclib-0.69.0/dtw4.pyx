# include "stdlib.pxi"
# include "math.pxi"
# cython: cdivision=True

cdef extern from "math.h":
	double fabs(double x) nogil
	double pow(double y, double x) nogil

cdef extern from "gpklib.h":
	float **float2alloc(int a, int b) nogil
	void float2free(float **x) nogil

import cython
# import numpy
import numpy
cimport numpy
cimport stdlib
ctypedef numpy.float_t DTYPE
ctypedef numpy.float_t FTYPE
ctypedef numpy.int32_t ITYPE

cdef struct node
ctypedef node node_t

cdef struct node:
	int i, j
	double d
	double gdist
	node_t *best


cdef class state_c:
	cdef node *nodes
	cdef int nx, ny, nparams
	cdef double alpha, beta
	cdef double BIG
	cdef float **x, **y

	def __cinit__(self, numpy.ndarray[FTYPE, ndim=2] x, numpy.ndarray[FTYPE, ndim=2] y,
				double alpha, double beta):
		self.nx = x.shape[1]
		self.ny = y.shape[1]
		self.nodes = <node_t *>stdlib.malloc(cython.sizeof(node)*self.nx*self.ny)
		self.x = float2alloc(x.shape[0], x.shape[1])
		self.y = float2alloc(y.shape[0], y.shape[1])

	def __dealloc__(self):
		stdlib.free(self.nodes)
		float2free(self.x)
		float2free(self.y)

	cdef node_t * gn(self, int i, int j) nogil:
		return & self.nodes[ i + self.nx*j ]

	def __init__(self, numpy.ndarray[FTYPE, ndim=2] x, numpy.ndarray[FTYPE, ndim=2] y,
				double alpha, double beta):
		assert x.shape[0]==y.shape[0]
		self.nparams = x.shape[0]
		cdef int i, j
		for i from 0 <= i < self.nparams:
			for  j from 0 <= j < self.nx:
				self.x[i][j] = x[i,j]
			for  j from 0 <= j < self.ny:
				self.y[i][j] = y[i,j]
		cdef node_t *n
		with nogil:
			for i from 0 <= i < self.nx*self.ny:
				n = & self.nodes[i]
				n.i = i % self.nx
				n.j = i // self.nx
				n.best = <node_t *>0
				n.d = -1.0
				n.gdist = -1.0
		self.gn(0, 0).gdist = 0.0
		self.alpha = alpha
		self.beta = beta
		self.BIG = 1e30
		

	cdef double get(self, int i, int j) nogil:
		cdef double s
		cdef node_t * n = self.gn(i, j)
		if n.d < 0.0:
			s = 0.0
			for k from 0 <= k < self.nparams:
				s += pow(fabs(self.x[k][i]-self.y[k][j]), self.alpha)
			n.d = pow(s, self.beta)
		return n.d


	cdef double search(self, int i, int j) nogil:
		cdef node_t * n = self.gn(i, j)
		if n.gdist >= 0:
			return n.gdist
		elif i==0 and j==0:
			n.best = <node_t *>0
			n.gdist = 0.0
			return n.gdist

		cdef double gi, gj, gij
		if i > 0:
			gi = self.search(i-1, j) + self.get(i-1, j)
		else:
			gi = self.BIG

		if j > 0:
			gj = self.search(i, j-1) + self.get(i, j-1)
		else:
			gj = self.BIG

		if i>0 and j>0:
			gij = self.search(i-1, j-1) + self.get(i-1, j-1)
		else:
			gij = self.BIG

		cdef double gbest = self.BIG
		if gij <= gi and gij <= gj:
			n.best = self.gn(i-1, j-1)
			n.gdist = gij
			# print 'n=', n.i, n.j, '->', n.best.i, n.best.j, 'cost=', n.gdist
		elif gi <= gij and gi <= gj:
			# print "%d,%d -> %d,%d cost %.1f" % (n.i. n.j, n.i-1, n.j, gi)
			n.best = self.gn(i-1, j)
			n.gdist = gi
			# print 'n=', n.i, n.j, '->', n.best.i, n.best.j, 'cost=', n.gdist
		else:
			# gj <= gij and gj <= gi:
			# print "%d,%d -> %d,%d cost %.1f" % (n.i. n.j, n.i, n.j-1, gj)
			n.best = self.gn(i, j-1)
			n.gdist = gj
			# print 'n=', n.i, n.j, '->', n.best.i, n.best.j, 'cost=', n.gdist
		return n.gdist


	cdef numpy.ndarray path(self, int i, int j):
		cdef node_t * n = self.gn(i, j)
		cdef int ns = 0
		with nogil:
			while n:
				n = n.best
				ns += 1
		cdef numpy.ndarray[ITYPE, ndim=2, mode="c"] o = numpy.zeros((ns, 2), numpy.int32)
		n = self.gn(i, j)
		ns -= 1
		while ns >= 0:
			# print 'Walking %d,%d' % (n.i, n.j)
			o[ns, 0] = n.i
			o[ns, 1] = n.j
			n = n.best
			ns -= 1
		return o


def dtw(x, y, alpha, beta):
	if x.shape[0] != y.shape[0]:
		raise ValueError, "Feature vectors different lengths: %d and %d" % (x.shape[0], y.shape[0])
	cdef state_c s = state_c(x, y, alpha, beta)
	with nogil:
		s.search(s.nx-1, s.ny-1)
	return s.path(s.nx-1, s.ny-1)



def test_same():
	LEN = 100
	FVL = 10
	x = numpy.random.normal(size=(FVL,LEN))
	q = dtw(x, x, 2, 1)
	assert numpy.equal(q[:,0], q[:,1]).all()

def test_partial():
	LEN = 11
	FVL = 20
	x = numpy.random.normal(size=(FVL,LEN))
	y = numpy.array(x, copy=True)
	y[0:6,:] = 0
	q = dtw(x, y, 2, 1)
	assert numpy.equal(q[:,0], q[:,1]).all()

def test_scaled():
	LEN = 20
	FVL = 30
	x = numpy.random.normal(size=(FVL,LEN))
	y = x*0.5
	q = dtw(x, y, 2, 1)
	assert numpy.equal(q[:,0], q[:,1]).all()

def test_stretched():
	LEN = 7
	FVL = 30
	x = numpy.random.normal(size=(FVL,LEN))
	y = numpy.zeros((FVL,2*LEN))
	for i in range(x.shape[1]):
		y[:,2*i] = x[:,i]
		y[:,2*i+1] = x[:,i]
	q = dtw(x, y, 2, 1)
	for i in range(x.shape[1]):
		assert q[i,1]==2*q[i,0] or q[i,1]==2*q[i,0]+1


def test():
	test_same()
	test_partial()
	test_scaled()
	test_stretched()

test()

import gpkimgclass
from gmisclib import edit_distance

def namelist(x):
	i = 0
	rv = []
	while 'TTYPE%d'%i in x.hdr:
		rv.append(x.hdr['TTYPE%d' % i])
		i += 1
	return rv

def check_names(x, y, approx_name):
	xn = namelist(x)
	yn = namelist(y)
	if approx_name:
		xs = ';'.join(xn)
		ys = ';'.join(yn)
		return edit_distance.distf(xs, ys, edit_distance.def_cost) < 0.1*0.5*(len(xs)+len(ys))
	return xn == yn


def dtw_ti(x, y, alpha, beta, x0=None, xe=None, y0=None, ye=None, approx_name=False):
	"""
	@type x: gpkimgclass.gpk_img
	@type y: gpkimgclass.gpk_img
	"""
	if x.d.shape[0] != y.d.shape[0]:
		raise ValueError, "Feature vectors different lengths: %d and %d" % (x.d.shape[0], y.d.shape[0])
	if not check_names(x, y, approx_name):
		raise ValueError, "Feature vectors are too different."
	if x0 is None:
		i0 = 0
	else:
		i0 = int(round(x.t_index(x0)))
	if xe is None:
		ie = x.d.shape[1]
	else:
		ie = int(round(x.t_index(xe)))
	if y0 is None:
		j0 = 0
	else:
		j0 = int(round(y.t_index(y0)))
	if ye is None:
		je = y.d.shape[1]
	else:
		je = int(round(y.t_index(ye)))
	imap = dtw(x.d[:,i0:ie+1], y.d[:,j0,je+1], alpha, beta)
	rv = numpy.array([x.time(imap[:,0]), y.time(imap[:,1])], axis=1)
	assert rv.shape[1] == 2
	return rv

