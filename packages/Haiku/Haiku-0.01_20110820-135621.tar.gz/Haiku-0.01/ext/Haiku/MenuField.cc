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
//static int Haiku_MenuField_init(Haiku_MenuField_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_MenuField_init(Haiku_MenuField_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	BMenu* menu;
	Haiku_Menu_Object* py_menu; // from generate_py()
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OssO|kk", &py_frame, &name, &label, &py_menu, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_menu != NULL) {
		menu = ((Haiku_Menu_Object*)py_menu)->cpp_object;
	}
	
	python_self->cpp_object = new BMenuField(frame, name, label, menu, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_MenuField_newFixedSize(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuField_newFixedSize(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuField_Object* python_self;
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	BMenu* menu;
	Haiku_Menu_Object* py_menu; // from generate_py()
	bool fixedSize;
	PyObject* py_fixedSize; // from generate_py ()
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuField_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "OssOO|kk", &py_frame, &name, &label, &py_menu, &py_fixedSize, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_menu != NULL) {
		menu = ((Haiku_Menu_Object*)py_menu)->cpp_object;
	}
	fixedSize = (bool)(PyObject_IsTrue(py_fixedSize));
	
	python_self->cpp_object = new BMenuField(frame, name, label, menu, fixedSize, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_MenuField_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuField_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuField_Object* python_self;
	const char* name;
	const char* label;
	BMenu* menu;
	Haiku_Menu_Object* py_menu; // from generate_py()
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuField_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "ssO|k", &name, &label, &py_menu, &flags);
	if (py_menu != NULL) {
		menu = ((Haiku_Menu_Object*)py_menu)->cpp_object;
	}
	
	python_self->cpp_object = new BMenuField(name, label, menu, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_MenuField_newBareBones(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuField_newBareBones(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuField_Object* python_self;
	const char* label;
	BMenu* menu;
	Haiku_Menu_Object* py_menu; // from generate_py()
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuField_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sO|k", &label, &py_menu, &flags);
	if (py_menu != NULL) {
		menu = ((Haiku_Menu_Object*)py_menu)->cpp_object;
	}
	
	python_self->cpp_object = new BMenuField(label, menu, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_MenuField_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuField_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuField_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuField_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BMenuField(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_MenuField_DESTROY(Haiku_MenuField_Object* python_self);
static void Haiku_MenuField_DESTROY(Haiku_MenuField_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_MenuField_Instantiate(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Instantiate(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_Archive(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Archive(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_AllArchived(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_AllArchived(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_AllUnarchived(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_AllUnarchived(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_MakeFocus(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_MakeFocus(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_Menu(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Menu(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	BMenu* retval;
	Haiku_Menu_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Menu();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Menu_Object*)Haiku_Menu_PyType.tp_alloc(&Haiku_Menu_PyType, 0);
	py_retval->cpp_object = (BMenu*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_MenuField_MenuBar(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_MenuBar(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	BMenuBar* retval;
	Haiku_MenuBar_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->MenuBar();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuBar_Object*)Haiku_MenuBar_PyType.tp_alloc(&Haiku_MenuBar_PyType, 0);
	py_retval->cpp_object = (BMenuBar*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_MenuField_MenuItem(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_MenuItem(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->MenuItem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_MenuField_SetLabel(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_SetLabel(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetLabel(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_Label(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Label(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Label();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_MenuField_SetEnabled(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_SetEnabled(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_IsEnabled(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_IsEnabled(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MenuField_SetAlignment(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_SetAlignment(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	alignment flag;
	
	PyArg_ParseTuple(python_args, "i", &flag);
	
	python_self->cpp_object->SetAlignment(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_Alignment(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Alignment(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	alignment retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Alignment();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_MenuField_SetDivider(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_SetDivider(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	float xCoordinate;
	
	PyArg_ParseTuple(python_args, "f", &xCoordinate);
	
	python_self->cpp_object->SetDivider(xCoordinate);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_Divider(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_Divider(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Divider();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_MenuField_ShowPopUpMarker(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_ShowPopUpMarker(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ShowPopUpMarker();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_HidePopUpMarker(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_HidePopUpMarker(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->HidePopUpMarker();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_ResolveSpecifier(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_ResolveSpecifier(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_GetSupportedSuites(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_GetSupportedSuites(Haiku_MenuField_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuField_ResizeToPreferred(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_ResizeToPreferred(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuField_GetPreferredSize(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_GetPreferredSize(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_MenuField_InvalidateLayout(Haiku_MenuField_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuField_InvalidateLayout(Haiku_MenuField_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_MenuField_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_MenuField_Object*)a)->cpp_object == ((Haiku_MenuField_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_MenuField_Object*)a)->cpp_object != ((Haiku_MenuField_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_MenuField_PyMethods[] = {
	{"FixedSize", (PyCFunction)Haiku_MenuField_newFixedSize, METH_VARARGS|METH_CLASS, ""},
	{"WithoutFrame", (PyCFunction)Haiku_MenuField_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"BareBones", (PyCFunction)Haiku_MenuField_newBareBones, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_MenuField_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_MenuField_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_MenuField_Archive, METH_VARARGS, ""},
	{"AllArchived", (PyCFunction)Haiku_MenuField_AllArchived, METH_VARARGS, ""},
	{"AllUnarchived", (PyCFunction)Haiku_MenuField_AllUnarchived, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_MenuField_MakeFocus, METH_VARARGS, ""},
	{"Menu", (PyCFunction)Haiku_MenuField_Menu, METH_VARARGS, ""},
	{"MenuBar", (PyCFunction)Haiku_MenuField_MenuBar, METH_VARARGS, ""},
	{"MenuItem", (PyCFunction)Haiku_MenuField_MenuItem, METH_VARARGS, ""},
	{"SetLabel", (PyCFunction)Haiku_MenuField_SetLabel, METH_VARARGS, ""},
	{"Label", (PyCFunction)Haiku_MenuField_Label, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_MenuField_SetEnabled, METH_VARARGS, ""},
	{"IsEnabled", (PyCFunction)Haiku_MenuField_IsEnabled, METH_VARARGS, ""},
	{"SetAlignment", (PyCFunction)Haiku_MenuField_SetAlignment, METH_VARARGS, ""},
	{"Alignment", (PyCFunction)Haiku_MenuField_Alignment, METH_VARARGS, ""},
	{"SetDivider", (PyCFunction)Haiku_MenuField_SetDivider, METH_VARARGS, ""},
	{"Divider", (PyCFunction)Haiku_MenuField_Divider, METH_VARARGS, ""},
	{"ShowPopUpMarker", (PyCFunction)Haiku_MenuField_ShowPopUpMarker, METH_VARARGS, ""},
	{"HidePopUpMarker", (PyCFunction)Haiku_MenuField_HidePopUpMarker, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_MenuField_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_MenuField_GetSupportedSuites, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_MenuField_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_MenuField_GetPreferredSize, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_MenuField_InvalidateLayout, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_MenuField_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.MenuField";
	type->tp_basicsize   = sizeof(Haiku_MenuField_Object);
	type->tp_dealloc     = (destructor)Haiku_MenuField_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_MenuField_RichCompare;
	type->tp_methods     = Haiku_MenuField_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_MenuField_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

