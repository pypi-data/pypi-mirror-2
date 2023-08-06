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
//static int Haiku_overlay_restrictions_init(Haiku_overlay_restrictions_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_overlay_restrictions_init(Haiku_overlay_restrictions_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new overlay_restrictions();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_overlay_restrictions_DESTROY(Haiku_overlay_restrictions_Object* python_self);
static void Haiku_overlay_restrictions_DESTROY(Haiku_overlay_restrictions_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_overlay_restrictions_Object_getsource(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	Haiku_overlay_rect_limits_Object* py_source;

	py_source = (Haiku_overlay_rect_limits_Object*)Haiku_overlay_rect_limits_PyType.tp_alloc(&Haiku_overlay_rect_limits_PyType, 0);
	py_source->cpp_object = (overlay_rect_limits*)&python_self->cpp_object->source;
	// cannot delete this object; we do not own it
	py_source->can_delete_cpp_object = false;
	return (PyObject*)py_source;
}

static int Haiku_overlay_restrictions_Object_setsource(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->source, (void*)((Haiku_overlay_rect_limits_Object*)value)->cpp_object, sizeof(overlay_rect_limits));
	}
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getdestination(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	Haiku_overlay_rect_limits_Object* py_destination;

	py_destination = (Haiku_overlay_rect_limits_Object*)Haiku_overlay_rect_limits_PyType.tp_alloc(&Haiku_overlay_rect_limits_PyType, 0);
	py_destination->cpp_object = (overlay_rect_limits*)&python_self->cpp_object->destination;
	// cannot delete this object; we do not own it
	py_destination->can_delete_cpp_object = false;
	return (PyObject*)py_destination;
}

static int Haiku_overlay_restrictions_Object_setdestination(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->destination, (void*)((Haiku_overlay_rect_limits_Object*)value)->cpp_object, sizeof(overlay_rect_limits));
	}
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getmin_width_scale(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	PyObject* py_min_width_scale; // from generate()
	py_min_width_scale = Py_BuildValue("f", python_self->cpp_object->min_width_scale);
	return py_min_width_scale;
}

static int Haiku_overlay_restrictions_Object_setmin_width_scale(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->min_width_scale = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getmax_width_scale(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	PyObject* py_max_width_scale; // from generate()
	py_max_width_scale = Py_BuildValue("f", python_self->cpp_object->max_width_scale);
	return py_max_width_scale;
}

static int Haiku_overlay_restrictions_Object_setmax_width_scale(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->max_width_scale = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getmin_height_scale(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	PyObject* py_min_height_scale; // from generate()
	py_min_height_scale = Py_BuildValue("f", python_self->cpp_object->min_height_scale);
	return py_min_height_scale;
}

static int Haiku_overlay_restrictions_Object_setmin_height_scale(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->min_height_scale = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getmax_height_scale(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	PyObject* py_max_height_scale; // from generate()
	py_max_height_scale = Py_BuildValue("f", python_self->cpp_object->max_height_scale);
	return py_max_height_scale;
}

static int Haiku_overlay_restrictions_Object_setmax_height_scale(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->max_height_scale = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_overlay_restrictions_Object_getreserved(Haiku_overlay_restrictions_Object* python_self, void* python_closure) {
	PyObject* py_reserved; // from generate()
	PyObject* py_reserved_element;	// from array_arg_builder
	py_reserved = PyList_New(0);
	for (int i = 0; i < 8; i++) {
		py_reserved_element = Py_BuildValue("l", python_self->cpp_object->reserved[i]);
		PyList_Append(py_reserved, py_reserved_element);
	}
	return py_reserved;
}

static int Haiku_overlay_restrictions_Object_setreserved(Haiku_overlay_restrictions_Object* python_self, PyObject* value, void* closure) {
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

static PyObject* Haiku_overlay_restrictions_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_overlay_restrictions_Object*)a)->cpp_object == ((Haiku_overlay_restrictions_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_overlay_restrictions_Object*)a)->cpp_object != ((Haiku_overlay_restrictions_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_overlay_restrictions_PyProperties[] = {
	{ (char*)"source", (getter)Haiku_overlay_restrictions_Object_getsource, (setter)Haiku_overlay_restrictions_Object_setsource, (char*)"<DOC>", NULL},
	{ (char*)"destination", (getter)Haiku_overlay_restrictions_Object_getdestination, (setter)Haiku_overlay_restrictions_Object_setdestination, (char*)"<DOC>", NULL},
	{ (char*)"min_width_scale", (getter)Haiku_overlay_restrictions_Object_getmin_width_scale, (setter)Haiku_overlay_restrictions_Object_setmin_width_scale, (char*)"<DOC>", NULL},
	{ (char*)"max_width_scale", (getter)Haiku_overlay_restrictions_Object_getmax_width_scale, (setter)Haiku_overlay_restrictions_Object_setmax_width_scale, (char*)"<DOC>", NULL},
	{ (char*)"min_height_scale", (getter)Haiku_overlay_restrictions_Object_getmin_height_scale, (setter)Haiku_overlay_restrictions_Object_setmin_height_scale, (char*)"<DOC>", NULL},
	{ (char*)"max_height_scale", (getter)Haiku_overlay_restrictions_Object_getmax_height_scale, (setter)Haiku_overlay_restrictions_Object_setmax_height_scale, (char*)"<DOC>", NULL},
	{ (char*)"reserved", (getter)Haiku_overlay_restrictions_Object_getreserved, (setter)Haiku_overlay_restrictions_Object_setreserved, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_overlay_restrictions_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.overlay_restrictions";
	type->tp_basicsize   = sizeof(Haiku_overlay_restrictions_Object);
	type->tp_dealloc     = (destructor)Haiku_overlay_restrictions_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_overlay_restrictions_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_overlay_restrictions_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_overlay_restrictions_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

