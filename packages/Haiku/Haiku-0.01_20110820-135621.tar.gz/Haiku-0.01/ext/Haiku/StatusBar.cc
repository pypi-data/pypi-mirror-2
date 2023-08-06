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
//static int Haiku_StatusBar_init(Haiku_StatusBar_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_StatusBar_init(Haiku_StatusBar_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label = NULL;
	const char* trailingLabel = NULL;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Os|ss", &py_frame, &name, &label, &trailingLabel);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BStatusBar(frame, name, label, trailingLabel);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_StatusBar_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_StatusBar_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_StatusBar_Object* python_self;
	const char* name;
	const char* label = NULL;
	const char* trailingLabel = NULL;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_StatusBar_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "s|ss", &name, &label, &trailingLabel);
	
	python_self->cpp_object = new BStatusBar(name, label, trailingLabel);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_StatusBar_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_StatusBar_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_StatusBar_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_StatusBar_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BStatusBar(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_StatusBar_DESTROY(Haiku_StatusBar_Object* python_self);
static void Haiku_StatusBar_DESTROY(Haiku_StatusBar_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_StatusBar_Instantiate(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Instantiate(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StatusBar_Archive(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Archive(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StatusBar_MakeFocus(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_MakeFocus(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_GetPreferredSize(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_GetPreferredSize(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_StatusBar_ResizeToPreferred(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_ResizeToPreferred(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetBarColor(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetBarColor(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_color);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetBarColor(color);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetBarHeight(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetBarHeight(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float height;
	
	PyArg_ParseTuple(python_args, "f", &height);
	
	python_self->cpp_object->SetBarHeight(height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetText(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetText(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetText(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetTrailingText(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetTrailingText(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetTrailingText(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetMaxValue(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetMaxValue(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float max;
	
	PyArg_ParseTuple(python_args, "f", &max);
	
	python_self->cpp_object->SetMaxValue(max);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_Update(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Update(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float delta;
	const char* text = NULL;
	const char* trailingText = NULL;
	
	PyArg_ParseTuple(python_args, "f|ss", &delta, &text, &trailingText);
	
	python_self->cpp_object->Update(delta, text, trailingText);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_Reset(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Reset(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* text = NULL;
	const char* trailingText = NULL;
	
	PyArg_ParseTuple(python_args, "|ss", &text, &trailingText);
	
	python_self->cpp_object->Reset(text, trailingText);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_SetTo(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_SetTo(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float value;
	const char* text = NULL;
	const char* trailingText = NULL;
	
	PyArg_ParseTuple(python_args, "f|ss", &value, &text, &trailingText);
	
	python_self->cpp_object->SetTo(value, text, trailingText);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StatusBar_CurrentValue(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_CurrentValue(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CurrentValue();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_MaxValue(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_MaxValue(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MaxValue();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_BarColor(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_BarColor(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->BarColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_StatusBar_BarHeight(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_BarHeight(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->BarHeight();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_Text(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Text(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Text();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_TrailingText(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_TrailingText(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TrailingText();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_Label(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_Label(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Label();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_TrailingLabel(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_TrailingLabel(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TrailingLabel();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_StatusBar_ResolveSpecifier(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_ResolveSpecifier(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StatusBar_GetSupportedSuites(Haiku_StatusBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StatusBar_GetSupportedSuites(Haiku_StatusBar_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_StatusBar_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_StatusBar_Object*)a)->cpp_object == ((Haiku_StatusBar_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_StatusBar_Object*)a)->cpp_object != ((Haiku_StatusBar_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_StatusBar_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_StatusBar_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_StatusBar_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_StatusBar_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_StatusBar_Archive, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_StatusBar_MakeFocus, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_StatusBar_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_StatusBar_ResizeToPreferred, METH_VARARGS, ""},
	{"SetBarColor", (PyCFunction)Haiku_StatusBar_SetBarColor, METH_VARARGS, ""},
	{"SetBarHeight", (PyCFunction)Haiku_StatusBar_SetBarHeight, METH_VARARGS, ""},
	{"SetText", (PyCFunction)Haiku_StatusBar_SetText, METH_VARARGS, ""},
	{"SetTrailingText", (PyCFunction)Haiku_StatusBar_SetTrailingText, METH_VARARGS, ""},
	{"SetMaxValue", (PyCFunction)Haiku_StatusBar_SetMaxValue, METH_VARARGS, ""},
	{"Update", (PyCFunction)Haiku_StatusBar_Update, METH_VARARGS, ""},
	{"Reset", (PyCFunction)Haiku_StatusBar_Reset, METH_VARARGS, ""},
	{"SetTo", (PyCFunction)Haiku_StatusBar_SetTo, METH_VARARGS, ""},
	{"CurrentValue", (PyCFunction)Haiku_StatusBar_CurrentValue, METH_VARARGS, ""},
	{"MaxValue", (PyCFunction)Haiku_StatusBar_MaxValue, METH_VARARGS, ""},
	{"BarColor", (PyCFunction)Haiku_StatusBar_BarColor, METH_VARARGS, ""},
	{"BarHeight", (PyCFunction)Haiku_StatusBar_BarHeight, METH_VARARGS, ""},
	{"Text", (PyCFunction)Haiku_StatusBar_Text, METH_VARARGS, ""},
	{"TrailingText", (PyCFunction)Haiku_StatusBar_TrailingText, METH_VARARGS, ""},
	{"Label", (PyCFunction)Haiku_StatusBar_Label, METH_VARARGS, ""},
	{"TrailingLabel", (PyCFunction)Haiku_StatusBar_TrailingLabel, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_StatusBar_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_StatusBar_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_StatusBar_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.StatusBar";
	type->tp_basicsize   = sizeof(Haiku_StatusBar_Object);
	type->tp_dealloc     = (destructor)Haiku_StatusBar_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_StatusBar_RichCompare;
	type->tp_methods     = Haiku_StatusBar_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_StatusBar_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

