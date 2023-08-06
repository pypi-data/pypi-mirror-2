/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_AlertConstants_PyMethods[] = {
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
//static int Haiku_Alert_init(Haiku_Alert_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Alert_init(Haiku_Alert_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* title;
	const char* text;
	const char* button0Label;
	const char* button1Label = NULL;
	const char* button2Label = NULL;
	button_width widthStyle = B_WIDTH_AS_USUAL;
	alert_type type = B_INFO_ALERT;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "sss|ssii", &title, &text, &button0Label, &button1Label, &button2Label, &widthStyle, &type);
	
	python_self->cpp_object = new BAlert(title, text, button0Label, button1Label, button2Label, widthStyle, type);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Alert_newWithSpacing(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Alert_newWithSpacing(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Alert_Object* python_self;
	const char* title;
	const char* text;
	const char* button0Label;
	const char* button1Label;
	const char* button2Label;
	button_width widthStyle;
	button_spacing spacing;
	alert_type type = B_INFO_ALERT;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Alert_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sssssii|i", &title, &text, &button0Label, &button1Label, &button2Label, &widthStyle, &spacing, &type);
	
	python_self->cpp_object = new BAlert(title, text, button0Label, button1Label, button2Label, widthStyle, spacing, type);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Alert_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Alert_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Alert_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Alert_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BAlert(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Alert_DESTROY(Haiku_Alert_Object* python_self);
static void Haiku_Alert_DESTROY(Haiku_Alert_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Alert_Instantiate(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_Instantiate(Haiku_Alert_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Alert_Archive(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_Archive(Haiku_Alert_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Alert_SetShortcut(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_SetShortcut(Haiku_Alert_Object* python_self, PyObject* python_args) {
	int32 index;
	char shortcut;
	PyObject* py_shortcut; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "lO", &index, &py_shortcut);
	PyString2Char(py_shortcut, &shortcut, 1, sizeof(char));
	
	python_self->cpp_object->SetShortcut(index, shortcut);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Alert_Shortcut(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_Shortcut(Haiku_Alert_Object* python_self, PyObject* python_args) {
	int32 index;
	char retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->Shortcut(index);
	
	py_retval = Char2PyString(&retval, 1, sizeof(char));
	return py_retval;
}

//static PyObject* Haiku_Alert_Go(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_Go(Haiku_Alert_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Go();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Alert_AsynchronousGo(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_AsynchronousGo(Haiku_Alert_Object* python_self, PyObject* python_args) {
	BInvoker* invoker;
	Haiku_Invoker_Object* py_invoker; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_invoker);
	if (py_invoker != NULL) {
		invoker = ((Haiku_Invoker_Object*)py_invoker)->cpp_object;
	}
	
	retval = python_self->cpp_object->Go(invoker);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Alert_ButtonAt(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_ButtonAt(Haiku_Alert_Object* python_self, PyObject* python_args) {
	uint32 index;
	BButton* retval;
	Haiku_Button_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "k", &index);
	
	retval = python_self->cpp_object->ButtonAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Button_Object*)Haiku_Button_PyType.tp_alloc(&Haiku_Button_PyType, 0);
	py_retval->cpp_object = (BButton*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Alert_TextView(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_TextView(Haiku_Alert_Object* python_self, PyObject* python_args) {
	BTextView* retval;
	Haiku_TextView_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->TextView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_TextView_Object*)Haiku_TextView_PyType.tp_alloc(&Haiku_TextView_PyType, 0);
	py_retval->cpp_object = (BTextView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Alert_ResolveSpecifier(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_ResolveSpecifier(Haiku_Alert_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Alert_GetSupportedSuites(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_GetSupportedSuites(Haiku_Alert_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Alert_DispatchMessage(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_DispatchMessage(Haiku_Alert_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Alert_Quit(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_Quit(Haiku_Alert_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Quit();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Alert_AlertPosition(Haiku_Alert_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Alert_AlertPosition(Haiku_Alert_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &width, &height);
	
	retval = python_self->cpp_object->AlertPosition(width, height);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Alert_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Alert_Object*)a)->cpp_object == ((Haiku_Alert_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Alert_Object*)a)->cpp_object != ((Haiku_Alert_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Alert_PyMethods[] = {
	{"WithSpacing", (PyCFunction)Haiku_Alert_newWithSpacing, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Alert_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Alert_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Alert_Archive, METH_VARARGS, ""},
	{"SetShortcut", (PyCFunction)Haiku_Alert_SetShortcut, METH_VARARGS, ""},
	{"Shortcut", (PyCFunction)Haiku_Alert_Shortcut, METH_VARARGS, ""},
	{"Go", (PyCFunction)Haiku_Alert_Go, METH_VARARGS, ""},
	{"AsynchronousGo", (PyCFunction)Haiku_Alert_AsynchronousGo, METH_VARARGS, ""},
	{"ButtonAt", (PyCFunction)Haiku_Alert_ButtonAt, METH_VARARGS, ""},
	{"TextView", (PyCFunction)Haiku_Alert_TextView, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Alert_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Alert_GetSupportedSuites, METH_VARARGS, ""},
	{"DispatchMessage", (PyCFunction)Haiku_Alert_DispatchMessage, METH_VARARGS, ""},
	{"Quit", (PyCFunction)Haiku_Alert_Quit, METH_VARARGS, ""},
	{"AlertPosition", (PyCFunction)Haiku_Alert_AlertPosition, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Alert_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Alert";
	type->tp_basicsize   = sizeof(Haiku_Alert_Object);
	type->tp_dealloc     = (destructor)Haiku_Alert_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Alert_RichCompare;
	type->tp_methods     = Haiku_Alert_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Window_PyType;
	type->tp_init        = (initproc)Haiku_Alert_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

