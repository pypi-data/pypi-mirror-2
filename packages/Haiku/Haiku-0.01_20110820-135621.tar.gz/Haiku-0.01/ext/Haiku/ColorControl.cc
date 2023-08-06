/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_ColorControlConstants_PyMethods[] = {
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
//static int Haiku_ColorControl_init(Haiku_ColorControl_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_ColorControl_init(Haiku_ColorControl_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BPoint start;
	Haiku_Point_Object* py_start; // from generate_py()
	color_control_layout layout;
	float cellSize;
	const char* name;
	BMessage* message = NULL;
	Haiku_Message_Object* py_message; // from generate_py()
	bool useOffscreen = false;
	PyObject* py_useOffscreen; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Oifs|OO", &py_start, &layout, &cellSize, &name, &py_message, &py_useOffscreen);
	if (py_start != NULL) {
		memcpy((void*)&start, (void*)((Haiku_Point_Object*)py_start)->cpp_object, sizeof(BPoint));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	useOffscreen = (bool)(PyObject_IsTrue(py_useOffscreen));
	
	python_self->cpp_object = new BColorControl(start, layout, cellSize, name, message, useOffscreen);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_ColorControl_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ColorControl_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ColorControl_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ColorControl_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BColorControl(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_ColorControl_DESTROY(Haiku_ColorControl_Object* python_self);
static void Haiku_ColorControl_DESTROY(Haiku_ColorControl_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_ColorControl_Instantiate(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_Instantiate(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ColorControl_Archive(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_Archive(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ColorControl_SetValueAsColor(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_SetValueAsColor(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_color);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetValue(color);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_SetValue(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_SetValue(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	int32 color_value;
	
	PyArg_ParseTuple(python_args, "l", &color_value);
	
	python_self->cpp_object->SetValue(color_value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_ValueAsColor(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_ValueAsColor(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ValueAsColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ColorControl_SetEnabled(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_SetEnabled(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetEnabled(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_SetCellSize(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_SetCellSize(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	float size;
	
	PyArg_ParseTuple(python_args, "f", &size);
	
	python_self->cpp_object->SetCellSize(size);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_CellSize(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_CellSize(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CellSize();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_ColorControl_SetLayout(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_SetLayout(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	color_control_layout layout;
	
	PyArg_ParseTuple(python_args, "i", &layout);
	
	python_self->cpp_object->SetLayout(layout);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_Layout(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_Layout(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	color_control_layout retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Layout();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_ColorControl_GetPreferredSize(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_GetPreferredSize(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_ColorControl_ResizeToPreferred(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_ResizeToPreferred(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ColorControl_Invoke(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_Invoke(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ColorControl_ResolveSpecifier(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_ResolveSpecifier(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ColorControl_GetSupportedSuites(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_GetSupportedSuites(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ColorControl_MakeFocus(Haiku_ColorControl_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ColorControl_MakeFocus(Haiku_ColorControl_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_ColorControl_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ColorControl_Object*)a)->cpp_object == ((Haiku_ColorControl_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ColorControl_Object*)a)->cpp_object != ((Haiku_ColorControl_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ColorControl_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_ColorControl_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_ColorControl_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_ColorControl_Archive, METH_VARARGS, ""},
	{"SetValueAsColor", (PyCFunction)Haiku_ColorControl_SetValueAsColor, METH_VARARGS, ""},
	{"SetValue", (PyCFunction)Haiku_ColorControl_SetValue, METH_VARARGS, ""},
	{"ValueAsColor", (PyCFunction)Haiku_ColorControl_ValueAsColor, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_ColorControl_SetEnabled, METH_VARARGS, ""},
	{"SetCellSize", (PyCFunction)Haiku_ColorControl_SetCellSize, METH_VARARGS, ""},
	{"CellSize", (PyCFunction)Haiku_ColorControl_CellSize, METH_VARARGS, ""},
	{"SetLayout", (PyCFunction)Haiku_ColorControl_SetLayout, METH_VARARGS, ""},
	{"Layout", (PyCFunction)Haiku_ColorControl_Layout, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_ColorControl_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_ColorControl_ResizeToPreferred, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_ColorControl_Invoke, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_ColorControl_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_ColorControl_GetSupportedSuites, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_ColorControl_MakeFocus, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ColorControl_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ColorControl";
	type->tp_basicsize   = sizeof(Haiku_ColorControl_Object);
	type->tp_dealloc     = (destructor)Haiku_ColorControl_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ColorControl_RichCompare;
	type->tp_methods     = Haiku_ColorControl_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Control_PyType;
	type->tp_init        = (initproc)Haiku_ColorControl_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

