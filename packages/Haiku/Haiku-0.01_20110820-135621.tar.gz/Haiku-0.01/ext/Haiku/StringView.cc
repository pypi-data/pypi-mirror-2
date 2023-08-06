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
//static int Haiku_StringView_init(Haiku_StringView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_StringView_init(Haiku_StringView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* text;
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Oss|kk", &py_frame, &name, &text, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BStringView(frame, name, text, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_StringView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_StringView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_StringView_Object* python_self;
	const char* name;
	const char* text;
	uint32 flags = B_WILL_DRAW;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_StringView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "ss|k", &name, &text, &flags);
	
	python_self->cpp_object = new BStringView(name, text, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_StringView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_StringView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_StringView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_StringView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BStringView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_StringView_DESTROY(Haiku_StringView_Object* python_self);
static void Haiku_StringView_DESTROY(Haiku_StringView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_StringView_Instantiate(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_Instantiate(Haiku_StringView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringView_Archive(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_Archive(Haiku_StringView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringView_SetText(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_SetText(Haiku_StringView_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetText(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringView_Text(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_Text(Haiku_StringView_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Text();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_StringView_SetAlignment(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_SetAlignment(Haiku_StringView_Object* python_self, PyObject* python_args) {
	alignment flag;
	
	PyArg_ParseTuple(python_args, "i", &flag);
	
	python_self->cpp_object->SetAlignment(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringView_Alignment(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_Alignment(Haiku_StringView_Object* python_self, PyObject* python_args) {
	alignment retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Alignment();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_StringView_MakeFocus(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_MakeFocus(Haiku_StringView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringView_GetPreferredSize(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_GetPreferredSize(Haiku_StringView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_StringView_InvalidateLayout(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_InvalidateLayout(Haiku_StringView_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringView_ResizeToPreferred(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_ResizeToPreferred(Haiku_StringView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringView_ResolveSpecifier(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_ResolveSpecifier(Haiku_StringView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringView_GetSupportedSuites(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_GetSupportedSuites(Haiku_StringView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringView_SetFont(Haiku_StringView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringView_SetFont(Haiku_StringView_Object* python_self, PyObject* python_args) {
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	uint32 mask = B_FONT_ALL;
	
	PyArg_ParseTuple(python_args, "O|k", &py_font, &mask);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	
	python_self->cpp_object->SetFont(font, mask);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_StringView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_StringView_Object*)a)->cpp_object == ((Haiku_StringView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_StringView_Object*)a)->cpp_object != ((Haiku_StringView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_StringView_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_StringView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_StringView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_StringView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_StringView_Archive, METH_VARARGS, ""},
	{"SetText", (PyCFunction)Haiku_StringView_SetText, METH_VARARGS, ""},
	{"Text", (PyCFunction)Haiku_StringView_Text, METH_VARARGS, ""},
	{"SetAlignment", (PyCFunction)Haiku_StringView_SetAlignment, METH_VARARGS, ""},
	{"Alignment", (PyCFunction)Haiku_StringView_Alignment, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_StringView_MakeFocus, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_StringView_GetPreferredSize, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_StringView_InvalidateLayout, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_StringView_ResizeToPreferred, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_StringView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_StringView_GetSupportedSuites, METH_VARARGS, ""},
	{"SetFont", (PyCFunction)Haiku_StringView_SetFont, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_StringView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.StringView";
	type->tp_basicsize   = sizeof(Haiku_StringView_Object);
	type->tp_dealloc     = (destructor)Haiku_StringView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_StringView_RichCompare;
	type->tp_methods     = Haiku_StringView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_StringView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

