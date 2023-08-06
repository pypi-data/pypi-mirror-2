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
//static int Haiku_key_info_init(Haiku_key_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_key_info_init(Haiku_key_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new key_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_key_info_DESTROY(Haiku_key_info_Object* python_self);
static void Haiku_key_info_DESTROY(Haiku_key_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_key_info_Object_getmodifiers(Haiku_key_info_Object* python_self, void* python_closure) {
	PyObject* py_modifiers; // from generate()
	py_modifiers = Py_BuildValue("k", python_self->cpp_object->modifiers);
	return py_modifiers;
}

static int Haiku_key_info_Object_setmodifiers(Haiku_key_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->modifiers = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_info_Object_getkey_states(Haiku_key_info_Object* python_self, void* python_closure) {
	PyObject* py_key_states; // from generate()
	PyObject* py_key_states_element;	// from array_arg_builder
	py_key_states = PyList_New(0);
	for (int i = 0; i < 16; i++) {
		py_key_states_element = Py_BuildValue("B", python_self->cpp_object->key_states[i]);
		PyList_Append(py_key_states, py_key_states_element);
	}
	return py_key_states;
}

static int Haiku_key_info_Object_setkey_states(Haiku_key_info_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 16; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->key_states[i] = (uint8)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_key_info_Object*)a)->cpp_object == ((Haiku_key_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_key_info_Object*)a)->cpp_object != ((Haiku_key_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_key_info_PyProperties[] = {
	{ (char*)"modifiers", (getter)Haiku_key_info_Object_getmodifiers, (setter)Haiku_key_info_Object_setmodifiers, (char*)"<DOC>", NULL},
	{ (char*)"key_states", (getter)Haiku_key_info_Object_getkey_states, (setter)Haiku_key_info_Object_setkey_states, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_key_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.key_info";
	type->tp_basicsize   = sizeof(Haiku_key_info_Object);
	type->tp_dealloc     = (destructor)Haiku_key_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_key_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_key_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_key_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

