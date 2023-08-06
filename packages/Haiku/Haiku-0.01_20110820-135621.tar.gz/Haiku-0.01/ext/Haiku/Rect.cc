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
//static int Haiku_Rect_init(Haiku_Rect_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Rect_init(Haiku_Rect_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	float left;
	float top;
	float right;
	float bottom;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "ffff", &left, &top, &right, &bottom);
	
	python_self->cpp_object = new BRect(left, top, right, bottom);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Rect_newFromRect(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Rect_newFromRect(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Rect_Object* python_self;
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Rect_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BRect(rect);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Rect_newFromPoints(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Rect_newFromPoints(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Rect_Object* python_self;
	BPoint leftTop;
	Haiku_Point_Object* py_leftTop; // from generate_py()
	BPoint rightBottom;
	Haiku_Point_Object* py_rightBottom; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Rect_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "OO", &py_leftTop, &py_rightBottom);
	if (py_leftTop != NULL) {
		memcpy((void*)&leftTop, (void*)((Haiku_Point_Object*)py_leftTop)->cpp_object, sizeof(BPoint));
	}
	if (py_rightBottom != NULL) {
		memcpy((void*)&rightBottom, (void*)((Haiku_Point_Object*)py_rightBottom)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object = new BRect(leftTop, rightBottom);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Rect_newFromSide(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Rect_newFromSide(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Rect_Object* python_self;
	float side;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Rect_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "f", &side);
	
	python_self->cpp_object = new BRect(side);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Rect_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Rect_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Rect_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Rect_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BRect();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Rect_DESTROY(Haiku_Rect_Object* python_self);
static void Haiku_Rect_DESTROY(Haiku_Rect_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Rect_Set(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_Set(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float left;
	float top;
	float right;
	float bottom;
	
	PyArg_ParseTuple(python_args, "ffff", &left, &top, &right, &bottom);
	
	python_self->cpp_object->Set(left, top, right, bottom);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_PrintToStream(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_PrintToStream(Haiku_Rect_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PrintToStream();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_LeftTop(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_LeftTop(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LeftTop();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_RightBottom(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_RightBottom(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->RightBottom();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_LeftBottom(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_LeftBottom(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LeftBottom();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_RightTop(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_RightTop(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->RightTop();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_SetLeftTop(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_SetLeftTop(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint leftTop;
	Haiku_Point_Object* py_leftTop; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_leftTop);
	if (py_leftTop != NULL) {
		memcpy((void*)&leftTop, (void*)((Haiku_Point_Object*)py_leftTop)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->SetLeftTop(leftTop);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_SetRightBottom(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_SetRightBottom(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint rightBottom;
	Haiku_Point_Object* py_rightBottom; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rightBottom);
	if (py_rightBottom != NULL) {
		memcpy((void*)&rightBottom, (void*)((Haiku_Point_Object*)py_rightBottom)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->SetRightBottom(rightBottom);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_SetLeftBottom(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_SetLeftBottom(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint leftBottom;
	Haiku_Point_Object* py_leftBottom; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_leftBottom);
	if (py_leftBottom != NULL) {
		memcpy((void*)&leftBottom, (void*)((Haiku_Point_Object*)py_leftBottom)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->SetLeftBottom(leftBottom);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_SetRightTop(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_SetRightTop(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint rightTop;
	Haiku_Point_Object* py_rightTop; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rightTop);
	if (py_rightTop != NULL) {
		memcpy((void*)&rightTop, (void*)((Haiku_Point_Object*)py_rightTop)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->SetRightTop(rightTop);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_InsetByPoint(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetByPoint(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint inset;
	Haiku_Point_Object* py_inset; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_inset);
	if (py_inset != NULL) {
		memcpy((void*)&inset, (void*)((Haiku_Point_Object*)py_inset)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->InsetBy(inset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_InsetBy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetBy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->InsetBy(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_OffsetByPoint(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetByPoint(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint delta;
	Haiku_Point_Object* py_delta; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_delta);
	if (py_delta != NULL) {
		memcpy((void*)&delta, (void*)((Haiku_Point_Object*)py_delta)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->OffsetBy(delta);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_OffsetBy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetBy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->OffsetBy(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_OffsetToPoint(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetToPoint(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint offset;
	Haiku_Point_Object* py_offset; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_offset);
	if (py_offset != NULL) {
		memcpy((void*)&offset, (void*)((Haiku_Point_Object*)py_offset)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->OffsetTo(offset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_OffsetTo(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetTo(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->OffsetTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Rect_InsetByPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetByPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint inset;
	Haiku_Point_Object* py_inset; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_inset);
	if (py_inset != NULL) {
		memcpy((void*)&inset, (void*)((Haiku_Point_Object*)py_inset)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->InsetBySelf(inset);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_InsetBySelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetBySelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->InsetBySelf(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetByPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetByPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint delta;
	Haiku_Point_Object* py_delta; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_delta);
	if (py_delta != NULL) {
		memcpy((void*)&delta, (void*)((Haiku_Point_Object*)py_delta)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->OffsetBySelf(delta);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetBySelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetBySelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->OffsetBySelf(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetToPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetToPointSelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint offset;
	Haiku_Point_Object* py_offset; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_offset);
	if (py_offset != NULL) {
		memcpy((void*)&offset, (void*)((Haiku_Point_Object*)py_offset)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->OffsetToSelf(offset);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetToSelf(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetToSelf(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->OffsetToSelf(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_InsetByPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetByPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint inset;
	Haiku_Point_Object* py_inset; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_inset);
	if (py_inset != NULL) {
		memcpy((void*)&inset, (void*)((Haiku_Point_Object*)py_inset)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->InsetByCopy(inset);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_InsetByCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_InsetByCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->InsetByCopy(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetByPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetByPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint delta;
	Haiku_Point_Object* py_delta; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_delta);
	if (py_delta != NULL) {
		memcpy((void*)&delta, (void*)((Haiku_Point_Object*)py_delta)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->OffsetByCopy(delta);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetByCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetByCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->OffsetByCopy(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetToPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetToPointCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint offset;
	Haiku_Point_Object* py_offset; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_offset);
	if (py_offset != NULL) {
		memcpy((void*)&offset, (void*)((Haiku_Point_Object*)py_offset)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->OffsetToCopy(offset);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_OffsetToCopy(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_OffsetToCopy(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	retval = python_self->cpp_object->OffsetToCopy(x, y);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Rect_IsValid(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_IsValid(Haiku_Rect_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsValid();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Rect_Width(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_Width(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Width();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Rect_IntegerWidth(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_IntegerWidth(Haiku_Rect_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IntegerWidth();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Rect_Height(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_Height(Haiku_Rect_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Height();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Rect_IntegerHeight(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_IntegerHeight(Haiku_Rect_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IntegerHeight();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Rect_Intersects(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_Intersects(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->Intersects(rect);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Rect_Contains(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_Contains(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BPoint rect;
	Haiku_Point_Object* py_rect; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Point_Object*)py_rect)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->Contains(rect);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Rect_ContainsRect(Haiku_Rect_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Rect_ContainsRect(Haiku_Rect_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->Contains(rect);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_Rect_Object_getleft(Haiku_Rect_Object* python_self, void* python_closure) {
	PyObject* py_left; // from generate()
	py_left = Py_BuildValue("f", python_self->cpp_object->left);
	return py_left;
}

static int Haiku_Rect_Object_setleft(Haiku_Rect_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Rect_Object_gettop(Haiku_Rect_Object* python_self, void* python_closure) {
	PyObject* py_top; // from generate()
	py_top = Py_BuildValue("f", python_self->cpp_object->top);
	return py_top;
}

static int Haiku_Rect_Object_settop(Haiku_Rect_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->top = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Rect_Object_getright(Haiku_Rect_Object* python_self, void* python_closure) {
	PyObject* py_right; // from generate()
	py_right = Py_BuildValue("f", python_self->cpp_object->right);
	return py_right;
}

static int Haiku_Rect_Object_setright(Haiku_Rect_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Rect_Object_getbottom(Haiku_Rect_Object* python_self, void* python_closure) {
	PyObject* py_bottom; // from generate()
	py_bottom = Py_BuildValue("f", python_self->cpp_object->bottom);
	return py_bottom;
}

static int Haiku_Rect_Object_setbottom(Haiku_Rect_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->bottom = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Rect__and__(PyObject* a, PyObject* b) {
	BRect* retval = new BRect();
	Haiku_Rect_Object* py_retval;
	
	*retval = *((Haiku_Rect_Object*)a)->cpp_object & *((Haiku_Rect_Object*)b)->cpp_object;
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Rect__or__(PyObject* a, PyObject* b) {
	BRect* retval = new BRect();
	Haiku_Rect_Object* py_retval;
	
	*retval = *((Haiku_Rect_Object*)a)->cpp_object | *((Haiku_Rect_Object*)b)->cpp_object;
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Rect_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Rect_Object*)a)->cpp_object == *((Haiku_Rect_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Rect_Object*)a)->cpp_object != *((Haiku_Rect_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_Rect_PyProperties[] = {
	{ (char*)"left", (getter)Haiku_Rect_Object_getleft, (setter)Haiku_Rect_Object_setleft, (char*)"<DOC>", NULL},
	{ (char*)"top", (getter)Haiku_Rect_Object_gettop, (setter)Haiku_Rect_Object_settop, (char*)"<DOC>", NULL},
	{ (char*)"right", (getter)Haiku_Rect_Object_getright, (setter)Haiku_Rect_Object_setright, (char*)"<DOC>", NULL},
	{ (char*)"bottom", (getter)Haiku_Rect_Object_getbottom, (setter)Haiku_Rect_Object_setbottom, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static PyMethodDef Haiku_Rect_PyMethods[] = {
	{"FromRect", (PyCFunction)Haiku_Rect_newFromRect, METH_VARARGS|METH_CLASS, ""},
	{"FromPoints", (PyCFunction)Haiku_Rect_newFromPoints, METH_VARARGS|METH_CLASS, ""},
	{"FromSide", (PyCFunction)Haiku_Rect_newFromSide, METH_VARARGS|METH_CLASS, ""},
	{"Empty", (PyCFunction)Haiku_Rect_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"Set", (PyCFunction)Haiku_Rect_Set, METH_VARARGS, ""},
	{"PrintToStream", (PyCFunction)Haiku_Rect_PrintToStream, METH_VARARGS, ""},
	{"LeftTop", (PyCFunction)Haiku_Rect_LeftTop, METH_VARARGS, ""},
	{"RightBottom", (PyCFunction)Haiku_Rect_RightBottom, METH_VARARGS, ""},
	{"LeftBottom", (PyCFunction)Haiku_Rect_LeftBottom, METH_VARARGS, ""},
	{"RightTop", (PyCFunction)Haiku_Rect_RightTop, METH_VARARGS, ""},
	{"SetLeftTop", (PyCFunction)Haiku_Rect_SetLeftTop, METH_VARARGS, ""},
	{"SetRightBottom", (PyCFunction)Haiku_Rect_SetRightBottom, METH_VARARGS, ""},
	{"SetLeftBottom", (PyCFunction)Haiku_Rect_SetLeftBottom, METH_VARARGS, ""},
	{"SetRightTop", (PyCFunction)Haiku_Rect_SetRightTop, METH_VARARGS, ""},
	{"InsetByPoint", (PyCFunction)Haiku_Rect_InsetByPoint, METH_VARARGS, ""},
	{"InsetBy", (PyCFunction)Haiku_Rect_InsetBy, METH_VARARGS, ""},
	{"OffsetByPoint", (PyCFunction)Haiku_Rect_OffsetByPoint, METH_VARARGS, ""},
	{"OffsetBy", (PyCFunction)Haiku_Rect_OffsetBy, METH_VARARGS, ""},
	{"OffsetToPoint", (PyCFunction)Haiku_Rect_OffsetToPoint, METH_VARARGS, ""},
	{"OffsetTo", (PyCFunction)Haiku_Rect_OffsetTo, METH_VARARGS, ""},
	{"InsetByPointSelf", (PyCFunction)Haiku_Rect_InsetByPointSelf, METH_VARARGS, ""},
	{"InsetBySelf", (PyCFunction)Haiku_Rect_InsetBySelf, METH_VARARGS, ""},
	{"OffsetByPointSelf", (PyCFunction)Haiku_Rect_OffsetByPointSelf, METH_VARARGS, ""},
	{"OffsetBySelf", (PyCFunction)Haiku_Rect_OffsetBySelf, METH_VARARGS, ""},
	{"OffsetToPointSelf", (PyCFunction)Haiku_Rect_OffsetToPointSelf, METH_VARARGS, ""},
	{"OffsetToSelf", (PyCFunction)Haiku_Rect_OffsetToSelf, METH_VARARGS, ""},
	{"InsetByPointCopy", (PyCFunction)Haiku_Rect_InsetByPointCopy, METH_VARARGS, ""},
	{"InsetByCopy", (PyCFunction)Haiku_Rect_InsetByCopy, METH_VARARGS, ""},
	{"OffsetByPointCopy", (PyCFunction)Haiku_Rect_OffsetByPointCopy, METH_VARARGS, ""},
	{"OffsetByCopy", (PyCFunction)Haiku_Rect_OffsetByCopy, METH_VARARGS, ""},
	{"OffsetToPointCopy", (PyCFunction)Haiku_Rect_OffsetToPointCopy, METH_VARARGS, ""},
	{"OffsetToCopy", (PyCFunction)Haiku_Rect_OffsetToCopy, METH_VARARGS, ""},
	{"IsValid", (PyCFunction)Haiku_Rect_IsValid, METH_VARARGS, ""},
	{"Width", (PyCFunction)Haiku_Rect_Width, METH_VARARGS, ""},
	{"IntegerWidth", (PyCFunction)Haiku_Rect_IntegerWidth, METH_VARARGS, ""},
	{"Height", (PyCFunction)Haiku_Rect_Height, METH_VARARGS, ""},
	{"IntegerHeight", (PyCFunction)Haiku_Rect_IntegerHeight, METH_VARARGS, ""},
	{"Intersects", (PyCFunction)Haiku_Rect_Intersects, METH_VARARGS, ""},
	{"Contains", (PyCFunction)Haiku_Rect_Contains, METH_VARARGS, ""},
	{"ContainsRect", (PyCFunction)Haiku_Rect_ContainsRect, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static PyNumberMethods Haiku_Rect_AsNumber = {
	/* nb_add */	0,
	/* nb_subtract */	0,
	/* nb_multiply */	0,
	/* nb_divide */	0,
	/* nb_remainder */	0,
	/* nb_divmod */	0,
	/* nb_power */	0,
	/* nb_negative */	0,
	/* nb_positive */	0,
	/* nb_absolute */	0,
	/* nb_nonzero */	0,
	/* nb_invert */	0,
	/* nb_lshift */	0,
	/* nb_rshift */	0,
	/* nb_and */	Haiku_Rect__and__,
	/* nb_xor */	0,
	/* nb_or */	Haiku_Rect__or__,
	/* nb_coerce */	0,
	/* nb_int */	0,
	/* nb_long */	0,
	/* nb_float */	0,
	/* nb_oct */	0,
	/* nb_hex */	0,
	/* nb_inplace_add */	0,
	/* nb_inplace_subtract */	0,
	/* nb_inplace_multiply */	0,
	/* nb_inplace_divide */	0,
	/* nb_inplace_remainder */	0,
	/* nb_inplace_power */	0,
	/* nb_inplace_lshift */	0,
	/* nb_inplace_rshift */	0,
	/* nb_inplace_and */	0,
	/* nb_inplace_xor */	0,
	/* nb_inplace_or */	0,
	/* nb_floor_divide */	0,
	/* nb_true_divide */	0,
	/* nb_inplace_floor_divide */	0,
	/* nb_inplace_true_divide */	0,
	/* nb_index */	0
};

static void init_Haiku_Rect_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Rect";
	type->tp_basicsize   = sizeof(Haiku_Rect_Object);
	type->tp_dealloc     = (destructor)Haiku_Rect_DESTROY;
	type->tp_as_number   = &Haiku_Rect_AsNumber;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Rect_RichCompare;
	type->tp_methods     = Haiku_Rect_PyMethods;
	type->tp_getset      = Haiku_Rect_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Rect_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

