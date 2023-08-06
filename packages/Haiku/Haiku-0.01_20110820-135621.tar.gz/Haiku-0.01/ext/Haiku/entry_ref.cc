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
//static int Haiku_entry_ref_init(Haiku_entry_ref_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_entry_ref_init(Haiku_entry_ref_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	dev_t device;
	ino_t dir;
	const char* name;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "lls", &device, &dir, &name);
	
	python_self->cpp_object = new entry_ref(device, dir, name);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_entry_ref_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_entry_ref_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_entry_ref_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_entry_ref_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new entry_ref();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_entry_ref_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_entry_ref_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_entry_ref_Object* python_self;
	entry_ref ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_entry_ref_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		memcpy((void*)&ref, (void*)((Haiku_entry_ref_Object*)py_ref)->cpp_object, sizeof(entry_ref));
	}
	
	python_self->cpp_object = new entry_ref(ref);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_entry_ref_DESTROY(Haiku_entry_ref_Object* python_self);
static void Haiku_entry_ref_DESTROY(Haiku_entry_ref_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_entry_ref_set_name(Haiku_entry_ref_Object* python_self, PyObject* python_args);
static PyObject* Haiku_entry_ref_set_name(Haiku_entry_ref_Object* python_self, PyObject* python_args) {
	const char* name;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->set_name(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_entry_ref_Object_getdevice(Haiku_entry_ref_Object* python_self, void* python_closure) {
	PyObject* py_device; // from generate()
	py_device = Py_BuildValue("l", python_self->cpp_object->device);
	return py_device;
}

static int Haiku_entry_ref_Object_setdevice(Haiku_entry_ref_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->device = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_entry_ref_Object_getdirectory(Haiku_entry_ref_Object* python_self, void* python_closure) {
	PyObject* py_directory; // from generate()
	py_directory = Py_BuildValue("l", python_self->cpp_object->directory);
	return py_directory;
}

static int Haiku_entry_ref_Object_setdirectory(Haiku_entry_ref_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->directory = (ino_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_entry_ref_Object_getname(Haiku_entry_ref_Object* python_self, void* python_closure) {
	PyObject* py_name; // from generate()
	py_name = Py_BuildValue("s", python_self->cpp_object->name);
	return py_name;
}

static int Haiku_entry_ref_Object_setname(Haiku_entry_ref_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->name = (char*)PyString_AsString(value);
	return 0;
}

static PyObject* Haiku_entry_ref_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_entry_ref_Object*)a)->cpp_object == *((Haiku_entry_ref_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_entry_ref_Object*)a)->cpp_object != *((Haiku_entry_ref_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_entry_ref_PyProperties[] = {
	{ (char*)"device", (getter)Haiku_entry_ref_Object_getdevice, (setter)Haiku_entry_ref_Object_setdevice, (char*)"<DOC>", NULL},
	{ (char*)"directory", (getter)Haiku_entry_ref_Object_getdirectory, (setter)Haiku_entry_ref_Object_setdirectory, (char*)"<DOC>", NULL},
	{ (char*)"name", (getter)Haiku_entry_ref_Object_getname, (setter)Haiku_entry_ref_Object_setname, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static PyMethodDef Haiku_entry_ref_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_entry_ref_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromEntryRef", (PyCFunction)Haiku_entry_ref_newFromEntryRef, METH_VARARGS|METH_CLASS, ""},
	{"set_name", (PyCFunction)Haiku_entry_ref_set_name, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_entry_ref_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.entry_ref";
	type->tp_basicsize   = sizeof(Haiku_entry_ref_Object);
	type->tp_dealloc     = (destructor)Haiku_entry_ref_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_entry_ref_RichCompare;
	type->tp_methods     = Haiku_entry_ref_PyMethods;
	type->tp_getset      = Haiku_entry_ref_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_entry_ref_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

