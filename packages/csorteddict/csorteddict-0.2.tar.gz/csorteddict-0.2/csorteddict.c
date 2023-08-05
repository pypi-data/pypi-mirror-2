#include <Python.h>
#include "csorteddict.h"

#define LEFT(x) ((AANode*)(x->left))
#define RIGHT(x) ((AANode*)(x->right))
#define LEAF(x) ((x == NULL)||(x && x->right == NULL && x->left == NULL))

AANodeStack* SSaddnode(AANodeStack* stack, AANode* node)
{
    AANodeStack* new_node;
    if (node == NULL)
        return stack;
    new_node = (AANodeStack*)PyMem_Malloc(sizeof(AANodeStack));
    new_node->node = node;
    new_node->next = stack;
    new_node->state = 0;
    return new_node;
}

void SSdelete(AANodeStack* node)
{
    while (node) {
        AANodeStack* next = (AANodeStack*)(node->next);
        PyMem_Free(node);
        node = next;
    }
}

AANodeStack* SSpop(AANodeStack* node)
{
    AANodeStack* next;
    if (node == NULL)
        return NULL;
    next = (AANodeStack*)node->next;
    PyMem_Free(node);
    return next;
}

AANode* AApredecessor(AANode* T)
{
    // One left, right until you hit NULL
    AANode* A = LEFT(T);
    AANode* B = A;
    if (A == NULL)
        return A;
    while (B != NULL) {
        A = B;
        B = RIGHT(B);
    }
    return A;
}

AANode* AAsuccessor(AANode* T)
{
    // One right, left until you hit NULL
    AANode* A = RIGHT(T);
    AANode* B = A;
    if (A == NULL)
        return A;
    while (B != NULL) {
        A = B;
        B = LEFT(B);
    }
    return A;
}

AANode* AAget(AANode* T, PyObject* key)
{
    int result;
    if (!T)
        return T;
    result = 0;
    // Identity first
    if (T->key != key)
    {
        if (PyObject_Cmp(key, T->key, &result) < 0) {
            AANode* val;
            if (PyErr_Occurred())
                PyErr_Clear();
            PyErr_WarnEx(PyExc_RuntimeWarning, "Some comparison failed; your items may be unreachable", 1);
            // Do the inefficient
            val = AAget(RIGHT(T), key);
            if (!val)
                val = AAget(LEFT(T), key);
            return val;
        }
    }
    
    if (result > 0) { // key > node
        return AAget(RIGHT(T), key);
    } else if (result < 0) { // key < node
        return AAget(LEFT(T), key);
    } else {
        return T;
    }
}

// So this makes the whole thing O(n), which is sad, but sometimes necessary.
AANode* AAgetlookreallyhard(AANode* T, PyObject* key)
{
    int result;
    if (!T)
        return T;
    result = 0;
    // Identity first
    if (T->key != key)
    {
        if (PyObject_Cmp(key, T->key, &result) < 0) {
            if (PyErr_Occurred())
                PyErr_Clear();
            PyErr_WarnEx(PyExc_RuntimeWarning, "Some comparison failed; your items may be unreachable", 1);
        }
    }
    if (result != 0) {
        // Do the inefficient
        AANode* val = AAgetlookreallyhard(RIGHT(T), key);
        if (!val)
            val = AAgetlookreallyhard(LEFT(T), key);
        return val;
    }

    return T;
}

AANode* AAskew(AANode* T)
{
    if (T == NULL)
        return NULL;
    else if (LEFT(T) && (LEFT(T)->level == T->level)) {
        AANode* L = LEFT(T);
        T->left = RIGHT(L);
        L->right = T;
        return L;
    }
    else
        return T;
}

AANode* AAsplit(AANode* T)
{
    if (T == NULL)
        return NULL;
    else if ((RIGHT(T)) && (RIGHT(T)->right) && (T->level == RIGHT(RIGHT(T))->level)) {
        AANode* R = RIGHT(T);
        T->right = R->left;
        R->left = T;
        (R->level)++;
        return R;
    }
    else
        return T;
}

