/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_QueryConstants_PyMethods[] = {
	{NULL} /* Sentinel */
};
/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Query_init(Haiku_Query_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Query_init(Haiku_Query_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BQuery();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_Query_DESTROY(Haiku_Query_Object* python_self);
static void Haiku_Query_DESTROY(Haiku_Query_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Query_Clear(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_Clear(Haiku_Query_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Clear();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushAttr(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushAttr(Haiku_Query_Object* python_self, PyObject* python_args) {
	const char* attrName;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &attrName);
	
	retval = python_self->cpp_object->PushAttr(attrName);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushOp(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushOp(Haiku_Query_Object* python_self, PyObject* python_args) {
	query_op op;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "i", &op);
	
	retval = python_self->cpp_object->PushOp(op);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushUInt32(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushUInt32(Haiku_Query_Object* python_self, PyObject* python_args) {
	uint32 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k", &value);
	
	retval = python_self->cpp_object->PushUInt32(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushInt32(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushInt32(Haiku_Query_Object* python_self, PyObject* python_args) {
	int32 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	retval = python_self->cpp_object->PushInt32(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushUInt64(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushUInt64(Haiku_Query_Object* python_self, PyObject* python_args) {
	uint64 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k", &value);
	
	retval = python_self->cpp_object->PushUInt64(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushInt64(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushInt64(Haiku_Query_Object* python_self, PyObject* python_args) {
	int64 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	retval = python_self->cpp_object->PushInt64(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushFloat(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushFloat(Haiku_Query_Object* python_self, PyObject* python_args) {
	float value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "f", &value);
	
	retval = python_self->cpp_object->PushFloat(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushDouble(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushDouble(Haiku_Query_Object* python_self, PyObject* python_args) {
	double value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "d", &value);
	
	retval = python_self->cpp_object->PushDouble(value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushString(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushString(Haiku_Query_Object* python_self, PyObject* python_args) {
	const char* value;
	bool caseInsensitive = false;
	PyObject* py_caseInsensitive; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|O", &value, &py_caseInsensitive);
	caseInsensitive = (bool)(PyObject_IsTrue(py_caseInsensitive));
	
	retval = python_self->cpp_object->PushString(value, caseInsensitive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_PushDate(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PushDate(Haiku_Query_Object* python_self, PyObject* python_args) {
	const char* date;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &date);
	
	retval = python_self->cpp_object->PushDate(date);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_SetVolume(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_SetVolume(Haiku_Query_Object* python_self, PyObject* python_args) {
	const BVolume* volume;
	Haiku_Volume_Object* py_volume; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_volume);
	if (py_volume != NULL) {
		volume = ((Haiku_Volume_Object*)py_volume)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetVolume(volume);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_SetPredicate(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_SetPredicate(Haiku_Query_Object* python_self, PyObject* python_args) {
	const char* expression;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &expression);
	
	retval = python_self->cpp_object->SetPredicate(expression);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_SetTarget(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_SetTarget(Haiku_Query_Object* python_self, PyObject* python_args) {
	BMessenger messenger;
	Haiku_Messenger_Object* py_messenger; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_messenger);
	if (py_messenger != NULL) {
		memcpy((void*)&messenger, (void*)((Haiku_Messenger_Object*)py_messenger)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->SetTarget(messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_IsLive(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_IsLive(Haiku_Query_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLive();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Query_GetPredicate(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_GetPredicate(Haiku_Query_Object* python_self, PyObject* python_args) {
	char* buffer;
	size_t length = python_self->cpp_object->PredicateLength();
	status_t retval;
	PyObject* py_buffer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|l", &length);
	
	retval = python_self->cpp_object->GetPredicate(buffer, length);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_buffer = Py_BuildValue("s#", &buffer, python_self->cpp_object->PredicateLength());
	return py_buffer;
}

//static PyObject* Haiku_Query_PredicateLength(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_PredicateLength(Haiku_Query_Object* python_self, PyObject* python_args) {
	size_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->PredicateLength();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Query_TargetDevice(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_TargetDevice(Haiku_Query_Object* python_self, PyObject* python_args) {
	dev_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TargetDevice();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Query_Fetch(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_Fetch(Haiku_Query_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Fetch();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_GetNextEntry(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_GetNextEntry(Haiku_Query_Object* python_self, PyObject* python_args) {
	BEntry* entry = new BEntry();
	bool traverse = false;
	PyObject* py_traverse; // from generate_py ()
	status_t retval;
	Haiku_Entry_Object* py_entry; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_traverse);
	traverse = (bool)(PyObject_IsTrue(py_traverse));
	
	retval = python_self->cpp_object->GetNextEntry(entry, traverse);
	
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

//static PyObject* Haiku_Query_GetNextRef(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_GetNextRef(Haiku_Query_Object* python_self, PyObject* python_args) {
	entry_ref* ref = new entry_ref();
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetNextRef(ref);
	
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

//static PyObject* Haiku_Query_GetNextDirents(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_GetNextDirents(Haiku_Query_Object* python_self, PyObject* python_args) {
	dirent* buffer;
	size_t length;
	int32 count = INT_MAX;
	int32 retval;
	Haiku_dirent_Object* py_buffer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l|l", &length, &count);
	
	retval = python_self->cpp_object->GetNextDirents(buffer, length, count);
	
	py_buffer = (Haiku_dirent_Object*)Haiku_dirent_PyType.tp_alloc(&Haiku_dirent_PyType, 0);
	py_buffer->cpp_object = (dirent*)buffer;
	// we own this object, so we can delete it
	py_buffer->can_delete_cpp_object = true;
	
	return Py_BuildValue("lO", retval, py_buffer);
}

//static PyObject* Haiku_Query_Rewind(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_Rewind(Haiku_Query_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Rewind();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Query_CountEntries(Haiku_Query_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Query_CountEntries(Haiku_Query_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountEntries();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

static PyObject* Haiku_Query_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Query_Object*)a)->cpp_object == ((Haiku_Query_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Query_Object*)a)->cpp_object != ((Haiku_Query_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Query_PyMethods[] = {
	{"Clear", (PyCFunction)Haiku_Query_Clear, METH_VARARGS, ""},
	{"PushAttr", (PyCFunction)Haiku_Query_PushAttr, METH_VARARGS, ""},
	{"PushOp", (PyCFunction)Haiku_Query_PushOp, METH_VARARGS, ""},
	{"PushUInt32", (PyCFunction)Haiku_Query_PushUInt32, METH_VARARGS, ""},
	{"PushInt32", (PyCFunction)Haiku_Query_PushInt32, METH_VARARGS, ""},
	{"PushUInt64", (PyCFunction)Haiku_Query_PushUInt64, METH_VARARGS, ""},
	{"PushInt64", (PyCFunction)Haiku_Query_PushInt64, METH_VARARGS, ""},
	{"PushFloat", (PyCFunction)Haiku_Query_PushFloat, METH_VARARGS, ""},
	{"PushDouble", (PyCFunction)Haiku_Query_PushDouble, METH_VARARGS, ""},
	{"PushString", (PyCFunction)Haiku_Query_PushString, METH_VARARGS, ""},
	{"PushDate", (PyCFunction)Haiku_Query_PushDate, METH_VARARGS, ""},
	{"SetVolume", (PyCFunction)Haiku_Query_SetVolume, METH_VARARGS, ""},
	{"SetPredicate", (PyCFunction)Haiku_Query_SetPredicate, METH_VARARGS, ""},
	{"SetTarget", (PyCFunction)Haiku_Query_SetTarget, METH_VARARGS, ""},
	{"IsLive", (PyCFunction)Haiku_Query_IsLive, METH_VARARGS, ""},
	{"GetPredicate", (PyCFunction)Haiku_Query_GetPredicate, METH_VARARGS, ""},
	{"PredicateLength", (PyCFunction)Haiku_Query_PredicateLength, METH_VARARGS, ""},
	{"TargetDevice", (PyCFunction)Haiku_Query_TargetDevice, METH_VARARGS, ""},
	{"Fetch", (PyCFunction)Haiku_Query_Fetch, METH_VARARGS, ""},
	{"GetNextEntry", (PyCFunction)Haiku_Query_GetNextEntry, METH_VARARGS, ""},
	{"GetNextRef", (PyCFunction)Haiku_Query_GetNextRef, METH_VARARGS, ""},
	{"GetNextDirents", (PyCFunction)Haiku_Query_GetNextDirents, METH_VARARGS, ""},
	{"Rewind", (PyCFunction)Haiku_Query_Rewind, METH_VARARGS, ""},
	{"CountEntries", (PyCFunction)Haiku_Query_CountEntries, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Query_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Query";
	type->tp_basicsize   = sizeof(Haiku_Query_Object);
	type->tp_dealloc     = (destructor)Haiku_Query_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Query_RichCompare;
	type->tp_methods     = Haiku_Query_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_EntryList_PyType;
	type->tp_init        = (initproc)Haiku_Query_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

