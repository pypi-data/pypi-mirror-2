#include "errors.h"
#include "iRel_Python.h"
#include "iBase_Python.h"
#include "structmember.h"

static int
get_entity_data(PyObject *obj,PyObject **array,iBase_EntityHandle **entities,
                int *size)
{
    if((*array = PyArray_TryFromObject(obj,NPY_IBASEENT,1,1)) != NULL)
    {
        *entities = PyArray_DATA(*array);
        *size = PyArray_SIZE(*array);
    }
    else if(iBaseEntity_Check(obj))
    {
        *entities = &iBaseEntity_GET_HANDLE(obj);
        *size = 1;
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return 0;
    }
    return 1;
}

static int
get_entityset_data(PyObject *obj,PyObject **array,iBase_EntitySetHandle **sets,
                   int *size)
{
    if((*array = PyArray_TryFromObject(obj,NPY_IBASEENTSET,1,1)) != NULL)
    {
        *sets = PyArray_DATA(*array);
        *size = PyArray_SIZE(*array);
    }
    else if(iBaseEntitySet_Check(obj))
    {
        *sets = &iBaseEntitySet_GET_HANDLE(obj);
        *size = 1;
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ENT_OR_ENTARR);
        return 0;
    }
    return 1;
}

static PyObject *
PyArray_NewFromMallocAny(int nd,npy_intp *dims,int typenum,
                         void *data,iBase_Object *inst)
{
    iBase_OutArray out = {0, data};
    return PyArray_NewFromOutBase(nd,dims,typenum,&out,inst);
}

static PyObject *
iAnyEntitySet_FromHandle(iBase_Object *instance,iBase_EntitySetHandle handle)
{
    if(iMesh_Check(instance))
        return iMeshEntitySet_FromHandle((iMesh_Object*)instance,handle);
    if(iGeom_Check(instance))
        return iGeomEntitySet_FromHandle((iGeom_Object*)instance,handle);

    return NULL;
}

static void
iRelPairObj_dealloc(iRelPair_Object *self)
{
    Py_XDECREF(self->instance);

    ((PyObject*)self)->ob_type->tp_free((PyObject*)self);
}

static PyObject *
iRelPairObj_getfirstType(iRelPair_Object *self,void *closure)
{
    int err;
    iBase_Instance iface[2];
    int ent_or_set[2];
    int type[2];

    iRel_getPairInfo(self->instance->handle,self->handle,
                     iface+0,ent_or_set+0,type+0,
                     iface+1,ent_or_set+1,type+1,&err);
    if(checkError(self->instance->handle,err))
        return NULL;

    return PyInt_FromLong(ent_or_set[0]);
}

static PyObject *
iRelPairObj_getsecondType(iRelPair_Object *self,void *closure)
{
    int err;
    iBase_Instance iface[2];
    int ent_or_set[2];
    int type[2];

    iRel_getPairInfo(self->instance->handle,self->handle,
                     iface+0,ent_or_set+0,type+0,
                     iface+1,ent_or_set+1,type+1,&err);
    if(checkError(self->instance->handle,err))
        return NULL;

    return PyInt_FromLong(ent_or_set[1]);
}

static PyObject *
iRelPairObj_repr(iRelPair_Object *self)
{
    return PyString_FromFormat("<%s '%s<->%s' %p>",
                               self->ob_type->tp_name,
                               self->related[0]->ob_type->tp_name,
                               self->related[1]->ob_type->tp_name,
                               self->handle);
}