AANode* AAdecrease_level(AANode* T)
{
    int left_level = 0;
    int right_level = 0;
    int should_be = 0;
    if (T == NULL)
        return NULL;
    left_level = T->level;
    right_level = T->level;
    if (T->left)
        left_level = LEFT(T)->level;
    if (T->right)
        right_level = RIGHT(T)->level;
    should_be = (left_level > right_level ? right_level : left_level)+1;
    if (should_be < T->level) {
        T->level = should_be;
        if (T->right && (should_be < RIGHT(T)->level))
            RIGHT(T)->level = should_be;
    }
    return T;
}

AANode* AAdelete(PyObject* key, AANode* T)
{
    int result;
    if (!T)
        return T;
    result = 0;
    // Identity first
    if (T->key != key)
    {
        if (PyObject_Cmp(key, T->key, &result) < 0) {
            PyErr_Clear();
            PyErr_WarnEx(PyExc_RuntimeWarning, "Some comparison failed; your items may be unreachable", 1);
            // To be safe, keep drilling. If you have broken comparators, this operation thus becomes
            // FANTASTICALLY inefficient.
            T->right = AAdelete(key, RIGHT(T));
            T->left = AAdelete(key, LEFT(T));
            return T;
        }
    }
    if (result > 0) { // key > node
        T->right = AAdelete(key, RIGHT(T));
    } else if (result < 0) { // key < node
        T->left = AAdelete(key, LEFT(T));
    } else { // key == node
        if LEAF(T) {
            Py_DECREF(T->key);
            Py_DECREF(T->value);
            PyMem_Free(T);
            return NULL;
        } else if (T->left == NULL) {
            AANode* L = AAsuccessor(T);
            Py_INCREF(L->key);
            Py_INCREF(L->value);
            Py_DECREF(T->key);
            Py_DECREF(T->value);
            T->key = L->key;
            T->value = L->value;
            T->right = AAdelete(L->key, RIGHT(T));
        } else {
            AANode* L = AApredecessor(T);
            Py_INCREF(L->key);
            Py_INCREF(L->value);
            Py_DECREF(T->key);
            Py_DECREF(T->value);
            T->key = L->key;
            T->value = L->value;
            T->left = AAdelete(L->key, LEFT(T));
        }
    }
    T = AAskew(AAdecrease_level(T));
    T->right = AAskew(RIGHT(T));
    if (T->right) {
        AANode* rt = RIGHT(T);
        rt->right = AAskew(RIGHT(rt));
    }
    T = AAsplit(T);
    T->right = AAsplit(RIGHT(T));
    return T;
}

AANode* AAinsert(PyObject* key, PyObject* value, AANode* T)
{
    int result = 0;
    // No value is a deletion
    if (value == NULL) {
        return AAdelete(key, T);
    }
    if (T == NULL) {
        T = PyMem_Malloc(sizeof(AANode));
        T->key = key;
        T->value = value;
        T->left = NULL;
        T->right = NULL;
        T->level = 1;
        Py_INCREF(T->key);
        Py_INCREF(T->value);
        return T;
    } else if (T->key == key) {
        Py_INCREF(value);
        Py_DECREF(T->value);
        T->value = value;
        return T;
    }
    if (key != T->key) {
        if (PyObject_Cmp(key, T->key, &result) < 0) {
            PyErr_SetString(PyExc_KeyError, "Some comparison failed on a key; your sorteddict may be in an unstable state.");
            return T;
        }
    }
    if (result > 0) { // key > node
        T->right = AAinsert(key, value, T->right);
    } else if (result < 0) { // key < node
        T->left = AAinsert(key, value, T->left);
    } else { // key == node
        Py_INCREF(value);
        Py_DECREF(T->value);
        T->value = value;
        return T;
    }

    T = AAskew(T);
    T = AAsplit(T);
    return T;
}

