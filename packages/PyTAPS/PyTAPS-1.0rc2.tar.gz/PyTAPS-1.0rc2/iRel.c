#define _IREL_MODULE
#include "iRel_Python.h"
#include "errors.h"
#include "common.h"
#include "helpers.h"
#include "numpy_extensions.h"

#include "iMesh_Python.h"
#include "iGeom_Python.h"

static PyTypeObject iRel_Type;
static PyTypeObject iRelRelation_Type;

static int
checkError(iRel_Instance mesh,int err)
{
    if(err)
    {
        PyErr_SetString(PyExc_ITAPSError,iRel_LAST_ERROR.description);
        return 1;
    }
    else
        return 0;
}

static int
get_iface_type(iBase_Object *o)
{
    if(iMesh_Check(o))
        return iRel_IMESH_IFACE;
    if(iGeom_Check(o))
        return iRel_IGEOM_IFACE;
    if(iRel_Check(o))
        return iRel_IREL_IFACE;

    return -1;
}

static iRelRelation_Object *
iRelRelation_FromInstance(iRel_Object *instance)
{
    iRelRelation_Object *o = iRelRelation_New();
    o->instance = instance;
    o->handle = NULL;
    Py_INCREF(o->instance);
    return o;
}

static int
iRelObj_init(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"options",0};
    int err;
    const char *options = "";

    if(!PyArg_ParseTupleAndKeywords(args,kw,"|s",kwlist,&options))
        return -1;

    /* __init__ can be called multiple times, so destroy the old interface
       if necessary */
    if(self->handle)
    {
        iRel_dtor(self->handle,&err);
        Py_XDECREF(self->refs);
        if(checkError(self->handle,err))
            return -1;
    }
    iRel_newAssoc(options,&self->handle,&err,strlen(options));
    if(checkError(self->handle,err))
        return -1;
    self->refs = PyDict_New();
    return 0;
}

static void
iRelObj_dealloc(iRel_Object *self)
{
    if(self->handle)
    {
        int err;
        iRel_dtor(self->handle,&err);
    }
    Py_XDECREF(self->refs);
    self->ob_type->tp_free((PyObject*)self);
}

static PyObject *
iRelObj_createAssociation(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"first","first_type","second","second_type",0};
    int err;
    iBase_Object *iface1;
    int ent_or_set1;
    iBase_Object *iface2;
    int ent_or_set2;

    int type1,type2;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O!iO!i",kwlist,&iBase_Type,&iface1,
                                    &ent_or_set1,&iBase_Type,&iface2,
                                    &ent_or_set2))
        return NULL;

    type1 = get_iface_type(iface1);
    type2 = get_iface_type(iface2);
    if(type1 == -1 || type2 == -1)
    {
        PyErr_SetString(PyExc_ITAPSError,ERR_UNKNOWN_INST);
        return NULL;
    }

    iRelRelation_Object *rel = iRelRelation_FromInstance(self);

    iRel_createAssociation(self->handle,iface1->handle,ent_or_set1,type1,
                           iface2->handle,ent_or_set2,type2,&rel->handle,&err);
    if(checkError(self->handle,err))
        return NULL;

    PyObject *key1 = PyInt_FromSize_t((size_t)iface1->handle);
    PyObject *key2 = PyInt_FromSize_t((size_t)iface2->handle);
    PyDict_SetItem(self->refs,key1,(PyObject*)iface1);
    PyDict_SetItem(self->refs,key2,(PyObject*)iface2);
    Py_DECREF(key1);
    Py_DECREF(key2);

    rel->related[0] = iface1;
    rel->related[1] = iface2;

    return (PyObject*)rel;
}

