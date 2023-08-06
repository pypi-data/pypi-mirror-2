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
//static int Haiku_RadioButton_init(Haiku_RadioButton_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_RadioButton_init(Haiku_RadioButton_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OssO|kk", &py_frame, &name, &label, &py_message, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object = new BRadioButton(frame, name, label, message, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_RadioButton_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_RadioButton_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_RadioButton_Object* python_self;
	const char* name;
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	uint32 flags = B_WILL_DRAW | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_RadioButton_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "ssO|k", &name, &label, &py_message, &flags);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object = new BRadioButton(name, label, message, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_RadioButton_newBareBones(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_RadioButton_newBareBones(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_RadioButton_Object* python_self;
	const char* label;
	BMessage* message = NULL;
	Haiku_Message_Object* py_message; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_RadioButton_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "s|O", &label, &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object = new BRadioButton(label, message);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_RadioButton_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_RadioButton_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_RadioButton_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_RadioButton_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BRadioButton(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_RadioButton_DESTROY(Haiku_RadioButton_Object* python_self);
static void Haiku_RadioButton_DESTROY(Haiku_RadioButton_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_RadioButton_Instantiate(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_Instantiate(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_RadioButton_Archive(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_Archive(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_RadioButton_SetValue(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_SetValue(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
	int32 value;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	python_self->cpp_object->SetValue(value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_RadioButton_GetPreferredSize(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_GetPreferredSize(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_RadioButton_ResizeToPreferred(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_ResizeToPreferred(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_RadioButton_Invoke(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_Invoke(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_RadioButton_ResolveSpecifier(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_ResolveSpecifier(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_RadioButton_MakeFocus(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_MakeFocus(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_RadioButton_GetSupportedSuites(Haiku_RadioButton_Object* python_self, PyObject* python_args);
static PyObject* Haiku_RadioButton_GetSupportedSuites(Haiku_RadioButton_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_RadioButton_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_RadioButton_Object*)a)->cpp_object == ((Haiku_RadioButton_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_RadioButton_Object*)a)->cpp_object != ((Haiku_RadioButton_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_RadioButton_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_RadioButton_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"BareBones", (PyCFunction)Haiku_RadioButton_newBareBones, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_RadioButton_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_RadioButton_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_RadioButton_Archive, METH_VARARGS, ""},
	{"SetValue", (PyCFunction)Haiku_RadioButton_SetValue, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_RadioButton_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_RadioButton_ResizeToPreferred, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_RadioButton_Invoke, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_RadioButton_ResolveSpecifier, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_RadioButton_MakeFocus, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_RadioButton_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_RadioButton_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.RadioButton";
	type->tp_basicsize   = sizeof(Haiku_RadioButton_Object);
	type->tp_dealloc     = (destructor)Haiku_RadioButton_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_RadioButton_RichCompare;
	type->tp_methods     = Haiku_RadioButton_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Control_PyType;
	type->tp_init        = (initproc)Haiku_RadioButton_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

