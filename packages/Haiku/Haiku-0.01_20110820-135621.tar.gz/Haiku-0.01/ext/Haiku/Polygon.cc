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
//static int Haiku_Polygon_init(Haiku_Polygon_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Polygon_init(Haiku_Polygon_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BPoint* points;
	PyObject* py_points; // from generate_py ()
	PyObject* py_points_element;	// from array_arg_parser()
	int32 count;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "O", &py_points);
	count = PyList_Size(py_points);
	for (int i = 0; i < count; i++) {
		py_points_element = PyList_GetItem(py_points, i);
		if (py_points_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_points_element != NULL) { // element code
			memcpy((void*)&points[i], (void*)((Haiku_Point_Object*)py_points_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	python_self->cpp_object = new BPolygon(points, count);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Polygon_newFromPolygon(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Polygon_newFromPolygon(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Polygon_Object* python_self;
	BPolygon other;
	Haiku_Polygon_Object* py_other; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Polygon_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_other);
	if (py_other != NULL) {
		memcpy((void*)&other, (void*)((Haiku_Polygon_Object*)py_other)->cpp_object, sizeof(BPolygon));
	}
	
	python_self->cpp_object = new BPolygon(other);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Polygon_DESTROY(Haiku_Polygon_Object* python_self);
static void Haiku_Polygon_DESTROY(Haiku_Polygon_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Polygon_Frame(Haiku_Polygon_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Polygon_Frame(Haiku_Polygon_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Frame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Polygon_AddPoints(Haiku_Polygon_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Polygon_AddPoints(Haiku_Polygon_Object* python_self, PyObject* python_args) {
	BPoint* points;
	PyObject* py_points; // from generate_py ()
	PyObject* py_points_element;	// from array_arg_parser()
	int32 count;
	
	PyArg_ParseTuple(python_args, "O", &py_points);
	count = PyList_Size(py_points);
	for (int i = 0; i < count; i++) {
		py_points_element = PyList_GetItem(py_points, i);
		if (py_points_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_points_element != NULL) { // element code
			memcpy((void*)&points[i], (void*)((Haiku_Point_Object*)py_points_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	python_self->cpp_object->AddPoints(points, count);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Polygon_CountPoints(Haiku_Polygon_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Polygon_CountPoints(Haiku_Polygon_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountPoints();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Polygon_MapTo(Haiku_Polygon_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Polygon_MapTo(Haiku_Polygon_Object* python_self, PyObject* python_args) {
	BRect srcRect;
	Haiku_Rect_Object* py_srcRect; // from generate_py()
	BRect dstRect;
	Haiku_Rect_Object* py_dstRect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_srcRect, &py_dstRect);
	if (py_srcRect != NULL) {
		memcpy((void*)&srcRect, (void*)((Haiku_Rect_Object*)py_srcRect)->cpp_object, sizeof(BRect));
	}
	if (py_dstRect != NULL) {
		memcpy((void*)&dstRect, (void*)((Haiku_Rect_Object*)py_dstRect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->MapTo(srcRect, dstRect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Polygon_PrintToStream(Haiku_Polygon_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Polygon_PrintToStream(Haiku_Polygon_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PrintToStream();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Polygon_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Polygon_Object*)a)->cpp_object == ((Haiku_Polygon_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Polygon_Object*)a)->cpp_object != ((Haiku_Polygon_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Polygon_PyMethods[] = {
	{"FromPolygon", (PyCFunction)Haiku_Polygon_newFromPolygon, METH_VARARGS|METH_CLASS, ""},
	{"Frame", (PyCFunction)Haiku_Polygon_Frame, METH_VARARGS, ""},
	{"AddPoints", (PyCFunction)Haiku_Polygon_AddPoints, METH_VARARGS, ""},
	{"CountPoints", (PyCFunction)Haiku_Polygon_CountPoints, METH_VARARGS, ""},
	{"MapTo", (PyCFunction)Haiku_Polygon_MapTo, METH_VARARGS, ""},
	{"PrintToStream", (PyCFunction)Haiku_Polygon_PrintToStream, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Polygon_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Polygon";
	type->tp_basicsize   = sizeof(Haiku_Polygon_Object);
	type->tp_dealloc     = (destructor)Haiku_Polygon_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Polygon_RichCompare;
	type->tp_methods     = Haiku_Polygon_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)Haiku_Polygon_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

