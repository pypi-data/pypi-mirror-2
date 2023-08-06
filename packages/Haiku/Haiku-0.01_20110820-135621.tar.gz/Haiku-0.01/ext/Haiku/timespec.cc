/*
 * Automatically generated file
 */

static PyObject* Haiku_timespec_Object_gettv_sec(Haiku_timespec_Object* python_self, void* python_closure) {
	PyObject* py_tv_sec; // from generate()
	py_tv_sec = Py_BuildValue("l", python_self->cpp_object->tv_sec);
	return py_tv_sec;
}

static int Haiku_timespec_Object_settv_sec(Haiku_timespec_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->tv_sec = (time_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_timespec_Object_gettv_nsec(Haiku_timespec_Object* python_self, void* python_closure) {
	PyObject* py_tv_nsec; // from generate()
	py_tv_nsec = Py_BuildValue("l", python_self->cpp_object->tv_nsec);
	return py_tv_nsec;
}

static int Haiku_timespec_Object_settv_nsec(Haiku_timespec_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->tv_nsec = (long)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_timespec_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_timespec_Object*)a)->cpp_object == ((Haiku_timespec_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_timespec_Object*)a)->cpp_object != ((Haiku_timespec_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_timespec_PyProperties[] = {
	{ (char*)"tv_sec", (getter)Haiku_timespec_Object_gettv_sec, (setter)Haiku_timespec_Object_settv_sec, (char*)"<DOC>", NULL},
	{ (char*)"tv_nsec", (getter)Haiku_timespec_Object_gettv_nsec, (setter)Haiku_timespec_Object_settv_nsec, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_timespec_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.timespec";
	type->tp_basicsize   = sizeof(Haiku_timespec_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_timespec_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_timespec_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

