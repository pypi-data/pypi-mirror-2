/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_WindowConstants_PyMethods[] = {
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
//static int Haiku_Window_init(Haiku_Window_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Window_init(Haiku_Window_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* title;
	window_type type;
	uint32 flags;
	uint32 workspaces = B_CURRENT_WORKSPACE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Osik|k", &py_frame, &title, &type, &flags, &workspaces);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BWindow(frame, title, type, flags, workspaces);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return 0;
}

//static PyObject* Haiku_Window_newFromLookAndFeel(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Window_newFromLookAndFeel(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Window_Object* python_self;
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* title;
	window_look look;
	window_feel feel;
	uint32 flags;
	uint32 workspaces = B_CURRENT_WORKSPACE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Window_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "Osiik|k", &py_frame, &title, &look, &feel, &flags, &workspaces);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BWindow(frame, title, look, feel, flags, workspaces);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Window_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Window_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Window_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Window_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BWindow(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return (PyObject*)python_self;
}

//static void Haiku_Window_DESTROY(Haiku_Window_Object* python_self);
static void Haiku_Window_DESTROY(Haiku_Window_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Window_Instantiate(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Instantiate(Haiku_Window_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Window_Archive(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Archive(Haiku_Window_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Window_Quit(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Quit(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Quit();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Close(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Close(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Close();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_AddChild(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_AddChild(Haiku_Window_Object* python_self, PyObject* python_args) {
	BView* view;
	Haiku_View_Object* py_view; // from generate_py()
	BView* sibling = NULL;
	Haiku_View_Object* py_sibling; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_view, &py_sibling);
	if (py_view != NULL) {
		view = ((Haiku_View_Object*)py_view)->cpp_object;
		((Haiku_View_Object*)py_view)->can_delete_cpp_object = false;
	}
	if (py_sibling != NULL) {
		sibling = ((Haiku_View_Object*)py_sibling)->cpp_object;
	}
	
	python_self->cpp_object->AddChild(view, sibling);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_RemoveChild(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_RemoveChild(Haiku_Window_Object* python_self, PyObject* python_args) {
	BView* view;
	Haiku_View_Object* py_view; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_view);
	if (py_view != NULL) {
		view = ((Haiku_View_Object*)py_view)->cpp_object;
	}
	
	retval = python_self->cpp_object->RemoveChild(view);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_CountChildren(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_CountChildren(Haiku_Window_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountChildren();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_ChildAt(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ChildAt(Haiku_Window_Object* python_self, PyObject* python_args) {
	int32 index;
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->ChildAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_DispatchMessage(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_DispatchMessage(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_message, &py_handler);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	python_self->cpp_object->DispatchMessage(message, handler);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Minimize(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Minimize(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool minimize;
	PyObject* py_minimize; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_minimize);
	minimize = (bool)(PyObject_IsTrue(py_minimize));
	
	python_self->cpp_object->Minimize(minimize);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_DoZoom(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_DoZoom(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Zoom();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SetZoomLimits(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetZoomLimits(Haiku_Window_Object* python_self, PyObject* python_args) {
	float maxWidth;
	float maxHeight;
	
	PyArg_ParseTuple(python_args, "ff", &maxWidth, &maxHeight);
	
	python_self->cpp_object->SetZoomLimits(maxWidth, maxHeight);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SetPulseRate(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetPulseRate(Haiku_Window_Object* python_self, PyObject* python_args) {
	bigtime_t microseconds;
	
	PyArg_ParseTuple(python_args, "l", &microseconds);
	
	python_self->cpp_object->SetPulseRate(microseconds);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_PulseRate(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_PulseRate(Haiku_Window_Object* python_self, PyObject* python_args) {
	bigtime_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->PulseRate();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_AddShortcut(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_AddShortcut(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 key;
	uint32 modifiers;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "kkO", &key, &modifiers, &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->AddShortcut(key, modifiers, message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_AddShortcutWithTarget(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_AddShortcutWithTarget(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 key;
	uint32 modifiers;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* target;
	Haiku_Handler_Object* py_target; // from generate_py()
	
	PyArg_ParseTuple(python_args, "kkOO", &key, &modifiers, &py_message, &py_target);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_target != NULL) {
		target = ((Haiku_Handler_Object*)py_target)->cpp_object;
	}
	
	python_self->cpp_object->AddShortcut(key, modifiers, message, target);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_RemoveShortcut(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_RemoveShortcut(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 key;
	uint32 modifiers;
	
	PyArg_ParseTuple(python_args, "kk", &key, &modifiers);
	
	python_self->cpp_object->RemoveShortcut(key, modifiers);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SetDefaultButton(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetDefaultButton(Haiku_Window_Object* python_self, PyObject* python_args) {
	BButton* button;
	Haiku_Button_Object* py_button; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_button);
	if (py_button != NULL) {
		button = ((Haiku_Button_Object*)py_button)->cpp_object;
	}
	
	python_self->cpp_object->SetDefaultButton(button);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_DefaultButton(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_DefaultButton(Haiku_Window_Object* python_self, PyObject* python_args) {
	BButton* retval;
	Haiku_Button_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->DefaultButton();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Button_Object*)Haiku_Button_PyType.tp_alloc(&Haiku_Button_PyType, 0);
	py_retval->cpp_object = (BButton*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_NeedsUpdate(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_NeedsUpdate(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->NeedsUpdate();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_UpdateIfNeeded(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_UpdateIfNeeded(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->UpdateIfNeeded();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_FindView(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_FindView(Haiku_Window_Object* python_self, PyObject* python_args) {
	const char* viewName;
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &viewName);
	
	retval = python_self->cpp_object->FindView(viewName);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_FindViewAtPoint(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_FindViewAtPoint(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->FindView(point);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_CurrentFocus(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_CurrentFocus(Haiku_Window_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->CurrentFocus();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_Activate(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Activate(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool flag = true;
	PyObject* py_flag; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_flag);
	flag = (bool)(PyObject_IsTrue(py_flag));
	
	python_self->cpp_object->Activate(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_ConvertPointToScreen(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ConvertPointToScreen(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint windowPoint;
	Haiku_Point_Object* py_windowPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_windowPoint);
	if (py_windowPoint != NULL) {
		memcpy((void*)&windowPoint, (void*)((Haiku_Point_Object*)py_windowPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertToScreen(windowPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_ConvertPointFromScreen(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ConvertPointFromScreen(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint windowPoint;
	Haiku_Point_Object* py_windowPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_windowPoint);
	if (py_windowPoint != NULL) {
		memcpy((void*)&windowPoint, (void*)((Haiku_Point_Object*)py_windowPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertFromScreen(windowPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_ConvertRectToScreen(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ConvertRectToScreen(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect windowRect;
	Haiku_Rect_Object* py_windowRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_windowRect);
	if (py_windowRect != NULL) {
		memcpy((void*)&windowRect, (void*)((Haiku_Rect_Object*)py_windowRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertToScreen(windowRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_ConvertRectFromScreen(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ConvertRectFromScreen(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect windowRect;
	Haiku_Rect_Object* py_windowRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_windowRect);
	if (py_windowRect != NULL) {
		memcpy((void*)&windowRect, (void*)((Haiku_Rect_Object*)py_windowRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertFromScreen(windowRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_MoveBy(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MoveBy(Haiku_Window_Object* python_self, PyObject* python_args) {
	float horizontal;
	float vertical;
	
	PyArg_ParseTuple(python_args, "ff", &horizontal, &vertical);
	
	python_self->cpp_object->MoveBy(horizontal, vertical);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_MoveTo(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MoveTo(Haiku_Window_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->MoveTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_MoveToPoint(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MoveToPoint(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_where);
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->MoveTo(where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_ResizeBy(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ResizeBy(Haiku_Window_Object* python_self, PyObject* python_args) {
	float horizontal;
	float vertical;
	
	PyArg_ParseTuple(python_args, "ff", &horizontal, &vertical);
	
	python_self->cpp_object->ResizeBy(horizontal, vertical);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_ResizeTo(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ResizeTo(Haiku_Window_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	PyArg_ParseTuple(python_args, "ff", &width, &height);
	
	python_self->cpp_object->ResizeTo(width, height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_CenterIn(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_CenterIn(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->CenterIn(rect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_CenterOnScreen(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_CenterOnScreen(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->CenterOnScreen();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Show(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Show(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Show();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Hide(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Hide(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Hide();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_IsHidden(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsHidden(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsHidden();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_IsMinimized(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsMinimized(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsMinimized();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_Flush(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Flush(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Flush();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Sync(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Sync(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Sync();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SendBehind(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SendBehind(Haiku_Window_Object* python_self, PyObject* python_args) {
	BWindow* window;
	Haiku_Window_Object* py_window; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_window);
	if (py_window != NULL) {
		window = ((Haiku_Window_Object*)py_window)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendBehind(window);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_DisableUpdates(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_DisableUpdates(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DisableUpdates();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_EnableUpdates(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_EnableUpdates(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->EnableUpdates();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_BeginViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_BeginViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BeginViewTransaction();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_EndViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_EndViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->EndViewTransaction();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_InViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_InViewTransaction(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->InViewTransaction();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_Bounds(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Bounds(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Bounds();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_Frame(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Frame(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Frame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_DecoratorFrame(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_DecoratorFrame(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->DecoratorFrame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_Title(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Title(Haiku_Window_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Title();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_SetTitle(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetTitle(Haiku_Window_Object* python_self, PyObject* python_args) {
	const char* newTitle;
	
	PyArg_ParseTuple(python_args, "s", &newTitle);
	
	python_self->cpp_object->SetTitle(newTitle);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_IsFront(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsFront(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFront();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_IsActive(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsActive(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsActive();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_SetKeyMenuBar(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetKeyMenuBar(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMenuBar* bar;
	Haiku_MenuBar_Object* py_bar; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_bar);
	if (py_bar != NULL) {
		bar = ((Haiku_MenuBar_Object*)py_bar)->cpp_object;
	}
	
	python_self->cpp_object->SetKeyMenuBar(bar);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_KeyMenuBar(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_KeyMenuBar(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMenuBar* retval;
	Haiku_MenuBar_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->KeyMenuBar();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuBar_Object*)Haiku_MenuBar_PyType.tp_alloc(&Haiku_MenuBar_PyType, 0);
	py_retval->cpp_object = (BMenuBar*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_SetSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args) {
	float minWidth;
	float maxWidth;
	float minHeight;
	float maxHeight;
	
	PyArg_ParseTuple(python_args, "ffff", &minWidth, &maxWidth, &minHeight, &maxHeight);
	
	python_self->cpp_object->SetSizeLimits(minWidth, maxWidth, minHeight, maxHeight);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_GetSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_GetSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args) {
	float minWidth;
	float maxWidth;
	float minHeight;
	float maxHeight;
	
	python_self->cpp_object->GetSizeLimits(&minWidth, &maxWidth, &minHeight, &maxHeight);
	
	return Py_BuildValue("ffff", minWidth, maxWidth, minHeight, maxHeight);
}

//static PyObject* Haiku_Window_UpdateSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_UpdateSizeLimits(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->UpdateSizeLimits();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SetDecoratorSettings(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetDecoratorSettings(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMessage settings;
	Haiku_Message_Object* py_settings; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_settings);
	if (py_settings != NULL) {
		memcpy((void*)&settings, (void*)((Haiku_Message_Object*)py_settings)->cpp_object, sizeof(BMessage));
	}
	
	retval = python_self->cpp_object->SetDecoratorSettings(settings);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_GetDecoratorSettings(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_GetDecoratorSettings(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMessage* settings;
	status_t retval;
	Haiku_Message_Object* py_settings; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetDecoratorSettings(settings);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_settings = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_settings->cpp_object = (BMessage*)settings;
	// we own this object, so we can delete it
	py_settings->can_delete_cpp_object = true;
	return (PyObject*)py_settings;
}

//static PyObject* Haiku_Window_SetWorkspaces(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetWorkspaces(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 workspaces;
	
	PyArg_ParseTuple(python_args, "k", &workspaces);
	
	python_self->cpp_object->SetWorkspaces(workspaces);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Workspaces(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Workspaces(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Workspaces();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_LastMouseMovedView(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_LastMouseMovedView(Haiku_Window_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LastMouseMovedView();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Window_ResolveSpecifier(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ResolveSpecifier(Haiku_Window_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Window_GetSupportedSuites(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_GetSupportedSuites(Haiku_Window_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Window_AddToSubset(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_AddToSubset(Haiku_Window_Object* python_self, PyObject* python_args) {
	BWindow* window;
	Haiku_Window_Object* py_window; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_window);
	if (py_window != NULL) {
		window = ((Haiku_Window_Object*)py_window)->cpp_object;
	}
	
	retval = python_self->cpp_object->AddToSubset(window);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_RemoveFromSubset(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_RemoveFromSubset(Haiku_Window_Object* python_self, PyObject* python_args) {
	BWindow* window;
	Haiku_Window_Object* py_window; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_window);
	if (py_window != NULL) {
		window = ((Haiku_Window_Object*)py_window)->cpp_object;
	}
	
	retval = python_self->cpp_object->RemoveFromSubset(window);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_SetType(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetType(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_type type;
	
	PyArg_ParseTuple(python_args, "i", &type);
	
	python_self->cpp_object->SetType(type);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Type(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Type(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_type retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Type();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_SetLook(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetLook(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_look look;
	
	PyArg_ParseTuple(python_args, "i", &look);
	
	python_self->cpp_object->SetLook(look);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Look(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Look(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_look retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Look();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_SetFeel(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetFeel(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_feel feel;
	
	PyArg_ParseTuple(python_args, "i", &feel);
	
	python_self->cpp_object->SetFeel(feel);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Feel(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Feel(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_feel retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Feel();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_SetFlags(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetFlags(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 flags;
	
	PyArg_ParseTuple(python_args, "k", &flags);
	
	python_self->cpp_object->SetFlags(flags);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Flags(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Flags(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Flags();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Window_IsFloating(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsFloating(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFloating();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_IsModal(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_IsModal(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsModal();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Window_SetWindowAlignment(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_SetWindowAlignment(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_alignment mode;
	int32 h;
	int32 hOffset = 0;
	int32 width = 0;
	int32 widthOffset = 0;
	int32 v = 0;
	int32 vOffset = 0;
	int32 height = 0;
	int32 heightOffset = 0;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "il|lllllll", &mode, &h, &hOffset, &width, &widthOffset, &v, &vOffset, &height, &heightOffset);
	
	retval = python_self->cpp_object->SetWindowAlignment(mode, h, hOffset, width, widthOffset, v, vOffset, height, heightOffset);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_GetWindowAlignment(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_GetWindowAlignment(Haiku_Window_Object* python_self, PyObject* python_args) {
	window_alignment mode;
	int32 h;
	int32 hOffset = 0;
	int32 width;
	int32 widthOffset = 0;
	int32 v;
	int32 vOffset = 0;
	int32 height;
	int32 heightOffset = 0;
	status_t retval;
	
	retval = python_self->cpp_object->GetWindowAlignment(&mode, &h, &hOffset, &width, &widthOffset, &v, &vOffset, &height, &heightOffset);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	
	return Py_BuildValue("illllllll", mode, h, hOffset, width, widthOffset, v, vOffset, height, heightOffset);
}

//static PyObject* Haiku_Window_Run(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Run(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Run();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_InvalidateLayout(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_InvalidateLayout(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_MessageReceived(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MessageReceived(Haiku_Window_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->BWindow::MessageReceived(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_FrameMoved(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_FrameMoved(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint newPosition;
	Haiku_Point_Object* py_newPosition; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_newPosition);
	if (py_newPosition != NULL) {
		memcpy((void*)&newPosition, (void*)((Haiku_Point_Object*)py_newPosition)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->BWindow::FrameMoved(newPosition);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_WorkspacesChanged(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_WorkspacesChanged(Haiku_Window_Object* python_self, PyObject* python_args) {
	uint32 oldWorkspaces;
	uint32 newWorkspaces;
	
	PyArg_ParseTuple(python_args, "kk", &oldWorkspaces, &newWorkspaces);
	
	python_self->cpp_object->BWindow::WorkspacesChanged(oldWorkspaces, newWorkspaces);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_WorkspaceActivated(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_WorkspaceActivated(Haiku_Window_Object* python_self, PyObject* python_args) {
	int32 workspaces;
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "lO", &workspaces, &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->BWindow::WorkspaceActivated(workspaces, state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_FrameResized(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_FrameResized(Haiku_Window_Object* python_self, PyObject* python_args) {
	float newWidth;
	float newHeight;
	
	PyArg_ParseTuple(python_args, "ff", &newWidth, &newHeight);
	
	python_self->cpp_object->BWindow::FrameResized(newWidth, newHeight);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_Zoom(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_Zoom(Haiku_Window_Object* python_self, PyObject* python_args) {
	BPoint origin;
	Haiku_Point_Object* py_origin; // from generate_py()
	float width;
	float height;
	
	PyArg_ParseTuple(python_args, "Off", &py_origin, &width, &height);
	if (py_origin != NULL) {
		memcpy((void*)&origin, (void*)((Haiku_Point_Object*)py_origin)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->BWindow::Zoom(origin, width, height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_ScreenChanged(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_ScreenChanged(Haiku_Window_Object* python_self, PyObject* python_args) {
	BRect screenSize;
	Haiku_Rect_Object* py_screenSize; // from generate_py()
	color_space format;
	
	PyArg_ParseTuple(python_args, "Oi", &py_screenSize, &format);
	if (py_screenSize != NULL) {
		memcpy((void*)&screenSize, (void*)((Haiku_Rect_Object*)py_screenSize)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->BWindow::ScreenChanged(screenSize, format);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_MenusBeginning(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MenusBeginning(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BWindow::MenusBeginning();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_MenusEnded(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_MenusEnded(Haiku_Window_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BWindow::MenusEnded();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_WindowActivated(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_WindowActivated(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->BWindow::WindowActivated(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Window_QuitRequested(Haiku_Window_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Window_QuitRequested(Haiku_Window_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->BWindow::QuitRequested();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_Window_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Window_Object*)a)->cpp_object == ((Haiku_Window_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Window_Object*)a)->cpp_object != ((Haiku_Window_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Window_PyMethods[] = {
	{"FromLookAndFeel", (PyCFunction)Haiku_Window_newFromLookAndFeel, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Window_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Window_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Window_Archive, METH_VARARGS, ""},
	{"Quit", (PyCFunction)Haiku_Window_Quit, METH_VARARGS, ""},
	{"Close", (PyCFunction)Haiku_Window_Close, METH_VARARGS, ""},
	{"AddChild", (PyCFunction)Haiku_Window_AddChild, METH_VARARGS, ""},
	{"RemoveChild", (PyCFunction)Haiku_Window_RemoveChild, METH_VARARGS, ""},
	{"CountChildren", (PyCFunction)Haiku_Window_CountChildren, METH_VARARGS, ""},
	{"ChildAt", (PyCFunction)Haiku_Window_ChildAt, METH_VARARGS, ""},
	{"DispatchMessage", (PyCFunction)Haiku_Window_DispatchMessage, METH_VARARGS, ""},
	{"Minimize", (PyCFunction)Haiku_Window_Minimize, METH_VARARGS, ""},
	{"DoZoom", (PyCFunction)Haiku_Window_DoZoom, METH_VARARGS, ""},
	{"SetZoomLimits", (PyCFunction)Haiku_Window_SetZoomLimits, METH_VARARGS, ""},
	{"SetPulseRate", (PyCFunction)Haiku_Window_SetPulseRate, METH_VARARGS, ""},
	{"PulseRate", (PyCFunction)Haiku_Window_PulseRate, METH_VARARGS, ""},
	{"AddShortcut", (PyCFunction)Haiku_Window_AddShortcut, METH_VARARGS, ""},
	{"AddShortcutWithTarget", (PyCFunction)Haiku_Window_AddShortcutWithTarget, METH_VARARGS, ""},
	{"RemoveShortcut", (PyCFunction)Haiku_Window_RemoveShortcut, METH_VARARGS, ""},
	{"SetDefaultButton", (PyCFunction)Haiku_Window_SetDefaultButton, METH_VARARGS, ""},
	{"DefaultButton", (PyCFunction)Haiku_Window_DefaultButton, METH_VARARGS, ""},
	{"NeedsUpdate", (PyCFunction)Haiku_Window_NeedsUpdate, METH_VARARGS, ""},
	{"UpdateIfNeeded", (PyCFunction)Haiku_Window_UpdateIfNeeded, METH_VARARGS, ""},
	{"FindView", (PyCFunction)Haiku_Window_FindView, METH_VARARGS, ""},
	{"FindViewAtPoint", (PyCFunction)Haiku_Window_FindViewAtPoint, METH_VARARGS, ""},
	{"CurrentFocus", (PyCFunction)Haiku_Window_CurrentFocus, METH_VARARGS, ""},
	{"Activate", (PyCFunction)Haiku_Window_Activate, METH_VARARGS, ""},
	{"ConvertPointToScreen", (PyCFunction)Haiku_Window_ConvertPointToScreen, METH_VARARGS, ""},
	{"ConvertPointFromScreen", (PyCFunction)Haiku_Window_ConvertPointFromScreen, METH_VARARGS, ""},
	{"ConvertRectToScreen", (PyCFunction)Haiku_Window_ConvertRectToScreen, METH_VARARGS, ""},
	{"ConvertRectFromScreen", (PyCFunction)Haiku_Window_ConvertRectFromScreen, METH_VARARGS, ""},
	{"MoveBy", (PyCFunction)Haiku_Window_MoveBy, METH_VARARGS, ""},
	{"MoveTo", (PyCFunction)Haiku_Window_MoveTo, METH_VARARGS, ""},
	{"MoveToPoint", (PyCFunction)Haiku_Window_MoveToPoint, METH_VARARGS, ""},
	{"ResizeBy", (PyCFunction)Haiku_Window_ResizeBy, METH_VARARGS, ""},
	{"ResizeTo", (PyCFunction)Haiku_Window_ResizeTo, METH_VARARGS, ""},
	{"CenterIn", (PyCFunction)Haiku_Window_CenterIn, METH_VARARGS, ""},
	{"CenterOnScreen", (PyCFunction)Haiku_Window_CenterOnScreen, METH_VARARGS, ""},
	{"Show", (PyCFunction)Haiku_Window_Show, METH_VARARGS, ""},
	{"Hide", (PyCFunction)Haiku_Window_Hide, METH_VARARGS, ""},
	{"IsHidden", (PyCFunction)Haiku_Window_IsHidden, METH_VARARGS, ""},
	{"IsMinimized", (PyCFunction)Haiku_Window_IsMinimized, METH_VARARGS, ""},
	{"Flush", (PyCFunction)Haiku_Window_Flush, METH_VARARGS, ""},
	{"Sync", (PyCFunction)Haiku_Window_Sync, METH_VARARGS, ""},
	{"SendBehind", (PyCFunction)Haiku_Window_SendBehind, METH_VARARGS, ""},
	{"DisableUpdates", (PyCFunction)Haiku_Window_DisableUpdates, METH_VARARGS, ""},
	{"EnableUpdates", (PyCFunction)Haiku_Window_EnableUpdates, METH_VARARGS, ""},
	{"BeginViewTransaction", (PyCFunction)Haiku_Window_BeginViewTransaction, METH_VARARGS, ""},
	{"EndViewTransaction", (PyCFunction)Haiku_Window_EndViewTransaction, METH_VARARGS, ""},
	{"InViewTransaction", (PyCFunction)Haiku_Window_InViewTransaction, METH_VARARGS, ""},
	{"Bounds", (PyCFunction)Haiku_Window_Bounds, METH_VARARGS, ""},
	{"Frame", (PyCFunction)Haiku_Window_Frame, METH_VARARGS, ""},
	{"DecoratorFrame", (PyCFunction)Haiku_Window_DecoratorFrame, METH_VARARGS, ""},
	{"Title", (PyCFunction)Haiku_Window_Title, METH_VARARGS, ""},
	{"SetTitle", (PyCFunction)Haiku_Window_SetTitle, METH_VARARGS, ""},
	{"IsFront", (PyCFunction)Haiku_Window_IsFront, METH_VARARGS, ""},
	{"IsActive", (PyCFunction)Haiku_Window_IsActive, METH_VARARGS, ""},
	{"SetKeyMenuBar", (PyCFunction)Haiku_Window_SetKeyMenuBar, METH_VARARGS, ""},
	{"KeyMenuBar", (PyCFunction)Haiku_Window_KeyMenuBar, METH_VARARGS, ""},
	{"SetSizeLimits", (PyCFunction)Haiku_Window_SetSizeLimits, METH_VARARGS, ""},
	{"GetSizeLimits", (PyCFunction)Haiku_Window_GetSizeLimits, METH_VARARGS, ""},
	{"UpdateSizeLimits", (PyCFunction)Haiku_Window_UpdateSizeLimits, METH_VARARGS, ""},
	{"SetDecoratorSettings", (PyCFunction)Haiku_Window_SetDecoratorSettings, METH_VARARGS, ""},
	{"GetDecoratorSettings", (PyCFunction)Haiku_Window_GetDecoratorSettings, METH_VARARGS, ""},
	{"SetWorkspaces", (PyCFunction)Haiku_Window_SetWorkspaces, METH_VARARGS, ""},
	{"Workspaces", (PyCFunction)Haiku_Window_Workspaces, METH_VARARGS, ""},
	{"LastMouseMovedView", (PyCFunction)Haiku_Window_LastMouseMovedView, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Window_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Window_GetSupportedSuites, METH_VARARGS, ""},
	{"AddToSubset", (PyCFunction)Haiku_Window_AddToSubset, METH_VARARGS, ""},
	{"RemoveFromSubset", (PyCFunction)Haiku_Window_RemoveFromSubset, METH_VARARGS, ""},
	{"SetType", (PyCFunction)Haiku_Window_SetType, METH_VARARGS, ""},
	{"Type", (PyCFunction)Haiku_Window_Type, METH_VARARGS, ""},
	{"SetLook", (PyCFunction)Haiku_Window_SetLook, METH_VARARGS, ""},
	{"Look", (PyCFunction)Haiku_Window_Look, METH_VARARGS, ""},
	{"SetFeel", (PyCFunction)Haiku_Window_SetFeel, METH_VARARGS, ""},
	{"Feel", (PyCFunction)Haiku_Window_Feel, METH_VARARGS, ""},
	{"SetFlags", (PyCFunction)Haiku_Window_SetFlags, METH_VARARGS, ""},
	{"Flags", (PyCFunction)Haiku_Window_Flags, METH_VARARGS, ""},
	{"IsFloating", (PyCFunction)Haiku_Window_IsFloating, METH_VARARGS, ""},
	{"IsModal", (PyCFunction)Haiku_Window_IsModal, METH_VARARGS, ""},
	{"SetWindowAlignment", (PyCFunction)Haiku_Window_SetWindowAlignment, METH_VARARGS, ""},
	{"GetWindowAlignment", (PyCFunction)Haiku_Window_GetWindowAlignment, METH_VARARGS, ""},
	{"Run", (PyCFunction)Haiku_Window_Run, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_Window_InvalidateLayout, METH_VARARGS, ""},
	{"MessageReceived", (PyCFunction)Haiku_Window_MessageReceived, METH_VARARGS, ""},
	{"FrameMoved", (PyCFunction)Haiku_Window_FrameMoved, METH_VARARGS, ""},
	{"WorkspacesChanged", (PyCFunction)Haiku_Window_WorkspacesChanged, METH_VARARGS, ""},
	{"WorkspaceActivated", (PyCFunction)Haiku_Window_WorkspaceActivated, METH_VARARGS, ""},
	{"FrameResized", (PyCFunction)Haiku_Window_FrameResized, METH_VARARGS, ""},
	{"Zoom", (PyCFunction)Haiku_Window_Zoom, METH_VARARGS, ""},
	{"ScreenChanged", (PyCFunction)Haiku_Window_ScreenChanged, METH_VARARGS, ""},
	{"MenusBeginning", (PyCFunction)Haiku_Window_MenusBeginning, METH_VARARGS, ""},
	{"MenusEnded", (PyCFunction)Haiku_Window_MenusEnded, METH_VARARGS, ""},
	{"WindowActivated", (PyCFunction)Haiku_Window_WindowActivated, METH_VARARGS, ""},
	{"QuitRequested", (PyCFunction)Haiku_Window_QuitRequested, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Window_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Window";
	type->tp_basicsize   = sizeof(Haiku_Window_Object);
	type->tp_dealloc     = (destructor)Haiku_Window_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Window_RichCompare;
	type->tp_methods     = Haiku_Window_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Looper_PyType;
	type->tp_init        = (initproc)Haiku_Window_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

