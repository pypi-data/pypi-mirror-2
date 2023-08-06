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
//static int Haiku_scroll_bar_info_init(Haiku_scroll_bar_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_scroll_bar_info_init(Haiku_scroll_bar_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new scroll_bar_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_scroll_bar_info_DESTROY(Haiku_scroll_bar_info_Object* python_self);
static void Haiku_scroll_bar_info_DESTROY(Haiku_scroll_bar_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_scroll_bar_info_Object_getproportional(Haiku_scroll_bar_info_Object* python_self, void* python_closure) {
	PyObject* py_proportional; // from generate()
	py_proportional = Py_BuildValue("b", (python_self->cpp_object->proportional ? 1 : 0));
	return py_proportional;
}

static int Haiku_scroll_bar_info_Object_setproportional(Haiku_scroll_bar_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->proportional = (bool)(PyObject_IsTrue(value));
	return 0;
}

static PyObject* Haiku_scroll_bar_info_Object_getdouble_arrows(Haiku_scroll_bar_info_Object* python_self, void* python_closure) {
	PyObject* py_double_arrows; // from generate()
	py_double_arrows = Py_BuildValue("b", (python_self->cpp_object->double_arrows ? 1 : 0));
	return py_double_arrows;
}

static int Haiku_scroll_bar_info_Object_setdouble_arrows(Haiku_scroll_bar_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->double_arrows = (bool)(PyObject_IsTrue(value));
	return 0;
}

static PyObject* Haiku_scroll_bar_info_Object_getknob(Haiku_scroll_bar_info_Object* python_self, void* python_closure) {
	PyObject* py_knob; // from generate()
	py_knob = Py_BuildValue("l", python_self->cpp_object->knob);
	return py_knob;
}

static int Haiku_scroll_bar_info_Object_setknob(Haiku_scroll_bar_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->knob = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_scroll_bar_info_Object_getmin_knob_size(Haiku_scroll_bar_info_Object* python_self, void* python_closure) {
	PyObject* py_min_knob_size; // from generate()
	py_min_knob_size = Py_BuildValue("l", python_self->cpp_object->min_knob_size);
	return py_min_knob_size;
}

static int Haiku_scroll_bar_info_Object_setmin_knob_size(Haiku_scroll_bar_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->min_knob_size = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_scroll_bar_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_scroll_bar_info_Object*)a)->cpp_object == ((Haiku_scroll_bar_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_scroll_bar_info_Object*)a)->cpp_object != ((Haiku_scroll_bar_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_scroll_bar_info_PyProperties[] = {
	{ (char*)"proportional", (getter)Haiku_scroll_bar_info_Object_getproportional, (setter)Haiku_scroll_bar_info_Object_setproportional, (char*)"<DOC>", NULL},
	{ (char*)"double_arrows", (getter)Haiku_scroll_bar_info_Object_getdouble_arrows, (setter)Haiku_scroll_bar_info_Object_setdouble_arrows, (char*)"<DOC>", NULL},
	{ (char*)"knob", (getter)Haiku_scroll_bar_info_Object_getknob, (setter)Haiku_scroll_bar_info_Object_setknob, (char*)"<DOC>", NULL},
	{ (char*)"min_knob_size", (getter)Haiku_scroll_bar_info_Object_getmin_knob_size, (setter)Haiku_scroll_bar_info_Object_setmin_knob_size, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_scroll_bar_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.scroll_bar_info";
	type->tp_basicsize   = sizeof(Haiku_scroll_bar_info_Object);
	type->tp_dealloc     = (destructor)Haiku_scroll_bar_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_scroll_bar_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_scroll_bar_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_scroll_bar_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

