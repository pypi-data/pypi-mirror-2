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
//static int Haiku_ShapeIterator_init(Haiku_ShapeIterator_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_ShapeIterator_init(Haiku_ShapeIterator_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BShapeIterator();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_ShapeIterator_DESTROY(Haiku_ShapeIterator_Object* python_self);
static void Haiku_ShapeIterator_DESTROY(Haiku_ShapeIterator_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_ShapeIterator_IterateMoveTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ShapeIterator_IterateMoveTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args) {
	BPoint* point;
	Haiku_Point_Object* py_point; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		point = ((Haiku_Point_Object*)py_point)->cpp_object;
	}
	
	retval = python_self->cpp_object->IterateMoveTo(point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ShapeIterator_IterateLineTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ShapeIterator_IterateLineTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args) {
	int32 lineCount;
	BPoint* linePts;
	PyObject* py_linePts; // from generate_py ()
	PyObject* py_linePts_element;	// from array_arg_parser()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_linePts);
	lineCount = PyList_Size(py_linePts);
	for (int i = 0; i < lineCount; i++) {
		py_linePts_element = PyList_GetItem(py_linePts, i);
		if (py_linePts_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_linePts_element != NULL) { // element code
			memcpy((void*)&linePts[i], (void*)((Haiku_Point_Object*)py_linePts_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	retval = python_self->cpp_object->IterateLineTo(lineCount, linePts);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ShapeIterator_IterateBezierTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ShapeIterator_IterateBezierTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args) {
	int32 bezierCount;
	BPoint* bezierPts;
	PyObject* py_bezierPts; // from generate_py ()
	PyObject* py_bezierPts_element;	// from array_arg_parser()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_bezierPts);
	bezierCount = PyList_Size(py_bezierPts);
	for (int i = 0; i < bezierCount; i++) {
		py_bezierPts_element = PyList_GetItem(py_bezierPts, i);
		if (py_bezierPts_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_bezierPts_element != NULL) { // element code
			memcpy((void*)&bezierPts[i], (void*)((Haiku_Point_Object*)py_bezierPts_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	retval = python_self->cpp_object->IterateBezierTo(bezierCount, bezierPts);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ShapeIterator_IterateClose(Haiku_ShapeIterator_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ShapeIterator_IterateClose(Haiku_ShapeIterator_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->IterateClose();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ShapeIterator_IterateArcTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ShapeIterator_IterateArcTo(Haiku_ShapeIterator_Object* python_self, PyObject* python_args) {
	float rx;
	float ry;
	float angle;
	bool largeArc;
	PyObject* py_largeArc; // from generate_py ()
	bool counterClockWise;
	PyObject* py_counterClockWise; // from generate_py ()
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "fffOOO", &rx, &ry, &angle, &py_largeArc, &py_counterClockWise, &py_point);
	largeArc = (bool)(PyObject_IsTrue(py_largeArc));
	counterClockWise = (bool)(PyObject_IsTrue(py_counterClockWise));
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->IterateArcTo(rx, ry, angle, largeArc, counterClockWise, point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_ShapeIterator_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ShapeIterator_Object*)a)->cpp_object == ((Haiku_ShapeIterator_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ShapeIterator_Object*)a)->cpp_object != ((Haiku_ShapeIterator_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ShapeIterator_PyMethods[] = {
	{"IterateMoveTo", (PyCFunction)Haiku_ShapeIterator_IterateMoveTo, METH_VARARGS, ""},
	{"IterateLineTo", (PyCFunction)Haiku_ShapeIterator_IterateLineTo, METH_VARARGS, ""},
	{"IterateBezierTo", (PyCFunction)Haiku_ShapeIterator_IterateBezierTo, METH_VARARGS, ""},
	{"IterateClose", (PyCFunction)Haiku_ShapeIterator_IterateClose, METH_VARARGS, ""},
	{"IterateArcTo", (PyCFunction)Haiku_ShapeIterator_IterateArcTo, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ShapeIterator_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ShapeIterator";
	type->tp_basicsize   = sizeof(Haiku_ShapeIterator_Object);
	type->tp_dealloc     = (destructor)Haiku_ShapeIterator_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ShapeIterator_RichCompare;
	type->tp_methods     = Haiku_ShapeIterator_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_ShapeIterator_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

