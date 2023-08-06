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
//static int Haiku_menu_info_init(Haiku_menu_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_menu_info_init(Haiku_menu_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new menu_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_menu_info_DESTROY(Haiku_menu_info_Object* python_self);
static void Haiku_menu_info_DESTROY(Haiku_menu_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_menu_info_Object_getfont_size(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_font_size; // from generate()
	py_font_size = Py_BuildValue("f", python_self->cpp_object->font_size);
	return py_font_size;
}

static int Haiku_menu_info_Object_setfont_size(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->font_size = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_menu_info_Object_getf_family(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_f_family; // from generate()
	Py_ssize_t py_f_family_length;
	py_f_family = Py_BuildValue("s", &python_self->cpp_object->f_family);	// 's' instead of 's#' lets Python calculate length
	
	py_f_family_length = PyString_Size(py_f_family);
	if (py_f_family_length > B_FONT_FAMILY_LENGTH + 1) {
		py_f_family_length = B_FONT_FAMILY_LENGTH + 1;
		_PyString_Resize(&py_f_family, py_f_family_length);
	}
	
	return py_f_family;
}

static int Haiku_menu_info_Object_setf_family(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	memcpy((void*)&python_self->cpp_object->f_family, (void*)PyString_AsString(value), B_FONT_FAMILY_LENGTH + 1);
	return 0;
}

static PyObject* Haiku_menu_info_Object_getf_style(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_f_style; // from generate()
	Py_ssize_t py_f_style_length;
	py_f_style = Py_BuildValue("s", &python_self->cpp_object->f_style);	// 's' instead of 's#' lets Python calculate length
	
	py_f_style_length = PyString_Size(py_f_style);
	if (py_f_style_length > B_FONT_STYLE_LENGTH + 1) {
		py_f_style_length = B_FONT_STYLE_LENGTH + 1;
		_PyString_Resize(&py_f_style, py_f_style_length);
	}
	
	return py_f_style;
}

static int Haiku_menu_info_Object_setf_style(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	memcpy((void*)&python_self->cpp_object->f_style, (void*)PyString_AsString(value), B_FONT_STYLE_LENGTH + 1);
	return 0;
}

static PyObject* Haiku_menu_info_Object_getbackground_color(Haiku_menu_info_Object* python_self, void* python_closure) {
	Haiku_rgb_color_Object* py_background_color;

	py_background_color = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_background_color->cpp_object = (rgb_color*)&python_self->cpp_object->background_color;
	// cannot delete this object; we do not own it
	py_background_color->can_delete_cpp_object = false;
	return (PyObject*)py_background_color;
}

static int Haiku_menu_info_Object_setbackground_color(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->background_color, (void*)((Haiku_rgb_color_Object*)value)->cpp_object, sizeof(rgb_color));
	}
	return 0;
}

static PyObject* Haiku_menu_info_Object_getseparator(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_separator; // from generate()
	py_separator = Py_BuildValue("l", python_self->cpp_object->separator);
	return py_separator;
}

static int Haiku_menu_info_Object_setseparator(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->separator = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_menu_info_Object_getclick_to_open(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_click_to_open; // from generate()
	py_click_to_open = Py_BuildValue("b", (python_self->cpp_object->click_to_open ? 1 : 0));
	return py_click_to_open;
}

static int Haiku_menu_info_Object_setclick_to_open(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->click_to_open = (bool)(PyObject_IsTrue(value));
	return 0;
}

static PyObject* Haiku_menu_info_Object_gettriggers_always_shown(Haiku_menu_info_Object* python_self, void* python_closure) {
	PyObject* py_triggers_always_shown; // from generate()
	py_triggers_always_shown = Py_BuildValue("b", (python_self->cpp_object->triggers_always_shown ? 1 : 0));
	return py_triggers_always_shown;
}

static int Haiku_menu_info_Object_settriggers_always_shown(Haiku_menu_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->triggers_always_shown = (bool)(PyObject_IsTrue(value));
	return 0;
}

static PyObject* Haiku_menu_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_menu_info_Object*)a)->cpp_object == ((Haiku_menu_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_menu_info_Object*)a)->cpp_object != ((Haiku_menu_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_menu_info_PyProperties[] = {
	{ (char*)"font_size", (getter)Haiku_menu_info_Object_getfont_size, (setter)Haiku_menu_info_Object_setfont_size, (char*)"<DOC>", NULL},
	{ (char*)"f_family", (getter)Haiku_menu_info_Object_getf_family, (setter)Haiku_menu_info_Object_setf_family, (char*)"<DOC>", NULL},
	{ (char*)"f_style", (getter)Haiku_menu_info_Object_getf_style, (setter)Haiku_menu_info_Object_setf_style, (char*)"<DOC>", NULL},
	{ (char*)"background_color", (getter)Haiku_menu_info_Object_getbackground_color, (setter)Haiku_menu_info_Object_setbackground_color, (char*)"<DOC>", NULL},
	{ (char*)"separator", (getter)Haiku_menu_info_Object_getseparator, (setter)Haiku_menu_info_Object_setseparator, (char*)"<DOC>", NULL},
	{ (char*)"click_to_open", (getter)Haiku_menu_info_Object_getclick_to_open, (setter)Haiku_menu_info_Object_setclick_to_open, (char*)"<DOC>", NULL},
	{ (char*)"triggers_always_shown", (getter)Haiku_menu_info_Object_gettriggers_always_shown, (setter)Haiku_menu_info_Object_settriggers_always_shown, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_menu_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.menu_info";
	type->tp_basicsize   = sizeof(Haiku_menu_info_Object);
	type->tp_dealloc     = (destructor)Haiku_menu_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_menu_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_menu_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_menu_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

