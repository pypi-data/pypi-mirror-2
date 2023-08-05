#define _IBASE_MODULE
#include "iBase_Python.h"
#include "common.h"
#include "errors.h"

#include <numpy/arrayobject.h>
#include <numpy/ufuncobject.h>

static PyObject *PyExc_ITAPSError;
static PyTypeObject iBaseArr_Type;

static PyObject *
PyArray_NewFromOutBase(int,npy_intp *,int,iBase_OutArray *,iBase_Object *);


static PyTypeObject iBase_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                        /* ob_size */
    "itaps.iBase.Base",                       /* tp_name */
    sizeof(iBase_Object),                     /* tp_basicsize */
    0,                                        /* tp_itemsize */
    0,                                        /* tp_dealloc */
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
    Py_TPFLAGS_DEFAULT,                       /* tp_flags */
    "iBase instance objects"                  /* tp_doc */
};

subarray_t subtypes[16];
static size_t counter = 0;

static void
iBase_RegisterSubArray(int dtype,PyTypeObject *inst_type,PyTypeObject *el_type,
                       arrgetfunc getter,arrcreatefunc creator)
{
    if(counter == sizeof(subtypes)/sizeof(subtypes[0]))
        return;
    subtypes[counter].dtype     = dtype;
    subtypes[counter].inst_type = inst_type;
    subtypes[counter].el_type   = el_type;
    subtypes[counter].getter    = getter;
    subtypes[counter].creator   = creator;
    counter++;
}

static subarray_t *
get_sub_array(int dtype,PyObject *type)
{
    size_t i;
    for(i=0; i<sizeof(subtypes)/sizeof(subtypes[0]); i++)
    {
        if(subtypes[i].dtype == dtype &&
           subtypes[i].inst_type == (PyTypeObject*)type)
            return &subtypes[i];
    }
    return NULL;
}

static int NPY_IBASEENT;
static int NPY_IBASEENTSET;
static int NPY_IBASETAG;

#define HANDLE_TYPE Entity
#define HANDLE_NPYTYPE NPY_IBASEENT
#include "iBase_handleTempl.def"
#undef HANDLE_TYPE
#undef HANDLE_NPYTYPE

#define HANDLE_TYPE EntitySet
#define HANDLE_NPYTYPE NPY_IBASEENTSET
#include "iBase_handleTempl.def"
#undef HANDLE_TYPE
#undef HANDLE_NPYTYPE

#define HANDLE_TYPE Tag
#define HANDLE_NPYTYPE NPY_IBASETAG
#include "iBase_handleTempl.def"
#undef HANDLE_TYPE
#undef HANDLE_NPYTYPE

ENUM_TYPE(iBaseType,           "iBase.Type",           "");
ENUM_TYPE(iBaseAdjCost,        "iBase.AdjCost",        "");
ENUM_TYPE(iBaseStorageOrder,   "iBase.StorageOrder",   "");
ENUM_TYPE(iBaseCreationStatus, "iBase.CreationStatus", "");

static PyMethodDef module_methods[] = {
    {0}
};

static void
ArrDeallocObj_dealloc(ArrDealloc_Object *self)
{
    free(self->memory);

    self->ob_type->tp_free((PyObject *)self);
}

static PyTypeObject ArrDealloc_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                          /* ob_size */
    "arrdealloc",                               /* tp_name */
    sizeof(ArrDealloc_Object),                  /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)ArrDeallocObj_dealloc,          /* tp_dealloc */
    0,                                          /* tp_print */
    0,                                          /* tp_getattr */
    0,                                          /* tp_setattr */
    0,                                          /* tp_compare */
    0,                                          /* tp_repr */
    0,                                          /* tp_as_number */
    0,                                          /* tp_as_sequence */
    0,                                          /* tp_as_mapping */
    0,                                          /* tp_hash */
    0,                                          /* tp_call */
    0,                                          /* tp_str */
    0,                                          /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT,                         /* tp_flags */
    "Internal deallocator object",              /* tp_doc */
};

static ArrDealloc_Object *
ArrDealloc_New(void *memory)
{
    ArrDealloc_Object *o = PyObject_New(ArrDealloc_Object,&ArrDealloc_Type);
    o->memory = memory;
    return o;
}

