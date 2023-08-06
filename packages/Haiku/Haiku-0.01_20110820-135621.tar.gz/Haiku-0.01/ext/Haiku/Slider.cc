/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_SliderConstants_PyMethods[] = {
	{NULL} /* Sentinel */
};
/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Slider_init(Haiku_Slider_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Slider_init(Haiku_Slider_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 minValue;
	int32 maxValue;
	thumb_style thumbType = B_BLOCK_THUMB;
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_NAVIGABLE | B_WILL_DRAW | B_FRAME_EVENTS;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OssOll|ikk", &py_frame, &name, &label, &py_message, &minValue, &maxValue, &thumbType, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BSlider(frame, name, label, message, minValue, maxValue, thumbType, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Slider_newWithOrientation(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Slider_newWithOrientation(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Slider_Object* python_self;
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 minValue;
	int32 maxValue;
	orientation posture;
	thumb_style thumbType = B_BLOCK_THUMB;
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_NAVIGABLE | B_WILL_DRAW | B_FRAME_EVENTS;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Slider_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "OssOlli|ikk", &py_frame, &name, &label, &py_message, &minValue, &maxValue, &posture, &thumbType, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BSlider(frame, name, label, message, minValue, maxValue, posture, thumbType, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Slider_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Slider_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Slider_Object* python_self;
	const char* name;
	const char* label;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 minValue;
	int32 maxValue;
	orientation posture;
	thumb_style thumbType = B_BLOCK_THUMB;
	uint32 flags = B_NAVIGABLE | B_WILL_DRAW | B_FRAME_EVENTS;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Slider_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "ssOlli|ik", &name, &label, &py_message, &minValue, &maxValue, &posture, &thumbType, &flags);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object = new BSlider(name, label, message, minValue, maxValue, posture, thumbType, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Slider_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Slider_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Slider_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Slider_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BSlider(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Slider_DESTROY(Haiku_Slider_Object* python_self);
static void Haiku_Slider_DESTROY(Haiku_Slider_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Slider_Instantiate(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Instantiate(Haiku_Slider_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Slider_Archive(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Archive(Haiku_Slider_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Slider_SetLabel(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetLabel(Haiku_Slider_Object* python_self, PyObject* python_args) {
	const char* label;
	
	PyArg_ParseTuple(python_args, "s", &label);
	
	python_self->cpp_object->SetLabel(label);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SetLimitLabels(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetLimitLabels(Haiku_Slider_Object* python_self, PyObject* python_args) {
	const char* minLabel;
	const char* maxLabel;
	
	PyArg_ParseTuple(python_args, "ss", &minLabel, &maxLabel);
	
	python_self->cpp_object->SetLimitLabels(minLabel, maxLabel);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_MinLimitLabel(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_MinLimitLabel(Haiku_Slider_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MinLimitLabel();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_MaxLimitLabel(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_MaxLimitLabel(Haiku_Slider_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MaxLimitLabel();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetValue(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetValue(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 value;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	python_self->cpp_object->SetValue(value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_ValueForPoint(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_ValueForPoint(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ValueForPoint(point);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetPosition(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetPosition(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float position;
	
	PyArg_ParseTuple(python_args, "f", &position);
	
	python_self->cpp_object->SetPosition(position);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_Position(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Position(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Position();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetEnabled(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetEnabled(Haiku_Slider_Object* python_self, PyObject* python_args) {
	bool on;
	PyObject* py_on; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_on);
	on = (bool)(PyObject_IsTrue(py_on));
	
	python_self->cpp_object->SetEnabled(on);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_GetLimits(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_GetLimits(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 minLabel;
	int32 maxLabel;
	
	python_self->cpp_object->GetLimits(&minLabel, &maxLabel);
	
	return Py_BuildValue("ll", minLabel, maxLabel);
}

//static PyObject* Haiku_Slider_UpdateTextChanged(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_UpdateTextChanged(Haiku_Slider_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->UpdateTextChanged();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_BarFrame(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_BarFrame(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->BarFrame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_HashMarksFrame(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_HashMarksFrame(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->HashMarksFrame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_ThumbFrame(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_ThumbFrame(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ThumbFrame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_SetFlags(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetFlags(Haiku_Slider_Object* python_self, PyObject* python_args) {
	uint32 flags;
	
	PyArg_ParseTuple(python_args, "k", &flags);
	
	python_self->cpp_object->SetFlags(flags);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SetResizingMode(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetResizingMode(Haiku_Slider_Object* python_self, PyObject* python_args) {
	uint32 mode;
	
	PyArg_ParseTuple(python_args, "k", &mode);
	
	python_self->cpp_object->SetResizingMode(mode);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_GetPreferredSize(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_GetPreferredSize(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_Slider_ResizeToPreferred(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_ResizeToPreferred(Haiku_Slider_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_Invoke(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Invoke(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BMessage* message = NULL;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Invoke(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_Slider_ResolveSpecifier(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_ResolveSpecifier(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 index;
	BMessage* specifier;
	Haiku_Message_Object* py_specifier; // from generate_py()
	int32 form;
	const char* property;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OlOls", &py_message, &index, &py_specifier, &form, &property);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_specifier != NULL) {
		specifier = ((Haiku_Message_Object*)py_specifier)->cpp_object;
	}
	
	retval = python_self->cpp_object->ResolveSpecifier(message, index, specifier, form, property);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_GetSupportedSuites(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_GetSupportedSuites(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetSupportedSuites(data);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SetModificationMessage(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetModificationMessage(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->SetModificationMessage(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_ModificationMessage(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_ModificationMessage(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ModificationMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_SetSnoozeAmount(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetSnoozeAmount(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 amount;
	
	PyArg_ParseTuple(python_args, "l", &amount);
	
	python_self->cpp_object->SetSnoozeAmount(amount);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SnoozeAmount(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SnoozeAmount(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->SnoozeAmount();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetKeyIncrementValue(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetKeyIncrementValue(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 value;
	
	PyArg_ParseTuple(python_args, "l", &value);
	
	python_self->cpp_object->SetKeyIncrementValue(value);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_KeyIncrementValue(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_KeyIncrementValue(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->KeyIncrementValue();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetHashMarkCount(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetHashMarkCount(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 count;
	
	PyArg_ParseTuple(python_args, "l", &count);
	
	python_self->cpp_object->SetHashMarkCount(count);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_HashMarkCount(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_HashMarkCount(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->HashMarkCount();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetHashMarks(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetHashMarks(Haiku_Slider_Object* python_self, PyObject* python_args) {
	hash_mark_location where;
	
	PyArg_ParseTuple(python_args, "i", &where);
	
	python_self->cpp_object->SetHashMarks(where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_HashMarks(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_HashMarks(Haiku_Slider_Object* python_self, PyObject* python_args) {
	hash_mark_location retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->HashMarks();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetStyle(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetStyle(Haiku_Slider_Object* python_self, PyObject* python_args) {
	thumb_style style;
	
	PyArg_ParseTuple(python_args, "i", &style);
	
	python_self->cpp_object->SetStyle(style);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_Style(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Style(Haiku_Slider_Object* python_self, PyObject* python_args) {
	thumb_style retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Style();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetBarColor(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetBarColor(Haiku_Slider_Object* python_self, PyObject* python_args) {
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_color);
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetBarColor(color);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_BarColor(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_BarColor(Haiku_Slider_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->BarColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_UseFillColor(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_UseFillColor(Haiku_Slider_Object* python_self, PyObject* python_args) {
	bool useFill;
	PyObject* py_useFill; // from generate_py ()
	const rgb_color* color = NULL;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_useFill, &py_color);
	useFill = (bool)(PyObject_IsTrue(py_useFill));
	if (py_color != NULL) {
		color = ((Haiku_rgb_color_Object*)py_color)->cpp_object;
	}
	
	python_self->cpp_object->UseFillColor(useFill, color);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_FillColor(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_FillColor(Haiku_Slider_Object* python_self, PyObject* python_args) {
	rgb_color* color = NULL;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|O", &py_color);
	if (py_color != NULL) {
		color = ((Haiku_rgb_color_Object*)py_color)->cpp_object;
	}
	
	retval = python_self->cpp_object->FillColor(color);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Slider_OffscreenView(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_OffscreenView(Haiku_Slider_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->OffscreenView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Slider_SetOrientation(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetOrientation(Haiku_Slider_Object* python_self, PyObject* python_args) {
	orientation posture;
	
	PyArg_ParseTuple(python_args, "i", &posture);
	
	python_self->cpp_object->SetOrientation(posture);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_Orientation(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_Orientation(Haiku_Slider_Object* python_self, PyObject* python_args) {
	orientation retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Orientation();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_BarThickness(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_BarThickness(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->BarThickness();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_SetBarThickness(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetBarThickness(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float thickness;
	
	PyArg_ParseTuple(python_args, "f", &thickness);
	
	python_self->cpp_object->SetBarThickness(thickness);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SetFont(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetFont(Haiku_Slider_Object* python_self, PyObject* python_args) {
	const BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	uint32 properties = B_FONT_ALL;
	
	PyArg_ParseTuple(python_args, "O|k", &py_font, &properties);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	
	python_self->cpp_object->SetFont(font, properties);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_SetLimits(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_SetLimits(Haiku_Slider_Object* python_self, PyObject* python_args) {
	int32 minLabel;
	int32 maxLabel;
	
	PyArg_ParseTuple(python_args, "ll", &minLabel, &maxLabel);
	
	python_self->cpp_object->SetLimits(minLabel, maxLabel);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Slider_MaxUpdateTextWidth(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_MaxUpdateTextWidth(Haiku_Slider_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MaxUpdateTextWidth();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Slider_InvalidateLayout(Haiku_Slider_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Slider_InvalidateLayout(Haiku_Slider_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Slider_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Slider_Object*)a)->cpp_object == ((Haiku_Slider_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Slider_Object*)a)->cpp_object != ((Haiku_Slider_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Slider_PyMethods[] = {
	{"WithOrientation", (PyCFunction)Haiku_Slider_newWithOrientation, METH_VARARGS|METH_CLASS, ""},
	{"WithoutFrame", (PyCFunction)Haiku_Slider_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Slider_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Slider_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Slider_Archive, METH_VARARGS, ""},
	{"SetLabel", (PyCFunction)Haiku_Slider_SetLabel, METH_VARARGS, ""},
	{"SetLimitLabels", (PyCFunction)Haiku_Slider_SetLimitLabels, METH_VARARGS, ""},
	{"MinLimitLabel", (PyCFunction)Haiku_Slider_MinLimitLabel, METH_VARARGS, ""},
	{"MaxLimitLabel", (PyCFunction)Haiku_Slider_MaxLimitLabel, METH_VARARGS, ""},
	{"SetValue", (PyCFunction)Haiku_Slider_SetValue, METH_VARARGS, ""},
	{"ValueForPoint", (PyCFunction)Haiku_Slider_ValueForPoint, METH_VARARGS, ""},
	{"SetPosition", (PyCFunction)Haiku_Slider_SetPosition, METH_VARARGS, ""},
	{"Position", (PyCFunction)Haiku_Slider_Position, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_Slider_SetEnabled, METH_VARARGS, ""},
	{"GetLimits", (PyCFunction)Haiku_Slider_GetLimits, METH_VARARGS, ""},
	{"UpdateTextChanged", (PyCFunction)Haiku_Slider_UpdateTextChanged, METH_VARARGS, ""},
	{"BarFrame", (PyCFunction)Haiku_Slider_BarFrame, METH_VARARGS, ""},
	{"HashMarksFrame", (PyCFunction)Haiku_Slider_HashMarksFrame, METH_VARARGS, ""},
	{"ThumbFrame", (PyCFunction)Haiku_Slider_ThumbFrame, METH_VARARGS, ""},
	{"SetFlags", (PyCFunction)Haiku_Slider_SetFlags, METH_VARARGS, ""},
	{"SetResizingMode", (PyCFunction)Haiku_Slider_SetResizingMode, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_Slider_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_Slider_ResizeToPreferred, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_Slider_Invoke, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Slider_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Slider_GetSupportedSuites, METH_VARARGS, ""},
	{"SetModificationMessage", (PyCFunction)Haiku_Slider_SetModificationMessage, METH_VARARGS, ""},
	{"ModificationMessage", (PyCFunction)Haiku_Slider_ModificationMessage, METH_VARARGS, ""},
	{"SetSnoozeAmount", (PyCFunction)Haiku_Slider_SetSnoozeAmount, METH_VARARGS, ""},
	{"SnoozeAmount", (PyCFunction)Haiku_Slider_SnoozeAmount, METH_VARARGS, ""},
	{"SetKeyIncrementValue", (PyCFunction)Haiku_Slider_SetKeyIncrementValue, METH_VARARGS, ""},
	{"KeyIncrementValue", (PyCFunction)Haiku_Slider_KeyIncrementValue, METH_VARARGS, ""},
	{"SetHashMarkCount", (PyCFunction)Haiku_Slider_SetHashMarkCount, METH_VARARGS, ""},
	{"HashMarkCount", (PyCFunction)Haiku_Slider_HashMarkCount, METH_VARARGS, ""},
	{"SetHashMarks", (PyCFunction)Haiku_Slider_SetHashMarks, METH_VARARGS, ""},
	{"HashMarks", (PyCFunction)Haiku_Slider_HashMarks, METH_VARARGS, ""},
	{"SetStyle", (PyCFunction)Haiku_Slider_SetStyle, METH_VARARGS, ""},
	{"Style", (PyCFunction)Haiku_Slider_Style, METH_VARARGS, ""},
	{"SetBarColor", (PyCFunction)Haiku_Slider_SetBarColor, METH_VARARGS, ""},
	{"BarColor", (PyCFunction)Haiku_Slider_BarColor, METH_VARARGS, ""},
	{"UseFillColor", (PyCFunction)Haiku_Slider_UseFillColor, METH_VARARGS, ""},
	{"FillColor", (PyCFunction)Haiku_Slider_FillColor, METH_VARARGS, ""},
	{"OffscreenView", (PyCFunction)Haiku_Slider_OffscreenView, METH_VARARGS, ""},
	{"SetOrientation", (PyCFunction)Haiku_Slider_SetOrientation, METH_VARARGS, ""},
	{"Orientation", (PyCFunction)Haiku_Slider_Orientation, METH_VARARGS, ""},
	{"BarThickness", (PyCFunction)Haiku_Slider_BarThickness, METH_VARARGS, ""},
	{"SetBarThickness", (PyCFunction)Haiku_Slider_SetBarThickness, METH_VARARGS, ""},
	{"SetFont", (PyCFunction)Haiku_Slider_SetFont, METH_VARARGS, ""},
	{"SetLimits", (PyCFunction)Haiku_Slider_SetLimits, METH_VARARGS, ""},
	{"MaxUpdateTextWidth", (PyCFunction)Haiku_Slider_MaxUpdateTextWidth, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_Slider_InvalidateLayout, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Slider_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Slider";
	type->tp_basicsize   = sizeof(Haiku_Slider_Object);
	type->tp_dealloc     = (destructor)Haiku_Slider_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Slider_RichCompare;
	type->tp_methods     = Haiku_Slider_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Control_PyType;
	type->tp_init        = (initproc)Haiku_Slider_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

