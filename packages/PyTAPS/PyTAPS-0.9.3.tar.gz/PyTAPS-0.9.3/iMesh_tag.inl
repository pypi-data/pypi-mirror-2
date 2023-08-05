#include "iMesh_Python.h"
#include "iBase_Python.h"
#include "errors.h"
#include "structmember.h"

static int
iMeshTagObj_init(iMeshTag_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"tag","instance",0};
    iMesh_Object *instance=0;
    iBaseTag_Object *tag;

    if( !PyArg_ParseTupleAndKeywords(args,kw,"O!|O!",kwlist,&iBaseTag_Type,
                                     &tag,&iMesh_Type,&instance))
        return -1;

    if(instance)
    {
        if(iMeshTag_Check(tag))
        {
            PyErr_SetString(PyExc_ValueError,ERR_MESH_TAG_CTOR);
            return -1;
        }
        self->instance = instance;
    }
    else
    {
        if(!iMeshTag_Check(tag))
        {
            PyErr_SetString(PyExc_ValueError,ERR_EXP_INSTANCE);
            return -1;
        }
        self->instance = iMeshTag_GetInstance(tag);
    }

    self->base.handle = tag->handle;
    Py_XINCREF(self->instance);
    return 0;
}

static void
iMeshTagObj_dealloc(iMeshTag_Object *self)
{
    Py_XDECREF(self->instance);
    ((PyObject*)self)->ob_type->tp_free((PyObject*)self);
}

static PyObject *
iMeshTagObj_getName(iMeshTag_Object *self,void *closure)
{
    char name[512];
    int err;
    iMesh_getTagName(self->instance->handle,self->base.handle,name,&err,
                     sizeof(name));
    if(checkError(self->instance->handle,err))
        return NULL;

    return PyString_FromString(name);
}

static PyObject *
iMeshTagObj_getSizeValues(iMeshTag_Object *self,void *closure)
{
    int size,err;
    iMesh_getTagSizeValues(self->instance->handle,self->base.handle,&size,&err);
    if(checkError(self->instance->handle,err))
        return NULL;

    return PyInt_FromLong(size);
}

static PyObject *
iMeshTagObj_getSizeBytes(iMeshTag_Object *self,void *closure)
{
    int size,err;
    iMesh_getTagSizeBytes(self->instance->handle,self->base.handle,&size,&err);
    if(checkError(self->instance->handle,err))
        return NULL;

    return PyInt_FromLong(size);
}

static PyObject *
iMeshTagObj_getType(iMeshTag_Object *self,void *closure)
{
    int type,err;
    iMesh_getTagType(self->instance->handle,self->base.handle,&type,&err);
    if(checkError(self->instance->handle,err))
        return NULL;

    return Py_BuildValue("c",iBaseTagType_ToChar(type));
}

