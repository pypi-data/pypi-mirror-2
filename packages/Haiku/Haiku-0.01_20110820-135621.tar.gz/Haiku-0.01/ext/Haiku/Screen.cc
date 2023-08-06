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
//static int Haiku_Screen_init(Haiku_Screen_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Screen_init(Haiku_Screen_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	screen_id id = B_MAIN_SCREEN_ID;
	Haiku_screen_id_Object* py_id; // from generate_py()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "|O", &py_id);
	if (py_id != NULL) {
		memcpy((void*)&id, (void*)((Haiku_screen_id_Object*)py_id)->cpp_object, sizeof(screen_id));
	}
	
	python_self->cpp_object = new BScreen(id);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Screen_newForWindow(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Screen_newForWindow(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Screen_Object* python_self;
	BWindow* window;
	Haiku_Window_Object* py_window; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Screen_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_window);
	if (py_window != NULL) {
		window = ((Haiku_Window_Object*)py_window)->cpp_object;
	}
	
	python_self->cpp_object = new BScreen(window);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Screen_DESTROY(Haiku_Screen_Object* python_self);
static void Haiku_Screen_DESTROY(Haiku_Screen_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Screen_IsValid(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_IsValid(Haiku_Screen_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsValid();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Screen_SetToNext(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_SetToNext(Haiku_Screen_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->SetToNext();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_ColorSpace(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_ColorSpace(Haiku_Screen_Object* python_self, PyObject* python_args) {
	color_space retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->ColorSpace();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Screen_Frame(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_Frame(Haiku_Screen_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Frame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_ID(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_ID(Haiku_Screen_Object* python_self, PyObject* python_args) {
	screen_id retval;
	Haiku_screen_id_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ID();
	
	py_retval = (Haiku_screen_id_Object*)Haiku_screen_id_PyType.tp_alloc(&Haiku_screen_id_PyType, 0);
	py_retval->cpp_object = (screen_id*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_WaitForRetrace(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_WaitForRetrace(Haiku_Screen_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->WaitForRetrace();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_WaitForRetraceWithTimeout(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_WaitForRetraceWithTimeout(Haiku_Screen_Object* python_self, PyObject* python_args) {
	bigtime_t timeout;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &timeout);
	
	retval = python_self->cpp_object->WaitForRetrace(timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_IndexForColor(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_IndexForColor(Haiku_Screen_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_color);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	
	retval = python_self->cpp_object->IndexForColor(color);
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_Screen_IndexForColorFromRGB(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_IndexForColorFromRGB(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint8 red;
	uint8 green;
	uint8 blue;
	uint8 alpha = 255;
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "BBB|B", &red, &green, &blue, &alpha);
	
	retval = python_self->cpp_object->IndexForColor(red, green, blue, alpha);
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_Screen_ColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_ColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint8 index;
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "B", &index);
	
	retval = python_self->cpp_object->ColorForIndex(index);
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_InvertIndex(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_InvertIndex(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint8 index;
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "B", &index);
	
	retval = python_self->cpp_object->InvertIndex(index);
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_Screen_ColorMap(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_ColorMap(Haiku_Screen_Object* python_self, PyObject* python_args) {
	const color_map* retval;
	Haiku_color_map_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ColorMap();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_color_map_Object*)Haiku_color_map_PyType.tp_alloc(&Haiku_color_map_PyType, 0);
	py_retval->cpp_object = (color_map*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_DesktopColor(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_DesktopColor(Haiku_Screen_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->DesktopColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_DesktopColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_DesktopColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint32 index;
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "k", &index);
	
	retval = python_self->cpp_object->DesktopColor(index);
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Screen_SetDesktopColor(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_SetDesktopColor(Haiku_Screen_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	bool makeDefault = true;
	PyObject* py_makeDefault; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O|O", &py_color, &py_makeDefault);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	makeDefault = (bool)(PyObject_IsTrue(py_makeDefault));
	
	python_self->cpp_object->SetDesktopColor(color, makeDefault);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_SetDesktopColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_SetDesktopColorForIndex(Haiku_Screen_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	uint32 index;
	bool makeDefault = true;
	PyObject* py_makeDefault; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "Ok|O", &py_color, &index, &py_makeDefault);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	makeDefault = (bool)(PyObject_IsTrue(py_makeDefault));
	
	python_self->cpp_object->SetDesktopColor(color, index, makeDefault);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_SetDPMS(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_SetDPMS(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint32 state;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k", &state);
	
	retval = python_self->cpp_object->SetDPMS(state);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Screen_DPMSState(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_DPMSState(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DPMSState();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Screen_DPMSCapabilities(Haiku_Screen_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Screen_DPMSCapabilities(Haiku_Screen_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DPMSCapabilites();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

static PyObject* Haiku_Screen_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Screen_Object*)a)->cpp_object == ((Haiku_Screen_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Screen_Object*)a)->cpp_object != ((Haiku_Screen_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Screen_PyMethods[] = {
	{"ForWindow", (PyCFunction)Haiku_Screen_newForWindow, METH_VARARGS|METH_CLASS, ""},
	{"IsValid", (PyCFunction)Haiku_Screen_IsValid, METH_VARARGS, ""},
	{"SetToNext", (PyCFunction)Haiku_Screen_SetToNext, METH_VARARGS, ""},
	{"ColorSpace", (PyCFunction)Haiku_Screen_ColorSpace, METH_VARARGS, ""},
	{"Frame", (PyCFunction)Haiku_Screen_Frame, METH_VARARGS, ""},
	{"ID", (PyCFunction)Haiku_Screen_ID, METH_VARARGS, ""},
	{"WaitForRetrace", (PyCFunction)Haiku_Screen_WaitForRetrace, METH_VARARGS, ""},
	{"WaitForRetraceWithTimeout", (PyCFunction)Haiku_Screen_WaitForRetraceWithTimeout, METH_VARARGS, ""},
	{"IndexForColor", (PyCFunction)Haiku_Screen_IndexForColor, METH_VARARGS, ""},
	{"IndexForColorFromRGB", (PyCFunction)Haiku_Screen_IndexForColorFromRGB, METH_VARARGS, ""},
	{"ColorForIndex", (PyCFunction)Haiku_Screen_ColorForIndex, METH_VARARGS, ""},
	{"InvertIndex", (PyCFunction)Haiku_Screen_InvertIndex, METH_VARARGS, ""},
	{"ColorMap", (PyCFunction)Haiku_Screen_ColorMap, METH_VARARGS, ""},
	{"DesktopColor", (PyCFunction)Haiku_Screen_DesktopColor, METH_VARARGS, ""},
	{"DesktopColorForIndex", (PyCFunction)Haiku_Screen_DesktopColorForIndex, METH_VARARGS, ""},
	{"SetDesktopColor", (PyCFunction)Haiku_Screen_SetDesktopColor, METH_VARARGS, ""},
	{"SetDesktopColorForIndex", (PyCFunction)Haiku_Screen_SetDesktopColorForIndex, METH_VARARGS, ""},
	{"SetDPMS", (PyCFunction)Haiku_Screen_SetDPMS, METH_VARARGS, ""},
	{"DPMSState", (PyCFunction)Haiku_Screen_DPMSState, METH_VARARGS, ""},
	{"DPMSCapabilities", (PyCFunction)Haiku_Screen_DPMSCapabilities, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Screen_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Screen";
	type->tp_basicsize   = sizeof(Haiku_Screen_Object);
	type->tp_dealloc     = (destructor)Haiku_Screen_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Screen_RichCompare;
	type->tp_methods     = Haiku_Screen_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Screen_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

