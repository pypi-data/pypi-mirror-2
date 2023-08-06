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
//static int Haiku_Shape_init(Haiku_Shape_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Shape_init(Haiku_Shape_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BShape();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Shape_newFromShape(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Shape_newFromShape(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Shape_Object* python_self;
	BShape other;
	Haiku_Shape_Object* py_other; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Shape_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_other);
	if (py_other != NULL) {
		memcpy((void*)&other, (void*)((Haiku_Shape_Object*)py_other)->cpp_object, sizeof(BShape));
	}
	
	python_self->cpp_object = new BShape(other);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Shape_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Shape_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Shape_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Shape_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BShape(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Shape_DESTROY(Haiku_Shape_Object* python_self);
static void Haiku_Shape_DESTROY(Haiku_Shape_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Shape_Instantiate(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_Instantiate(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	BArchivable* retval;
	Haiku_Archivable_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->Instantiate(data);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Archivable_Object*)Haiku_Archivable_PyType.tp_alloc(&Haiku_Archivable_PyType, 0);
	py_retval->cpp_object = (BArchivable*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Shape_Archive(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_Archive(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BMessage* data;
	bool deep = true;
	PyObject* py_deep; // from generate_py ()
	status_t retval;
	Haiku_Message_Object* py_data; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_deep);
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->Archive(data, deep);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_data->cpp_object = (BMessage*)data;
	// we own this object, so we can delete it
	py_data->can_delete_cpp_object = true;
	return (PyObject*)py_data;
}

//static PyObject* Haiku_Shape_Clear(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_Clear(Haiku_Shape_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Clear();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_Bounds(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_Bounds(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Bounds();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Shape_CurrentPosition(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_CurrentPosition(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->CurrentPosition();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Shape_AddShape(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_AddShape(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BShape* other;
	Haiku_Shape_Object* py_other; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_other);
	if (py_other != NULL) {
		other = ((Haiku_Shape_Object*)py_other)->cpp_object;
	}
	
	retval = python_self->cpp_object->AddShape(other);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_MoveTo(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_MoveTo(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->MoveTo(point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_LineTo(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_LineTo(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BPoint linePoint;
	Haiku_Point_Object* py_linePoint; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_linePoint);
	if (py_linePoint != NULL) {
		memcpy((void*)&linePoint, (void*)((Haiku_Point_Object*)py_linePoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->LineTo(linePoint);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_BezierTo(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_BezierTo(Haiku_Shape_Object* python_self, PyObject* python_args) {
	BPoint* controlPoints;
	PyObject* py_controlPoints; // from generate_py ()
	PyObject* py_controlPoints_element;	// from array_arg_parser()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_controlPoints);
	for (int i = 0; i < 3; i++) {
		py_controlPoints_element = PyList_GetItem(py_controlPoints, i);
		if (py_controlPoints_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_controlPoints_element != NULL) { // element code
			memcpy((void*)&controlPoints[i], (void*)((Haiku_Point_Object*)py_controlPoints_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	retval = python_self->cpp_object->BezierTo(controlPoints);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_BezierToPoints(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_BezierToPoints(Haiku_Shape_Object* python_self, PyObject* python_args) {
	const BPoint control1;
	Haiku_Point_Object* py_control1; // from generate_py()
	const BPoint control2;
	Haiku_Point_Object* py_control2; // from generate_py()
	const BPoint endPoint;
	Haiku_Point_Object* py_endPoint; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OOO", &py_control1, &py_control2, &py_endPoint);
	if (py_control1 != NULL) {
		memcpy((void*)&control1, (void*)((Haiku_Point_Object*)py_control1)->cpp_object, sizeof(const BPoint));
	}
	if (py_control2 != NULL) {
		memcpy((void*)&control2, (void*)((Haiku_Point_Object*)py_control2)->cpp_object, sizeof(const BPoint));
	}
	if (py_endPoint != NULL) {
		memcpy((void*)&endPoint, (void*)((Haiku_Point_Object*)py_endPoint)->cpp_object, sizeof(const BPoint));
	}
	
	retval = python_self->cpp_object->BezierTo(control1, control2, endPoint);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_ArcTo(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_ArcTo(Haiku_Shape_Object* python_self, PyObject* python_args) {
	float rx;
	float ry;
	float angle;
	bool largeArc;
	PyObject* py_largeArc; // from generate_py ()
	bool counterClockWise;
	PyObject* py_counterClockWise; // from generate_py ()
	const BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "fffOOO", &rx, &ry, &angle, &py_largeArc, &py_counterClockWise, &py_point);
	largeArc = (bool)(PyObject_IsTrue(py_largeArc));
	counterClockWise = (bool)(PyObject_IsTrue(py_counterClockWise));
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(const BPoint));
	}
	
	retval = python_self->cpp_object->ArcTo(rx, ry, angle, largeArc, counterClockWise, point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Shape_Close(Haiku_Shape_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Shape_Close(Haiku_Shape_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Close();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_Shape_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Shape_Object*)a)->cpp_object == *((Haiku_Shape_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Shape_Object*)a)->cpp_object != *((Haiku_Shape_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Shape_PyMethods[] = {
	{"FromShape", (PyCFunction)Haiku_Shape_newFromShape, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Shape_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Shape_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Shape_Archive, METH_VARARGS, ""},
	{"Clear", (PyCFunction)Haiku_Shape_Clear, METH_VARARGS, ""},
	{"Bounds", (PyCFunction)Haiku_Shape_Bounds, METH_VARARGS, ""},
	{"CurrentPosition", (PyCFunction)Haiku_Shape_CurrentPosition, METH_VARARGS, ""},
	{"AddShape", (PyCFunction)Haiku_Shape_AddShape, METH_VARARGS, ""},
	{"MoveTo", (PyCFunction)Haiku_Shape_MoveTo, METH_VARARGS, ""},
	{"LineTo", (PyCFunction)Haiku_Shape_LineTo, METH_VARARGS, ""},
	{"BezierTo", (PyCFunction)Haiku_Shape_BezierTo, METH_VARARGS, ""},
	{"BezierToPoints", (PyCFunction)Haiku_Shape_BezierToPoints, METH_VARARGS, ""},
	{"ArcTo", (PyCFunction)Haiku_Shape_ArcTo, METH_VARARGS, ""},
	{"Close", (PyCFunction)Haiku_Shape_Close, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Shape_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Shape";
	type->tp_basicsize   = sizeof(Haiku_Shape_Object);
	type->tp_dealloc     = (destructor)Haiku_Shape_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Shape_RichCompare;
	type->tp_methods     = Haiku_Shape_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)Haiku_Shape_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

