import __builtin__
import sys
import math
from numpy import isscalar, array, zeros

cdef extern from "complex.h":
	ctypedef struct Complex "complex":
		double re
		double im

#	ctypedef complex* pcomplex
	ctypedef double * pdouble

cdef extern from "mie.h":
	cdef void Mie (double x,  Complex m, double *mu, long nangles,  Complex *s1, Complex *s2, double *qext, double *qsca, double *qback, double *g)
	cdef extern void ez_Mie (double x, double n, double *qsca, double *g)
	cdef extern void Qbsc_Mie(double x, double n, double im, double *qbsc, double *g)

def QbscMie(x, m):
	cdef double qbsc, g
	qbsc=0
	g=0
	Qbsc_Mie(x, m.real, m.imag, &qbsc, &g)
	return qbsc, g
	

def QbscMieV(x, m):
	qbsc = []
	g = []
	N=len(x)
	for i in range(N):
		[qtmp, gtmp] = QbscMie(x[i], m.real, m.imag)
		qbsc.append(qtmp)
		g.append(gtmp)
	return qbsc, g

#def ezMie(x, n):
#	cdef double qsca, g
#	qsca=0
#	g=0
#	ez_Mie(x, n, &qsca, &g)
#	return qsca, g

def QMie(x, m):
	cdef double mu, qext, qsca, qback, g
	cdef Complex s1, s2, n
	mu=0
	qext=0
	qsca=0
	qback=0
	g=0
	n.re = m.real
	n.im = m.imag
	s1.re = 0
	s1.im = 0
	s2.re = 0
	s2.im = 0
	Mie(x, n, &mu, 0, &s1, &s2, &qext, &qsca, &qback, &g)
	S1=complex(s1.re, s1.im)
	S2=complex(s2.re, s2.im)
	return qext, qsca, qback, mu, S1, S2, g

def MieExt(x, m):
	if isscalar(x):
		qext, qsca, qback, mu, S1, S2, g = QMie(x, m)
	else:
		N=len(x)
		qext=zeros(N)
		for i in range(N):
			qext[i], qsca, qback, mu, S1, S2, g = QMie(x[i], m)
	return qext

def MieSca(x, m):
	if isscalar(x):
		qext, qsca, qback, mu, S1, S2, g = QMie(x, m)
	else:
		N=len(x)
		qsca=zeros(N)
		for i in range(N):
			qext, qsca[i], qback, mu, S1, S2, g = QMie(x[i], m)
	return qsca

def MieBsc(x, m):
	if isscalar(x):
		qext, qsca, qback, mu, S1, S2, g = QMie(x, m)
	else:
		N=len(x)
		qback=zeros(N)
		for i in range(N):
			qext, qsca, qback[i], mu, S1, S2, g = QMie(x[i], m)
	return qback

