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
//static int Haiku_font_cache_info_init(Haiku_font_cache_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_font_cache_info_init(Haiku_font_cache_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new font_cache_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_font_cache_info_DESTROY(Haiku_font_cache_info_Object* python_self);
static void Haiku_font_cache_info_DESTROY(Haiku_font_cache_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_font_cache_info_Object_getsheared_font_penalty(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_sheared_font_penalty; // from generate()
	py_sheared_font_penalty = Py_BuildValue("l", python_self->cpp_object->sheared_font_penalty);
	return py_sheared_font_penalty;
}

static int Haiku_font_cache_info_Object_setsheared_font_penalty(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->sheared_font_penalty = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_Object_getrotated_font_penalty(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_rotated_font_penalty; // from generate()
	py_rotated_font_penalty = Py_BuildValue("l", python_self->cpp_object->rotated_font_penalty);
	return py_rotated_font_penalty;
}

static int Haiku_font_cache_info_Object_setrotated_font_penalty(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->rotated_font_penalty = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_Object_getoversize_threshold(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_oversize_threshold; // from generate()
	py_oversize_threshold = Py_BuildValue("f", python_self->cpp_object->oversize_threshold);
	return py_oversize_threshold;
}

static int Haiku_font_cache_info_Object_setoversize_threshold(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->oversize_threshold = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_Object_getoversize_penalty(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_oversize_penalty; // from generate()
	py_oversize_penalty = Py_BuildValue("l", python_self->cpp_object->oversize_penalty);
	return py_oversize_penalty;
}

static int Haiku_font_cache_info_Object_setoversize_penalty(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->oversize_penalty = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_Object_getcache_size(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_cache_size; // from generate()
	py_cache_size = Py_BuildValue("l", python_self->cpp_object->cache_size);
	return py_cache_size;
}

static int Haiku_font_cache_info_Object_setcache_size(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->cache_size = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_Object_getspacing_size_threshold(Haiku_font_cache_info_Object* python_self, void* python_closure) {
	PyObject* py_spacing_size_threshold; // from generate()
	py_spacing_size_threshold = Py_BuildValue("f", python_self->cpp_object->spacing_size_threshold);
	return py_spacing_size_threshold;
}

static int Haiku_font_cache_info_Object_setspacing_size_threshold(Haiku_font_cache_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->spacing_size_threshold = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_font_cache_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_font_cache_info_Object*)a)->cpp_object == ((Haiku_font_cache_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_font_cache_info_Object*)a)->cpp_object != ((Haiku_font_cache_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_font_cache_info_PyProperties[] = {
	{ (char*)"sheared_font_penalty", (getter)Haiku_font_cache_info_Object_getsheared_font_penalty, (setter)Haiku_font_cache_info_Object_setsheared_font_penalty, (char*)"<DOC>", NULL},
	{ (char*)"rotated_font_penalty", (getter)Haiku_font_cache_info_Object_getrotated_font_penalty, (setter)Haiku_font_cache_info_Object_setrotated_font_penalty, (char*)"<DOC>", NULL},
	{ (char*)"oversize_threshold", (getter)Haiku_font_cache_info_Object_getoversize_threshold, (setter)Haiku_font_cache_info_Object_setoversize_threshold, (char*)"<DOC>", NULL},
	{ (char*)"oversize_penalty", (getter)Haiku_font_cache_info_Object_getoversize_penalty, (setter)Haiku_font_cache_info_Object_setoversize_penalty, (char*)"<DOC>", NULL},
	{ (char*)"cache_size", (getter)Haiku_font_cache_info_Object_getcache_size, (setter)Haiku_font_cache_info_Object_setcache_size, (char*)"<DOC>", NULL},
	{ (char*)"spacing_size_threshold", (getter)Haiku_font_cache_info_Object_getspacing_size_threshold, (setter)Haiku_font_cache_info_Object_setspacing_size_threshold, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_font_cache_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.font_cache_info";
	type->tp_basicsize   = sizeof(Haiku_font_cache_info_Object);
	type->tp_dealloc     = (destructor)Haiku_font_cache_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_font_cache_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_font_cache_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_font_cache_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