static PyObject *
iRelPairObj_setRelation(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"first","second",0};
    int err;
    PyObject *in_ents1,*ents1 = NULL;
    PyObject *in_ents2,*ents2 = NULL;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"OO",kwlist,&in_ents1,&in_ents2))
        return NULL;

    iBase_EntityHandle *entities1 = NULL;
    iBase_EntityHandle *entities2 = NULL;
    iBase_EntitySetHandle *sets1  = NULL;
    iBase_EntitySetHandle *sets2  = NULL;
    int size1;
    int size2;

    if(!get_entity_data   (in_ents1,&ents1,&entities1,&size1) &&
       !get_entityset_data(in_ents1,&ents1,&sets1,    &size1))
        goto err;
    if(!get_entity_data   (in_ents2,&ents2,&entities2,&size2) &&
       !get_entityset_data(in_ents2,&ents2,&sets2,    &size2))
        goto err;

    int swapped = 0;
    if(ents1 && !ents2)
    {
        PyObject *tmp_arr;
        iBase_EntityHandle *tmp_ents;
        iBase_EntitySetHandle *tmp_sets;
        int tmp_size;

        tmp_arr = ents1; ents1 = ents2; ents2 = tmp_arr;
        tmp_ents = entities1; entities1 = entities2; entities2 = tmp_ents;
        tmp_sets = sets1; sets1 = sets2; sets2 = tmp_sets;
        tmp_size = size1; size1 = size2; size2 = tmp_size;

        swapped = 1;
    }

    if(ents1 && ents2)
    {
        if(entities1)
        {
            if(entities2)
                iRel_setEntArrEntArrRelation(self->instance->handle,
                                             self->handle,entities1,size1,
                                             entities2,size2,&err);
            else
                iRel_setEntArrSetArrRelation(self->instance->handle,
                                             self->handle,entities1,size1,
                                             sets2,size2,&err);
        }
        else
        {
            if(entities2)
                iRel_setSetArrEntArrRelation(self->instance->handle,
                                             self->handle,sets1,size1,
                                             entities2,size2,&err);
            else
                iRel_setSetArrSetArrRelation(self->instance->handle,
                                             self->handle,sets1,size1,
                                             sets2,size2,&err);
        }
    }
    else if(ents2)
    {
        if(entities1)
        {
            if(entities2)
                iRel_setEntEntArrRelation(self->instance->handle,
                                          self->handle,entities1[0],swapped,
                                          entities2,size2,&err);
            else
                iRel_setEntSetArrRelation(self->instance->handle,
                                          self->handle,entities1[0],swapped,
                                          sets2,size2,&err);
        }
        else
        {
            if(entities2)
                iRel_setSetEntArrRelation(self->instance->handle,
                                          self->handle,sets1[0],swapped,
                                          entities2,size2,&err);
            else
                iRel_setSetSetArrRelation(self->instance->handle,
                                          self->handle,sets1[0],swapped,
                                          sets2,size2,&err);
        }
    }
    else
    {
        if(entities1)
        {
            if(entities2)
                iRel_setEntEntRelation(self->instance->handle,self->handle,
                                       entities1[0],entities2[0],&err);
            else
                iRel_setEntSetRelation(self->instance->handle,self->handle,
                                       entities1[0],sets2[0],&err);
        }
        else
        {
            if(entities2)
                iRel_setSetEntRelation(self->instance->handle,self->handle,
                                       sets1[0],entities2[0],&err);
            else
                iRel_setSetSetRelation(self->instance->handle,self->handle,
                                       sets1[0],sets2[0],&err);
        }
    }

    Py_XDECREF(ents1);
    Py_XDECREF(ents2);
    if(checkError(self->handle,err))
        return NULL;

    Py_RETURN_NONE;

err:
    Py_XDECREF(ents1);
    Py_XDECREF(ents2);
    return NULL;
}

static PyObject *
iRelPairObj_getEntRelation(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","switch_order",0};
    int err;
    PyObject *in_ents,*ents;
    PyObject *in_swapped;
    int swapped;

    if(PyArg_ParseTupleAndKeywords(args,kw,"OO!",kwlist,&in_ents,&PyBool_Type,
                                   &in_swapped))
        swapped = (in_swapped == Py_True);
    else
    {
        if(kw == NULL || PyDict_Size(kw) != 1)
            return NULL;

        if((in_ents = PyDict_GetItemString(kw,"first")) != NULL)
            swapped = 0;
        else if((in_ents = PyDict_GetItemString(kw,"second")) != NULL)
            swapped = 1;
        else
            return NULL;
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1);
    if(ents)
    {
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;
        int *offsets=NULL;
        int off_alloc=0,off_size;

        iRel_getEntArrEntArrRelation(self->instance->handle,self->handle,
                                     entities,ent_size,swapped,
                                     &result, &res_alloc,&res_size,
                                     &offsets,&off_alloc,&off_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp off_dims[] = {off_size};
        npy_intp res_dims[] = {res_size};
        return OffsetList_New(
            PyArray_NewFromMalloc(1,off_dims,NPY_INT,offsets),
            PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result)
            );
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENTSET,1,1);
    if(ents)
    {
        iBase_EntitySetHandle *sets = PyArray_DATA(ents);
        int set_size = PyArray_SIZE(ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;
        int *offsets=NULL;
        int off_alloc=0,off_size;

        iRel_getSetArrEntArrRelation(self->instance->handle,self->handle,
                                     sets,set_size,swapped,
                                     &result, &res_alloc,&res_size,
                                     &offsets,&off_alloc,&off_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp off_dims[] = {off_size};
        npy_intp res_dims[] = {res_size};
        return OffsetList_New(
            PyArray_NewFromMalloc(1,off_dims,NPY_INT,offsets),
            PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result)
            );
    }

    if(iBaseEntity_Check(in_ents))
    {
        iBase_EntityHandle entity = iBaseEntity_GET_HANDLE(in_ents);
        iBaseEntity_Object *result = iBaseEntity_New();

        iRel_getEntEntRelation(self->instance->handle,self->handle,entity,
                               swapped,&result->handle,&err);
        if(checkError(self->handle,err))
        {
            Py_DECREF(result);
            return NULL;
        }
        return (PyObject*)result;
    }

    if(iBaseEntitySet_Check(in_ents))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GET_HANDLE(in_ents);
        iBaseEntity_Object *result = iBaseEntity_New();

        iRel_getSetEntRelation(self->instance->handle,self->handle,set,
                               swapped,&result->handle,&err);
        if(checkError(self->handle,err))
            return NULL;
        return (PyObject*)result;
    }

    PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
    return NULL;
}