void AAalldone(AANode* node, PyObject* seen_addrs)
{
    AANode* right = NULL;
    AANode* left = NULL;
    PyObject* ptr_addr = NULL;
    if (!node)
        return;

    if (node->key) {
        Py_DECREF(node->key);
    }
    if (node->value) {
        Py_DECREF(node->value);
    }

    right = RIGHT(node);
    left = LEFT(node);

    ptr_addr = PyInt_FromLong((unsigned)node);
    if (!PySet_Contains(seen_addrs, ptr_addr)) {
        PySet_Add(seen_addrs, ptr_addr);
        Py_DECREF(ptr_addr);
        PyMem_Free(node);
    }

    if (right)
        AAalldone(right, seen_addrs);

    if (left)
        AAalldone(left, seen_addrs);
}

static Py_ssize_t SortedDictLengthHelper(AANode* current)
{
    Py_ssize_t count = 0;
    if (current)
    {
        count++;
        count += SortedDictLengthHelper(current->left);
        count += SortedDictLengthHelper(current->right);
    }
    return count;
}

static Py_ssize_t SortedDict_length(SortedDict* self)
{
    if (self->T == NULL)
        return 0;
    return SortedDictLengthHelper(self->T);
}

static PyObject* SortedDict_getitem(SortedDict* self, PyObject* key)
{
    AANode* node = AAget(self->T, key);
    // Bubble up error
    if (PyErr_Occurred())
        return NULL;

    if (!node) {
        PyErr_SetString(PyExc_KeyError, "Key not found.");
        return 0;
    }

    if (node->value)
        Py_INCREF(node->value);

    return node->value;
}

static int SortedDict_setitem(SortedDict* self, PyObject* key, PyObject* value)
{
    if (PyList_Check(key)||PyDict_Check(key))
        PyErr_WarnEx(PyExc_RuntimeWarning, "Lists and dictionaries are dangerous to use as keys.", 1);
    self->T = AAinsert(key, value, self->T);
    self->version ^= (unsigned int)key;
    if (PyErr_Occurred())
        return -1;
    return 0;
}

static int SortedDict_contains(SortedDict* self, PyObject* key)
{
    AANode* node = AAget(self->T, key);
    if (PyErr_Occurred())
        return -1;
    return (node != NULL);
}

static PyObject* SortedDict_new(PyTypeObject* type, PyObject* args, PyObject* keywds)
{
    SortedDict* self;
    if (!(self = ((SortedDict *)type->tp_alloc(type, 0))))
    {
        PyErr_SetString(PyExc_MemoryError, "Could not allocate new Sorted Dictionary");
        return NULL;
    }
    self->T = NULL;
    self->version = 0;
    return (PyObject *)self;
}

static void SortedDict_dealloc(SortedDict* self)
{
    PyObject* seen_set = PySet_New(NULL);
    AAalldone(self->T, seen_set);
    Py_DECREF(seen_set);
    self->ob_type->tp_free(self);
}

static long SortedDict_hash(PyObject* self) {
  PyErr_SetString(PyExc_TypeError, "SortedDict objects are unhashable");
  return -1;
}

PyObject* SortedDict_get(SortedDict* self, PyObject* args)
{
    PyObject* key = NULL;
    PyObject* defaultvalue = NULL;
    AANode* item = NULL;
    if (!PyArg_ParseTuple(args, "O|O", &key, &defaultvalue))
        return NULL;
    item = AAget(self->T, key);
    if (PyErr_Occurred())
        return NULL;
    if (item) {
        Py_INCREF(item->value);
        return item->value;
    } else if (defaultvalue) {
        Py_INCREF(defaultvalue);
        return defaultvalue;
    } else {
        PyErr_SetString(PyExc_KeyError, "Key not found.");
        return NULL;
    }
}

PyObject* value_for_node(AANode* node, int mode)
{
    if (mode == KEY_ONLY) {
        Py_INCREF(node->key);
        return node->key;
    } else if (mode == VALUE_ONLY) {
        Py_INCREF(node->value);
        return node->value;
    } else if (mode == KEY_AND_VALUE) {
        PyObject* tuple = PyTuple_New(2);
        Py_INCREF(node->key);
        Py_INCREF(node->value);
        PyTuple_SetItem(tuple, 0, node->key);
        PyTuple_SetItem(tuple, 1, node->value);
        return tuple;
    }
    PyErr_SetString(PyExc_RuntimeError, "Unknown iteration method");
    return 0;
}