static PyObject *
iRelObj_destroyAssociation(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"relation",0};
    int err;
    iRelRelation_Object *rel;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O!",kwlist,&iRelRelation_Type,
                                    &rel))
        return NULL;

    iRel_destroyAssociation(self->handle,rel->handle,&err);
    if(checkError(self->handle,err))
        return NULL;

    PyObject *key1 = PyInt_FromSize_t((size_t)rel->related[0]->handle);
    PyObject *key2 = PyInt_FromSize_t((size_t)rel->related[1]->handle);
    PyDict_DelItem(self->refs,key1);
    PyDict_DelItem(self->refs,key2);
    Py_DECREF(key1);
    Py_DECREF(key2);

    Py_RETURN_NONE;
}

static PyObject *
iRelObj_getAssociatedInterfaces(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"interface",0};
    int err;
    iBase_Object *iface;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O!",kwlist,&iBase_Type,&iface))
        return NULL;

    iBase_Instance *ifaces=NULL;
    int iface_alloc=0,iface_size;

    iRel_getAssociatedInterfaces(self->handle,iface->handle,&ifaces,
                                 &iface_alloc,&iface_size,&err);
    if(checkError(self->handle,err))
        return NULL;

    PyObject *result = PyList_New(iface_size);
    int i;
    for(i=0; i<iface_size; i++)
    {
        PyObject *key = PyInt_FromSize_t((size_t)ifaces[i]);
        PyObject *o = PyDict_GetItem(self->refs,key);
        if(o)
        {
            Py_INCREF(o);
            PyList_SET_ITEM(result,i,o);
        }
        else
        {
            Py_DECREF(result);
            return NULL;
        }
        Py_DECREF(key);
    }

    return result;
}

static PyObject *
iRelObj_createVtxAndAssociate(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"coords","entities","storage_order",0};
    int err;
    PyObject *in_verts,*verts;
    PyObject *in_ents,*ents;
    int storage_order = iBase_INTERLEAVED;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"OO|i",kwlist,&in_verts,&in_ents,
                                    &storage_order))
        return NULL;

    ents = PyArray_TryFromObject(in_ents,NPY_IBASEENT,1,1);
    if(ents)
    {
        verts = PyArray_ToVectors(in_verts,NPY_DOUBLE,2,3,
                                  storage_order==iBase_INTERLEAVED);
        if(verts == NULL)
            goto err;

        iBase_EntityHandle *entities = PyArray_DATA(ents);
        int ent_size = PyArray_SIZE(ents);
        double *coords = PyArray_DATA(verts);
        int coord_size = PyArray_SIZE(verts);

        iBase_EntityHandle *result=NULL;
        int res_alloc=0,res_size;

        iRel_createVtxArrAndAssociate(self->handle,coord_size/3,storage_order,
                                      coords,coord_size,entities,ent_size,
                                      &result,&res_alloc,&res_size,&err);
        Py_DECREF(ents);
        Py_DECREF(verts);
        if(checkError(self->handle,err))
            return NULL;

        npy_intp res_dims[] = {res_size};
        return PyArray_NewFromMalloc(1,res_dims,NPY_IBASEENT,result);
    }
    else if(iBaseEntity_Check(in_ents))
    {
        verts = PyArray_ToVectors(in_verts,NPY_DOUBLE,1,3,0);
        if(verts == NULL)
            goto err;

        iBase_EntityHandle entity = iBaseEntity_GET_HANDLE(in_ents);
        double *v = PyArray_DATA(verts);

        iBaseEntity_Object *result = iBaseEntity_New();

        iRel_createVtxAndAssociate(self->handle,v[0],v[1],v[2],entity,
                                   &result->handle,&err);
        Py_DECREF(verts);
        if(checkError(self->handle,err))
            return NULL;

        return (PyObject*)result;
    }
    else
    {
        PyErr_SetString(PyExc_ValueError,ERR_ENT_OR_ENTARR);
        return NULL;
    }

err:
    Py_XDECREF(verts);
    Py_XDECREF(ents);
    return NULL;
}