static PyObject *
iMeshTagObj_setData(iMeshTag_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","data","type",0};
    PyObject *obj;
    PyObject *data_obj;
    int type = -1;
    int err;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"OO|O&",kwlist,&obj,&data_obj,
                                    &type))
        return NULL;

    if(type == -1)
    {
        /* infer the type of the data */
        iMesh_getTagType(self->instance->handle,self->base.handle,&type,&err);
        if(checkError(self->instance->handle,err))
            return NULL;
    }
 
    PyObject *ents = PyArray_TryFromObject(obj,NPY_IBASEENT,1,1);
    if(ents)
    {
        int ent_size;
        iBase_EntityHandle *entities;
        int data_size;
        PyObject *data_arr=0;

        ent_size = PyArray_SIZE(ents);
        entities = PyArray_DATA(ents);

        if(type == iBase_INTEGER)
        {
            data_arr = PyArray_FROMANY(data_obj,NPY_INT,1,1,NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            data_size = PyArray_SIZE(data_arr);
            int *data = PyArray_DATA(data_arr);
            iMesh_setIntArrData(self->instance->handle,entities,ent_size,
                                self->base.handle,data,data_size,&err);
        }
        else if(type == iBase_DOUBLE)
        {
            data_arr = PyArray_FROMANY(data_obj,NPY_DOUBLE,1,1,
                                       NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            data_size = PyArray_SIZE(data_arr);
            double *data = PyArray_DATA(data_arr);
            iMesh_setDblArrData(self->instance->handle,entities,ent_size,
                                self->base.handle,data,data_size,&err);
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            data_arr = PyArray_FROMANY(data_obj,NPY_IBASEENT,1,1,
                                       NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            data_size = PyArray_SIZE(data_arr);
            iBase_EntityHandle *data = PyArray_DATA(data_arr);
            iMesh_setEHArrData(self->instance->handle,entities,ent_size,
                               self->base.handle,data,data_size,&err);
        }
        else /* iBase_BYTES */
        {
            data_arr = PyArray_FROMANY(data_obj,NPY_BYTE,1,1,NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            data_size = PyArray_SIZE(data_arr);
            char *data = PyArray_DATA(data_arr);
            iMesh_setArrData(self->instance->handle,entities,ent_size,
                             self->base.handle,data,data_size,&err);
        }

        Py_DECREF(ents);
        Py_XDECREF(data_arr);
    }
    else if(iBaseEntitySet_Check(obj))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GetHandle(obj);

        if(type == iBase_INTEGER)
        {
            PyObject *o = PyNumber_Int(data_obj);
            if(o == NULL)
                return NULL;
            iMesh_setEntSetIntData(self->instance->handle,set,self->base.handle,
                                   PyInt_AsLong(o),&err);
            Py_DECREF(o);
        }
        else if(type == iBase_DOUBLE)
        {
            PyObject *o = PyNumber_Float(data_obj);
            if(o == NULL)
                return NULL;
            iMesh_setEntSetDblData(self->instance->handle,set,self->base.handle,
                                   PyFloat_AsDouble(o),&err);
            Py_DECREF(o);
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            if(!iBaseEntity_Check(data_obj))
                return NULL;
            iMesh_setEntSetEHData(self->instance->handle,set,self->base.handle,
                                  iBaseEntity_GetHandle(data_obj),&err);
        }
        else /* iBase_BYTES */
        {
            PyObject *data_arr = PyArray_FROMANY(data_obj,NPY_BYTE,1,1,
                                                 NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            char *data = PyArray_DATA(data_arr);
            int data_size = PyArray_SIZE(data_arr);
            iMesh_setEntSetData(self->instance->handle,set,self->base.handle,
                                data,data_size,&err);
            Py_DECREF(data_arr);
        }
    }
    else if(iBaseEntity_Check(obj))
    {
        iBase_EntityHandle entity = iBaseEntity_GetHandle(obj);

        if(type == iBase_INTEGER)
        {
            PyObject *o = PyNumber_Int(data_obj);
            if(o == NULL)
                return NULL;
            iMesh_setIntData(self->instance->handle,entity,self->base.handle,
                             PyInt_AsLong(o),&err);
            Py_DECREF(o);
        }
        else if(type == iBase_DOUBLE)
        {
            PyObject *o = PyNumber_Float(data_obj);
            if(o == NULL)
                return NULL;
            iMesh_setDblData(self->instance->handle,entity,self->base.handle,
                             PyFloat_AsDouble(o),&err);
            Py_DECREF(o);
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            if(!iBaseEntity_Check(data_obj))
                return NULL;
            iMesh_setEHData(self->instance->handle,entity,self->base.handle,
                            iBaseEntity_GetHandle(data_obj),&err);
        }
        else /* iBase_BYTES */
        {
            PyObject *data_arr = PyArray_FROMANY(data_obj,NPY_BYTE,1,1,
                                                 NPY_C_CONTIGUOUS);
            if(data_arr == NULL)
                return NULL;

            char *data = PyArray_DATA(data_arr);
            int data_size = PyArray_SIZE(data_arr);
            iMesh_setData(self->instance->handle,entity,self->base.handle,data,
                          data_size,&err);
            Py_DECREF(data_arr);
        }
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return NULL;
    }

    if(checkError(self->instance->handle,err))
        return NULL;
    Py_RETURN_NONE;
}

static PyObject *
iMeshTagObj_getData(iMeshTag_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","type",0};
    PyObject *obj;
    int type = -1;
    int err;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O|O&",kwlist,&obj,iBaseTagType_Cvt,
                                    &type))
        return NULL;

    if(type == -1)
    {
        /* infer the type of the data */
        iMesh_getTagType(self->instance->handle,self->base.handle,&type,&err);
        if(checkError(self->instance->handle,err))
            return NULL;
    }

    PyObject *ents = PyArray_TryFromObject(obj,NPY_IBASEENT,1,1);
    if(ents)
    {
        int ent_size = PyArray_SIZE(ents);
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        PyObject *ret = 0;

        if(type == iBase_INTEGER)
        {
            int *data=0;
            int alloc=0,size;

            iMesh_getIntArrData(self->instance->handle,entities,ent_size,
                                self->base.handle,&data,&alloc,&size,&err);
            if(!checkError(self->instance->handle,err))
            {
                npy_intp dims[] = {size};
                ret = PyArray_NewFromMalloc(1,dims,NPY_INT,data);
            }
        }
        else if(type == iBase_DOUBLE)
        {
            double *data=0;
            int alloc=0,size;

            iMesh_getDblArrData(self->instance->handle,entities,ent_size,
                                self->base.handle,&data,&alloc,&size,&err);
            if(!checkError(self->instance->handle,err))
            {
                npy_intp dims[] = {size};
                ret = PyArray_NewFromMalloc(1,dims,NPY_DOUBLE,data);
            }
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            iBase_EntityHandle *data=0;
            int alloc=0,size;

            iMesh_getEHArrData(self->instance->handle,entities,ent_size,
                               self->base.handle,&data,&alloc,&size,&err);
            if(!checkError(self->instance->handle,err))
            {
                npy_intp dims[] = {size};
                ret = PyArray_NewFromMalloc(1,dims,NPY_IBASEENT,data);
            }
        }
        else /* iBase_BYTES */
        {
            char *data=0;
            int alloc=0,size;

            iMesh_getArrData(self->instance->handle,entities,ent_size,
                             self->base.handle,&data,&alloc,&size,&err);
            if(!checkError(self->instance->handle,err))
            {
                npy_intp dims[] = {size};
                ret = PyArray_NewFromMalloc(1,dims,NPY_BYTE,data);
            }
        }

        Py_DECREF(ents);
        return ret;
    }
    else if(iBaseEntitySet_Check(obj))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GetHandle(obj);

        if(type == iBase_INTEGER)
        {
            int data;
            iMesh_getEntSetIntData(self->instance->handle,set,
                                   self->base.handle,&data,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            return PyInt_FromLong(data);
        }
        else if(type == iBase_DOUBLE)
        {
            double data;
            iMesh_getEntSetDblData(self->instance->handle,set,
                                   self->base.handle,&data,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            return PyFloat_FromDouble(data);
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            iBaseEntity_Object *data = iBaseEntity_New();
            iMesh_getEntSetEHData(self->instance->handle,set,self->base.handle,
                                  &data->handle,&err);
            if(checkError(self->instance->handle,err))
            {
                Py_DECREF(data);
                return NULL;
            }
            return (PyObject*)data;
        }
        else /* iBase_BYTES */
        {
            char *data=0;
            int alloc=0,size;
            iMesh_getEntSetData(self->instance->handle,set,self->base.handle,
                                &data,&alloc,&size,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            npy_intp dims[] = {size};
            return PyArray_NewFromMalloc(1,dims,NPY_BYTE,data);
        }
    }
    else if(iBaseEntity_Check(obj))
    {
        iBase_EntityHandle entity = iBaseEntity_GetHandle(obj);

        if(type == iBase_INTEGER)
        {
            int data;
            iMesh_getIntData(self->instance->handle,entity,self->base.handle,
                             &data,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            return PyInt_FromLong(data);
        }
        else if(type == iBase_DOUBLE)
        {
            double data;
            iMesh_getDblData(self->instance->handle,entity,self->base.handle,
                             &data,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            return PyFloat_FromDouble(data);
        }
        else if(type == iBase_ENTITY_HANDLE)
        {
            iBaseEntity_Object *data = iBaseEntity_New();
            iMesh_getEHData(self->instance->handle,entity,self->base.handle,
                            &data->handle,&err);
            if(checkError(self->instance->handle,err))
            {
                Py_DECREF(data);
                return NULL;
            }
            return (PyObject*)data;
        }
        else /* iBase_BYTES */
        {
            char *data=0;
            int alloc=0,size;
            iMesh_getData(self->instance->handle,entity,self->base.handle,&data,
                          &alloc,&size,&err);
            if(checkError(self->instance->handle,err))
                return NULL;
            npy_intp dims[] = {size};
            return PyArray_NewFromMalloc(1,dims,NPY_BYTE,data);
        }
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return NULL;
    }
}

static PyObject *
iMeshTagObj_remove(iMeshTag_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities",0};
    PyObject *obj;
    int err;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O",kwlist,&obj))
        return NULL;

    PyObject *ents = PyArray_TryFromObject(obj,NPY_IBASEENT,1,1);
    if(ents)
    {
        int ent_size = PyArray_SIZE(ents);
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        iMesh_rmvArrTag(self->instance->handle,entities,ent_size,
                        self->base.handle,&err);
        Py_DECREF(ents);
    }
    else if(iBaseEntitySet_Check(obj))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GetHandle(obj);
        iMesh_rmvEntSetTag(self->instance->handle,set,self->base.handle,&err);
    }
    else if(iBaseEntity_Check(obj))
    {
        iBase_EntityHandle entity = iBaseEntity_GetHandle(obj);
        iMesh_rmvTag(self->instance->handle,entity,self->base.handle,&err);
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return NULL;
    }

    if(checkError(self->instance->handle,err))
        return NULL;
    Py_RETURN_NONE;
}

static PyObject *
iMeshTagObj_repr(iMeshTag_Object *self)
{
    char name[512];
    int err;
    iMesh_getTagName(self->instance->handle,self->base.handle,name,&err,
                     sizeof(name));
    if(checkError(self->instance->handle,err))
    {
        PyErr_Clear();
        return PyString_FromFormat("<itaps.iMesh.Tag %p>",self->base.handle);
    }
    else
    {
        return PyString_FromFormat("<itaps.iMesh.Tag '%s' %p>",name,
                                   self->base.handle);
    }
}

static PyObject *
iMeshTagObj_richcompare(iMeshTag_Object *lhs,
                        iMeshTag_Object *rhs,int op)
{
    if(!iMeshTag_Check(lhs) || !iMeshTag_Check(rhs))
    {
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }

    switch(op)
    {
    case Py_EQ:
        return PyBool_FromLong(lhs->base.handle == rhs->base.handle &&
                               lhs->instance->handle == rhs->instance->handle);
    case Py_NE:
        return PyBool_FromLong(lhs->base.handle != rhs->base.handle ||
                               lhs->instance->handle != rhs->instance->handle);
    default:
        PyErr_SetNone(PyExc_TypeError);
        return NULL;
    }
}

static long
iMeshTagObj_hash(iMeshTag_Object *self)
{
    return (long)self->base.handle;
}


static PyMethodDef iMeshTagObj_methods[] = {
    { "setData", (PyCFunction)iMeshTagObj_setData, METH_KEYWORDS,
      "Set tag values on an entity (or array/set of entities)"
    },
    { "getData", (PyCFunction)iMeshTagObj_getData, METH_KEYWORDS,
      "Get tag values on an entity (or array/set of entities)"
    },
    { "remove", (PyCFunction)iMeshTagObj_remove, METH_KEYWORDS,
      "Remove a tag value from an entity (or array/set of entities)"
    },
    {0}
};

static PyMemberDef iMeshTagObj_members[] = {
    {"instance", T_OBJECT_EX, offsetof(iMeshTag_Object, instance), READONLY,
     "base iMesh instance"},
    {0}
};

static PyGetSetDef iMeshTagObj_getset[] = {
    { "name", (getter)iMeshTagObj_getName, 0,
      "Get the name for a given tag handle", 0
    },
    { "sizeValues", (getter)iMeshTagObj_getSizeValues, 0,
      "Get size of a tag in units of numbers of tag data type", 0
    },
    { "sizeBytes", (getter)iMeshTagObj_getSizeBytes, 0,
      "Get size of a tag in units of bytes", 0
    },
    { "type", (getter)iMeshTagObj_getType, 0,
      "Get the data type of the specified tag handle", 0
    },
    {0}
};


static PyTypeObject iMeshTag_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
    "itaps.iMesh.Tag",                        /* tp_name */
    sizeof(iMeshTag_Object),                  /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)iMeshTagObj_dealloc,          /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    (reprfunc)iMeshTagObj_repr,               /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    (hashfunc)iMeshTagObj_hash,               /* tp_hash */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    "iMesh tag object",                       /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    (richcmpfunc)iMeshTagObj_richcompare,     /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    iMeshTagObj_methods,                      /* tp_methods */
    iMeshTagObj_members,                      /* tp_members */
    iMeshTagObj_getset,                       /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    (initproc)iMeshTagObj_init,               /* tp_init */
    0,                                        /* tp_alloc */
    0,                                        /* tp_new */
};

