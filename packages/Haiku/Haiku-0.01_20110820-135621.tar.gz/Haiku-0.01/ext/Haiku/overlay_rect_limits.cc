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
//static int Haiku_overlay_rect_limits_init(Haiku_overlay_rect_limits_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_overlay_rect_limits_init(Haiku_overlay_rect_limits_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new overlay_rect_limits();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_overlay_rect_limits_DESTROY(Haiku_overlay_rect_limits_Object* python_self);
static void Haiku_overlay_rect_limits_DESTROY(Haiku_overlay_rect_limits_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_overlay_rect_limits_Object_gethorizontal_alignment(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_horizontal_alignment; // from generate()
	py_horizontal_alignment = Py_BuildValue("h", python_self->cpp_object->horizontal_alignment);
	return py_horizontal_alignment;
}

static int Haiku_overlay_rect_limits_Object_sethorizontal_alignment(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->horizontal_alignment = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getvertical_alignment(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_vertical_alignment; // from generate()
	py_vertical_alignment = Py_BuildValue("h", python_self->cpp_object->vertical_alignment);
	return py_vertical_alignment;
}

static int Haiku_overlay_rect_limits_Object_setvertical_alignment(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->vertical_alignment = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getwidth_alignment(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_width_alignment; // from generate()
	py_width_alignment = Py_BuildValue("h", python_self->cpp_object->width_alignment);
	return py_width_alignment;
}

static int Haiku_overlay_rect_limits_Object_setwidth_alignment(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->width_alignment = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getheight_alignment(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_height_alignment; // from generate()
	py_height_alignment = Py_BuildValue("h", python_self->cpp_object->height_alignment);
	return py_height_alignment;
}

static int Haiku_overlay_rect_limits_Object_setheight_alignment(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->height_alignment = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getmin_width(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_min_width; // from generate()
	py_min_width = Py_BuildValue("h", python_self->cpp_object->min_width);
	return py_min_width;
}

static int Haiku_overlay_rect_limits_Object_setmin_width(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->min_width = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getmax_width(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_max_width; // from generate()
	py_max_width = Py_BuildValue("h", python_self->cpp_object->max_width);
	return py_max_width;
}

static int Haiku_overlay_rect_limits_Object_setmax_width(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->max_width = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getmin_height(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_min_height; // from generate()
	py_min_height = Py_BuildValue("h", python_self->cpp_object->min_height);
	return py_min_height;
}

static int Haiku_overlay_rect_limits_Object_setmin_height(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->min_height = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getmax_height(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_max_height; // from generate()
	py_max_height = Py_BuildValue("h", python_self->cpp_object->max_height);
	return py_max_height;
}

static int Haiku_overlay_rect_limits_Object_setmax_height(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->max_height = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_Object_getreserved(Haiku_overlay_rect_limits_Object* python_self, void* python_closure) {
	PyObject* py_reserved; // from generate()
	PyObject* py_reserved_element;	// from array_arg_builder
	py_reserved = PyList_New(0);
	for (int i = 0; i < 8; i++) {
		py_reserved_element = Py_BuildValue("l", python_self->cpp_object->reserved[i]);
		PyList_Append(py_reserved, py_reserved_element);
	}
	return py_reserved;
}

static int Haiku_overlay_rect_limits_Object_setreserved(Haiku_overlay_rect_limits_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 8; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->reserved[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_overlay_rect_limits_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_overlay_rect_limits_Object*)a)->cpp_object == ((Haiku_overlay_rect_limits_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_overlay_rect_limits_Object*)a)->cpp_object != ((Haiku_overlay_rect_limits_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_overlay_rect_limits_PyProperties[] = {
	{ (char*)"horizontal_alignment", (getter)Haiku_overlay_rect_limits_Object_gethorizontal_alignment, (setter)Haiku_overlay_rect_limits_Object_sethorizontal_alignment, (char*)"<DOC>", NULL},
	{ (char*)"vertical_alignment", (getter)Haiku_overlay_rect_limits_Object_getvertical_alignment, (setter)Haiku_overlay_rect_limits_Object_setvertical_alignment, (char*)"<DOC>", NULL},
	{ (char*)"width_alignment", (getter)Haiku_overlay_rect_limits_Object_getwidth_alignment, (setter)Haiku_overlay_rect_limits_Object_setwidth_alignment, (char*)"<DOC>", NULL},
	{ (char*)"height_alignment", (getter)Haiku_overlay_rect_limits_Object_getheight_alignment, (setter)Haiku_overlay_rect_limits_Object_setheight_alignment, (char*)"<DOC>", NULL},
	{ (char*)"min_width", (getter)Haiku_overlay_rect_limits_Object_getmin_width, (setter)Haiku_overlay_rect_limits_Object_setmin_width, (char*)"<DOC>", NULL},
	{ (char*)"max_width", (getter)Haiku_overlay_rect_limits_Object_getmax_width, (setter)Haiku_overlay_rect_limits_Object_setmax_width, (char*)"<DOC>", NULL},
	{ (char*)"min_height", (getter)Haiku_overlay_rect_limits_Object_getmin_height, (setter)Haiku_overlay_rect_limits_Object_setmin_height, (char*)"<DOC>", NULL},
	{ (char*)"max_height", (getter)Haiku_overlay_rect_limits_Object_getmax_height, (setter)Haiku_overlay_rect_limits_Object_setmax_height, (char*)"<DOC>", NULL},
	{ (char*)"reserved", (getter)Haiku_overlay_rect_limits_Object_getreserved, (setter)Haiku_overlay_rect_limits_Object_setreserved, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_overlay_rect_limits_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.overlay_rect_limits";
	type->tp_basicsize   = sizeof(Haiku_overlay_rect_limits_Object);
	type->tp_dealloc     = (destructor)Haiku_overlay_rect_limits_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_overlay_rect_limits_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_overlay_rect_limits_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_overlay_rect_limits_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

