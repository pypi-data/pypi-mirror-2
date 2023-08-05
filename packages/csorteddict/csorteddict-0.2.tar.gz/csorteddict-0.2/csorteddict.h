#include <Python.h>

#ifndef CSortedDict_H
#define CSortedDict_H

#ifdef __cplusplus
extern "C" {
#endif

typedef struct _AANode
{
    PyObject* key;
    PyObject* value;
    int level;
    void* left;
    void* right;
} AANode;

typedef struct _SortedDict
{
    PyObject_HEAD
    AANode* T;
    unsigned version;
} SortedDict;

typedef struct _AANodeStack
{
    AANode* node;
    void* next;
    char state;
} AANodeStack;

typedef enum { KEY_ONLY, VALUE_ONLY, KEY_AND_VALUE } itertype;

typedef struct _SortedDictIterator
{
    PyObject_HEAD
    itertype key_or_value_or_both;
    AANodeStack* stack;
    unsigned version;
    SortedDict* sorted_dict;
} SortedDictIterator;

#ifdef __cplusplus
}
#endif
#endif