static PyObject *
iRelPairObj_getEntArrRelation(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","switch_order",0};
    int err;
    PyObject *in_ents,*ents;
    PyObject *in_swapped;
    int swapped;

    if(PyArg_ParseTupleAndKeywords(args,kw,"OO!",kwlist,&in_ents,&PyBool_Type,
                                   &in_swapped))
        swapped = (in_swapped == Py_True);
    else
    {
        if(kw == NULL || PyDict_Size(kw) != 1)
            return NULL;

        if((in_ents = PyDict_GetItemString(kw,"first")) != NULL)
            swapped = 0;
        else if((in_ents = PyDict_GetItemString(kw,"second")) != NULL)
            swapped = 1;
        else
            return NULL;
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1);
    if(ents)
    {
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;
        int *offsets=NULL;
        int off_alloc=0,off_size;

        iRel_getEntArrEntArrRelation(self->instance->handle,self->handle,
                                     entities,ent_size,swapped,
                                     &result, &res_alloc,&res_size,
                                     &offsets,&off_alloc,&off_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp off_dims[] = {off_size};
        npy_intp res_dims[] = {res_size};
        return OffsetList_New(
            PyArray_NewFromMalloc(1,off_dims,NPY_INT,offsets),
            PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result)
            );
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENTSET,1,1);
    if(ents)
    {
        iBase_EntitySetHandle *sets = PyArray_DATA(ents);
        int set_size = PyArray_SIZE(ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;
        int *offsets=NULL;
        int off_alloc=0,off_size;

        iRel_getSetArrEntArrRelation(self->instance->handle,self->handle,
                                     sets,set_size,swapped,
                                     &result, &res_alloc,&res_size,
                                     &offsets,&off_alloc,&off_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp off_dims[] = {off_size};
        npy_intp res_dims[] = {res_size};
        return OffsetList_New(
            PyArray_NewFromMalloc(1,off_dims,NPY_INT,offsets),
            PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result)
            );
    }

    if(iBaseEntity_Check(in_ents))
    {
        iBase_EntityHandle entity = iBaseEntity_GET_HANDLE(in_ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getEntEntArrRelation(self->instance->handle,self->handle,entity,
                                  swapped,&result,&res_alloc,&res_size,&err);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result);
    }

    if(iBaseEntitySet_Check(in_ents))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GET_HANDLE(in_ents);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getSetEntArrRelation(self->instance->handle,self->handle,set,
                                  swapped,&result,&res_alloc,&res_size,&err);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result);
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return NULL;
    }
}

