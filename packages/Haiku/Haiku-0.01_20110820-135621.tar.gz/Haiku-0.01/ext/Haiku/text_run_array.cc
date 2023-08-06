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
//static int Haiku_text_run_array_init(Haiku_text_run_array_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_text_run_array_init(Haiku_text_run_array_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new text_run_array();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_text_run_array_DESTROY(Haiku_text_run_array_Object* python_self);
static void Haiku_text_run_array_DESTROY(Haiku_text_run_array_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_text_run_array_Object_getcount(Haiku_text_run_array_Object* python_self, void* python_closure) {
	PyObject* py_count; // from generate()
	py_count = Py_BuildValue("l", python_self->cpp_object->count);
	return py_count;
}

static int Haiku_text_run_array_Object_setcount(Haiku_text_run_array_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->count = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_text_run_array_Object_getruns(Haiku_text_run_array_Object* python_self, void* python_closure) {
	PyObject* py_runs; // from generate()
	Haiku_text_run_Object* py_runs_element;	// from array_arg_builder
	py_runs = PyList_New(0);
	for (int i = 0; i < python_self->cpp_object->count; i++) {
		py_runs_element = (Haiku_text_run_Object*)Haiku_text_run_PyType.tp_alloc(&Haiku_text_run_PyType, 0);
		py_runs_element->cpp_object = (text_run*)&python_self->cpp_object->runs[i];
		// cannot delete this object; we do not own it
		py_runs_element->can_delete_cpp_object = false;
		PyList_Append(py_runs, (PyObject*)py_runs_element);
	}
	return py_runs;
}

static int Haiku_text_run_array_Object_setruns(Haiku_text_run_array_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < python_self->cpp_object->count; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (value_element != NULL) { // element code
			memcpy((void*)&python_self->cpp_object->runs[i], (void*)((Haiku_text_run_Object*)value_element)->cpp_object, sizeof(text_run)); // element code
		} // element code
	}
	return 0;
}

static PyObject* Haiku_text_run_array_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_text_run_array_Object*)a)->cpp_object == ((Haiku_text_run_array_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_text_run_array_Object*)a)->cpp_object != ((Haiku_text_run_array_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_text_run_array_PyProperties[] = {
	{ (char*)"count", (getter)Haiku_text_run_array_Object_getcount, (setter)Haiku_text_run_array_Object_setcount, (char*)"<DOC>", NULL},
	{ (char*)"runs", (getter)Haiku_text_run_array_Object_getruns, (setter)Haiku_text_run_array_Object_setruns, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_text_run_array_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.text_run_array";
	type->tp_basicsize   = sizeof(Haiku_text_run_array_Object);
	type->tp_dealloc     = (destructor)Haiku_text_run_array_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_text_run_array_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_text_run_array_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_text_run_array_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