static PyObject *
iRelObj_createEntAndAssociate(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"topo","entities","assoc",0};
    int err;
    int topo;
    PyObject *in_ents,*ents;
    iBaseEntity_Object *assoc;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"iOO!",kwlist,&topo,&in_ents,
                                    &iBaseEntity_Type,&assoc))
        return NULL;

    ents = PyArray_FROMANY(in_ents,NPY_IBASEENT,1,1,NPY_C_CONTIGUOUS);
    if(ents == NULL)
        return NULL;

    iBase_EntityHandle *lower = PyArray_DATA(ents);
    int lower_size = PyArray_SIZE(ents);

    iBaseEntity_Object *entity = iBaseEntity_New();
    int status;

    iRel_createEntAndAssociate(self->handle,topo,lower,lower_size,
                               iBaseEntity_GET_HANDLE(assoc),&entity->handle,
                               &status,&err);
    Py_DECREF(ents);
    if(checkError(self->handle,err))
    {
        Py_DECREF((PyObject*)entity);
        return NULL;
    }

    return NamedTuple_New(&CreateEnt_Type,"(Ni)",entity,status);
}

/* TODO: should the underlying function be changed?? */
/*static PyObject *
iRelObj_createEntArrAndAssociate(iMesh_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"topo","entities","assoc",0};
    int topo,err;
    PyObject *obj1;
    PyObject *obj2;
    PyObject *ents;
    PyObject *assoc;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"iOO",kwlist,&topo,&obj1,&obj2))
        return NULL;

    if((ents = PyArray_FROMANY(obj1,NPY_IBASEENT,1,1,NPY_C_CONTIGUOUS)) == NULL)
        goto err;
    if((assoc = PyArray_FROMANY(obj2,NPY_IBASEENT,1,1,NPY_C_CONTIGUOUS)) ==
       NULL)
        goto err;

    iBase_EntityHandle *lower = PyArray_DATA(ents);
    int lower_size = PyArray_SIZE(ents);
    iBase_EntityHandle *assoc_ents = PyArray_DATA(assoc);
    iBase_EntityHandle *assoc_size = PyArray_SIZE(assoc);

    iBase_EntityHandle *entities = NULL;
    int ent_alloc = 0,ent_size;
    int *status = NULL;
    int stat_alloc = 0,stat_size;

    iRel_createEntArrAndAssociate(self->handle,topo,lower,lower_size,&entities,&ent_alloc,
                       &ent_size,&status,&stat_alloc,&stat_size,&err);
    Py_DECREF(ents);
    Py_DECREF(assoc);
    if(checkError(self->handle,err))
        return NULL;

    npy_intp ent_dims[] = {ent_size};
    npy_intp stat_dims[] = {stat_size};
    return NamedTuple_New(CreateEnt_Type,"(NN)",
        PyArray_NewFromMalloc(1,ent_dims,NPY_IBASEENT,entities),
        PyArray_NewFromMalloc(1,stat_dims,NPY_INT,status)
        );
}
*/

static PyObject *
iRelObj_moveTo(iRel_Object *self,PyObject *args,PyObject *kw)
{
    static char *kwlist[] = {"geom","mesh","entity",0};
    int err;
    iGeom_Object *geom;
    iMesh_Object *mesh;
    iBaseEntity_Object *entity;

    if(!PyArg_ParseTupleAndKeywords(args,kw,"O!O!O!",kwlist,&iGeom_Type,
                                    &geom,&iMesh_Type,&mesh,
                                    &iBaseEntity_Type,&entity))
        return NULL;

    iRel_moveTo(self->handle,geom->handle,mesh->handle,entity->handle,&err);
    if(checkError(self->handle,err))
        return NULL;

    Py_RETURN_NONE;
}

static PyObject *
iRelObj_repr(iRel_Object *self)
{
    return PyString_FromFormat("<itaps.iRel.Rel %p>",self->handle);
}

