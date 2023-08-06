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
//static int Haiku_Tab_init(Haiku_Tab_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Tab_init(Haiku_Tab_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BView* tabView = NULL;
	Haiku_View_Object* py_tabView; // from generate_py()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "|O", &py_tabView);
	if (py_tabView != NULL) {
		tabView = ((Haiku_View_Object*)py_tabView)->cpp_object;
	}
	
	python_self->cpp_object = new BTab(tabView);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Tab_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Tab_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Tab_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Tab_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BTab(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Tab_DESTROY(Haiku_Tab_Object* python_self);
static void Haiku_Tab_DESTROY(Haiku_Tab_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Tab_Instantiate(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_Instantiate(Haiku_Tab_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Tab_Archive(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_Archive(Haiku_Tab_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Tab_Label(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_Label(Haiku_Tab_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Label();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Tab_SetLabel(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_SetLabel(Haiku_Tab_Object* python_self, PyObject* python_args) {
	const char* label;
	
	PyArg_ParseTuple(python_args, "s", &label);
	
	python_self->cpp_object->SetLabel(label);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_IsSelected(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_IsSelected(Haiku_Tab_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSelected();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Tab_Select(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_Select(Haiku_Tab_Object* python_self, PyObject* python_args) {
	BView* owner;
	Haiku_View_Object* py_owner; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_owner);
	if (py_owner != NULL) {
		owner = ((Haiku_View_Object*)py_owner)->cpp_object;
	}
	
	python_self->cpp_object->Select(owner);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_Deselect(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_Deselect(Haiku_Tab_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Deselect();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_SetEnabled(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_SetEnabled(Haiku_Tab_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_IsEnabled(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_IsEnabled(Haiku_Tab_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Tab_MakeFocus(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_MakeFocus(Haiku_Tab_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_IsFocus(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_IsFocus(Haiku_Tab_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFocus();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Tab_SetView(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_SetView(Haiku_Tab_Object* python_self, PyObject* python_args) {
	BView* view;
	Haiku_View_Object* py_view; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_view);
	if (py_view != NULL) {
		view = ((Haiku_View_Object*)py_view)->cpp_object;
	}
	
	python_self->cpp_object->SetView(view);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Tab_View(Haiku_Tab_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Tab_View(Haiku_Tab_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->View();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Tab_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Tab_Object*)a)->cpp_object == ((Haiku_Tab_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Tab_Object*)a)->cpp_object != ((Haiku_Tab_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Tab_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_Tab_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Tab_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Tab_Archive, METH_VARARGS, ""},
	{"Label", (PyCFunction)Haiku_Tab_Label, METH_VARARGS, ""},
	{"SetLabel", (PyCFunction)Haiku_Tab_SetLabel, METH_VARARGS, ""},
	{"IsSelected", (PyCFunction)Haiku_Tab_IsSelected, METH_VARARGS, ""},
	{"Select", (PyCFunction)Haiku_Tab_Select, METH_VARARGS, ""},
	{"Deselect", (PyCFunction)Haiku_Tab_Deselect, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_Tab_SetEnabled, METH_VARARGS, ""},
	{"IsEnabled", (PyCFunction)Haiku_Tab_IsEnabled, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_Tab_MakeFocus, METH_VARARGS, ""},
	{"IsFocus", (PyCFunction)Haiku_Tab_IsFocus, METH_VARARGS, ""},
	{"SetView", (PyCFunction)Haiku_Tab_SetView, METH_VARARGS, ""},
	{"View", (PyCFunction)Haiku_Tab_View, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Tab_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Tab";
	type->tp_basicsize   = sizeof(Haiku_Tab_Object);
	type->tp_dealloc     = (destructor)Haiku_Tab_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Tab_RichCompare;
	type->tp_methods     = Haiku_Tab_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)Haiku_Tab_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

