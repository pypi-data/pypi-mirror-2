/*
 * Automatically generated file
 */

static PyObject* Haiku_EntryList_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_EntryList_Object*)a)->cpp_object == ((Haiku_EntryList_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_EntryList_Object*)a)->cpp_object != ((Haiku_EntryList_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static void init_Haiku_EntryList_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.EntryList";
	type->tp_basicsize   = sizeof(Haiku_EntryList_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_EntryList_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

