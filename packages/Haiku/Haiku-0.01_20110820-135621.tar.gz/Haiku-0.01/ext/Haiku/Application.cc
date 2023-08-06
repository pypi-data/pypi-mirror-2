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
//static int Haiku_Application_init(Haiku_Application_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Application_init(Haiku_Application_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* signature;
	status_t error;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s", &signature);
	
	python_self->cpp_object = new BApplication(signature, &error);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	if (error != B_OK) {
		PyObject* errval = Py_BuildValue("l", error);
		PyErr_SetObject(HaikuError, errval);
		return -1;
	}
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Application_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Application_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Application_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Application_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BApplication(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Application_DESTROY(Haiku_Application_Object* python_self);
static void Haiku_Application_DESTROY(Haiku_Application_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Application_Instantiate(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_Instantiate(Haiku_Application_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Application_Archive(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_Archive(Haiku_Application_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Application_InitCheck(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_InitCheck(Haiku_Application_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_Run(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_Run(Haiku_Application_Object* python_self, PyObject* python_args) {
	thread_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Run();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Application_Quit(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_Quit(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Quit();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_ResolveSpecifier(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_ResolveSpecifier(Haiku_Application_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Application_ShowCursor(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_ShowCursor(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ShowCursor();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_HideCursor(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_HideCursor(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->HideCursor();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_ObscureCursor(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_ObscureCursor(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ObscureCursor();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_IsCursorHidden(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_IsCursorHidden(Haiku_Application_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsCursorHidden();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Application_SetCursorData(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_SetCursorData(Haiku_Application_Object* python_self, PyObject* python_args) {
	const void* cursor;
	PyObject* py_cursor; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_cursor);
	cursor = PyString_AsString(py_cursor);
	
	python_self->cpp_object->SetCursor(cursor);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_SetCursor(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_SetCursor(Haiku_Application_Object* python_self, PyObject* python_args) {
	BCursor* cursor;
	Haiku_Cursor_Object* py_cursor; // from generate_py()
	bool sync = true;
	PyObject* py_sync; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O|O", &py_cursor, &py_sync);
	if (py_cursor != NULL) {
		cursor = ((Haiku_Cursor_Object*)py_cursor)->cpp_object;
	}
	sync = (bool)(PyObject_IsTrue(py_sync));
	
	python_self->cpp_object->SetCursor(cursor, sync);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_CountWindows(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_CountWindows(Haiku_Application_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountWindows();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Application_WindowAt(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_WindowAt(Haiku_Application_Object* python_self, PyObject* python_args) {
	int32 index;
	BWindow* retval;
	Haiku_Window_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->WindowAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Window_Object*)Haiku_Window_PyType.tp_alloc(&Haiku_Window_PyType, 0);
	py_retval->cpp_object = (BWindow*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Application_CountLoopers(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_CountLoopers(Haiku_Application_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountLoopers();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Application_LooperAt(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_LooperAt(Haiku_Application_Object* python_self, PyObject* python_args) {
	int32 index;
	BLooper* retval;
	Haiku_Looper_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->LooperAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Looper_Object*)Haiku_Looper_PyType.tp_alloc(&Haiku_Looper_PyType, 0);
	py_retval->cpp_object = (BLooper*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Application_IsLaunching(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_IsLaunching(Haiku_Application_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLaunching();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Application_DispatchMessage(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_DispatchMessage(Haiku_Application_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_message, &py_handler);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	python_self->cpp_object->DispatchMessage(message, handler);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_SetPulseRate(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_SetPulseRate(Haiku_Application_Object* python_self, PyObject* python_args) {
	bigtime_t rate;
	
	PyArg_ParseTuple(python_args, "l", &rate);
	
	python_self->cpp_object->SetPulseRate(rate);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_GetSupportedSuites(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_GetSupportedSuites(Haiku_Application_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Application_QuitRequested(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_QuitRequested(Haiku_Application_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->BApplication::QuitRequested();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Application_Pulse(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_Pulse(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BApplication::Pulse();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_ReadyToRun(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_ReadyToRun(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BApplication::ReadyToRun();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_MessageReceived(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_MessageReceived(Haiku_Application_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->BApplication::MessageReceived(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_ArgvReceived(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_ArgvReceived(Haiku_Application_Object* python_self, PyObject* python_args) {
	int32 argc;
	char** argv;
	PyObject* py_argv; // from generate_py ()
	PyObject* py_argv_element;	// from array_arg_parser()
	
	PyArg_ParseTuple(python_args, "O", &py_argv);
	argc = PyList_Size(py_argv);
	for (int i = 0; i < argc; i++) {
		py_argv_element = PyList_GetItem(py_argv, i);
		if (py_argv_element == NULL) {
			argv[i] = NULL;
			continue;
		}
		argv[i] = (char*)PyString_AsString(py_argv_element); // element code
	}
	
	python_self->cpp_object->BApplication::ArgvReceived(argc, argv);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_AppActivated(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_AppActivated(Haiku_Application_Object* python_self, PyObject* python_args) {
	bool active;
	PyObject* py_active; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_active);
	active = (bool)(PyObject_IsTrue(py_active));
	
	python_self->cpp_object->BApplication::AppActivated(active);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_RefsReceived(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_RefsReceived(Haiku_Application_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->BApplication::RefsReceived(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Application_AboutRequested(Haiku_Application_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Application_AboutRequested(Haiku_Application_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BApplication::AboutRequested();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Application_Object_be_app(Haiku_Application_Object* python_dummy) {
	Haiku_Application_Object* py_be_app;
	py_be_app = (Haiku_Application_Object*)Haiku_Application_PyType.tp_alloc(&Haiku_Application_PyType, 0);
	py_be_app->cpp_object = (BApplication*)be_app;
	// cannot delete this object; we do not own it
	py_be_app->can_delete_cpp_object = false;
	return (PyObject*)py_be_app;
}

static PyObject* Haiku_Application_Object_be_app_messenger(Haiku_Application_Object* python_dummy) {
	Haiku_Messenger_Object* py_be_app_messenger;
	py_be_app_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_be_app_messenger->cpp_object = (BMessenger*)&be_app_messenger;
	// cannot delete this object; we do not own it
	py_be_app_messenger->can_delete_cpp_object = false;
	return (PyObject*)py_be_app_messenger;
}

static PyObject* Haiku_Application_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Application_Object*)a)->cpp_object == ((Haiku_Application_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Application_Object*)a)->cpp_object != ((Haiku_Application_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Application_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_Application_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Application_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Application_Archive, METH_VARARGS, ""},
	{"InitCheck", (PyCFunction)Haiku_Application_InitCheck, METH_VARARGS, ""},
	{"Run", (PyCFunction)Haiku_Application_Run, METH_VARARGS, ""},
	{"Quit", (PyCFunction)Haiku_Application_Quit, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Application_ResolveSpecifier, METH_VARARGS, ""},
	{"ShowCursor", (PyCFunction)Haiku_Application_ShowCursor, METH_VARARGS, ""},
	{"HideCursor", (PyCFunction)Haiku_Application_HideCursor, METH_VARARGS, ""},
	{"ObscureCursor", (PyCFunction)Haiku_Application_ObscureCursor, METH_VARARGS, ""},
	{"IsCursorHidden", (PyCFunction)Haiku_Application_IsCursorHidden, METH_VARARGS, ""},
	{"SetCursorData", (PyCFunction)Haiku_Application_SetCursorData, METH_VARARGS, ""},
	{"SetCursor", (PyCFunction)Haiku_Application_SetCursor, METH_VARARGS, ""},
	{"CountWindows", (PyCFunction)Haiku_Application_CountWindows, METH_VARARGS, ""},
	{"WindowAt", (PyCFunction)Haiku_Application_WindowAt, METH_VARARGS, ""},
	{"CountLoopers", (PyCFunction)Haiku_Application_CountLoopers, METH_VARARGS, ""},
	{"LooperAt", (PyCFunction)Haiku_Application_LooperAt, METH_VARARGS, ""},
	{"IsLaunching", (PyCFunction)Haiku_Application_IsLaunching, METH_VARARGS, ""},
	{"DispatchMessage", (PyCFunction)Haiku_Application_DispatchMessage, METH_VARARGS, ""},
	{"SetPulseRate", (PyCFunction)Haiku_Application_SetPulseRate, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Application_GetSupportedSuites, METH_VARARGS, ""},
	{"QuitRequested", (PyCFunction)Haiku_Application_QuitRequested, METH_VARARGS, ""},
	{"Pulse", (PyCFunction)Haiku_Application_Pulse, METH_VARARGS, ""},
	{"ReadyToRun", (PyCFunction)Haiku_Application_ReadyToRun, METH_VARARGS, ""},
	{"MessageReceived", (PyCFunction)Haiku_Application_MessageReceived, METH_VARARGS, ""},
	{"ArgvReceived", (PyCFunction)Haiku_Application_ArgvReceived, METH_VARARGS, ""},
	{"AppActivated", (PyCFunction)Haiku_Application_AppActivated, METH_VARARGS, ""},
	{"RefsReceived", (PyCFunction)Haiku_Application_RefsReceived, METH_VARARGS, ""},
	{"AboutRequested", (PyCFunction)Haiku_Application_AboutRequested, METH_VARARGS, ""},
	{"be_app", (PyCFunction)Haiku_Application_Object_be_app, METH_NOARGS|METH_STATIC, ""},
	{"be_app_messenger", (PyCFunction)Haiku_Application_Object_be_app_messenger, METH_NOARGS|METH_STATIC, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Application_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Application";
	type->tp_basicsize   = sizeof(Haiku_Application_Object);
	type->tp_dealloc     = (destructor)Haiku_Application_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Application_RichCompare;
	type->tp_methods     = Haiku_Application_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Looper_PyType;
	type->tp_init        = (initproc)Haiku_Application_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