static int
iBaseType_Cvt(PyObject *object,int *val)
{
    int tmp = PyInt_AsLong(object);
    if(PyErr_Occurred())
        return 0;
    if(tmp < iBase_VERTEX || tmp > iBase_ALL_TYPES)
    {
        PyErr_SetString(PyExc_ValueError,ERR_INVALID_TYPE);
        return 0;
    }

    *val = tmp;
    return 1;
}

static int
iBaseStorageOrder_Cvt(PyObject *object,int *val)
{
    int tmp = PyInt_AsLong(object);
    if(PyErr_Occurred())
        return 0;
    if(tmp < iBase_BLOCKED || tmp > iBase_INTERLEAVED)
    {
        PyErr_SetString(PyExc_ValueError,ERR_INVALID_STG);
        return 0;
    }

    *val = tmp;
    return 1;
}

static char typechars[] = {'i','d','E','b'};
static PyTypeObject *types[] = {&PyInt_Type,0,&iBaseEntity_Type,0};
static int typenums[] = {NPY_INT, NPY_DOUBLE, 0 /* set below */, NPY_BYTE};

static int
iBaseTagType_Cvt(PyObject *object,int *val)
{
    int i;
    char c;
    PyArray_Descr *dtype;

    /* first try matching type objects directly, if we have overrides */
    for(i=0; i<sizeof(types)/sizeof(types[0]); i++)
    {
        if(types[i] && PyObject_RichCompareBool((PyObject*)types[i],object,
                                                Py_EQ))
        {
            *val = i;
            return 1;
        }
    }

    /* now try matching type chars */
    if(PyArg_Parse(object,"c",&c))
    {
        for(i=0; i<sizeof(typechars); i++)
        {
            if(typechars[i] == c)
            {
                *val = i;
                return 1;
            }
        }
    }
    PyErr_Clear();

    /* finally, try grabbing a NumPy dtype and checking with that */
    if(PyArray_DescrConverter(object,&dtype))
    {
        for(i=0; i<sizeof(typenums)/sizeof(typenums[0]); i++)
        {
            if(typenums[i] == dtype->type_num)
            {
                *val = i;
                return 1;
            }
        }
        Py_DECREF(dtype);
    }

    PyErr_SetString(PyExc_ValueError,ERR_TYPE_CODE);
    return 0;
}

static char
iBaseTagType_ToChar(enum iBase_TagValueType t)
{
    return typechars[t];
}

static int
iBaseTagType_ToTypenum(enum iBase_TagValueType t)
{
    return typenums[t];
}

static int iBaseBuffer_Cvt(PyObject *obj,iBase_OutArray *arr)
{
    PyArray_Chunk chunk;
    if(!PyArray_BufferConverter(obj,&chunk))
        return 0;

    arr->base = chunk.base;
    arr->data = chunk.ptr;
    arr->alloc = chunk.len;

    return 1;
}

#include "numpy_extensions.h"