static PyObject *
iRelPairObj_getSetRelation(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","switch_order",0};
    int err;
    PyObject *in_ents,*ents;
    PyObject *in_swapped;
    int swapped;

    if(PyArg_ParseTupleAndKeywords(args,kw,"OO!",kwlist,&in_ents,&PyBool_Type,
                                   &in_swapped))
        swapped = (in_swapped == Py_True);
    else
    {
        if(kw == NULL || PyDict_Size(kw) != 1)
            return NULL;

        if((in_ents = PyDict_GetItemString(kw,"first")) != NULL)
            swapped = 0;
        else if((in_ents = PyDict_GetItemString(kw,"second")) != NULL)
            swapped = 1;
        else
            return NULL;
    }

    iBase_Object *related = self->related[!swapped];

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1);
    if(ents)
    {
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);

        iBase_EntitySetHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getEntArrSetArrRelation(self->instance->handle,self->handle,
                                     entities,ent_size,swapped,
                                     &result,&res_alloc,&res_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMallocAny(1,res_dims,NPY_IBASEENTSET,result,
                                        related);
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENTSET,1,1);
    if(ents)
    {
        iBase_EntitySetHandle *sets = PyArray_DATA(ents);
        int set_size = PyArray_SIZE(ents);

        iBase_EntitySetHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getSetArrSetArrRelation(self->instance->handle,self->handle,
                                     sets,set_size,swapped,
                                     &result,&res_alloc,&res_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMallocAny(1,res_dims,NPY_IBASEENTSET,result,
                                        related);
    }

    if(iBaseEntity_Check(in_ents))
    {
        iBase_EntityHandle entity = iBaseEntity_GET_HANDLE(in_ents);
        iBase_EntitySetHandle result;

        iRel_getEntSetRelation(self->instance->handle,self->handle,entity,
                               swapped,&result,&err);
        if(checkError(self->handle,err))
            return NULL;
        return iAnyEntitySet_FromHandle(related,result);
    }

    if(iBaseEntitySet_Check(in_ents))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GET_HANDLE(in_ents);
        iBase_EntitySetHandle result;

        iRel_getSetSetRelation(self->instance->handle,self->handle,set,
                               swapped,&result,&err);
        if(checkError(self->handle,err))
            return NULL;
        return iAnyEntitySet_FromHandle(related,result);
    }

    PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
    return NULL;
}

static PyObject *
iRelPairObj_getSetArrRelation(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","switch_order",0};
    int err;
    PyObject *in_ents,*ents;
    PyObject *in_swapped;
    int swapped;

    if(PyArg_ParseTupleAndKeywords(args,kw,"OO!",kwlist,&in_ents,&PyBool_Type,
                                   &in_swapped))
        swapped = (in_swapped == Py_True);
    else
    {
        if(kw == NULL || PyDict_Size(kw) != 1)
            return NULL;

        if((in_ents = PyDict_GetItemString(kw,"first")) != NULL)
            swapped = 0;
        else if((in_ents = PyDict_GetItemString(kw,"second")) != NULL)
            swapped = 1;
        else
            return NULL;
    }

    iBase_Object *related = self->related[!swapped];

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1);
    if(ents)
    {
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);

        iBase_EntitySetHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getEntArrSetArrRelation(self->instance->handle,self->handle,
                                     entities,ent_size,swapped,
                                     &result,&res_alloc,&res_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMallocAny(1,res_dims,NPY_IBASEENTSET,result,
                                        related);
    }

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENTSET,1,1);
    if(ents)
    {
        iBase_EntitySetHandle *sets = PyArray_DATA(ents);
        int set_size = PyArray_SIZE(ents);

        iBase_EntitySetHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_getSetArrSetArrRelation(self->instance->handle,self->handle,
                                     sets,set_size,swapped,
                                     &result,&res_alloc,&res_size,&err);
        Py_DECREF(ents);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMallocAny(1,res_dims,NPY_IBASEENTSET,result,
                                        related);
    }

    PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
    return NULL;
}

static PyObject *
iRelPairObj_inferAllRelations(iRelPair_Object *self)
{
    int err;
    iRel_inferAllRelations(self->instance->handle,self->handle,&err);
    if(checkError(self->handle,err))
        return NULL;
    Py_RETURN_NONE;
}

