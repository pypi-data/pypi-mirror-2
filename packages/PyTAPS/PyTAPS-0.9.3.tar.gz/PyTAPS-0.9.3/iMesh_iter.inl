#include "iMesh_Python.h"
#include "iBase_Python.h"
#include "structmember.h"

static int
iMeshIterObj_init(iMeshIter_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"set","type","topo","size",0};
    iMeshEntitySet_Object *set;
    int type = iBase_ALL_TYPES;
    int topo = iMesh_ALL_TOPOLOGIES;
    int array_size = 1;
    int err;

    if( !PyArg_ParseTupleAndKeywords(args,kw,"O!|O&O&i",kwlist,
                                     &iMeshEntitySet_Type,&set,iBaseType_Cvt,
                                     &type,iMeshTopology_Cvt,&topo,&array_size))
        return -1;

    self->instance = set->instance;
    Py_INCREF(self->instance);

    if(array_size == 1)
    {
        self->is_arr = 0;
        iMesh_initEntIter(self->instance->handle,set->base.handle,type,topo,
                          &self->iter.one,&err);
    }
    else
    {
        self->is_arr = 1;
        iMesh_initEntArrIter(self->instance->handle,set->base.handle,type,topo,
                             array_size,&self->iter.arr,&err);
    }
    if(checkError(self->instance->handle,err))
        return -1;

    return 0;
}

static void
iMeshIterObj_dealloc(iMeshIter_Object *self)
{
    if(self->instance && self->iter.one)
    {
        int err;
        if(self->is_arr)
            iMesh_endEntArrIter(self->instance->handle,self->iter.arr,&err);
        else
            iMesh_endEntIter(self->instance->handle,self->iter.one,&err);
    }

    Py_XDECREF(self->instance);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
iMeshIterObj_reset(iMeshIter_Object *self)
{
    int err;
    if(self->is_arr)
        iMesh_resetEntArrIter(self->instance->handle,self->iter.arr,&err);
    else
        iMesh_resetEntIter(self->instance->handle,self->iter.one,&err);

    if(checkError(self->instance->handle,err))
        return NULL;
    Py_RETURN_NONE;
}

static PyObject *
iMeshIterObj_iternext(iMeshIter_Object *self)
{
    int has_data,err;

    if(self->is_arr)
    {
        iBase_EntityHandle *entities=0;
        int alloc=0,size;

        iMesh_getNextEntArrIter(self->instance->handle,self->iter.arr,&entities,
                                &alloc,&size,&has_data,&err);
        if(checkError(self->instance->handle,err))
            return NULL;
        if(!has_data)
            return NULL;

        npy_intp dims[] = {size};
        return PyArray_NewFromMalloc(1,dims,NPY_IBASEENT,entities);
    }
    else
    {
        iBase_EntityHandle entity;
        iMesh_getNextEntIter(self->instance->handle,self->iter.one,&entity,
                             &has_data,&err);
        if(checkError(self->instance->handle,err))
            return NULL;
        if(!has_data)
            return NULL;

        iBaseEntity_Object *o = iBaseEntity_New();
        o->handle = entity;
        return (PyObject*)o;
    }
}

static PyMethodDef iMeshIterObj_methods[] = {
    { "reset", (PyCFunction)iMeshIterObj_reset, METH_NOARGS,
      "Reset the iterator"
    },
    {0}
};

static PyMemberDef iMeshIterObj_members[] = {
    {"instance", T_OBJECT_EX, offsetof(iMeshIter_Object, instance), READONLY,
     "base iMesh instance"},
    {0}
};

static PyTypeObject iMeshIter_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
    "itaps.iMesh.Iterator",                   /* tp_name */
    sizeof(iMeshIter_Object),                 /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)iMeshIterObj_dealloc,         /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    0,                                        /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_ITER |
    Py_TPFLAGS_BASETYPE,                      /* tp_flags */
    "iMesh iterator object",                  /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    0,                                        /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    PyObject_SelfIter,                        /* tp_iter */
    (iternextfunc)iMeshIterObj_iternext,      /* tp_iternext */
    iMeshIterObj_methods,                     /* tp_methods */
    iMeshIterObj_members,                     /* tp_members */
    0,                                        /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    (initproc)iMeshIterObj_init,              /* tp_init */
    0,                                        /* tp_alloc */
    0,                                        /* tp_new */
};
