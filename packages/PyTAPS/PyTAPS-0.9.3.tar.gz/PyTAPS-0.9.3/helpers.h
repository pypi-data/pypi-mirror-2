#ifndef PYTAPS_HELPERS_H
#define PYTAPS_HELPERS_H

#include <Python.h>

/* NOTE: these are never freed! (Fix in Python 3.x?) */
static PyObject *g_offset_list;
static PyObject *g_indexed_list;

/* NOTE: steals references to offsets and data */
#define OffsetList_New(offsets,data)                                    \
    PyObject_CallFunction(g_offset_list,"NN",(offsets),(data))

/* NOTE: steals references to offsets and data */
#define IndexedList_New(offsets,indices,data)                           \
    PyObject_CallFunction(g_indexed_list,"NNN",(offsets),(indices),     \
                          (data))

#if PY_VERSION_HEX >= 0x020600f0

static PyObject *g_namedtuple;

static PyObject *
NamedTuple_New(PyObject *type,const char *fmt,...)
{
    va_list args;
    va_start(args,fmt);
    PyObject *py_args = Py_VaBuildValue(fmt,args);
    va_end(args);

    PyObject *res = PyObject_Call(type,py_args,NULL);
    Py_DECREF(py_args);

    return res;
}

static PyObject *
NamedTuple_CreateType(PyObject *module,const char *name,const char *fields)
{
    PyObject *type = PyObject_CallFunction(g_namedtuple,"ss",name,fields);
    if(module)
        PyModule_AddObject(module,name,type);
    return type;
}

#else

static PyObject *
NamedTuple_New(PyObject *type,const char *fmt,...)
{
    va_list args;
    va_start(args,fmt);
    PyObject *res = Py_VaBuildValue(fmt,args);
    va_end(args);

    return res;
}
#define NamedTuple_CreateType(module,name,fields) 0

#endif

static int import_helpers(void)
{
    PyObject *helper_module;

    if( (helper_module = PyImport_ImportModule("itaps.helpers")) == NULL)
        return -1;
    if( (g_offset_list = PyObject_GetAttrString(helper_module,"OffsetList"))
        == NULL)
        return -1;
    if( (g_indexed_list = PyObject_GetAttrString(helper_module, "IndexedList")) 
        == NULL)
        return -1;
    Py_DECREF(helper_module);

#if PY_VERSION_HEX >= 0x020600f0
    PyObject *collections_module;

    if( (collections_module = PyImport_ImportModule("collections")) == NULL)
        return -1;
    if( (g_namedtuple = PyObject_GetAttrString(collections_module,
        "namedtuple")) == NULL)
        return -1;
    Py_DECREF(collections_module);
#endif

    return 0;

    /* Suppress warnings if this function isn't used */
    (void)NamedTuple_New;
}

#endif
