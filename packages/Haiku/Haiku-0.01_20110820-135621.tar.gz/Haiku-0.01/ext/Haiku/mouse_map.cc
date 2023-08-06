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
//static int Haiku_mouse_map_init(Haiku_mouse_map_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_mouse_map_init(Haiku_mouse_map_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new mouse_map();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_mouse_map_DESTROY(Haiku_mouse_map_Object* python_self);
static void Haiku_mouse_map_DESTROY(Haiku_mouse_map_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_mouse_map_Object_getbutton(Haiku_mouse_map_Object* python_self, void* python_closure) {
	PyObject* py_button; // from generate()
	PyObject* py_button_element;	// from array_arg_builder
	py_button = PyList_New(0);
	for (int i = 0; i < B_MAX_MOUSE_BUTTONS; i++) {
		py_button_element = Py_BuildValue("k", python_self->cpp_object->button[i]);
		PyList_Append(py_button, py_button_element);
	}
	return py_button;
}

static int Haiku_mouse_map_Object_setbutton(Haiku_mouse_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < B_MAX_MOUSE_BUTTONS; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->button[i] = (uint32)PyLong_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_mouse_map_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_mouse_map_Object*)a)->cpp_object == ((Haiku_mouse_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_mouse_map_Object*)a)->cpp_object != ((Haiku_mouse_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_mouse_map_PyProperties[] = {
	{ (char*)"button", (getter)Haiku_mouse_map_Object_getbutton, (setter)Haiku_mouse_map_Object_setbutton, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_mouse_map_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.mouse_map";
	type->tp_basicsize   = sizeof(Haiku_mouse_map_Object);
	type->tp_dealloc     = (destructor)Haiku_mouse_map_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_mouse_map_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_mouse_map_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_mouse_map_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

