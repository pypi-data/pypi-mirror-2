/*
 * Automatically generated file
 */

/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_node_ref_init(Haiku_node_ref_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_node_ref_init(Haiku_node_ref_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new node_ref();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_node_ref_newFromNodeRef(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_node_ref_newFromNodeRef(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_node_ref_Object* python_self;
	node_ref ref;
	Haiku_node_ref_Object* py_ref; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_node_ref_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		memcpy((void*)&ref, (void*)((Haiku_node_ref_Object*)py_ref)->cpp_object, sizeof(node_ref));
	}
	
	python_self->cpp_object = new node_ref(ref);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_node_ref_DESTROY(Haiku_node_ref_Object* python_self);
static void Haiku_node_ref_DESTROY(Haiku_node_ref_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_node_ref_Object_getdevice(Haiku_node_ref_Object* python_self, void* python_closure) {
	PyObject* py_device; // from generate()
	py_device = Py_BuildValue("l", python_self->cpp_object->device);
	return py_device;
}

static int Haiku_node_ref_Object_setdevice(Haiku_node_ref_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->device = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_node_ref_Object_getnode(Haiku_node_ref_Object* python_self, void* python_closure) {
	PyObject* py_node; // from generate()
	py_node = Py_BuildValue("l", python_self->cpp_object->node);
	return py_node;
}

static int Haiku_node_ref_Object_setnode(Haiku_node_ref_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->node = (ino_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_node_ref_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_node_ref_Object*)a)->cpp_object == *((Haiku_node_ref_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_node_ref_Object*)a)->cpp_object != *((Haiku_node_ref_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_node_ref_PyProperties[] = {
	{ (char*)"device", (getter)Haiku_node_ref_Object_getdevice, (setter)Haiku_node_ref_Object_setdevice, (char*)"<DOC>", NULL},
	{ (char*)"node", (getter)Haiku_node_ref_Object_getnode, (setter)Haiku_node_ref_Object_setnode, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static PyMethodDef Haiku_node_ref_PyMethods[] = {
	{"FromNodeRef", (PyCFunction)Haiku_node_ref_newFromNodeRef, METH_VARARGS|METH_CLASS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_node_ref_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.node_ref";
	type->tp_basicsize   = sizeof(Haiku_node_ref_Object);
	type->tp_dealloc     = (destructor)Haiku_node_ref_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_node_ref_RichCompare;
	type->tp_methods     = Haiku_node_ref_PyMethods;
	type->tp_getset      = Haiku_node_ref_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_node_ref_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

