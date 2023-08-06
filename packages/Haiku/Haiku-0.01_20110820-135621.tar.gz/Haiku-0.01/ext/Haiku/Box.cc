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
//static int Haiku_Box_init(Haiku_Box_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Box_init(Haiku_Box_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name = NULL;
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE_JUMP;
	border_style border = B_FANCY_BORDER;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "O|skki", &py_frame, &name, &resizingMode, &flags, &border);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BBox(frame, name, resizingMode, flags, border);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Box_newWithChildAndName(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Box_newWithChildAndName(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Box_Object* python_self;
	const char* name = NULL;
	uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE_JUMP;
	border_style border = B_FANCY_BORDER;
	BView* child = NULL;
	Haiku_View_Object* py_child; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Box_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "|skiO", &name, &flags, &border, &py_child);
	if (py_child != NULL) {
		child = ((Haiku_View_Object*)py_child)->cpp_object;
	}
	
	python_self->cpp_object = new BBox(name, flags, border, child);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Box_newWithChild(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Box_newWithChild(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Box_Object* python_self;
	border_style border = B_FANCY_BORDER;
	BView* child = NULL;
	Haiku_View_Object* py_child; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Box_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "|iO", &border, &py_child);
	if (py_child != NULL) {
		child = ((Haiku_View_Object*)py_child)->cpp_object;
	}
	
	python_self->cpp_object = new BBox(border, child);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Box_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Box_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Box_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Box_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BBox(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Box_DESTROY(Haiku_Box_Object* python_self);
static void Haiku_Box_DESTROY(Haiku_Box_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Box_Instantiate(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_Instantiate(Haiku_Box_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Box_Archive(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_Archive(Haiku_Box_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Box_SetBorder(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_SetBorder(Haiku_Box_Object* python_self, PyObject* python_args) {
	border_style border;
	
	PyArg_ParseTuple(python_args, "i", &border);
	
	python_self->cpp_object->SetBorder(border);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_Border(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_Border(Haiku_Box_Object* python_self, PyObject* python_args) {
	border_style retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Border();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Box_TopBorderOffset(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_TopBorderOffset(Haiku_Box_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TopBorderOffset();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Box_InnerFrame(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_InnerFrame(Haiku_Box_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->InnerFrame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Box_SetLabel(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_SetLabel(Haiku_Box_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetLabel(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_SetLabelView(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_SetLabelView(Haiku_Box_Object* python_self, PyObject* python_args) {
	BView* viewLabel;
	Haiku_View_Object* py_viewLabel; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_viewLabel);
	if (py_viewLabel != NULL) {
		viewLabel = ((Haiku_View_Object*)py_viewLabel)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetLabel(viewLabel);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_Label(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_Label(Haiku_Box_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Label();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Box_LabelView(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_LabelView(Haiku_Box_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LabelView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Box_ResolveSpecifier(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_ResolveSpecifier(Haiku_Box_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Box_ResizeToPreferred(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_ResizeToPreferred(Haiku_Box_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_GetPreferredSize(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_GetPreferredSize(Haiku_Box_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_Box_MakeFocus(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_MakeFocus(Haiku_Box_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_GetSupportedSuites(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_GetSupportedSuites(Haiku_Box_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Box_InvalidateLayout(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_InvalidateLayout(Haiku_Box_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Box_DoLayout(Haiku_Box_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Box_DoLayout(Haiku_Box_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DoLayout();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Box_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Box_Object*)a)->cpp_object == ((Haiku_Box_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Box_Object*)a)->cpp_object != ((Haiku_Box_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Box_PyMethods[] = {
	{"WithChildAndName", (PyCFunction)Haiku_Box_newWithChildAndName, METH_VARARGS|METH_CLASS, ""},
	{"WithChild", (PyCFunction)Haiku_Box_newWithChild, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Box_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Box_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Box_Archive, METH_VARARGS, ""},
	{"SetBorder", (PyCFunction)Haiku_Box_SetBorder, METH_VARARGS, ""},
	{"Border", (PyCFunction)Haiku_Box_Border, METH_VARARGS, ""},
	{"TopBorderOffset", (PyCFunction)Haiku_Box_TopBorderOffset, METH_VARARGS, ""},
	{"InnerFrame", (PyCFunction)Haiku_Box_InnerFrame, METH_VARARGS, ""},
	{"SetLabel", (PyCFunction)Haiku_Box_SetLabel, METH_VARARGS, ""},
	{"SetLabelView", (PyCFunction)Haiku_Box_SetLabelView, METH_VARARGS, ""},
	{"Label", (PyCFunction)Haiku_Box_Label, METH_VARARGS, ""},
	{"LabelView", (PyCFunction)Haiku_Box_LabelView, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Box_ResolveSpecifier, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_Box_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_Box_GetPreferredSize, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_Box_MakeFocus, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Box_GetSupportedSuites, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_Box_InvalidateLayout, METH_VARARGS, ""},
	{"DoLayout", (PyCFunction)Haiku_Box_DoLayout, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Box_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Box";
	type->tp_basicsize   = sizeof(Haiku_Box_Object);
	type->tp_dealloc     = (destructor)Haiku_Box_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Box_RichCompare;
	type->tp_methods     = Haiku_Box_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_Box_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

