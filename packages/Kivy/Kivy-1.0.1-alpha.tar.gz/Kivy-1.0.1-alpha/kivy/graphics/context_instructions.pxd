cdef class LineWidth
cdef class Color
cdef class BindTexture

from transformation cimport Matrix
from instructions cimport ContextInstruction
from texture cimport Texture

cdef class LineWidth(ContextInstruction):
    cdef apply(self)

cdef class Color(ContextInstruction):
    cdef apply(self)

cdef class BindTexture(ContextInstruction):
    cdef str _source
    cdef Texture _texture
    cdef apply(self)


cdef class PushMatrix(ContextInstruction):
    cdef apply(self)

cdef class PopMatrix(ContextInstruction):
    cdef apply(self)

cdef class MatrixInstruction(ContextInstruction):
    cdef Matrix matrix
    cdef apply(self)

cdef class Transform(MatrixInstruction):
    cpdef transform(self, Matrix trans)
    cpdef translate(self, float tx, float ty, float tz)
    cpdef rotate(self, float angle, float ax, float ay, float az)
    cpdef scale(self, float s)
    cpdef identity(self)
    cdef apply(self)

cdef class Rotate(Transform):
    cdef float _angle
    cdef tuple _axis
    cdef apply(self)

cdef class Scale(Transform):
    cdef float s
    cdef apply(self)



cdef class Translate(Transform):
    cdef float _x, _y, _z
    cdef apply(self)