PyObject* SortedDictIter_iternextitem(SortedDictIterator *self)
{
    if (self->sorted_dict->version != self->version)
    {
        PyErr_SetString(PyExc_RuntimeError, "Sorted dictionary has changed!");
        return NULL;
    }
    if (self->stack == NULL) {
        PyErr_SetString(PyExc_StopIteration, "Ok, all done.");
        return NULL;
    }
    while (self->stack->state == 0 && self->stack->node->left)
    {
        self->stack->state++;
        self->stack = SSaddnode(self->stack, self->stack->node->left);
    }
    if (self->stack->state == 0 && self->stack->node->left == NULL)
        self->stack->state++;
    if (self->stack->state == 1) {
        AANode* right = NULL;
        PyObject* retval = NULL;
        self->stack->state++;
        right = self->stack->node->right;
        retval = value_for_node(self->stack->node, self->key_or_value_or_both);
        self->stack = SSpop(self->stack);
        if (right)
            self->stack = SSaddnode(self->stack, right);
        return retval;
    } else {
        PyErr_SetString(PyExc_StopIteration, "Ok, all done.");
        return NULL;
    }
}

static void SortedDictIter_dealloc(SortedDictIterator *self)
{
    Py_DECREF(self->sorted_dict);
    SSdelete(self->stack);
    self->ob_type->tp_free(self);
}

static PyMethodDef SortedDictIter_methods[] = {
    {NULL, NULL}
};

PyTypeObject SortedDictIter_Type = {
    PyObject_HEAD_INIT(NULL)
    0, 
    "sorteddict-iterator",                      /* tp_name */
    sizeof(SortedDictIterator),                 /* tp_basicsize */
    0,                                          /* tp_itemsize */
    (destructor)SortedDictIter_dealloc,         /* tp_dealloc */
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
    PyObject_GenericGetAttr,                    /* tp_getattro */
    0,                                          /* tp_setattro */
    0,                                          /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,    /* tp_flags */
    0,                                          /* tp_doc */
    0,                                          /* tp_traverse */
    0,                                          /* tp_clear */
    0,                                          /* tp_richcompare */
    0,                                          /* tp_weaklistoffset */
    PyObject_SelfIter,                          /* tp_iter */
    (iternextfunc)SortedDictIter_iternextitem,  /* tp_iternext */
    SortedDictIter_methods,                     /* tp_methods */
    0,
};

PyObject* SortedDictIterMaker(SortedDict* self, int mode)
{
    SortedDictIterator* iter;
    if (!(iter = ((SortedDictIterator *)SortedDictIter_Type.tp_alloc(&SortedDictIter_Type, 0))))
        return 0;

    iter->key_or_value_or_both = mode;
    iter->stack = SSaddnode(NULL, self->T);
    iter->version = self->version;
    iter->sorted_dict = self;
    Py_INCREF(iter->sorted_dict);
    return (PyObject *)iter;
}

PyObject* SortedDict_GetIter_keys(SortedDict* self)
{
    return SortedDictIterMaker(self, KEY_ONLY);
}

PyObject* SortedDict_GetIter_values(SortedDict* self)
{
    return SortedDictIterMaker(self, VALUE_ONLY);
}

PyObject* SortedDict_GetIter_items(SortedDict* self)
{
    return SortedDictIterMaker(self, KEY_AND_VALUE);
}

static PyMappingMethods SortedDict_as_mapping = {
  (lenfunc)SortedDict_length,        /* mp_length (inquiry/lenfunc )*/
  (binaryfunc)SortedDict_getitem,    /* mp_subscript */
  (objobjargproc)SortedDict_setitem, /* mp_ass_subscript */
};