PyMODINIT_FUNC initiBase(void)
{
    PyObject *m = Py_InitModule("iBase",module_methods);
    import_array();
    import_ufunc();

    PyExc_ITAPSError = PyErr_NewException("iBase.ITAPSError",0,0);
    Py_INCREF(PyExc_ITAPSError);
    PyModule_AddObject(m,"ITAPSError",PyExc_ITAPSError);

    ArrDealloc_Type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&ArrDealloc_Type) < 0)
        return;

    /***** register C API *****/
    static void *IBase_API[] = {
        NULL, /* PyExc_ITAPSError */
        &ArrDealloc_Type,
        &ArrDealloc_New,
        &iBase_Type,
        &iBaseEntity_Type,
        &iBaseEntitySet_Type,
        &iBaseTag_Type,
        &iBaseEntity_FromHandle,
        &iBaseEntitySet_FromHandle,
        &iBaseTag_FromHandle,
        &iBaseEntity_GetHandle,
        &iBaseEntitySet_GetHandle,
        &iBaseTag_GetHandle,
        &NPY_IBASEENT,
        &NPY_IBASEENTSET,
        &NPY_IBASETAG,
        &iBaseType_Cvt,
        &iBaseStorageOrder_Cvt,
        &iBaseTagType_Cvt,
        &iBaseBuffer_Cvt,
        &iBaseTagType_ToChar,
        &iBaseTagType_ToTypenum,
        &iBase_RegisterSubArray,
        &PyArray_NewFromOutBase,
    };
    IBase_API[0] = PyExc_ITAPSError;
    PyObject *api_obj;

    /* Create a CObject containing the API pointer array's address */
    api_obj = PyCObject_FromVoidPtr(IBase_API,NULL);

    if(api_obj != NULL)
        PyModule_AddObject(m, "_C_API", api_obj);

    /***** acquire "equal"/"not_equal" ufuncs *****/
    PyObject *ops = PyArray_GetNumericOps();
    PyUFuncObject *eq  = (PyUFuncObject*)PyDict_GetItemString(ops,"equal");
    PyUFuncObject *neq = (PyUFuncObject*)PyDict_GetItemString(ops,"not_equal");
    Py_DECREF(ops);

    REGISTER_CLASS(m,"Base",iBase);

    /***** initialize type enum *****/
    REGISTER_CLASS(m,"Type",iBaseType);

    ADD_ENUM(iBaseType,"vertex", iBase_VERTEX);
    ADD_ENUM(iBaseType,"edge",   iBase_EDGE);
    ADD_ENUM(iBaseType,"face",   iBase_FACE);
    ADD_ENUM(iBaseType,"region", iBase_REGION);
    ADD_ENUM(iBaseType,"all",    iBase_ALL_TYPES);

    /***** initialize adjacency cost enum *****/
    REGISTER_CLASS(m,"AdjCost",iBaseAdjCost);

    ADD_ENUM(iBaseAdjCost,"unavailable",     iBase_UNAVAILABLE);
    ADD_ENUM(iBaseAdjCost,"all_order_1",     iBase_ALL_ORDER_1);
    ADD_ENUM(iBaseAdjCost,"all_order_logn",  iBase_ALL_ORDER_LOGN);
    ADD_ENUM(iBaseAdjCost,"all_order_n",     iBase_ALL_ORDER_N);
    ADD_ENUM(iBaseAdjCost,"some_order_1",    iBase_SOME_ORDER_1);
    ADD_ENUM(iBaseAdjCost,"some_order_logn", iBase_SOME_ORDER_LOGN);
    ADD_ENUM(iBaseAdjCost,"some_order_n",    iBase_SOME_ORDER_N);

    /***** initialize storage order enum *****/
    REGISTER_CLASS(m,"StorageOrder",iBaseStorageOrder);

    ADD_ENUM(iBaseStorageOrder,"blocked",     iBase_BLOCKED);
    ADD_ENUM(iBaseStorageOrder,"interleaved", iBase_INTERLEAVED);

    /***** initialize creation status enum *****/
    REGISTER_CLASS(m,"CreationStatus",iBaseCreationStatus);

    ADD_ENUM(iBaseCreationStatus,"new",        iBase_NEW);
    ADD_ENUM(iBaseCreationStatus,"exists",     iBase_ALREADY_EXISTED);
    ADD_ENUM(iBaseCreationStatus,"duplicated", iBase_CREATED_DUPLICATE);
    ADD_ENUM(iBaseCreationStatus,"failed",     iBase_CREATION_FAILED);

    /***** initialize handles *****/
    REGISTER_CLASS_BASE(m,"Entity",    iBaseEntity,    PyGenericArrType);
    REGISTER_CLASS_BASE(m,"EntitySet", iBaseEntitySet, PyGenericArrType);
    REGISTER_CLASS_BASE(m,"Tag",       iBaseTag,       PyGenericArrType);

    iBaseEntity_RegisterArray   ('j',eq,neq);
    iBaseEntitySet_RegisterArray('J',eq,neq);
    iBaseTag_RegisterArray      ('T',eq,neq);

    typenums[2] = NPY_IBASEENT;

    /* PyArray_Type's tp_alloc/tp_free are sucky */
    iBaseArr_Type.tp_alloc = PyType_GenericAlloc;
    iBaseArr_Type.tp_free  = _PyObject_Del;
    REGISTER_CLASS_BASE(m,"Array",iBaseArr,PyArray);

    /* eliminate warnings */
    (void)PyArray_TryFromObject;
    (void)PyArray_ToVectors;
}

#include "iBase_array.inl"
