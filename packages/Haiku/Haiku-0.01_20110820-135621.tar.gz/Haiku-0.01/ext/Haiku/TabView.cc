/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_TabViewConstants_PyMethods[] = {
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
//static int Haiku_TabView_init(Haiku_TabView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_TabView_init(Haiku_TabView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	button_width width = B_WIDTH_AS_USUAL;
	uint32 resizingMode = B_FOLLOW_ALL;
	uint32 flags = B_FULL_UPDATE_ON_RESIZE | B_WILL_DRAW | B_NAVIGABLE_JUMP | B_FRAME_EVENTS | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Os|ikk", &py_frame, &name, &width, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BTabView(frame, name, width, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_TabView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TabView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TabView_Object* python_self;
	const char* name;
	button_width width = B_WIDTH_AS_USUAL;
	uint32 flags = B_FULL_UPDATE_ON_RESIZE | B_WILL_DRAW | B_NAVIGABLE_JUMP | B_FRAME_EVENTS | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TabView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "s|ik", &name, &width, &flags);
	
	python_self->cpp_object = new BTabView(name, width, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TabView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TabView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TabView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TabView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BTabView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_TabView_DESTROY(Haiku_TabView_Object* python_self);
static void Haiku_TabView_DESTROY(Haiku_TabView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_TabView_Instantiate(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_Instantiate(Haiku_TabView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TabView_Archive(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_Archive(Haiku_TabView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TabView_AllUnarchived(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_AllUnarchived(Haiku_TabView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TabView_Select(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_Select(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 tab;
	
	PyArg_ParseTuple(python_args, "l", &tab);
	
	python_self->cpp_object->Select(tab);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_Selection(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_Selection(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Selection();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_MakeFocus(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_MakeFocus(Haiku_TabView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_SetFocusTab(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetFocusTab(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 tab;
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "l|O", &tab, &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->SetFocusTab(tab, focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_FocusTab(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_FocusTab(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FocusTab();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_TabFrame(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_TabFrame(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 tab;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &tab);
	
	retval = python_self->cpp_object->TabFrame(tab);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TabView_SetFlags(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetFlags(Haiku_TabView_Object* python_self, PyObject* python_args) {
	uint32 flags;
	
	PyArg_ParseTuple(python_args, "k", &flags);
	
	python_self->cpp_object->SetFlags(flags);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_SetResizingMode(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetResizingMode(Haiku_TabView_Object* python_self, PyObject* python_args) {
	uint32 mode;
	
	PyArg_ParseTuple(python_args, "k", &mode);
	
	python_self->cpp_object->SetResizingMode(mode);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_ResizeToPreferred(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_ResizeToPreferred(Haiku_TabView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_GetPreferredSize(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_GetPreferredSize(Haiku_TabView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_TabView_ResolveSpecifier(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_ResolveSpecifier(Haiku_TabView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TabView_GetSupportedSuites(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_GetSupportedSuites(Haiku_TabView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TabView_AddTab(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_AddTab(Haiku_TabView_Object* python_self, PyObject* python_args) {
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	BTab* tab = NULL;
	Haiku_Tab_Object* py_tab; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_target, &py_tab);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
	}
	if (py_tab != NULL) {
		tab = ((Haiku_Tab_Object*)py_tab)->cpp_object;
	}
	
	python_self->cpp_object->AddTab(target, tab);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_RemoveTab(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_RemoveTab(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 tabIndex;
	BTab* retval;
	Haiku_Tab_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &tabIndex);
	
	retval = python_self->cpp_object->RemoveTab(tabIndex);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Tab_Object*)Haiku_Tab_PyType.tp_alloc(&Haiku_Tab_PyType, 0);
	py_retval->cpp_object = (BTab*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TabView_TabAt(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_TabAt(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 index;
	BTab* retval;
	Haiku_Tab_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->TabAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Tab_Object*)Haiku_Tab_PyType.tp_alloc(&Haiku_Tab_PyType, 0);
	py_retval->cpp_object = (BTab*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TabView_SetTabWidth(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetTabWidth(Haiku_TabView_Object* python_self, PyObject* python_args) {
	button_width width;
	
	PyArg_ParseTuple(python_args, "i", &width);
	
	python_self->cpp_object->SetTabWidth(width);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_TabWidth(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_TabWidth(Haiku_TabView_Object* python_self, PyObject* python_args) {
	button_width retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TabWidth();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_SetTabHeight(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetTabHeight(Haiku_TabView_Object* python_self, PyObject* python_args) {
	float height;
	
	PyArg_ParseTuple(python_args, "f", &height);
	
	python_self->cpp_object->SetTabHeight(height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_TabHeight(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_TabHeight(Haiku_TabView_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TabHeight();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_SetBorder(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_SetBorder(Haiku_TabView_Object* python_self, PyObject* python_args) {
	border_style style;
	
	PyArg_ParseTuple(python_args, "i", &style);
	
	python_self->cpp_object->SetBorder(style);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TabView_Border(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_Border(Haiku_TabView_Object* python_self, PyObject* python_args) {
	border_style retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Border();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_ContainerView(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_ContainerView(Haiku_TabView_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ContainerView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TabView_CountTabs(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_CountTabs(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountTabs();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TabView_ViewForTab(Haiku_TabView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TabView_ViewForTab(Haiku_TabView_Object* python_self, PyObject* python_args) {
	int32 tabIndex;
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &tabIndex);
	
	retval = python_self->cpp_object->ViewForTab(tabIndex);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_TabView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_TabView_Object*)a)->cpp_object == ((Haiku_TabView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_TabView_Object*)a)->cpp_object != ((Haiku_TabView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_TabView_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_TabView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_TabView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_TabView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_TabView_Archive, METH_VARARGS, ""},
	{"AllUnarchived", (PyCFunction)Haiku_TabView_AllUnarchived, METH_VARARGS, ""},
	{"Select", (PyCFunction)Haiku_TabView_Select, METH_VARARGS, ""},
	{"Selection", (PyCFunction)Haiku_TabView_Selection, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_TabView_MakeFocus, METH_VARARGS, ""},
	{"SetFocusTab", (PyCFunction)Haiku_TabView_SetFocusTab, METH_VARARGS, ""},
	{"FocusTab", (PyCFunction)Haiku_TabView_FocusTab, METH_VARARGS, ""},
	{"TabFrame", (PyCFunction)Haiku_TabView_TabFrame, METH_VARARGS, ""},
	{"SetFlags", (PyCFunction)Haiku_TabView_SetFlags, METH_VARARGS, ""},
	{"SetResizingMode", (PyCFunction)Haiku_TabView_SetResizingMode, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_TabView_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_TabView_GetPreferredSize, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_TabView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_TabView_GetSupportedSuites, METH_VARARGS, ""},
	{"AddTab", (PyCFunction)Haiku_TabView_AddTab, METH_VARARGS, ""},
	{"RemoveTab", (PyCFunction)Haiku_TabView_RemoveTab, METH_VARARGS, ""},
	{"TabAt", (PyCFunction)Haiku_TabView_TabAt, METH_VARARGS, ""},
	{"SetTabWidth", (PyCFunction)Haiku_TabView_SetTabWidth, METH_VARARGS, ""},
	{"TabWidth", (PyCFunction)Haiku_TabView_TabWidth, METH_VARARGS, ""},
	{"SetTabHeight", (PyCFunction)Haiku_TabView_SetTabHeight, METH_VARARGS, ""},
	{"TabHeight", (PyCFunction)Haiku_TabView_TabHeight, METH_VARARGS, ""},
	{"SetBorder", (PyCFunction)Haiku_TabView_SetBorder, METH_VARARGS, ""},
	{"Border", (PyCFunction)Haiku_TabView_Border, METH_VARARGS, ""},
	{"ContainerView", (PyCFunction)Haiku_TabView_ContainerView, METH_VARARGS, ""},
	{"CountTabs", (PyCFunction)Haiku_TabView_CountTabs, METH_VARARGS, ""},
	{"ViewForTab", (PyCFunction)Haiku_TabView_ViewForTab, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_TabView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.TabView";
	type->tp_basicsize   = sizeof(Haiku_TabView_Object);
	type->tp_dealloc     = (destructor)Haiku_TabView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_TabView_RichCompare;
	type->tp_methods     = Haiku_TabView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_TabView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

