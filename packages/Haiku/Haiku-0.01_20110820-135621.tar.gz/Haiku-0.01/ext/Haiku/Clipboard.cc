/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_ClipboardConstants_PyMethods[] = {
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
//static int Haiku_Clipboard_init(Haiku_Clipboard_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Clipboard_init(Haiku_Clipboard_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name;
	bool discard = false;
	PyObject* py_discard; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|O", &name, &py_discard);
	discard = (bool)(PyObject_IsTrue(py_discard));
	
	python_self->cpp_object = new BClipboard(name, discard);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_Clipboard_DESTROY(Haiku_Clipboard_Object* python_self);
static void Haiku_Clipboard_DESTROY(Haiku_Clipboard_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Clipboard_Name(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Name(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Name();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Clipboard_LocalCount(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_LocalCount(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LocalCount();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Clipboard_SystemCount(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_SystemCount(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->SystemCount();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Clipboard_StartWatching(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_StartWatching(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StartWatching(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_StopWatching(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_StopWatching(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StopWatching(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_Lock(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Lock(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Lock();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Clipboard_Unlock(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Unlock(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unlock();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_IsLocked(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_IsLocked(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLocked();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Clipboard_Clear(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Clear(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Clear();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_Commit(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Commit(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	bool failIfChanged = false;
	PyObject* py_failIfChanged; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|O", &py_failIfChanged);
	failIfChanged = (bool)(PyObject_IsTrue(py_failIfChanged));
	
	retval = python_self->cpp_object->Commit(failIfChanged);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_Revert(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Revert(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Revert();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Clipboard_DataSource(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_DataSource(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	BMessenger retval;
	Haiku_Messenger_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->DataSource();
	
	py_retval = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_retval->cpp_object = (BMessenger*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Clipboard_Data(Haiku_Clipboard_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Clipboard_Data(Haiku_Clipboard_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Data();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Clipboard_Object_be_clipboard(Haiku_Clipboard_Object* python_dummy) {
	Haiku_Clipboard_Object* py_be_clipboard;
	py_be_clipboard = (Haiku_Clipboard_Object*)Haiku_Clipboard_PyType.tp_alloc(&Haiku_Clipboard_PyType, 0);
	py_be_clipboard->cpp_object = (BClipboard*)be_clipboard;
	// cannot delete this object; we do not own it
	py_be_clipboard->can_delete_cpp_object = false;
	return (PyObject*)py_be_clipboard;
}

static PyObject* Haiku_Clipboard_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Clipboard_Object*)a)->cpp_object == ((Haiku_Clipboard_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Clipboard_Object*)a)->cpp_object != ((Haiku_Clipboard_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Clipboard_PyMethods[] = {
	{"Name", (PyCFunction)Haiku_Clipboard_Name, METH_VARARGS, ""},
	{"LocalCount", (PyCFunction)Haiku_Clipboard_LocalCount, METH_VARARGS, ""},
	{"SystemCount", (PyCFunction)Haiku_Clipboard_SystemCount, METH_VARARGS, ""},
	{"StartWatching", (PyCFunction)Haiku_Clipboard_StartWatching, METH_VARARGS, ""},
	{"StopWatching", (PyCFunction)Haiku_Clipboard_StopWatching, METH_VARARGS, ""},
	{"Lock", (PyCFunction)Haiku_Clipboard_Lock, METH_VARARGS, ""},
	{"Unlock", (PyCFunction)Haiku_Clipboard_Unlock, METH_VARARGS, ""},
	{"IsLocked", (PyCFunction)Haiku_Clipboard_IsLocked, METH_VARARGS, ""},
	{"Clear", (PyCFunction)Haiku_Clipboard_Clear, METH_VARARGS, ""},
	{"Commit", (PyCFunction)Haiku_Clipboard_Commit, METH_VARARGS, ""},
	{"Revert", (PyCFunction)Haiku_Clipboard_Revert, METH_VARARGS, ""},
	{"DataSource", (PyCFunction)Haiku_Clipboard_DataSource, METH_VARARGS, ""},
	{"Data", (PyCFunction)Haiku_Clipboard_Data, METH_VARARGS, ""},
	{"be_clipboard", (PyCFunction)Haiku_Clipboard_Object_be_clipboard, METH_NOARGS|METH_STATIC, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Clipboard_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Clipboard";
	type->tp_basicsize   = sizeof(Haiku_Clipboard_Object);
	type->tp_dealloc     = (destructor)Haiku_Clipboard_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Clipboard_RichCompare;
	type->tp_methods     = Haiku_Clipboard_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Clipboard_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