static PyObject *
iRelPairObj_inferRelations(iRelPair_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"entities","switch_order",0};
    int err;
    PyObject *in_ents,*ents;
    PyObject *in_swapped;
    int swapped;

    if(PyArg_ParseTupleAndKeywords(args,kw,"OO!",kwlist,&in_ents,&PyBool_Type,
                                   &in_swapped))
        swapped = (in_swapped == Py_True);
    else
    {
        if(kw == NULL || PyDict_Size(kw) != 1)
            return NULL;

        if((in_ents = PyDict_GetItemString(kw,"first")) != NULL)
            swapped = 0;
        else if((in_ents = PyDict_GetItemString(kw,"second")) != NULL)
            swapped = 1;
        else
            return NULL;
    }

    if((ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1)) != NULL)
    {
        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);

        iRel_inferEntArrRelations(self->instance->handle,self->handle,
                                  entities,ent_size,swapped,&err);
        Py_DECREF(ents);
    }
    else if((ents = PyArray_TryFromObject(in_ents,NPY_IBASEENTSET,1,1)) != NULL)
    {
        iBase_EntitySetHandle *sets = PyArray_DATA(ents);
        int set_size = PyArray_SIZE(ents);

        iRel_inferSetArrRelations(self->instance->handle,self->handle,
                                  sets,set_size,swapped,&err);
        Py_DECREF(ents);
    }
    else if(iBaseEntity_Check(in_ents))
    {
        iBase_EntityHandle entity = iBaseEntity_GET_HANDLE(in_ents);

        iRel_inferEntRelations(self->instance->handle,self->handle,entity,
                               swapped,&err);
    }
    else if(iBaseEntitySet_Check(in_ents))
    {
        iBase_EntitySetHandle set = iBaseEntitySet_GET_HANDLE(in_ents);

        iRel_inferSetRelations(self->instance->handle,self->handle,set,
                               swapped,&err);
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ANY_ENT);
        return NULL;
    }

    if(checkError(self->handle,err))
        return NULL;
    Py_RETURN_NONE;
}

static PyObject *
iRelPairObj_richcompare(iRelPair_Object *lhs,iRelPair_Object *rhs,int op)
{
    if(!iRelPair_Check(lhs) || !iRelPair_Check(rhs))
    {
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }

    switch(op)
    {
    case Py_EQ:
        return PyBool_FromLong(lhs->handle == rhs->handle &&
                               lhs->instance->handle == rhs->instance->handle);
    case Py_NE:
        return PyBool_FromLong(lhs->handle != rhs->handle ||
                               lhs->instance->handle != rhs->instance->handle);
    default:
        PyErr_SetNone(PyExc_TypeError);
        return NULL;
    }
}



static PyMethodDef iRelPairObj_methods[] = {
    IREL_METHOD(iRelPair, setRelation,        METH_VARARGS|METH_KEYWORDS),
    IREL_METHOD(iRelPair, getEntRelation,     METH_VARARGS|METH_KEYWORDS),
    IREL_METHOD(iRelPair, getEntArrRelation,  METH_VARARGS|METH_KEYWORDS),
    IREL_METHOD(iRelPair, getSetRelation,     METH_VARARGS|METH_KEYWORDS),
    IREL_METHOD(iRelPair, getSetArrRelation,  METH_VARARGS|METH_KEYWORDS),
    IREL_METHOD(iRelPair, inferAllRelations,  METH_NOARGS),
    IREL_METHOD(iRelPair, inferRelations,     METH_VARARGS|METH_KEYWORDS),
    {0}
};

static PyMemberDef iRelPairObj_members[] = {
    {"instance", T_OBJECT_EX, offsetof(iRelPair_Object, instance),
     READONLY, IRELDOC_iRelPair_instance},
    {"first", T_OBJECT_EX, offsetof(iRelPair_Object, related[0]),
     READONLY, IRELDOC_iRelPair_first},
    {"second", T_OBJECT_EX, offsetof(iRelPair_Object, related[1]),
     READONLY, IRELDOC_iRelPair_second},
    {0}
};

static PyGetSetDef iRelPairObj_getset[] = {
    IREL_GET(iRelPair, firstType),
    IREL_GET(iRelPair, secondType),
    {0}
};


static PyTypeObject iRelPair_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
    "itaps.iRel.Pair",                        /* tp_name */
    sizeof(iRelPair_Object),                  /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)iRelPairObj_dealloc,          /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    (reprfunc)iRelPairObj_repr,               /* tp_repr */
    0,                                        /* tp_as_number */
    0,                                        /* tp_as_sequence */
    0,                                        /* tp_as_mapping */
    0,                                        /* tp_hash */
    0,                                        /* tp_call */
    0,                                        /* tp_str */
    0,                                        /* tp_getattro */
    0,                                        /* tp_setattro */
    0,                                        /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /* tp_flags */
    IRELDOC_iRelPair,                         /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    (richcmpfunc)iRelPairObj_richcompare,     /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    iRelPairObj_methods,                      /* tp_methods */
    iRelPairObj_members,                      /* tp_members */
    iRelPairObj_getset,                       /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    0,                                        /* tp_init */
    0,                                        /* tp_alloc */
    0,                                        /* tp_new */
};