static PySequenceMethods SortedDict_as_sequence = {
  0,                                 /* sq_length */
  0,                                 /* sq_concat */
  0,                                 /* sq_repeat */
  0,                                 /* sq_item */
  0,                                 /* sq_slice */
  0,                                 /* sq_ass_item */
  0,                                 /* sq_ass_slice */
  (objobjproc)SortedDict_contains,   /* sq_contains */
  0,                                 /* sq_inplace_concat */
  0,                                 /* sq_inplace_repeat */
};

static PyMethodDef SortedDict_methods[] = {
    {"get", (PyCFunction)SortedDict_get, METH_VARARGS, "Get an item in the Sorted Dict, or return a default."},
    {"keys", (PyCFunction)SortedDict_GetIter_keys, METH_NOARGS, "Get an iterator over the keys in an SortedDict"},
    {"iterkeys", (PyCFunction)SortedDict_GetIter_keys, METH_NOARGS, "Get an iterator over the keys in an SortedDict"},
    {"values", (PyCFunction)SortedDict_GetIter_values, METH_NOARGS, "Get an iterator over the values in an SortedDict"},
    {"itervalues", (PyCFunction)SortedDict_GetIter_values, METH_NOARGS, "Get an iterator over the values in an SortedDict"},
    {"items", (PyCFunction)SortedDict_GetIter_items, METH_NOARGS, "Get an iterator over the items (key, value tuple) in an SortedDict"},
    {"iteritems", (PyCFunction)SortedDict_GetIter_items, METH_NOARGS, "Get an iterator over the items (key, value tuple) in an SortedDict"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject SortedDict_Type = {
  PyObject_HEAD_INIT(NULL)
  0,                                          /* ob_size */
  "sorteddict.SortedDict",                    /* tp_name */
  sizeof(SortedDict),                         /* tp_basicsize */
  0,                                          /* tp_itemsize */
  (destructor)SortedDict_dealloc,             /* tp_dealloc */
  0,                                          /* tp_print */
  0,                                          /* tp_getattr */
  0,                                          /* tp_setattr */
  0,                                          /* tp_compare */
  0,                                          /* tp_repr */
  0,                                          /* tp_as_number */
  &SortedDict_as_sequence,                    /* tp_as_sequence */
  &SortedDict_as_mapping,                     /* tp_as_mapping */
  SortedDict_hash,                            /* tp_hash  */
  0,                                          /* tp_call */
  0,                                          /* tp_str */
  0,                                          /* tp_getattro */
  0,                                          /* tp_setattro */
  0,                                          /* tp_as_buffer */
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
  "Sorted Dictionary",                        /* tp_doc */
  0,                                          /* tp_traverse */
  0,                                          /* tp_clear */
  0,                                          /* tp_richcompare */
  0,                                          /* tp_weaklistoffset */
  (getiterfunc)SortedDict_GetIter_keys,       /* tp_iter */
  0,                                          /* tp_iternext */
  SortedDict_methods,                         /* tp_methods */
  0,                                          /* tp_members */
  0,                                          /* tp_getset */
  0,                                          /* tp_base */
  0,                                          /* tp_dict */
  0,                                          /* tp_descr_get */
  0,                                          /* tp_descr_set */
  0,                                          /* tp_dictoffset */
  0,                                          /* tp_init */
  0,                                          /* tp_alloc */
  SortedDict_new,                             /* tp_new */
};

static PyMethodDef SortedDictMethods[] = {
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initcsorteddict(void)
{
    PyObject *m;

    PyType_Ready(&SortedDictIter_Type);

    if (PyType_Ready(&SortedDict_Type) < 0) {
        PyErr_SetString(PyExc_TypeError, "Could not ready the dict.");
        return;
    }

    m = Py_InitModule3("csorteddict",
                       SortedDictMethods,
                       "Sorted Dictionary Class");
    Py_INCREF(&SortedDict_Type);
    PyModule_AddObject(m, "SortedDict", (PyObject *)&SortedDict_Type);
    Py_INCREF(m);
}