static PyObject *
iRelObj_richcompare(iRel_Object *lhs,iRel_Object *rhs,int op)
{
    if(!iRel_Check(lhs) || !iRel_Check(rhs))
    {
        Py_INCREF(Py_NotImplemented);
        return Py_NotImplemented;
    }

    switch(op)
    {
    case Py_EQ:
        return PyBool_FromLong(lhs->handle == rhs->handle);
    case Py_NE:
        return PyBool_FromLong(lhs->handle != rhs->handle);
    default:
        PyErr_SetNone(PyExc_TypeError);
        return NULL;
    }
}

static PyMethodDef iRelObj_methods[] = {
    { "createAssociation", (PyCFunction)iRelObj_createAssociation,
      METH_KEYWORDS, "Create a relation pair between two interfaces"
    },
    { "destroyAssociation", (PyCFunction)iRelObj_destroyAssociation,
      METH_KEYWORDS, "Destroy a relation pair"
    },
    { "getAssociatedInterfaces", (PyCFunction)iRelObj_getAssociatedInterfaces,
      METH_KEYWORDS, "Get interfaces related to the specified interface"
    },
    { "createVtxAndAssociate", (PyCFunction)iRelObj_createVtxAndAssociate,
      METH_KEYWORDS, "Create mesh vertex(ices) and associate with geometry "
      "entity(ies)"
    },
    { "createEntAndAssociate", (PyCFunction)iRelObj_createEntAndAssociate,
      METH_KEYWORDS, "Create mesh entity(ies) and associate with geometry "
      "entity(ies)"
    },
    { "moveTo", (PyCFunction)iRelObj_moveTo, METH_KEYWORDS,
      "Move related mesh entities to the closest point on the specified "
      "geometry entity"
    },
    {0}
};

static PyTypeObject iRel_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
    "itaps.iRel.Assoc",                       /* tp_name */
    sizeof(iRel_Object),                      /* tp_basicsize */
    0,                                        /* tp_itemsize */
    (destructor)iRelObj_dealloc,              /* tp_dealloc */
    0,                                        /* tp_print */
    0,                                        /* tp_getattr */
    0,                                        /* tp_setattr */
    0,                                        /* tp_compare */
    (reprfunc)iRelObj_repr,                   /* tp_repr */
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
    "iRel objects",                           /* tp_doc */
    0,                                        /* tp_traverse */
    0,                                        /* tp_clear */
    (richcmpfunc)iRelObj_richcompare,         /* tp_richcompare */
    0,                                        /* tp_weaklistoffset */
    0,                                        /* tp_iter */
    0,                                        /* tp_iternext */
    iRelObj_methods,                          /* tp_methods */
    0,                                        /* tp_members */
    0,                                        /* tp_getset */
    0,                                        /* tp_base */
    0,                                        /* tp_dict */
    0,                                        /* tp_descr_get */
    0,                                        /* tp_descr_set */
    0,                                        /* tp_dictoffset */
    (initproc)iRelObj_init,                   /* tp_init */
    0,                                        /* tp_alloc */
    0,                                        /* tp_new */
};


static PyMethodDef module_methods[] = {
    {0}
};

PyMODINIT_FUNC initiRel(void)
{
    PyObject *m;

    m = Py_InitModule("iRel",module_methods);
    import_array();
    import_iBase();
    import_iMesh();
    import_iGeom();
    import_helpers();

    /***** register C API *****/
    static void *IRel_API[1];
    PyObject *api_obj;

    /* Initialize the C API pointer array */
    IRel_API[0] = &iRel_Type;

    /* Create a CObject containing the API pointer array's address */
    api_obj = PyCObject_FromVoidPtr(IRel_API,NULL);

    if(api_obj != NULL)
        PyModule_AddObject(m, "_C_API", api_obj);

    REGISTER_CLASS(m,"Assoc",iRel);
    REGISTER_CLASS(m,"Relation",iRelRelation);
}

/* Include source files so that everything is in one translation unit */
#include "iRel_relation.inl"
