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
//static int Haiku_color_map_init(Haiku_color_map_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_color_map_init(Haiku_color_map_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new color_map();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_color_map_DESTROY(Haiku_color_map_Object* python_self);
static void Haiku_color_map_DESTROY(Haiku_color_map_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_color_map_Object_getid(Haiku_color_map_Object* python_self, void* python_closure) {
	PyObject* py_id; // from generate()
	py_id = Py_BuildValue("l", python_self->cpp_object->id);
	return py_id;
}

static int Haiku_color_map_Object_setid(Haiku_color_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->id = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_color_map_Object_getcolor_list(Haiku_color_map_Object* python_self, void* python_closure) {
	PyObject* py_color_list; // from generate()
	Haiku_rgb_color_Object* py_color_list_element;	// from array_arg_builder
	py_color_list = PyList_New(0);
	for (int i = 0; i < 256; i++) {
		py_color_list_element = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
		py_color_list_element->cpp_object = (rgb_color*)&python_self->cpp_object->color_list[i];
		// cannot delete this object; we do not own it
		py_color_list_element->can_delete_cpp_object = false;
		PyList_Append(py_color_list, (PyObject*)py_color_list_element);
	}
	return py_color_list;
}

static int Haiku_color_map_Object_setcolor_list(Haiku_color_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 256; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (value_element != NULL) { // element code
			memcpy((void*)&python_self->cpp_object->color_list[i], (void*)((Haiku_rgb_color_Object*)value_element)->cpp_object, sizeof(rgb_color)); // element code
		} // element code
	}
	return 0;
}

static PyObject* Haiku_color_map_Object_getinversion_map(Haiku_color_map_Object* python_self, void* python_closure) {
	PyObject* py_inversion_map; // from generate()
	PyObject* py_inversion_map_element;	// from array_arg_builder
	py_inversion_map = PyList_New(0);
	for (int i = 0; i < 256; i++) {
		py_inversion_map_element = Py_BuildValue("B", python_self->cpp_object->inversion_map[i]);
		PyList_Append(py_inversion_map, py_inversion_map_element);
	}
	return py_inversion_map;
}

static int Haiku_color_map_Object_setinversion_map(Haiku_color_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 256; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->inversion_map[i] = (uint8)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_color_map_Object_getindex_map(Haiku_color_map_Object* python_self, void* python_closure) {
	PyObject* py_index_map; // from generate()
	PyObject* py_index_map_element;	// from array_arg_builder
	py_index_map = PyList_New(0);
	for (int i = 0; i < 32768; i++) {
		py_index_map_element = Py_BuildValue("B", python_self->cpp_object->index_map[i]);
		PyList_Append(py_index_map, py_index_map_element);
	}
	return py_index_map;
}

static int Haiku_color_map_Object_setindex_map(Haiku_color_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32768; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->index_map[i] = (uint8)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_color_map_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_color_map_Object*)a)->cpp_object == ((Haiku_color_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_color_map_Object*)a)->cpp_object != ((Haiku_color_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_color_map_PyProperties[] = {
	{ (char*)"id", (getter)Haiku_color_map_Object_getid, (setter)Haiku_color_map_Object_setid, (char*)"<DOC>", NULL},
	{ (char*)"color_list", (getter)Haiku_color_map_Object_getcolor_list, (setter)Haiku_color_map_Object_setcolor_list, (char*)"<DOC>", NULL},
	{ (char*)"inversion_map", (getter)Haiku_color_map_Object_getinversion_map, (setter)Haiku_color_map_Object_setinversion_map, (char*)"<DOC>", NULL},
	{ (char*)"index_map", (getter)Haiku_color_map_Object_getindex_map, (setter)Haiku_color_map_Object_setindex_map, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_color_map_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.color_map";
	type->tp_basicsize   = sizeof(Haiku_color_map_Object);
	type->tp_dealloc     = (destructor)Haiku_color_map_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_color_map_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_color_map_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_color_map_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

