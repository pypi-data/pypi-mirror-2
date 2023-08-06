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
//static int Haiku_PopUpMenu_init(Haiku_PopUpMenu_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_PopUpMenu_init(Haiku_PopUpMenu_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name;
	bool radioMode = true;
	PyObject* py_radioMode; // from generate_py ()
	bool labelFromMarked = true;
	PyObject* py_labelFromMarked; // from generate_py ()
	menu_layout layout = B_ITEMS_IN_COLUMN;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|OOi", &name, &py_radioMode, &py_labelFromMarked, &layout);
	radioMode = (bool)(PyObject_IsTrue(py_radioMode));
	labelFromMarked = (bool)(PyObject_IsTrue(py_labelFromMarked));
	
	python_self->cpp_object = new BPopUpMenu(name, radioMode, labelFromMarked, layout);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_PopUpMenu_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_PopUpMenu_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_PopUpMenu_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BPopUpMenu(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_PopUpMenu_DESTROY(Haiku_PopUpMenu_Object* python_self);
static void Haiku_PopUpMenu_DESTROY(Haiku_PopUpMenu_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_PopUpMenu_Instantiate(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_Instantiate(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_PopUpMenu_Archive(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_Archive(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_PopUpMenu_Go(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_Go(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	BPoint screenPoint;
	Haiku_Point_Object* py_screenPoint; // from generate_py()
	bool deliversMessage = false;
	PyObject* py_deliversMessage; // from generate_py ()
	bool openAnyway = false;
	PyObject* py_openAnyway; // from generate_py ()
	bool asynchronous = false;
	PyObject* py_asynchronous; // from generate_py ()
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O|OOO", &py_screenPoint, &py_deliversMessage, &py_openAnyway, &py_asynchronous);
	if (py_screenPoint != NULL) {
		memcpy((void*)&screenPoint, (void*)((Haiku_Point_Object*)py_screenPoint)->cpp_object, sizeof(BPoint));
	}
	deliversMessage = (bool)(PyObject_IsTrue(py_deliversMessage));
	openAnyway = (bool)(PyObject_IsTrue(py_openAnyway));
	asynchronous = (bool)(PyObject_IsTrue(py_asynchronous));
	
	retval = python_self->cpp_object->Go(screenPoint, deliversMessage, openAnyway, asynchronous);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_PopUpMenu_GoWithClickRect(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_GoWithClickRect(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	BPoint screenPoint;
	Haiku_Point_Object* py_screenPoint; // from generate_py()
	bool deliversMessage;
	PyObject* py_deliversMessage; // from generate_py ()
	bool openAnyway;
	PyObject* py_openAnyway; // from generate_py ()
	BRect clickToOpenRect;
	Haiku_Rect_Object* py_clickToOpenRect; // from generate_py()
	bool asynchronous = false;
	PyObject* py_asynchronous; // from generate_py ()
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OOOO|O", &py_screenPoint, &py_deliversMessage, &py_openAnyway, &py_clickToOpenRect, &py_asynchronous);
	if (py_screenPoint != NULL) {
		memcpy((void*)&screenPoint, (void*)((Haiku_Point_Object*)py_screenPoint)->cpp_object, sizeof(BPoint));
	}
	deliversMessage = (bool)(PyObject_IsTrue(py_deliversMessage));
	openAnyway = (bool)(PyObject_IsTrue(py_openAnyway));
	if (py_clickToOpenRect != NULL) {
		memcpy((void*)&clickToOpenRect, (void*)((Haiku_Rect_Object*)py_clickToOpenRect)->cpp_object, sizeof(BRect));
	}
	asynchronous = (bool)(PyObject_IsTrue(py_asynchronous));
	
	retval = python_self->cpp_object->Go(screenPoint, deliversMessage, openAnyway, clickToOpenRect, asynchronous);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_PopUpMenu_ResolveSpecifier(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_ResolveSpecifier(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_PopUpMenu_GetSupportedSuites(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_GetSupportedSuites(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_PopUpMenu_ResizeToPreferred(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_ResizeToPreferred(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_PopUpMenu_GetPreferredSize(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_GetPreferredSize(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_PopUpMenu_SetAsyncAutoDestruct(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_SetAsyncAutoDestruct(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetAsyncAutoDestruct(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_PopUpMenu_AsyncAutoDestruct(Haiku_PopUpMenu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_PopUpMenu_AsyncAutoDestruct(Haiku_PopUpMenu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->AsyncAutoDestruct();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_PopUpMenu_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_PopUpMenu_Object*)a)->cpp_object == ((Haiku_PopUpMenu_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_PopUpMenu_Object*)a)->cpp_object != ((Haiku_PopUpMenu_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_PopUpMenu_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_PopUpMenu_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_PopUpMenu_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_PopUpMenu_Archive, METH_VARARGS, ""},
	{"Go", (PyCFunction)Haiku_PopUpMenu_Go, METH_VARARGS, ""},
	{"GoWithClickRect", (PyCFunction)Haiku_PopUpMenu_GoWithClickRect, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_PopUpMenu_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_PopUpMenu_GetSupportedSuites, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_PopUpMenu_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_PopUpMenu_GetPreferredSize, METH_VARARGS, ""},
	{"SetAsyncAutoDestruct", (PyCFunction)Haiku_PopUpMenu_SetAsyncAutoDestruct, METH_VARARGS, ""},
	{"AsyncAutoDestruct", (PyCFunction)Haiku_PopUpMenu_AsyncAutoDestruct, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_PopUpMenu_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.PopUpMenu";
	type->tp_basicsize   = sizeof(Haiku_PopUpMenu_Object);
	type->tp_dealloc     = (destructor)Haiku_PopUpMenu_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_PopUpMenu_RichCompare;
	type->tp_methods     = Haiku_PopUpMenu_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Menu_PyType;
	type->tp_init        = (initproc)Haiku_PopUpMenu_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

