#ifndef PYTAPS_IMESH_PYTHON_H
#define PYTAPS_IMESH_PYTHON_H

#include <Python.h>
#include <iMesh.h>
#include "iBase_Python.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct
{
    PyObject_HEAD
    iMesh_Instance handle;
} iMesh_Object;

#define iMesh_Check(o)                                 \
    PyObject_TypeCheck((PyObject*)(o),&iMesh_Type)

typedef struct
{
    PyObject_HEAD
    iMesh_Object *instance;
    int is_arr;
    union
    {
        iMesh_EntityIterator    one;
        iMesh_EntityArrIterator arr;
    } iter;
} iMeshIter_Object;

typedef struct
{
    iBaseEntitySet_Object base;
    iMesh_Object *instance;
} iMeshEntitySet_Object;

#define iMeshEntitySet_NewRaw()                         \
    PyObject_New(iMeshEntitySet_Object,&iMeshEntitySet_Type)

#define iMeshEntitySet_Check(o)                         \
    PyObject_TypeCheck((PyObject*)(o),&iMeshEntitySet_Type)

#define iMeshEntitySet_GetInstance(o)                   \
    ( ((iMeshEntitySet_Object*)(o))->instance )

typedef struct
{
    iBaseTag_Object base;
    iMesh_Object *instance;
} iMeshTag_Object;

#define iMeshTag_NewRaw()                               \
    PyObject_New(iMeshTag_Object,&iMeshTag_Type)

#define iMeshTag_Check(o)                               \
    PyObject_TypeCheck((PyObject*)(o),&iMeshTag_Type)

#define iMeshTag_GetInstance(o)                         \
    ( ((iMeshTag_Object*)(o))->instance )


#ifndef _IMESH_MODULE

#if defined(PY_IMESH_UNIQUE_SYMBOL)
#define IMesh_API PY_IMESH_UNIQUE_SYMBOL
#endif

#if defined(NO_IMPORT) || defined(NO_IMPORT_IMESH)
extern void **IMesh_API;
#elif defined(PY_IMESH_UNIQUE_SYMBOL)
void **IMesh_API;
#else
static void **IMesh_API = NULL;
#endif

#define iMesh_Type          (*(PyTypeObject*)    IMesh_API[0])
#define iMeshIter_Type      (*(PyTypeObject*)    IMesh_API[1])
#define iMeshEntitySet_Type (*(PyTypeObject*)    IMesh_API[2])
#define iMeshTag_Type       (*(PyTypeObject*)    IMesh_API[3])
#define NPY_IMESHENTSET     (*(int*)             IMesh_API[4])
#define NPY_IMESHTAG        (*(int*)             IMesh_API[5])
#define iMeshEntitySet_New  ( (iMeshEntitySet_Object * (*)     \
                              (iMesh_Object *))  IMesh_API[6])
#define iMeshTag_New        ( (iMeshTag_Object * (*)           \
                              (iMesh_Object *))  IMesh_API[7])
#define CreateEnt_Type      ( (PyObject*)        IMesh_API[8])
#define iMeshTopology_cvt   ( (cvtfunc)          IMesh_API[9])


#if !defined(NO_IMPORT_IMESH) && !defined(NO_IMPORT)
static int import_iMesh(void)
{
    PyObject *module = PyImport_ImportModule("itaps.iMesh");
    PyObject *c_api = NULL;

    if(module == NULL)
        return -1;

    c_api = PyObject_GetAttrString(module,"_C_API");
    if(c_api == NULL)
    {
        Py_DECREF(module);
        return -2;
    }

    if(PyCObject_Check(c_api))
        IMesh_API = (void **)PyCObject_AsVoidPtr(c_api);

    Py_DECREF(c_api);
    Py_DECREF(module);

    if(IMesh_API == NULL)
        return -3;
    return 0;
}
#endif

#endif


#ifdef __cplusplus
} /* extern "C" */
#endif

#endif
