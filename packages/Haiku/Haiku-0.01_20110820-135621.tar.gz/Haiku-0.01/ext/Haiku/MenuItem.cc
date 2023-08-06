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
//static int Haiku_MenuItem_init(Haiku_MenuItem_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_MenuItem_init(Haiku_MenuItem_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	char shortcut = 0;
	PyObject* py_shortcut; // from generate_py ()
	uint32 modifiers = 0;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "sO|Ok", &label, &py_message, &py_shortcut, &modifiers);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	memcpy((void*)&shortcut, (void*)PyString_AsString(py_shortcut), 1);
	
	python_self->cpp_object = new BMenuItem(label, message, shortcut, modifiers);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_MenuItem_newSubmenu(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuItem_newSubmenu(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuItem_Object* python_self;
	BMenu* submenu;
	Haiku_Menu_Object* py_submenu; // from generate_py()
	BMessage* message = NULL;
	Haiku_Message_Object* py_message; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuItem_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O|O", &py_submenu, &py_message);
	if (py_submenu != NULL) {
		submenu = ((Haiku_Menu_Object*)py_submenu)->cpp_object;
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BMenuItem(submenu, message);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_MenuItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MenuItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MenuItem_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MenuItem_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BMenuItem(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_MenuItem_DESTROY(Haiku_MenuItem_Object* python_self);
static void Haiku_MenuItem_DESTROY(Haiku_MenuItem_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_MenuItem_Instantiate(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Instantiate(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuItem_Archive(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Archive(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuItem_SetLabel(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_SetLabel(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	const char* string;
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	python_self->cpp_object->SetLabel(string);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuItem_SetEnabled(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_SetEnabled(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuItem_SetMarked(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_SetMarked(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	bool flag;
	PyObject* py_flag; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_flag);
	flag = (bool)(PyObject_IsTrue(py_flag));
	
	python_self->cpp_object->SetMarked(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuItem_SetTrigger(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_SetTrigger(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	char trigger;
	PyObject* py_trigger; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_trigger);
	PyString2Char(py_trigger, &trigger, 1, sizeof(char));
	
	python_self->cpp_object->SetTrigger(trigger);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuItem_SetShortcut(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_SetShortcut(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	char shortcut;
	PyObject* py_shortcut; // from generate_py ()
	uint32 modifiers;
	
	PyArg_ParseTuple(python_args, "Ok", &py_shortcut, &modifiers);
	memcpy((void*)&shortcut, (void*)PyString_AsString(py_shortcut), 1);
	
	python_self->cpp_object->SetShortcut(shortcut, modifiers);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MenuItem_Label(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Label(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Label();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_MenuItem_IsEnabled(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_IsEnabled(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MenuItem_IsMarked(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_IsMarked(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsMarked();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MenuItem_Trigger(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Trigger(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	char retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Trigger();
	
	py_retval = Char2PyString(&retval, 1, sizeof(char));
	return py_retval;
}

//static PyObject* Haiku_MenuItem_Shortcut(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Shortcut(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	uint32 modifiers;
	char retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Shortcut(&modifiers);
	
	py_retval = Py_BuildValue("s#", &retval, 1);
	
	return Py_BuildValue("Ok", py_retval, modifiers);
}

//static PyObject* Haiku_MenuItem_Submenu(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Submenu(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	BMenu* retval;
	Haiku_Menu_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Submenu();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Menu_Object*)Haiku_Menu_PyType.tp_alloc(&Haiku_Menu_PyType, 0);
	py_retval->cpp_object = (BMenu*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_MenuItem_Menu(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Menu(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_MenuItem_Frame(Haiku_MenuItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MenuItem_Frame(Haiku_MenuItem_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Frame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_MenuItem_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_MenuItem_Object*)a)->cpp_object == ((Haiku_MenuItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_MenuItem_Object*)a)->cpp_object != ((Haiku_MenuItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_MenuItem_PyMethods[] = {
	{"Submenu", (PyCFunction)Haiku_MenuItem_newSubmenu, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_MenuItem_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_MenuItem_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_MenuItem_Archive, METH_VARARGS, ""},
	{"SetLabel", (PyCFunction)Haiku_MenuItem_SetLabel, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_MenuItem_SetEnabled, METH_VARARGS, ""},
	{"SetMarked", (PyCFunction)Haiku_MenuItem_SetMarked, METH_VARARGS, ""},
	{"SetTrigger", (PyCFunction)Haiku_MenuItem_SetTrigger, METH_VARARGS, ""},
	{"SetShortcut", (PyCFunction)Haiku_MenuItem_SetShortcut, METH_VARARGS, ""},
	{"Label", (PyCFunction)Haiku_MenuItem_Label, METH_VARARGS, ""},
	{"IsEnabled", (PyCFunction)Haiku_MenuItem_IsEnabled, METH_VARARGS, ""},
	{"IsMarked", (PyCFunction)Haiku_MenuItem_IsMarked, METH_VARARGS, ""},
	{"Trigger", (PyCFunction)Haiku_MenuItem_Trigger, METH_VARARGS, ""},
	{"Shortcut", (PyCFunction)Haiku_MenuItem_Shortcut, METH_VARARGS, ""},
	{"Submenu", (PyCFunction)Haiku_MenuItem_Submenu, METH_VARARGS, ""},
	{"Menu", (PyCFunction)Haiku_MenuItem_Menu, METH_VARARGS, ""},
	{"Frame", (PyCFunction)Haiku_MenuItem_Frame, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_MenuItem_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.MenuItem";
	type->tp_basicsize   = sizeof(Haiku_MenuItem_Object);
	type->tp_dealloc     = (destructor)Haiku_MenuItem_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_MenuItem_RichCompare;
	type->tp_methods     = Haiku_MenuItem_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Invoker_PyType;
	type->tp_init        = (initproc)Haiku_MenuItem_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

