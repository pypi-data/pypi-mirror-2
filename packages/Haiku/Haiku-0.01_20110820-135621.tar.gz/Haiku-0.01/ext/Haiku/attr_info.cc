/*
 * Automatically generated file
 */

static PyObject* Haiku_attr_info_Object_gettype(Haiku_attr_info_Object* python_self, void* python_closure) {
	PyObject* py_type; // from generate()
	py_type = Py_BuildValue("k", python_self->cpp_object->type);
	return py_type;
}

static int Haiku_attr_info_Object_settype(Haiku_attr_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->type = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_attr_info_Object_getsize(Haiku_attr_info_Object* python_self, void* python_closure) {
	PyObject* py_size; // from generate()
	py_size = Py_BuildValue("l", python_self->cpp_object->size);
	return py_size;
}

static int Haiku_attr_info_Object_setsize(Haiku_attr_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->size = (off_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_attr_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_attr_info_Object*)a)->cpp_object == ((Haiku_attr_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_attr_info_Object*)a)->cpp_object != ((Haiku_attr_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_attr_info_PyProperties[] = {
	{ (char*)"type", (getter)Haiku_attr_info_Object_gettype, (setter)Haiku_attr_info_Object_settype, (char*)"<DOC>", NULL},
	{ (char*)"size", (getter)Haiku_attr_info_Object_getsize, (setter)Haiku_attr_info_Object_setsize, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_attr_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.attr_info";
	type->tp_basicsize   = sizeof(Haiku_attr_info_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_attr_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_attr_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

