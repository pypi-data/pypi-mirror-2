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
//static int Haiku_TextControl_init(Haiku_TextControl_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_TextControl_init(Haiku_TextControl_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	const char* text;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OsssO|kk", &py_frame, &name, &label, &text, &py_message, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BTextControl(frame, name, label, text, message, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_TextControl_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextControl_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextControl_Object* python_self;
	const char* name;
	const char* label;
	const char* text;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextControl_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sssO|k", &name, &label, &text, &py_message, &flags);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BTextControl(name, label, text, message, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TextControl_newBareBones(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextControl_newBareBones(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextControl_Object* python_self;
	const char* label;
	const char* text;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextControl_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "ssO", &label, &text, &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BTextControl(label, text, message);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TextControl_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextControl_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextControl_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextControl_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BTextControl(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_TextControl_DESTROY(Haiku_TextControl_Object* python_self);
static void Haiku_TextControl_DESTROY(Haiku_TextControl_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_TextControl_Instantiate(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_Instantiate(Haiku_TextControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextControl_Archive(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_Archive(Haiku_TextControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextControl_AllArchived(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_AllArchived(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllArchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_AllUnarchived(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_AllUnarchived(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllUnarchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_SetText(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetText(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	const char* text;
	
	PyArg_ParseTuple(python_args, "s", &text);
	
	python_self->cpp_object->SetText(text);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_Text(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_Text(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Text();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_TextControl_SetValue(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetValue(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	int32 value;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	python_self->cpp_object->SetValue(value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_Invoke(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_Invoke(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BMessage* message = NULL;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Invoke(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_TextControl_TextView(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_TextView(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BTextView* retval;
	Haiku_TextView_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->TextView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_TextView_Object*)Haiku_TextView_PyType.tp_alloc(&Haiku_TextView_PyType, 0);
	py_retval->cpp_object = (BTextView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TextControl_SetModificationMessage(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetModificationMessage(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->SetModificationMessage(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_ModificationMessage(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_ModificationMessage(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ModificationMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TextControl_SetAlignment(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetAlignment(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	alignment forLabel;
	alignment forText;
	
	PyArg_ParseTuple(python_args, "ii", &forLabel, &forText);
	
	python_self->cpp_object->SetAlignment(forLabel, forText);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_GetAlignment(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_GetAlignment(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	alignment forLabel;
	alignment forText;
	
	python_self->cpp_object->GetAlignment(&forLabel, &forText);
	
	return Py_BuildValue("ii", forLabel, forText);
}

//static PyObject* Haiku_TextControl_SetDivider(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetDivider(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	float xCoordinate;
	
	PyArg_ParseTuple(python_args, "f", &xCoordinate);
	
	python_self->cpp_object->SetDivider(xCoordinate);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_Divider(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_Divider(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Divider();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TextControl_MakeFocus(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_MakeFocus(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_SetEnabled(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_SetEnabled(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_ResizeToPreferred(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_ResizeToPreferred(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextControl_GetPreferredSize(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_GetPreferredSize(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_TextControl_ResolveSpecifier(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_ResolveSpecifier(Haiku_TextControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextControl_GetSupportedSuites(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_GetSupportedSuites(Haiku_TextControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextControl_InvalidateLayout(Haiku_TextControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextControl_InvalidateLayout(Haiku_TextControl_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_TextControl_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_TextControl_Object*)a)->cpp_object == ((Haiku_TextControl_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_TextControl_Object*)a)->cpp_object != ((Haiku_TextControl_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_TextControl_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_TextControl_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"BareBones", (PyCFunction)Haiku_TextControl_newBareBones, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_TextControl_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_TextControl_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_TextControl_Archive, METH_VARARGS, ""},
	{"AllArchived", (PyCFunction)Haiku_TextControl_AllArchived, METH_VARARGS, ""},
	{"AllUnarchived", (PyCFunction)Haiku_TextControl_AllUnarchived, METH_VARARGS, ""},
	{"SetText", (PyCFunction)Haiku_TextControl_SetText, METH_VARARGS, ""},
	{"Text", (PyCFunction)Haiku_TextControl_Text, METH_VARARGS, ""},
	{"SetValue", (PyCFunction)Haiku_TextControl_SetValue, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_TextControl_Invoke, METH_VARARGS, ""},
	{"TextView", (PyCFunction)Haiku_TextControl_TextView, METH_VARARGS, ""},
	{"SetModificationMessage", (PyCFunction)Haiku_TextControl_SetModificationMessage, METH_VARARGS, ""},
	{"ModificationMessage", (PyCFunction)Haiku_TextControl_ModificationMessage, METH_VARARGS, ""},
	{"SetAlignment", (PyCFunction)Haiku_TextControl_SetAlignment, METH_VARARGS, ""},
	{"GetAlignment", (PyCFunction)Haiku_TextControl_GetAlignment, METH_VARARGS, ""},
	{"SetDivider", (PyCFunction)Haiku_TextControl_SetDivider, METH_VARARGS, ""},
	{"Divider", (PyCFunction)Haiku_TextControl_Divider, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_TextControl_MakeFocus, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_TextControl_SetEnabled, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_TextControl_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_TextControl_GetPreferredSize, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_TextControl_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_TextControl_GetSupportedSuites, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_TextControl_InvalidateLayout, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_TextControl_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.TextControl";
	type->tp_basicsize   = sizeof(Haiku_TextControl_Object);
	type->tp_dealloc     = (destructor)Haiku_TextControl_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_TextControl_RichCompare;
	type->tp_methods     = Haiku_TextControl_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Control_PyType;
	type->tp_init        = (initproc)Haiku_TextControl_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

