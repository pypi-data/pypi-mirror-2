/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_HandlerConstants_PyMethods[] = {
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
//static int Haiku_Handler_init(Haiku_Handler_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Handler_init(Haiku_Handler_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name = NULL;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "|s", &name);
	
	python_self->cpp_object = new BHandler(name);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Handler_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Handler_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Handler_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Handler_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BHandler();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Handler_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Handler_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Handler_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Handler_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BHandler(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Handler_DESTROY(Haiku_Handler_Object* python_self);
static void Haiku_Handler_DESTROY(Haiku_Handler_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Handler_Instantiate(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_Instantiate(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	BArchivable* retval;
	Haiku_Archivable_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->Instantiate(data);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Archivable_Object*)Haiku_Archivable_PyType.tp_alloc(&Haiku_Archivable_PyType, 0);
	py_retval->cpp_object = (BArchivable*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Handler_Archive(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_Archive(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessage* data;
	bool deep = true;
	PyObject* py_deep; // from generate_py ()
	status_t retval;
	Haiku_Message_Object* py_data; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_deep);
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->Archive(data, deep);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_data->cpp_object = (BMessage*)data;
	// we own this object, so we can delete it
	py_data->can_delete_cpp_object = true;
	return (PyObject*)py_data;
}

//static PyObject* Haiku_Handler_Looper(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_Looper(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BLooper* retval;
	Haiku_Looper_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Looper();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Looper_Object*)Haiku_Looper_PyType.tp_alloc(&Haiku_Looper_PyType, 0);
	py_retval->cpp_object = (BLooper*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Handler_LockLooper(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_LockLooper(Haiku_Handler_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LockLooper();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Handler_LockLooperWithTimeout(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_LockLooperWithTimeout(Haiku_Handler_Object* python_self, PyObject* python_args) {
	bigtime_t timeout;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &timeout);
	
	retval = python_self->cpp_object->LockLooperWithTimeout(timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_UnlockLooper(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_UnlockLooper(Haiku_Handler_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->UnlockLooper();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_ResolveSpecifier(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_ResolveSpecifier(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 index;
	BMessage* specifier;
	Haiku_Message_Object* py_specifier; // from generate_py()
	int32 form;
	const char* property;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OlOls", &py_message, &index, &py_specifier, &form, &property);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_specifier != NULL) {
		specifier = ((Haiku_Message_Object*)py_specifier)->cpp_object;
	}
	
	retval = python_self->cpp_object->ResolveSpecifier(message, index, specifier, form, property);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Handler_GetSupportedSuites(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_GetSupportedSuites(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetSupportedSuites(data);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StartWatching(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StartWatching(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	uint32 what;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "Ok", &py_target, &what);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StartWatching(target, what);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StartWatchingAll(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StartWatchingAll(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StartWatchingAll(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StopWatching(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StopWatching(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	uint32 what;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "Ok", &py_target, &what);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StopWatching(target, what);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StopWatchingAll(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StopWatchingAll(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StopWatchingAll(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StartWatchingHandler(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StartWatchingHandler(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BHandler* observer;
	Haiku_Handler_Object* py_observer; // from generate_py()
	uint32 what;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "Ok", &py_observer, &what);
	if (py_observer != NULL) {
		observer = ((Haiku_Handler_Object*)py_observer)->cpp_object;
	}
	
	retval = python_self->cpp_object->StartWatching(observer, what);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StartWatchingHandlerAll(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StartWatchingHandlerAll(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BHandler* observer;
	Haiku_Handler_Object* py_observer; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_observer);
	if (py_observer != NULL) {
		observer = ((Haiku_Handler_Object*)py_observer)->cpp_object;
	}
	
	retval = python_self->cpp_object->StartWatchingAll(observer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StopWatchingHandler(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StopWatchingHandler(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BHandler* observer;
	Haiku_Handler_Object* py_observer; // from generate_py()
	uint32 what;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "Ok", &py_observer, &what);
	if (py_observer != NULL) {
		observer = ((Haiku_Handler_Object*)py_observer)->cpp_object;
	}
	
	retval = python_self->cpp_object->StopWatching(observer, what);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_StopWatchingHandlerAll(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_StopWatchingHandlerAll(Haiku_Handler_Object* python_self, PyObject* python_args) {
	BHandler* observer;
	Haiku_Handler_Object* py_observer; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_observer);
	if (py_observer != NULL) {
		observer = ((Haiku_Handler_Object*)py_observer)->cpp_object;
	}
	
	retval = python_self->cpp_object->StopWatchingAll(observer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_SendNotices(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_SendNotices(Haiku_Handler_Object* python_self, PyObject* python_args) {
	uint32 what;
	BMessage* notice = NULL;
	Haiku_Message_Object* py_notice; // from generate_py()
	
	PyArg_ParseTuple(python_args, "k|O", &what, &py_notice);
	if (py_notice != NULL) {
		notice = ((Haiku_Message_Object*)py_notice)->cpp_object;
	}
	
	python_self->cpp_object->SendNotices(what, notice);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Handler_IsWatched(Haiku_Handler_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Handler_IsWatched(Haiku_Handler_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsWatched();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_Handler_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Handler_Object*)a)->cpp_object == ((Haiku_Handler_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Handler_Object*)a)->cpp_object != ((Haiku_Handler_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Handler_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Handler_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Handler_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Handler_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Handler_Archive, METH_VARARGS, ""},
	{"Looper", (PyCFunction)Haiku_Handler_Looper, METH_VARARGS, ""},
	{"LockLooper", (PyCFunction)Haiku_Handler_LockLooper, METH_VARARGS, ""},
	{"LockLooperWithTimeout", (PyCFunction)Haiku_Handler_LockLooperWithTimeout, METH_VARARGS, ""},
	{"UnlockLooper", (PyCFunction)Haiku_Handler_UnlockLooper, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Handler_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Handler_GetSupportedSuites, METH_VARARGS, ""},
	{"StartWatching", (PyCFunction)Haiku_Handler_StartWatching, METH_VARARGS, ""},
	{"StartWatchingAll", (PyCFunction)Haiku_Handler_StartWatchingAll, METH_VARARGS, ""},
	{"StopWatching", (PyCFunction)Haiku_Handler_StopWatching, METH_VARARGS, ""},
	{"StopWatchingAll", (PyCFunction)Haiku_Handler_StopWatchingAll, METH_VARARGS, ""},
	{"StartWatchingHandler", (PyCFunction)Haiku_Handler_StartWatchingHandler, METH_VARARGS, ""},
	{"StartWatchingHandlerAll", (PyCFunction)Haiku_Handler_StartWatchingHandlerAll, METH_VARARGS, ""},
	{"StopWatchingHandler", (PyCFunction)Haiku_Handler_StopWatchingHandler, METH_VARARGS, ""},
	{"StopWatchingHandlerAll", (PyCFunction)Haiku_Handler_StopWatchingHandlerAll, METH_VARARGS, ""},
	{"SendNotices", (PyCFunction)Haiku_Handler_SendNotices, METH_VARARGS, ""},
	{"IsWatched", (PyCFunction)Haiku_Handler_IsWatched, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Handler_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Handler";
	type->tp_basicsize   = sizeof(Haiku_Handler_Object);
	type->tp_dealloc     = (destructor)Haiku_Handler_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Handler_RichCompare;
	type->tp_methods     = Haiku_Handler_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)Haiku_Handler_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

