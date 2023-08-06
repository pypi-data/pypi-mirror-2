/*
 * Automatically generated file
 */

//static PyObject* Haiku_Volume_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Volume_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Volume_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Volume_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BVolume();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Volume_init(Haiku_Volume_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Volume_init(Haiku_Volume_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	dev_t device;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "l", &device);
	
	python_self->cpp_object = new BVolume(device);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Volume_newFromVolume(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Volume_newFromVolume(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Volume_Object* python_self;
	const BVolume volume;
	Haiku_Volume_Object* py_volume; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Volume_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_volume);
	if (py_volume != NULL) {
		memcpy((void*)&volume, (void*)((Haiku_Volume_Object*)py_volume)->cpp_object, sizeof(const BVolume));
	}
	
	python_self->cpp_object = new BVolume(volume);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Volume_DESTROY(Haiku_Volume_Object* python_self);
static void Haiku_Volume_DESTROY(Haiku_Volume_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Volume_InitCheck(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_InitCheck(Haiku_Volume_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Volume_SetTo(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_SetTo(Haiku_Volume_Object* python_self, PyObject* python_args) {
	dev_t device;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &device);
	
	retval = python_self->cpp_object->SetTo(device);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Volume_Unset(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_Unset(Haiku_Volume_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unset();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Volume_Device(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_Device(Haiku_Volume_Object* python_self, PyObject* python_args) {
	dev_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Device();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Volume_Capacity(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_Capacity(Haiku_Volume_Object* python_self, PyObject* python_args) {
	off_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Capacity();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Volume_FreeBytes(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_FreeBytes(Haiku_Volume_Object* python_self, PyObject* python_args) {
	off_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FreeBytes();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Volume_BlockSize(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_BlockSize(Haiku_Volume_Object* python_self, PyObject* python_args) {
	off_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->BlockSize();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Volume_GetName(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_GetName(Haiku_Volume_Object* python_self, PyObject* python_args) {
	char* name;
	status_t retval;
	PyObject* py_name; // from generate_py()
	Py_ssize_t py_name_length;
	
	retval = python_self->cpp_object->GetName(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_name = Py_BuildValue("s", &name);	// 's' instead of 's#' lets Python calculate length
	
	py_name_length = PyString_Size(py_name);
	if (py_name_length > B_FILE_NAME_LENGTH) {
		py_name_length = B_FILE_NAME_LENGTH;
		_PyString_Resize(&py_name, py_name_length);
	}
	
	return py_name;
}

//static PyObject* Haiku_Volume_SetName(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_SetName(Haiku_Volume_Object* python_self, PyObject* python_args) {
	char* name;
	PyObject* py_name; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_name);
	name = PyString_AsString(py_name);
	
	retval = python_self->cpp_object->SetName(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Volume_GetIconData(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_GetIconData(Haiku_Volume_Object* python_self, PyObject* python_args) {
	uint8** data;
	size_t size;
	type_code type;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	retval = python_self->cpp_object->GetIcon(data, &size, &type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, size);
	
	return Py_BuildValue("Ok", py_data, type);
}

//static PyObject* Haiku_Volume_IsRemovable(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_IsRemovable(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsRemovable();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_IsReadOnly(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_IsReadOnly(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsReadOnly();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_IsPersistent(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_IsPersistent(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsPersistent();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_IsShared(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_IsShared(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsShared();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_KnowsMime(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_KnowsMime(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->KnowsMime();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_KnowsAttr(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_KnowsAttr(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->KnowsAttr();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Volume_KnowsQuery(Haiku_Volume_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Volume_KnowsQuery(Haiku_Volume_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->KnowsQuery();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_Volume_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Volume_Object*)a)->cpp_object == *((Haiku_Volume_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Volume_Object*)a)->cpp_object != *((Haiku_Volume_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Volume_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Volume_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromVolume", (PyCFunction)Haiku_Volume_newFromVolume, METH_VARARGS|METH_CLASS, ""},
	{"InitCheck", (PyCFunction)Haiku_Volume_InitCheck, METH_VARARGS, ""},
	{"SetTo", (PyCFunction)Haiku_Volume_SetTo, METH_VARARGS, ""},
	{"Unset", (PyCFunction)Haiku_Volume_Unset, METH_VARARGS, ""},
	{"Device", (PyCFunction)Haiku_Volume_Device, METH_VARARGS, ""},
	{"Capacity", (PyCFunction)Haiku_Volume_Capacity, METH_VARARGS, ""},
	{"FreeBytes", (PyCFunction)Haiku_Volume_FreeBytes, METH_VARARGS, ""},
	{"BlockSize", (PyCFunction)Haiku_Volume_BlockSize, METH_VARARGS, ""},
	{"GetName", (PyCFunction)Haiku_Volume_GetName, METH_VARARGS, ""},
	{"SetName", (PyCFunction)Haiku_Volume_SetName, METH_VARARGS, ""},
	{"GetIconData", (PyCFunction)Haiku_Volume_GetIconData, METH_VARARGS, ""},
	{"IsRemovable", (PyCFunction)Haiku_Volume_IsRemovable, METH_VARARGS, ""},
	{"IsReadOnly", (PyCFunction)Haiku_Volume_IsReadOnly, METH_VARARGS, ""},
	{"IsPersistent", (PyCFunction)Haiku_Volume_IsPersistent, METH_VARARGS, ""},
	{"IsShared", (PyCFunction)Haiku_Volume_IsShared, METH_VARARGS, ""},
	{"KnowsMime", (PyCFunction)Haiku_Volume_KnowsMime, METH_VARARGS, ""},
	{"KnowsAttr", (PyCFunction)Haiku_Volume_KnowsAttr, METH_VARARGS, ""},
	{"KnowsQuery", (PyCFunction)Haiku_Volume_KnowsQuery, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Volume_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Volume";
	type->tp_basicsize   = sizeof(Haiku_Volume_Object);
	type->tp_dealloc     = (destructor)Haiku_Volume_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Volume_RichCompare;
	type->tp_methods     = Haiku_Volume_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Volume_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

