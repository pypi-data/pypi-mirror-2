/*
 * Automatically generated file
 */

static PyObject* Haiku_stat_beos_time_Object_gettv_sec(Haiku_stat_beos_time_Object* python_self, void* python_closure) {
	PyObject* py_tv_sec; // from generate()
	py_tv_sec = Py_BuildValue("l", python_self->cpp_object->tv_sec);
	return py_tv_sec;
}

static int Haiku_stat_beos_time_Object_settv_sec(Haiku_stat_beos_time_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->tv_sec = (time_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_beos_time_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_stat_beos_time_Object*)a)->cpp_object == ((Haiku_stat_beos_time_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_stat_beos_time_Object*)a)->cpp_object != ((Haiku_stat_beos_time_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_stat_beos_time_PyProperties[] = {
	{ (char*)"tv_sec", (getter)Haiku_stat_beos_time_Object_gettv_sec, (setter)Haiku_stat_beos_time_Object_settv_sec, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_stat_beos_time_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.stat_beos_time";
	type->tp_basicsize   = sizeof(Haiku_stat_beos_time_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_stat_beos_time_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_stat_beos_time_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

