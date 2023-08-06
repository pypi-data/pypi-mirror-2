/*
 * Automatically generated file
 */

//static PyObject* Haiku_Path_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Path_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Path_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Path_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BPath();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Path_newFromPath(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Path_newFromPath(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Path_Object* python_self;
	const BPath path;
	Haiku_Path_Object* py_path; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Path_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_path);
	if (py_path != NULL) {
		memcpy((void*)&path, (void*)((Haiku_Path_Object*)py_path)->cpp_object, sizeof(const BPath));
	}
	
	python_self->cpp_object = new BPath(path);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Path_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Path_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Path_Object* python_self;
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Path_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	python_self->cpp_object = new BPath(ref);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Path_newFromEntry(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Path_newFromEntry(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Path_Object* python_self;
	const BEntry* entry;
	Haiku_Entry_Object* py_entry; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Path_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_entry);
	if (py_entry != NULL) {
		entry = ((Haiku_Entry_Object*)py_entry)->cpp_object;
	}
	
	python_self->cpp_object = new BPath(entry);
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
//static int Haiku_Path_init(Haiku_Path_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Path_init(Haiku_Path_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* path;
	const char* leaf;
	bool normalize = false;
	PyObject* py_normalize; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "ss|O", &path, &leaf, &py_normalize);
	normalize = (bool)(PyObject_IsTrue(py_normalize));
	
	python_self->cpp_object = new BPath(path, leaf, normalize);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_Path_DESTROY(Haiku_Path_Object* python_self);
static void Haiku_Path_DESTROY(Haiku_Path_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Path_InitCheck(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_InitCheck(Haiku_Path_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_SetToEntryRef(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_SetToEntryRef(Haiku_Path_Object* python_self, PyObject* python_args) {
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTo(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_SetToEntry(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_SetToEntry(Haiku_Path_Object* python_self, PyObject* python_args) {
	const BEntry* entry;
	Haiku_Entry_Object* py_entry; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_entry);
	if (py_entry != NULL) {
		entry = ((Haiku_Entry_Object*)py_entry)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTo(entry);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_SetTo(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_SetTo(Haiku_Path_Object* python_self, PyObject* python_args) {
	const char* path;
	const char* leaf;
	bool normalize = false;
	PyObject* py_normalize; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "ss|O", &path, &leaf, &py_normalize);
	normalize = (bool)(PyObject_IsTrue(py_normalize));
	
	retval = python_self->cpp_object->SetTo(path, leaf, normalize);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_Unset(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_Unset(Haiku_Path_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unset();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_Append(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_Append(Haiku_Path_Object* python_self, PyObject* python_args) {
	const char* path;
	bool normalize = false;
	PyObject* py_normalize; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|O", &path, &py_normalize);
	normalize = (bool)(PyObject_IsTrue(py_normalize));
	
	retval = python_self->cpp_object->Append(path, normalize);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Path_Path(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_Path(Haiku_Path_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	Py_ssize_t py_retval_length;
	
	retval = python_self->cpp_object->Path();
	
	py_retval = Py_BuildValue("s", retval);	// 's' instead of 's#' lets Python calculate length
	
	py_retval_length = PyString_Size(py_retval);
	if (py_retval_length > B_FILE_NAME_LENGTH) {
		py_retval_length = B_FILE_NAME_LENGTH;
		_PyString_Resize(&py_retval, py_retval_length);
	}
	
	return py_retval;
}

//static PyObject* Haiku_Path_Leaf(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_Leaf(Haiku_Path_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	Py_ssize_t py_retval_length;
	
	retval = python_self->cpp_object->Leaf();
	
	py_retval = Py_BuildValue("s", retval);	// 's' instead of 's#' lets Python calculate length
	
	py_retval_length = PyString_Size(py_retval);
	if (py_retval_length > B_FILE_NAME_LENGTH) {
		py_retval_length = B_FILE_NAME_LENGTH;
		_PyString_Resize(&py_retval, py_retval_length);
	}
	
	return py_retval;
}

//static PyObject* Haiku_Path_GetParent(Haiku_Path_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Path_GetParent(Haiku_Path_Object* python_self, PyObject* python_args) {
	BPath* path;
	status_t retval;
	Haiku_Path_Object* py_path; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetParent(path);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_path = (Haiku_Path_Object*)Haiku_Path_PyType.tp_alloc(&Haiku_Path_PyType, 0);
	py_path->cpp_object = (BPath*)path;
	// we own this object, so we can delete it
	py_path->can_delete_cpp_object = true;
	return (PyObject*)py_path;
}

static PyObject* Haiku_Path_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Path_Object*)a)->cpp_object == *((Haiku_Path_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Path_Object*)a)->cpp_object != *((Haiku_Path_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Path_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Path_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromPath", (PyCFunction)Haiku_Path_newFromPath, METH_VARARGS|METH_CLASS, ""},
	{"FromEntryRef", (PyCFunction)Haiku_Path_newFromEntryRef, METH_VARARGS|METH_CLASS, ""},
	{"FromEntry", (PyCFunction)Haiku_Path_newFromEntry, METH_VARARGS|METH_CLASS, ""},
	{"InitCheck", (PyCFunction)Haiku_Path_InitCheck, METH_VARARGS, ""},
	{"SetToEntryRef", (PyCFunction)Haiku_Path_SetToEntryRef, METH_VARARGS, ""},
	{"SetToEntry", (PyCFunction)Haiku_Path_SetToEntry, METH_VARARGS, ""},
	{"SetTo", (PyCFunction)Haiku_Path_SetTo, METH_VARARGS, ""},
	{"Unset", (PyCFunction)Haiku_Path_Unset, METH_VARARGS, ""},
	{"Append", (PyCFunction)Haiku_Path_Append, METH_VARARGS, ""},
	{"Path", (PyCFunction)Haiku_Path_Path, METH_VARARGS, ""},
	{"Leaf", (PyCFunction)Haiku_Path_Leaf, METH_VARARGS, ""},
	{"GetParent", (PyCFunction)Haiku_Path_GetParent, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Path_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Path";
	type->tp_basicsize   = sizeof(Haiku_Path_Object);
	type->tp_dealloc     = (destructor)Haiku_Path_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Path_RichCompare;
	type->tp_methods     = Haiku_Path_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Path_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

