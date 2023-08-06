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
//static int Haiku_ScrollView_init(Haiku_ScrollView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_ScrollView_init(Haiku_ScrollView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name;
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = 0;
	bool horizontal = false;
	PyObject* py_horizontal; // from generate_py ()
	bool vertical = false;
	PyObject* py_vertical; // from generate_py ()
	border_style border = B_FANCY_BORDER;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "sO|kkOOi", &name, &py_target, &resizingMode, &flags, &py_horizontal, &py_vertical, &border);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
		((Haiku_View_Object*)py_target)->can_delete_cpp_object = false;
	}
	horizontal = (bool)(PyObject_IsTrue(py_horizontal));
	vertical = (bool)(PyObject_IsTrue(py_vertical));
	
	python_self->cpp_object = new BScrollView(name, target, resizingMode, flags, horizontal, vertical, border);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_ScrollView_newWithoutResize(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ScrollView_newWithoutResize(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ScrollView_Object* python_self;
	const char* name;
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	uint32 flags;
	bool horizontal;
	PyObject* py_horizontal; // from generate_py ()
	bool vertical;
	PyObject* py_vertical; // from generate_py ()
	border_style border = B_FANCY_BORDER;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ScrollView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sOkOO|i", &name, &py_target, &flags, &py_horizontal, &py_vertical, &border);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
		((Haiku_View_Object*)py_target)->can_delete_cpp_object = false;
	}
	horizontal = (bool)(PyObject_IsTrue(py_horizontal));
	vertical = (bool)(PyObject_IsTrue(py_vertical));
	
	python_self->cpp_object = new BScrollView(name, target, flags, horizontal, vertical, border);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_ScrollView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ScrollView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ScrollView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ScrollView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BScrollView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_ScrollView_DESTROY(Haiku_ScrollView_Object* python_self);
static void Haiku_ScrollView_DESTROY(Haiku_ScrollView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_ScrollView_Instantiate(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_Instantiate(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollView_Archive(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_Archive(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollView_MakeFocus(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_MakeFocus(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_GetPreferredSize(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_GetPreferredSize(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_ScrollView_ResizeToPreferred(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_ResizeToPreferred(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_InvalidateLayout(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_InvalidateLayout(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_DoLayout(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_DoLayout(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DoLayout();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_ScrollBar(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_ScrollBar(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	orientation posture;
	BScrollBar* retval;
	Haiku_ScrollBar_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "i", &posture);
	
	retval = python_self->cpp_object->ScrollBar(posture);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ScrollBar_Object*)Haiku_ScrollBar_PyType.tp_alloc(&Haiku_ScrollBar_PyType, 0);
	py_retval->cpp_object = (BScrollBar*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ScrollView_SetBorder(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_SetBorder(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	border_style border;
	
	PyArg_ParseTuple(python_args, "i", &border);
	
	python_self->cpp_object->SetBorder(border);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_Border(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_Border(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	border_style retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Border();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_ScrollView_SetBorderHighlighted(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_SetBorderHighlighted(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetBorderHighlighted(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_IsBorderHighlighted(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_IsBorderHighlighted(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsBorderHighlighted();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ScrollView_SetTarget(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_SetTarget(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
		((Haiku_View_Object*)py_target)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->SetTarget(target);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollView_Target(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_Target(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Target();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ScrollView_ResolveSpecifier(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_ResolveSpecifier(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollView_GetSupportedSuites(Haiku_ScrollView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollView_GetSupportedSuites(Haiku_ScrollView_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_ScrollView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ScrollView_Object*)a)->cpp_object == ((Haiku_ScrollView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ScrollView_Object*)a)->cpp_object != ((Haiku_ScrollView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ScrollView_PyMethods[] = {
	{"WithoutResize", (PyCFunction)Haiku_ScrollView_newWithoutResize, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_ScrollView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_ScrollView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_ScrollView_Archive, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_ScrollView_MakeFocus, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_ScrollView_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_ScrollView_ResizeToPreferred, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_ScrollView_InvalidateLayout, METH_VARARGS, ""},
	{"DoLayout", (PyCFunction)Haiku_ScrollView_DoLayout, METH_VARARGS, ""},
	{"ScrollBar", (PyCFunction)Haiku_ScrollView_ScrollBar, METH_VARARGS, ""},
	{"SetBorder", (PyCFunction)Haiku_ScrollView_SetBorder, METH_VARARGS, ""},
	{"Border", (PyCFunction)Haiku_ScrollView_Border, METH_VARARGS, ""},
	{"SetBorderHighlighted", (PyCFunction)Haiku_ScrollView_SetBorderHighlighted, METH_VARARGS, ""},
	{"IsBorderHighlighted", (PyCFunction)Haiku_ScrollView_IsBorderHighlighted, METH_VARARGS, ""},
	{"SetTarget", (PyCFunction)Haiku_ScrollView_SetTarget, METH_VARARGS, ""},
	{"Target", (PyCFunction)Haiku_ScrollView_Target, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_ScrollView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_ScrollView_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ScrollView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ScrollView";
	type->tp_basicsize   = sizeof(Haiku_ScrollView_Object);
	type->tp_dealloc     = (destructor)Haiku_ScrollView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ScrollView_RichCompare;
	type->tp_methods     = Haiku_ScrollView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_ScrollView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

