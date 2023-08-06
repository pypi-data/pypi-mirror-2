/*
 * Automatically generated file
 */

//static PyObject* Haiku_Entry_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Entry_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Entry_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Entry_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BEntry();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Entry_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Entry_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Entry_Object* python_self;
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	bool traverse = false;
	PyObject* py_traverse; // from generate_py ()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Entry_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O|O", &py_ref, &py_traverse);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	traverse = (bool)(PyObject_IsTrue(py_traverse));
	
	python_self->cpp_object = new BEntry(ref, traverse);
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
//static int Haiku_Entry_init(Haiku_Entry_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Entry_init(Haiku_Entry_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* path;
	bool traverse = false;
	PyObject* py_traverse; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|O", &path, &py_traverse);
	traverse = (bool)(PyObject_IsTrue(py_traverse));
	
	python_self->cpp_object = new BEntry(path, traverse);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Entry_newFromEntry(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Entry_newFromEntry(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Entry_Object* python_self;
	const BEntry entry;
	Haiku_Entry_Object* py_entry; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Entry_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_entry);
	if (py_entry != NULL) {
		memcpy((void*)&entry, (void*)((Haiku_Entry_Object*)py_entry)->cpp_object, sizeof(const BEntry));
	}
	
	python_self->cpp_object = new BEntry(entry);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Entry_DESTROY(Haiku_Entry_Object* python_self);
static void Haiku_Entry_DESTROY(Haiku_Entry_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Entry_InitCheck(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_InitCheck(Haiku_Entry_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Entry_Exists(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_Exists(Haiku_Entry_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Exists();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Entry_GetStat(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_GetStat(Haiku_Entry_Object* python_self, PyObject* python_args) {
	struct stat* stat;
	status_t retval;
	Haiku_stat_Object* py_stat; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetStat(stat);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_stat = (Haiku_stat_Object*)Haiku_stat_PyType.tp_alloc(&Haiku_stat_PyType, 0);
	py_stat->cpp_object = (struct stat*)stat;
	// we own this object, so we can delete it
	py_stat->can_delete_cpp_object = true;
	return (PyObject*)py_stat;
}

//static PyObject* Haiku_Entry_SetToEntryRef(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_SetToEntryRef(Haiku_Entry_Object* python_self, PyObject* python_args) {
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	bool traverse = false;
	PyObject* py_traverse; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O|O", &py_ref, &py_traverse);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	traverse = (bool)(PyObject_IsTrue(py_traverse));
	
	retval = python_self->cpp_object->SetTo(ref, traverse);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Entry_SetTo(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_SetTo(Haiku_Entry_Object* python_self, PyObject* python_args) {
	const char* path;
	bool traverse = false;
	PyObject* py_traverse; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|O", &path, &py_traverse);
	traverse = (bool)(PyObject_IsTrue(py_traverse));
	
	retval = python_self->cpp_object->SetTo(path, traverse);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Entry_Unset(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_Unset(Haiku_Entry_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unset();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Entry_GetRef(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_GetRef(Haiku_Entry_Object* python_self, PyObject* python_args) {
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetRef(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Entry_GetPath(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_GetPath(Haiku_Entry_Object* python_self, PyObject* python_args) {
	BPath* path = new BPath();
	status_t retval;
	Haiku_Path_Object* py_path; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetPath(path);
	
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

//static PyObject* Haiku_Entry_GetParent(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_GetParent(Haiku_Entry_Object* python_self, PyObject* python_args) {
	BEntry* entry;
	status_t retval;
	Haiku_Entry_Object* py_entry; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetParent(entry);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_entry = (Haiku_Entry_Object*)Haiku_Entry_PyType.tp_alloc(&Haiku_Entry_PyType, 0);
	py_entry->cpp_object = (BEntry*)entry;
	// we own this object, so we can delete it
	py_entry->can_delete_cpp_object = true;
	return (PyObject*)py_entry;
}

//static PyObject* Haiku_Entry_GetName(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_GetName(Haiku_Entry_Object* python_self, PyObject* python_args) {
	char* buffer;
	status_t retval;
	PyObject* py_buffer; // from generate_py()
	Py_ssize_t py_buffer_length;
	
	retval = python_self->cpp_object->GetName(buffer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_buffer = Py_BuildValue("s", &buffer);	// 's' instead of 's#' lets Python calculate length
	
	py_buffer_length = PyString_Size(py_buffer);
	if (py_buffer_length > B_FILE_NAME_LENGTH) {
		py_buffer_length = B_FILE_NAME_LENGTH;
		_PyString_Resize(&py_buffer, py_buffer_length);
	}
	
	return py_buffer;
}

//static PyObject* Haiku_Entry_Rename(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_Rename(Haiku_Entry_Object* python_self, PyObject* python_args) {
	const char* path;
	bool clobber = false;
	PyObject* py_clobber; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|O", &path, &py_clobber);
	clobber = (bool)(PyObject_IsTrue(py_clobber));
	
	retval = python_self->cpp_object->Rename(path, clobber);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Entry_Remove(Haiku_Entry_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Entry_Remove(Haiku_Entry_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Remove();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_Entry_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Entry_Object*)a)->cpp_object == *((Haiku_Entry_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Entry_Object*)a)->cpp_object != *((Haiku_Entry_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Entry_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Entry_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromEntryRef", (PyCFunction)Haiku_Entry_newFromEntryRef, METH_VARARGS|METH_CLASS, ""},
	{"FromEntry", (PyCFunction)Haiku_Entry_newFromEntry, METH_VARARGS|METH_CLASS, ""},
	{"InitCheck", (PyCFunction)Haiku_Entry_InitCheck, METH_VARARGS, ""},
	{"Exists", (PyCFunction)Haiku_Entry_Exists, METH_VARARGS, ""},
	{"GetStat", (PyCFunction)Haiku_Entry_GetStat, METH_VARARGS, ""},
	{"SetToEntryRef", (PyCFunction)Haiku_Entry_SetToEntryRef, METH_VARARGS, ""},
	{"SetTo", (PyCFunction)Haiku_Entry_SetTo, METH_VARARGS, ""},
	{"Unset", (PyCFunction)Haiku_Entry_Unset, METH_VARARGS, ""},
	{"GetRef", (PyCFunction)Haiku_Entry_GetRef, METH_VARARGS, ""},
	{"GetPath", (PyCFunction)Haiku_Entry_GetPath, METH_VARARGS, ""},
	{"GetParent", (PyCFunction)Haiku_Entry_GetParent, METH_VARARGS, ""},
	{"GetName", (PyCFunction)Haiku_Entry_GetName, METH_VARARGS, ""},
	{"Rename", (PyCFunction)Haiku_Entry_Rename, METH_VARARGS, ""},
	{"Remove", (PyCFunction)Haiku_Entry_Remove, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Entry_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Entry";
	type->tp_basicsize   = sizeof(Haiku_Entry_Object);
	type->tp_dealloc     = (destructor)Haiku_Entry_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Entry_RichCompare;
	type->tp_methods     = Haiku_Entry_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Statable_PyType;
	type->tp_init        = (initproc)Haiku_Entry_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

