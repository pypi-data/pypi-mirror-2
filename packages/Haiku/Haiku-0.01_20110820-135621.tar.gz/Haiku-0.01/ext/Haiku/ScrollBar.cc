/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_ScrollBarConstants_PyMethods[] = {
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
//static int Haiku_ScrollBar_init(Haiku_ScrollBar_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_ScrollBar_init(Haiku_ScrollBar_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	float min;
	float max;
	orientation direction;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OsOffi", &py_frame, &name, &py_target, &min, &max, &direction);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
	}
	
	python_self->cpp_object = new BScrollBar(frame, name, target, min, max, direction);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_ScrollBar_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ScrollBar_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ScrollBar_Object* python_self;
	const char* name;
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	float min;
	float max;
	orientation direction;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ScrollBar_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sOffi", &name, &py_target, &min, &max, &direction);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
	}
	
	python_self->cpp_object = new BScrollBar(name, target, min, max, direction);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_ScrollBar_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ScrollBar_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ScrollBar_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ScrollBar_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BScrollBar(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_ScrollBar_DESTROY(Haiku_ScrollBar_Object* python_self);
static void Haiku_ScrollBar_DESTROY(Haiku_ScrollBar_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_ScrollBar_Instantiate(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Instantiate(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollBar_Archive(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Archive(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollBar_SetValue(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetValue(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float value;
	
	PyArg_ParseTuple(python_args, "f", &value);
	
	python_self->cpp_object->SetValue(value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_Value(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Value(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Value();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_ScrollBar_SetProportion(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetProportion(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float proportion;
	
	PyArg_ParseTuple(python_args, "f", &proportion);
	
	python_self->cpp_object->SetProportion(proportion);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_Proportion(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Proportion(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Proportion();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_ScrollBar_SetRange(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetRange(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float min;
	float max;
	
	PyArg_ParseTuple(python_args, "ff", &min, &max);
	
	python_self->cpp_object->SetRange(min, max);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_GetRange(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_GetRange(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float min;
	float max;
	
	python_self->cpp_object->GetRange(&min, &max);
	
	return Py_BuildValue("ff", min, max);
}

//static PyObject* Haiku_ScrollBar_SetSteps(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetSteps(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float smallStep;
	float largeStep;
	
	PyArg_ParseTuple(python_args, "ff", &smallStep, &largeStep);
	
	python_self->cpp_object->SetSteps(smallStep, largeStep);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_GetSteps(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_GetSteps(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float smallStep;
	float largeStep;
	
	python_self->cpp_object->GetSteps(&smallStep, &largeStep);
	
	return Py_BuildValue("ff", smallStep, largeStep);
}

//static PyObject* Haiku_ScrollBar_SetTarget(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetTarget(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	BView* target;
	Haiku_View_Object* py_target; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		target = ((Haiku_View_Object*)py_target)->cpp_object;
	}
	
	python_self->cpp_object->SetTarget(target);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_Target(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Target(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Target();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ScrollBar_SetOrientation(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetOrientation(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	orientation direction;
	
	PyArg_ParseTuple(python_args, "i", &direction);
	
	python_self->cpp_object->SetOrientation(direction);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_Orientation(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_Orientation(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	orientation retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Orientation();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_ScrollBar_SetBorderHighlighted(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_SetBorderHighlighted(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetBorderHighlighted(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_ResolveSpecifier(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_ResolveSpecifier(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ScrollBar_ResizeToPreferred(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_ResizeToPreferred(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_GetPreferredSize(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_GetPreferredSize(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_ScrollBar_MakeFocus(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_MakeFocus(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ScrollBar_GetSupportedSuites(Haiku_ScrollBar_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ScrollBar_GetSupportedSuites(Haiku_ScrollBar_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_ScrollBar_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ScrollBar_Object*)a)->cpp_object == ((Haiku_ScrollBar_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ScrollBar_Object*)a)->cpp_object != ((Haiku_ScrollBar_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ScrollBar_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_ScrollBar_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_ScrollBar_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_ScrollBar_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_ScrollBar_Archive, METH_VARARGS, ""},
	{"SetValue", (PyCFunction)Haiku_ScrollBar_SetValue, METH_VARARGS, ""},
	{"Value", (PyCFunction)Haiku_ScrollBar_Value, METH_VARARGS, ""},
	{"SetProportion", (PyCFunction)Haiku_ScrollBar_SetProportion, METH_VARARGS, ""},
	{"Proportion", (PyCFunction)Haiku_ScrollBar_Proportion, METH_VARARGS, ""},
	{"SetRange", (PyCFunction)Haiku_ScrollBar_SetRange, METH_VARARGS, ""},
	{"GetRange", (PyCFunction)Haiku_ScrollBar_GetRange, METH_VARARGS, ""},
	{"SetSteps", (PyCFunction)Haiku_ScrollBar_SetSteps, METH_VARARGS, ""},
	{"GetSteps", (PyCFunction)Haiku_ScrollBar_GetSteps, METH_VARARGS, ""},
	{"SetTarget", (PyCFunction)Haiku_ScrollBar_SetTarget, METH_VARARGS, ""},
	{"Target", (PyCFunction)Haiku_ScrollBar_Target, METH_VARARGS, ""},
	{"SetOrientation", (PyCFunction)Haiku_ScrollBar_SetOrientation, METH_VARARGS, ""},
	{"Orientation", (PyCFunction)Haiku_ScrollBar_Orientation, METH_VARARGS, ""},
	{"SetBorderHighlighted", (PyCFunction)Haiku_ScrollBar_SetBorderHighlighted, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_ScrollBar_ResolveSpecifier, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_ScrollBar_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_ScrollBar_GetPreferredSize, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_ScrollBar_MakeFocus, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_ScrollBar_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ScrollBar_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ScrollBar";
	type->tp_basicsize   = sizeof(Haiku_ScrollBar_Object);
	type->tp_dealloc     = (destructor)Haiku_ScrollBar_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ScrollBar_RichCompare;
	type->tp_methods     = Haiku_ScrollBar_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_ScrollBar_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

