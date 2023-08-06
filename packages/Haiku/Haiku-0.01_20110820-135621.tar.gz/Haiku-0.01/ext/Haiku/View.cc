/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_ViewConstants_PyMethods[] = {
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
//static int Haiku_View_init(Haiku_View_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_View_init(Haiku_View_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	uint32 resizingMode;
	uint32 flags;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Oskk", &py_frame, &name, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BView(frame, name, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_View_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_View_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_View_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_View_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_View_DESTROY(Haiku_View_Object* python_self);
static void Haiku_View_DESTROY(Haiku_View_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_View_Instantiate(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Instantiate(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_Archive(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Archive(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_AllUnarchived(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_AllUnarchived(Haiku_View_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllUnarchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_AllArchived(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_AllArchived(Haiku_View_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllArchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_AddChild(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_AddChild(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_RemoveChild(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_RemoveChild(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_CountChildren(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_CountChildren(Haiku_View_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountChildren();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_View_ChildAt(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ChildAt(Haiku_View_Object* python_self, PyObject* python_args) {
	int32 index;
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->ChildAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_NextSibling(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_NextSibling(Haiku_View_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->NextSibling();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_PreviousSibling(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_PreviousSibling(Haiku_View_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->PreviousSibling();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_RemoveSelf(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_RemoveSelf(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->RemoveSelf();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_Window(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Window(Haiku_View_Object* python_self, PyObject* python_args) {
	BWindow* retval;
	Haiku_Window_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Window();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Window_Object*)Haiku_Window_PyType.tp_alloc(&Haiku_Window_PyType, 0);
	py_retval->cpp_object = (BWindow*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_BeginRectTracking(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_BeginRectTracking(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	uint32 how = B_TRACK_WHOLE_RECT;
	
	PyArg_ParseTuple(python_args, "O|k", &py_rect, &how);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->BeginRectTracking(rect, how);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_EndRectTracking(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_EndRectTracking(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->EndRectTracking();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_GetMouse(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetMouse(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint location;
	uint32 buttons;
	bool checkMessageQueue = true;
	PyObject* py_checkMessageQueue; // from generate_py ()
	Haiku_Point_Object* py_location; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|O", &py_checkMessageQueue);
	checkMessageQueue = (bool)(PyObject_IsTrue(py_checkMessageQueue));
	
	python_self->cpp_object->GetMouse(&location, &buttons, checkMessageQueue);
	
	py_location = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_location->cpp_object = (BPoint*)&location;
	// we own this object, so we can delete it
	py_location->can_delete_cpp_object = true;
	
	return Py_BuildValue("Ok", py_location, buttons);
}

//static PyObject* Haiku_View_WithRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_WithRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	BHandler* replyTarget = NULL;
	Haiku_Handler_Object* py_replyTarget; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO|O", &py_message, &py_rect, &py_replyTarget);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_replyTarget != NULL) {
		replyTarget = ((Haiku_Handler_Object*)py_replyTarget)->cpp_object;
	}
	
	python_self->cpp_object->DragMessage(message, rect, replyTarget);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FindView(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FindView(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* name;
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindView(name);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_Parent(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Parent(Haiku_View_Object* python_self, PyObject* python_args) {
	BView* retval;
	Haiku_View_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Parent();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_View_Object*)Haiku_View_PyType.tp_alloc(&Haiku_View_PyType, 0);
	py_retval->cpp_object = (BView*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_Bounds(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Bounds(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Bounds();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_Frame(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Frame(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Frame();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertPointToScreen(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertPointToScreen(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint localPoint;
	Haiku_Point_Object* py_localPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_localPoint);
	if (py_localPoint != NULL) {
		memcpy((void*)&localPoint, (void*)((Haiku_Point_Object*)py_localPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertToScreen(localPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertPointFromScreen(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertPointFromScreen(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint screenPoint;
	Haiku_Point_Object* py_screenPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_screenPoint);
	if (py_screenPoint != NULL) {
		memcpy((void*)&screenPoint, (void*)((Haiku_Point_Object*)py_screenPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertFromScreen(screenPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertRectToScreen(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertRectToScreen(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect localRect;
	Haiku_Rect_Object* py_localRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_localRect);
	if (py_localRect != NULL) {
		memcpy((void*)&localRect, (void*)((Haiku_Rect_Object*)py_localRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertToScreen(localRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertRectFromScreen(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertRectFromScreen(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect screenRect;
	Haiku_Rect_Object* py_screenRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_screenRect);
	if (py_screenRect != NULL) {
		memcpy((void*)&screenRect, (void*)((Haiku_Rect_Object*)py_screenRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertFromScreen(screenRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertPointToParent(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertPointToParent(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint localPoint;
	Haiku_Point_Object* py_localPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_localPoint);
	if (py_localPoint != NULL) {
		memcpy((void*)&localPoint, (void*)((Haiku_Point_Object*)py_localPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertToParent(localPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertPointFromParent(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertPointFromParent(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint parentPoint;
	Haiku_Point_Object* py_parentPoint; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_parentPoint);
	if (py_parentPoint != NULL) {
		memcpy((void*)&parentPoint, (void*)((Haiku_Point_Object*)py_parentPoint)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->ConvertFromParent(parentPoint);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertRectToParent(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertRectToParent(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect localRect;
	Haiku_Rect_Object* py_localRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_localRect);
	if (py_localRect != NULL) {
		memcpy((void*)&localRect, (void*)((Haiku_Rect_Object*)py_localRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertToParent(localRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ConvertRectFromParent(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ConvertRectFromParent(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect parentRect;
	Haiku_Rect_Object* py_parentRect; // from generate_py()
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_parentRect);
	if (py_parentRect != NULL) {
		memcpy((void*)&parentRect, (void*)((Haiku_Rect_Object*)py_parentRect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->ConvertFromParent(parentRect);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_LeftTop(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_LeftTop(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LeftTop();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ClipToPicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ClipToPicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* picture;
	Haiku_Picture_Object* py_picture; // from generate_py()
	BPoint where = B_ORIGIN;
	Haiku_Point_Object* py_where; // from generate_py()
	bool sync = true;
	PyObject* py_sync; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O|OO", &py_picture, &py_where, &py_sync);
	if (py_picture != NULL) {
		picture = ((Haiku_Picture_Object*)py_picture)->cpp_object;
	}
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	sync = (bool)(PyObject_IsTrue(py_sync));
	
	python_self->cpp_object->ClipToPicture(picture, where, sync);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ClipToInversePicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ClipToInversePicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* picture;
	Haiku_Picture_Object* py_picture; // from generate_py()
	BPoint where = B_ORIGIN;
	Haiku_Point_Object* py_where; // from generate_py()
	bool sync = true;
	PyObject* py_sync; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O|OO", &py_picture, &py_where, &py_sync);
	if (py_picture != NULL) {
		picture = ((Haiku_Picture_Object*)py_picture)->cpp_object;
	}
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	sync = (bool)(PyObject_IsTrue(py_sync));
	
	python_self->cpp_object->ClipToInversePicture(picture, where, sync);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetDrawingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetDrawingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	drawing_mode mode;
	
	PyArg_ParseTuple(python_args, "i", &mode);
	
	python_self->cpp_object->SetDrawingMode(mode);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	drawing_mode retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DrawingMode();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_View_SetBlendingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetBlendingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	source_alpha srcAlpha;
	alpha_function alphaFunc;
	
	PyArg_ParseTuple(python_args, "ii", &srcAlpha, &alphaFunc);
	
	python_self->cpp_object->SetBlendingMode(srcAlpha, alphaFunc);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_GetBlendingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetBlendingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	source_alpha srcAlpha;
	alpha_function alphaFunc;
	
	python_self->cpp_object->GetBlendingMode(&srcAlpha, &alphaFunc);
	
	return Py_BuildValue("ii", srcAlpha, alphaFunc);
}

//static PyObject* Haiku_View_SetPenSize(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetPenSize(Haiku_View_Object* python_self, PyObject* python_args) {
	float size;
	
	PyArg_ParseTuple(python_args, "f", &size);
	
	python_self->cpp_object->SetPenSize(size);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_PenSize(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_PenSize(Haiku_View_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->PenSize();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_View_SetViewCursor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetViewCursor(Haiku_View_Object* python_self, PyObject* python_args) {
	BCursor* cursor;
	Haiku_Cursor_Object* py_cursor; // from generate_py()
	bool sync = true;
	PyObject* py_sync; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O|O", &py_cursor, &py_sync);
	if (py_cursor != NULL) {
		cursor = ((Haiku_Cursor_Object*)py_cursor)->cpp_object;
	}
	sync = (bool)(PyObject_IsTrue(py_sync));
	
	python_self->cpp_object->SetViewCursor(cursor, sync);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetViewColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetViewColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color c;
	Haiku_rgb_color_Object* py_c; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_c);
	if (py_c != NULL) {
		memcpy((void*)&c, (void*)((Haiku_rgb_color_Object*)py_c)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetViewColor(c);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetViewColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetViewColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args) {
	uchar r;
	uchar g;
	uchar b;
	uchar a = 255;
	
	PyArg_ParseTuple(python_args, "BBB|B", &r, &g, &b, &a);
	
	python_self->cpp_object->SetViewColor(r, g, b, a);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ViewColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ViewColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ViewColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ClearViewOverlay(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ClearViewOverlay(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ClearViewOverlay();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetHighColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetHighColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color c;
	Haiku_rgb_color_Object* py_c; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_c);
	if (py_c != NULL) {
		memcpy((void*)&c, (void*)((Haiku_rgb_color_Object*)py_c)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetHighColor(c);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetHighColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetHighColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args) {
	uchar r;
	uchar g;
	uchar b;
	uchar a = 255;
	
	PyArg_ParseTuple(python_args, "BBB|B", &r, &g, &b, &a);
	
	python_self->cpp_object->SetHighColor(r, g, b, a);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_HighColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_HighColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->HighColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_SetLowColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetLowColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color c;
	Haiku_rgb_color_Object* py_c; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_c);
	if (py_c != NULL) {
		memcpy((void*)&c, (void*)((Haiku_rgb_color_Object*)py_c)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->SetLowColor(c);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetLowColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetLowColorWithRGBA(Haiku_View_Object* python_self, PyObject* python_args) {
	uchar r;
	uchar g;
	uchar b;
	uchar a = 255;
	
	PyArg_ParseTuple(python_args, "BBB|B", &r, &g, &b, &a);
	
	python_self->cpp_object->SetLowColor(r, g, b, a);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_LowColor(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_LowColor(Haiku_View_Object* python_self, PyObject* python_args) {
	rgb_color retval;
	Haiku_rgb_color_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LowColor();
	
	py_retval = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_retval->cpp_object = (rgb_color*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_SetLineMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetLineMode(Haiku_View_Object* python_self, PyObject* python_args) {
	cap_mode lineCap;
	join_mode lineJoin;
	float miterLimit = B_DEFAULT_MITER_LIMIT;
	
	PyArg_ParseTuple(python_args, "ii|f", &lineCap, &lineJoin, &miterLimit);
	
	python_self->cpp_object->SetLineMode(lineCap, lineJoin, miterLimit);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_LineJoinMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_LineJoinMode(Haiku_View_Object* python_self, PyObject* python_args) {
	join_mode retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LineJoinMode();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_View_LineCapMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_LineCapMode(Haiku_View_Object* python_self, PyObject* python_args) {
	cap_mode retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LineCapMode();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_View_LineMiterLimit(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_LineMiterLimit(Haiku_View_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LineMiterLimit();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_View_SetOrigin(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetOrigin(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->SetOrigin(point);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetOriginWithXY(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetOriginWithXY(Haiku_View_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->SetOrigin(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Origin(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Origin(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Origin();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_PushState(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_PushState(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PushState();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_PopState(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_PopState(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PopState();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_MovePenTo(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MovePenTo(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->MovePenTo(point);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_MovePenToXY(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MovePenToXY(Haiku_View_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->MovePenTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_MovePenBy(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MovePenBy(Haiku_View_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->MovePenBy(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_PenLocation(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_PenLocation(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->PenLocation();
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_StrokeLineFromPenLocation(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeLineFromPenLocation(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint toPoint;
	Haiku_Point_Object* py_toPoint; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_toPoint, &py_p);
	if (py_toPoint != NULL) {
		memcpy((void*)&toPoint, (void*)((Haiku_Point_Object*)py_toPoint)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeLine(toPoint, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeLine(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeLine(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint a;
	Haiku_Point_Object* py_a; // from generate_py()
	BPoint b;
	Haiku_Point_Object* py_b; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO|O", &py_a, &py_b, &py_p);
	if (py_a != NULL) {
		memcpy((void*)&a, (void*)((Haiku_Point_Object*)py_a)->cpp_object, sizeof(BPoint));
	}
	if (py_b != NULL) {
		memcpy((void*)&b, (void*)((Haiku_Point_Object*)py_b)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeLine(a, b, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_BeginLineArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_BeginLineArray(Haiku_View_Object* python_self, PyObject* python_args) {
	int32 count;
	
	PyArg_ParseTuple(python_args, "l", &count);
	
	python_self->cpp_object->BeginLineArray(count);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_AddLine(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_AddLine(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint a;
	Haiku_Point_Object* py_a; // from generate_py()
	BPoint b;
	Haiku_Point_Object* py_b; // from generate_py()
	rgb_color color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OOO", &py_a, &py_b, &py_color);
	if (py_a != NULL) {
		memcpy((void*)&a, (void*)((Haiku_Point_Object*)py_a)->cpp_object, sizeof(BPoint));
	}
	if (py_b != NULL) {
		memcpy((void*)&b, (void*)((Haiku_Point_Object*)py_b)->cpp_object, sizeof(BPoint));
	}
	if (py_color != NULL) {
		memcpy((void*)&color, (void*)((Haiku_rgb_color_Object*)py_color)->cpp_object, sizeof(rgb_color));
	}
	
	python_self->cpp_object->AddLine(a, b, color);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_EndLineArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_EndLineArray(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->EndLineArray();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokePolygon(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokePolygon(Haiku_View_Object* python_self, PyObject* python_args) {
	BPolygon* polygon;
	Haiku_Polygon_Object* py_polygon; // from generate_py()
	bool closed = true;
	PyObject* py_closed; // from generate_py ()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|OO", &py_polygon, &py_closed, &py_p);
	if (py_polygon != NULL) {
		polygon = ((Haiku_Polygon_Object*)py_polygon)->cpp_object;
	}
	closed = (bool)(PyObject_IsTrue(py_closed));
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokePolygon(polygon, closed, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokePolygonFromPointArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokePolygonFromPointArray(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* pointArray;
	PyObject* py_pointArray; // from generate_py ()
	PyObject* py_pointArray_element;	// from array_arg_parser()
	int32 numPoints;
	bool closed = true;
	PyObject* py_closed; // from generate_py ()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|OO", &py_pointArray, &py_closed, &py_p);
	numPoints = PyList_Size(py_pointArray);
	for (int i = 0; i < numPoints; i++) {
		py_pointArray_element = PyList_GetItem(py_pointArray, i);
		if (py_pointArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_pointArray_element != NULL) { // element code
			memcpy((void*)&pointArray[i], (void*)((Haiku_Point_Object*)py_pointArray_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	closed = (bool)(PyObject_IsTrue(py_closed));
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokePolygon(pointArray, numPoints, closed, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokePolygonFromPointArrayWithinBounds(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokePolygonFromPointArrayWithinBounds(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* pointArray;
	PyObject* py_pointArray; // from generate_py ()
	PyObject* py_pointArray_element;	// from array_arg_parser()
	int32 numPoints;
	BRect bounds;
	Haiku_Rect_Object* py_bounds; // from generate_py()
	bool closed = true;
	PyObject* py_closed; // from generate_py ()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO|OO", &py_pointArray, &py_bounds, &py_closed, &py_p);
	numPoints = PyList_Size(py_pointArray);
	for (int i = 0; i < numPoints; i++) {
		py_pointArray_element = PyList_GetItem(py_pointArray, i);
		if (py_pointArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_pointArray_element != NULL) { // element code
			memcpy((void*)&pointArray[i], (void*)((Haiku_Point_Object*)py_pointArray_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	if (py_bounds != NULL) {
		memcpy((void*)&bounds, (void*)((Haiku_Rect_Object*)py_bounds)->cpp_object, sizeof(BRect));
	}
	closed = (bool)(PyObject_IsTrue(py_closed));
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokePolygon(pointArray, numPoints, bounds, closed, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillPolygon(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillPolygon(Haiku_View_Object* python_self, PyObject* python_args) {
	BPolygon* polygon;
	Haiku_Polygon_Object* py_polygon; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_polygon, &py_p);
	if (py_polygon != NULL) {
		polygon = ((Haiku_Polygon_Object*)py_polygon)->cpp_object;
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillPolygon(polygon, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillPolygonFromPointArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillPolygonFromPointArray(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* pointArray;
	PyObject* py_pointArray; // from generate_py ()
	PyObject* py_pointArray_element;	// from array_arg_parser()
	int32 numPoints;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_pointArray, &py_p);
	numPoints = PyList_Size(py_pointArray);
	for (int i = 0; i < numPoints; i++) {
		py_pointArray_element = PyList_GetItem(py_pointArray, i);
		if (py_pointArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_pointArray_element != NULL) { // element code
			memcpy((void*)&pointArray[i], (void*)((Haiku_Point_Object*)py_pointArray_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillPolygon(pointArray, numPoints, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillPolygonFromPointArrayWithinBounds(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillPolygonFromPointArrayWithinBounds(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* pointArray;
	PyObject* py_pointArray; // from generate_py ()
	PyObject* py_pointArray_element;	// from array_arg_parser()
	int32 numPoints;
	BRect bounds;
	Haiku_Rect_Object* py_bounds; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO|O", &py_pointArray, &py_bounds, &py_p);
	numPoints = PyList_Size(py_pointArray);
	for (int i = 0; i < numPoints; i++) {
		py_pointArray_element = PyList_GetItem(py_pointArray, i);
		if (py_pointArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_pointArray_element != NULL) { // element code
			memcpy((void*)&pointArray[i], (void*)((Haiku_Point_Object*)py_pointArray_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	if (py_bounds != NULL) {
		memcpy((void*)&bounds, (void*)((Haiku_Rect_Object*)py_bounds)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillPolygon(pointArray, numPoints, bounds, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeTriangle(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeTriangle(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point1;
	Haiku_Point_Object* py_point1; // from generate_py()
	BPoint point2;
	Haiku_Point_Object* py_point2; // from generate_py()
	BPoint point3;
	Haiku_Point_Object* py_point3; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OOO|O", &py_point1, &py_point2, &py_point3, &py_p);
	if (py_point1 != NULL) {
		memcpy((void*)&point1, (void*)((Haiku_Point_Object*)py_point1)->cpp_object, sizeof(BPoint));
	}
	if (py_point2 != NULL) {
		memcpy((void*)&point2, (void*)((Haiku_Point_Object*)py_point2)->cpp_object, sizeof(BPoint));
	}
	if (py_point3 != NULL) {
		memcpy((void*)&point3, (void*)((Haiku_Point_Object*)py_point3)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeTriangle(point1, point2, point3, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeTriangleWithinBounds(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeTriangleWithinBounds(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point1;
	Haiku_Point_Object* py_point1; // from generate_py()
	BPoint point2;
	Haiku_Point_Object* py_point2; // from generate_py()
	BPoint point3;
	Haiku_Point_Object* py_point3; // from generate_py()
	BRect bounds;
	Haiku_Rect_Object* py_bounds; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OOOO|O", &py_point1, &py_point2, &py_point3, &py_bounds, &py_p);
	if (py_point1 != NULL) {
		memcpy((void*)&point1, (void*)((Haiku_Point_Object*)py_point1)->cpp_object, sizeof(BPoint));
	}
	if (py_point2 != NULL) {
		memcpy((void*)&point2, (void*)((Haiku_Point_Object*)py_point2)->cpp_object, sizeof(BPoint));
	}
	if (py_point3 != NULL) {
		memcpy((void*)&point3, (void*)((Haiku_Point_Object*)py_point3)->cpp_object, sizeof(BPoint));
	}
	if (py_bounds != NULL) {
		memcpy((void*)&bounds, (void*)((Haiku_Rect_Object*)py_bounds)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeTriangle(point1, point2, point3, bounds, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillTriangle(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillTriangle(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point1;
	Haiku_Point_Object* py_point1; // from generate_py()
	BPoint point2;
	Haiku_Point_Object* py_point2; // from generate_py()
	BPoint point3;
	Haiku_Point_Object* py_point3; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OOO|O", &py_point1, &py_point2, &py_point3, &py_p);
	if (py_point1 != NULL) {
		memcpy((void*)&point1, (void*)((Haiku_Point_Object*)py_point1)->cpp_object, sizeof(BPoint));
	}
	if (py_point2 != NULL) {
		memcpy((void*)&point2, (void*)((Haiku_Point_Object*)py_point2)->cpp_object, sizeof(BPoint));
	}
	if (py_point3 != NULL) {
		memcpy((void*)&point3, (void*)((Haiku_Point_Object*)py_point3)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillTriangle(point1, point2, point3, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillTriangleWithinBounds(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillTriangleWithinBounds(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint point1;
	Haiku_Point_Object* py_point1; // from generate_py()
	BPoint point2;
	Haiku_Point_Object* py_point2; // from generate_py()
	BPoint point3;
	Haiku_Point_Object* py_point3; // from generate_py()
	BRect bounds;
	Haiku_Rect_Object* py_bounds; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OOOO|O", &py_point1, &py_point2, &py_point3, &py_bounds, &py_p);
	if (py_point1 != NULL) {
		memcpy((void*)&point1, (void*)((Haiku_Point_Object*)py_point1)->cpp_object, sizeof(BPoint));
	}
	if (py_point2 != NULL) {
		memcpy((void*)&point2, (void*)((Haiku_Point_Object*)py_point2)->cpp_object, sizeof(BPoint));
	}
	if (py_point3 != NULL) {
		memcpy((void*)&point3, (void*)((Haiku_Point_Object*)py_point3)->cpp_object, sizeof(BPoint));
	}
	if (py_bounds != NULL) {
		memcpy((void*)&bounds, (void*)((Haiku_Rect_Object*)py_bounds)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillTriangle(point1, point2, point3, bounds, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_rect, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeRect(rect, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_rect, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillRect(rect, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_InvertRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_InvertRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->InvertRect(rect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeRoundRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeRoundRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	float xRadius;
	float yRadius;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Off|O", &py_rect, &xRadius, &yRadius, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeRoundRect(rect, xRadius, yRadius, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillRoundRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillRoundRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	float xRadius;
	float yRadius;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Off|O", &py_rect, &xRadius, &yRadius, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillRoundRect(rect, xRadius, yRadius, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeEllipse(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeEllipse(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Off|O", &py_center, &xRadius, &yRadius, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeEllipse(center, xRadius, yRadius, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeEllipseFromRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeEllipseFromRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_rect, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeEllipse(rect, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillEllipse(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillEllipse(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Off|O", &py_center, &xRadius, &yRadius, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillEllipse(center, xRadius, yRadius, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillEllipseFromRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillEllipseFromRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_rect, &py_p);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillEllipse(rect, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeArc(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeArc(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	float startAngle;
	float arcAngle;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Offff|O", &py_center, &xRadius, &yRadius, &startAngle, &arcAngle, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeArc(center, xRadius, yRadius, startAngle, arcAngle, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeArcFromRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeArcFromRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	float startAngle;
	float arcAngle;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Offff|O", &py_center, &xRadius, &yRadius, &startAngle, &arcAngle, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeArc(center, xRadius, yRadius, startAngle, arcAngle, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillArc(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillArc(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	float startAngle;
	float arcAngle;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Offff|O", &py_center, &xRadius, &yRadius, &startAngle, &arcAngle, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillArc(center, xRadius, yRadius, startAngle, arcAngle, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillArcFromRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillArcFromRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint center;
	Haiku_Point_Object* py_center; // from generate_py()
	float xRadius;
	float yRadius;
	float startAngle;
	float arcAngle;
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Offff|O", &py_center, &xRadius, &yRadius, &startAngle, &arcAngle, &py_p);
	if (py_center != NULL) {
		memcpy((void*)&center, (void*)((Haiku_Point_Object*)py_center)->cpp_object, sizeof(BPoint));
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillArc(center, xRadius, yRadius, startAngle, arcAngle, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeBezier(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeBezier(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* controlPoints;
	Haiku_Point_Object* py_controlPoints; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_controlPoints, &py_p);
	if (py_controlPoints != NULL) {
		controlPoints = ((Haiku_Point_Object*)py_controlPoints)->cpp_object;
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeBezier(controlPoints, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillBezier(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillBezier(Haiku_View_Object* python_self, PyObject* python_args) {
	BPoint* controlPoints;
	Haiku_Point_Object* py_controlPoints; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_controlPoints, &py_p);
	if (py_controlPoints != NULL) {
		controlPoints = ((Haiku_Point_Object*)py_controlPoints)->cpp_object;
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillBezier(controlPoints, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_StrokeShape(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StrokeShape(Haiku_View_Object* python_self, PyObject* python_args) {
	BShape* shape;
	Haiku_Shape_Object* py_shape; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_shape, &py_p);
	if (py_shape != NULL) {
		shape = ((Haiku_Shape_Object*)py_shape)->cpp_object;
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->StrokeShape(shape, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_FillShape(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_FillShape(Haiku_View_Object* python_self, PyObject* python_args) {
	BShape* shape;
	Haiku_Shape_Object* py_shape; // from generate_py()
	pattern p = B_SOLID_HIGH;
	Haiku_pattern_Object* py_p; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_shape, &py_p);
	if (py_shape != NULL) {
		shape = ((Haiku_Shape_Object*)py_shape)->cpp_object;
	}
	if (py_p != NULL) {
		memcpy((void*)&p, (void*)((Haiku_pattern_Object*)py_p)->cpp_object, sizeof(pattern));
	}
	
	python_self->cpp_object->FillShape(shape, p);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_CopyBits(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_CopyBits(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect src;
	Haiku_Rect_Object* py_src; // from generate_py()
	BRect dst;
	Haiku_Rect_Object* py_dst; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_src, &py_dst);
	if (py_src != NULL) {
		memcpy((void*)&src, (void*)((Haiku_Rect_Object*)py_src)->cpp_object, sizeof(BRect));
	}
	if (py_dst != NULL) {
		memcpy((void*)&dst, (void*)((Haiku_Rect_Object*)py_dst)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->CopyBits(src, dst);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawChar(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawChar(Haiku_View_Object* python_self, PyObject* python_args) {
	char aChar;
	PyObject* py_aChar; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_aChar);
	PyString2Char(py_aChar, &aChar, 1, sizeof(char));
	
	python_self->cpp_object->DrawChar(aChar);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawCharToPoint(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawCharToPoint(Haiku_View_Object* python_self, PyObject* python_args) {
	char aChar;
	PyObject* py_aChar; // from generate_py ()
	BPoint location;
	Haiku_Point_Object* py_location; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_aChar, &py_location);
	PyString2Char(py_aChar, &aChar, 1, sizeof(char));
	if (py_location != NULL) {
		memcpy((void*)&location, (void*)((Haiku_Point_Object*)py_location)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->DrawChar(aChar, location);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawString(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawString(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	escapement_delta* delta = NULL;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s|O", &string, &py_delta);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->DrawString(string, delta);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawStringToPoint(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawStringToPoint(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	BPoint location;
	Haiku_Point_Object* py_location; // from generate_py()
	escapement_delta* delta = NULL;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sO|O", &string, &py_location, &py_delta);
	if (py_location != NULL) {
		memcpy((void*)&location, (void*)((Haiku_Point_Object*)py_location)->cpp_object, sizeof(BPoint));
	}
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->DrawString(string, location, delta);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawStringWithLength(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawStringWithLength(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	PyObject* py_string; // from generate_py ()
	int32 length;
	escapement_delta* delta = NULL;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_string, &py_delta);
	PyString_AsStringAndSize(py_string, &string, (Py_ssize_t*)&length);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->DrawString(string, length, delta);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawStringWithLengthToPoint(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawStringWithLengthToPoint(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	PyObject* py_string; // from generate_py ()
	int32 length;
	BPoint location;
	Haiku_Point_Object* py_location; // from generate_py()
	escapement_delta* delta = NULL;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO|O", &py_string, &py_location, &py_delta);
	PyString_AsStringAndSize(py_string, &string, (Py_ssize_t*)&length);
	if (py_location != NULL) {
		memcpy((void*)&location, (void*)((Haiku_Point_Object*)py_location)->cpp_object, sizeof(BPoint));
	}
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->DrawString(string, length, location, delta);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawStringToPointArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawStringToPointArray(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	BPoint* locations;
	PyObject* py_locations; // from generate_py ()
	PyObject* py_locations_element;	// from array_arg_parser()
	int32 locationCount;
	
	PyArg_ParseTuple(python_args, "sO", &string, &py_locations);
	locationCount = PyList_Size(py_locations);
	for (int i = 0; i < locationCount; i++) {
		py_locations_element = PyList_GetItem(py_locations, i);
		if (py_locations_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_locations_element != NULL) { // element code
			memcpy((void*)&locations[i], (void*)((Haiku_Point_Object*)py_locations_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	python_self->cpp_object->DrawString(string, locations, locationCount);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawStringWithLengthToPointArray(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawStringWithLengthToPointArray(Haiku_View_Object* python_self, PyObject* python_args) {
	char* string;
	PyObject* py_string; // from generate_py ()
	int32 length;
	BPoint* locations;
	PyObject* py_locations; // from generate_py ()
	PyObject* py_locations_element;	// from array_arg_parser()
	int32 locationCount;
	
	PyArg_ParseTuple(python_args, "OO", &py_string, &py_locations);
	PyString_AsStringAndSize(py_string, &string, (Py_ssize_t*)&length);
	locationCount = PyList_Size(py_locations);
	for (int i = 0; i < locationCount; i++) {
		py_locations_element = PyList_GetItem(py_locations, i);
		if (py_locations_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_locations_element != NULL) { // element code
			memcpy((void*)&locations[i], (void*)((Haiku_Point_Object*)py_locations_element)->cpp_object, sizeof(BPoint)); // element code
		} // element code
	}
	
	python_self->cpp_object->DrawString(string, length, locations, locationCount);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetFont(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetFont(Haiku_View_Object* python_self, PyObject* python_args) {
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	uint32 mask = B_FONT_ALL;
	
	PyArg_ParseTuple(python_args, "O|k", &py_font, &mask);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	
	python_self->cpp_object->SetFont(font, mask);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_GetFont(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetFont(Haiku_View_Object* python_self, PyObject* python_args) {
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py() (for outputs)
	
	python_self->cpp_object->GetFont(font);
	
	py_font = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_font->cpp_object = (BFont*)font;
	// we own this object, so we can delete it
	py_font->can_delete_cpp_object = true;
	return (PyObject*)py_font;
}

//static PyObject* Haiku_View_StringWidth(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StringWidth(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* string;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	retval = python_self->cpp_object->StringWidth(string);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_View_StringWidthWithLength(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_StringWidthWithLength(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* string;
	PyObject* py_string; // from generate_py ()
	int32 length;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_string);
	PyString_AsStringAndSize(py_string, (char**)&string, (Py_ssize_t*)&length);
	
	retval = python_self->cpp_object->StringWidth(string, length);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_View_GetStringWidths(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetStringWidths(Haiku_View_Object* python_self, PyObject* python_args) {
	char** stringArray;
	PyObject* py_stringArray; // from generate_py ()
	PyObject* py_stringArray_element;	// from array_arg_parser()
	int32* lengthArray;
	PyObject* py_lengthArray; // from generate_py ()
	PyObject* py_lengthArray_element;	// from array_arg_parser()
	int32 numStrings;
	float* widthArray;
	PyObject* py_widthArray; // from generate_py()
	PyObject* py_widthArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OO", &py_stringArray, &py_lengthArray);
	numStrings = PyList_Size(py_stringArray);
	for (int i = 0; i < numStrings; i++) {
		py_stringArray_element = PyList_GetItem(py_stringArray, i);
		if (py_stringArray_element == NULL) {
			stringArray[i] = NULL;
			continue;
		}
		stringArray[i] = (char*)PyString_AsString(py_stringArray_element); // element code
	}
	for (int i = 0; i < numStrings; i++) {
		py_lengthArray_element = PyList_GetItem(py_lengthArray, i);
		if (py_lengthArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		lengthArray[i] = (int32)PyInt_AsLong(py_lengthArray_element); // element code
	}
	
	python_self->cpp_object->GetStringWidths(stringArray, lengthArray, numStrings, widthArray);
	
	py_widthArray = PyList_New(0);
	for (int i = 0; i < numStrings; i++) {
		py_widthArray_element = Py_BuildValue("f", widthArray[i]);
		PyList_Append(py_widthArray, py_widthArray_element);
	}
	return py_widthArray;
}

//static PyObject* Haiku_View_SetFontSize(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetFontSize(Haiku_View_Object* python_self, PyObject* python_args) {
	float size;
	
	PyArg_ParseTuple(python_args, "f", &size);
	
	python_self->cpp_object->SetFontSize(size);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ForceFontAliasing(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ForceFontAliasing(Haiku_View_Object* python_self, PyObject* python_args) {
	bool enable;
	PyObject* py_enable; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enable);
	enable = (bool)(PyObject_IsTrue(py_enable));
	
	python_self->cpp_object->ForceFontAliasing(enable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_GetFontHeight(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetFontHeight(Haiku_View_Object* python_self, PyObject* python_args) {
	font_height* height;
	Haiku_font_height_Object* py_height; // from generate_py() (for outputs)
	
	python_self->cpp_object->GetFontHeight(height);
	
	py_height = (Haiku_font_height_Object*)Haiku_font_height_PyType.tp_alloc(&Haiku_font_height_PyType, 0);
	py_height->cpp_object = (font_height*)height;
	// we own this object, so we can delete it
	py_height->can_delete_cpp_object = true;
	return (PyObject*)py_height;
}

//static PyObject* Haiku_View_Invalidate(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Invalidate(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Invalidate();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_InavlidateRect(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_InavlidateRect(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect invalRect;
	Haiku_Rect_Object* py_invalRect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_invalRect);
	if (py_invalRect != NULL) {
		memcpy((void*)&invalRect, (void*)((Haiku_Rect_Object*)py_invalRect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->Invalidate(invalRect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetDiskMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetDiskMode(Haiku_View_Object* python_self, PyObject* python_args) {
	char* filename;
	long offset;
	
	PyArg_ParseTuple(python_args, "sl", &filename, &offset);
	
	python_self->cpp_object->SetDiskMode(filename, offset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_BeginPicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_BeginPicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_aPicture);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	
	python_self->cpp_object->BeginPicture(aPicture);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_AppendToPicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_AppendToPicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_aPicture);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	
	python_self->cpp_object->AppendToPicture(aPicture);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_EndPicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_EndPicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* retval;
	Haiku_Picture_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->EndPicture();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Picture_Object*)Haiku_Picture_PyType.tp_alloc(&Haiku_Picture_PyType, 0);
	py_retval->cpp_object = (BPicture*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_DrawPicture(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPicture(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_aPicture);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	
	python_self->cpp_object->DrawPicture(aPicture);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawPictureToPoint(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPictureToPoint(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_aPicture, &py_where);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->DrawPicture(aPicture, where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawPictureFromFile(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPictureFromFile(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* filename;
	long offset;
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "slO", &filename, &offset, &py_where);
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->DrawPicture(filename, offset, where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawPictureAsync(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPictureAsync(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_aPicture);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	
	python_self->cpp_object->DrawPictureAsync(aPicture);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawPictureAsyncToPoint(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPictureAsyncToPoint(Haiku_View_Object* python_self, PyObject* python_args) {
	BPicture* aPicture;
	Haiku_Picture_Object* py_aPicture; // from generate_py()
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_aPicture, &py_where);
	if (py_aPicture != NULL) {
		aPicture = ((Haiku_Picture_Object*)py_aPicture)->cpp_object;
	}
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->DrawPictureAsync(aPicture, where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DrawPictureAsyncFromFile(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawPictureAsyncFromFile(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* filename;
	long offset;
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "slO", &filename, &offset, &py_where);
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->DrawPictureAsync(filename, offset, where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetEventMask(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetEventMask(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 mask;
	uint32 options = 0;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k|k", &mask, &options);
	
	retval = python_self->cpp_object->SetEventMask(mask, options);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_EventMask(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_EventMask(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->EventMask();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_View_SetMouseEventMask(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetMouseEventMask(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 mask;
	uint32 options = 0;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k|k", &mask, &options);
	
	retval = python_self->cpp_object->SetMouseEventMask(mask, options);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetFlags(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetFlags(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 flags;
	
	PyArg_ParseTuple(python_args, "k", &flags);
	
	python_self->cpp_object->SetFlags(flags);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Flags(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Flags(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Flags();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_View_SetResizingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetResizingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 mode;
	
	PyArg_ParseTuple(python_args, "k", &mode);
	
	python_self->cpp_object->SetResizingMode(mode);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ResizingMode(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResizingMode(Haiku_View_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->ResizingMode();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_View_MoveBy(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MoveBy(Haiku_View_Object* python_self, PyObject* python_args) {
	float horizontal;
	float vertical;
	
	PyArg_ParseTuple(python_args, "ff", &horizontal, &vertical);
	
	python_self->cpp_object->MoveBy(horizontal, vertical);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_MoveTo(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MoveTo(Haiku_View_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->MoveTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ResizeBy(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResizeBy(Haiku_View_Object* python_self, PyObject* python_args) {
	float horizontal;
	float vertical;
	
	PyArg_ParseTuple(python_args, "ff", &horizontal, &vertical);
	
	python_self->cpp_object->ResizeBy(horizontal, vertical);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ResizeTo(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResizeTo(Haiku_View_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	PyArg_ParseTuple(python_args, "ff", &width, &height);
	
	python_self->cpp_object->ResizeTo(width, height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ScrollBy(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ScrollBy(Haiku_View_Object* python_self, PyObject* python_args) {
	float horizontal;
	float vertical;
	
	PyArg_ParseTuple(python_args, "ff", &horizontal, &vertical);
	
	python_self->cpp_object->ScrollBy(horizontal, vertical);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ScrollTo(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ScrollTo(Haiku_View_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->ScrollTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_MakeFocus(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_MakeFocus(Haiku_View_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_IsFocus(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_IsFocus(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFocus();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_Show(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Show(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Show();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Hide(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Hide(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Hide();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_IsHidden(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_IsHidden(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsHidden();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_Flush(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Flush(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Flush();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Sync(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Sync(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Sync();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_GetPreferredSize(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetPreferredSize(Haiku_View_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_View_ResizeToPreferred(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResizeToPreferred(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ScrollBar(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ScrollBar(Haiku_View_Object* python_self, PyObject* python_args) {
	orientation posture;
	BScrollBar* retval;
	Haiku_ScrollBar_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "i", &posture);
	
	retval = python_self->cpp_object->ScrollBar(posture);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ScrollBar_Object*)Haiku_ScrollBar_PyType.tp_alloc(&Haiku_ScrollBar_PyType, 0);
	py_retval->cpp_object = (BScrollBar*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_View_ResolveSpecifier(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResolveSpecifier(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_GetSupportedSuites(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetSupportedSuites(Haiku_View_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_View_IsPrinting(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_IsPrinting(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsPrinting();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_SetScale(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetScale(Haiku_View_Object* python_self, PyObject* python_args) {
	float scale;
	
	PyArg_ParseTuple(python_args, "f", &scale);
	
	python_self->cpp_object->SetScale(scale);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Scale(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Scale(Haiku_View_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Scale();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_View_DrawAfterChildren(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DrawAfterChildren(Haiku_View_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->DrawAfterChildren(rect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_HasHeightForWidth(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_HasHeightForWidth(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->HasHeightForWidth();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_GetHeightForWidth(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_GetHeightForWidth(Haiku_View_Object* python_self, PyObject* python_args) {
	float width;
	float min;
	float max;
	float preferred;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->GetHeightForWidth(width, &min, &max, &preferred);
	
	return Py_BuildValue("fff", min, max, preferred);
}

//static PyObject* Haiku_View_InvalidateLayout(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_InvalidateLayout(Haiku_View_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_EnableLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_EnableLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->EnableLayoutInvalidation();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_DisableLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_DisableLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DisableLayoutInvalidation();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_IsLayoutValid(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_IsLayoutValid(Haiku_View_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLayoutValid();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_View_ResetLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ResetLayoutInvalidation(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResetLayoutInvalidation();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Layout(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Layout(Haiku_View_Object* python_self, PyObject* python_args) {
	bool force;
	PyObject* py_force; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_force);
	force = (bool)(PyObject_IsTrue(py_force));
	
	python_self->cpp_object->Layout(force);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_Relayout(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_Relayout(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Relayout();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_SetTooltipWithText(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_SetTooltipWithText(Haiku_View_Object* python_self, PyObject* python_args) {
	const char* text;
	
	PyArg_ParseTuple(python_args, "s", &text);
	
	python_self->cpp_object->SetToolTip(text);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_ShowToolTip(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_ShowToolTip(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ShowToolTip();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_View_HideToolTip(Haiku_View_Object* python_self, PyObject* python_args);
static PyObject* Haiku_View_HideToolTip(Haiku_View_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->HideToolTip();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_View_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_View_Object*)a)->cpp_object == ((Haiku_View_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_View_Object*)a)->cpp_object != ((Haiku_View_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_View_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_View_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_View_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_View_Archive, METH_VARARGS, ""},
	{"AllUnarchived", (PyCFunction)Haiku_View_AllUnarchived, METH_VARARGS, ""},
	{"AllArchived", (PyCFunction)Haiku_View_AllArchived, METH_VARARGS, ""},
	{"AddChild", (PyCFunction)Haiku_View_AddChild, METH_VARARGS, ""},
	{"RemoveChild", (PyCFunction)Haiku_View_RemoveChild, METH_VARARGS, ""},
	{"CountChildren", (PyCFunction)Haiku_View_CountChildren, METH_VARARGS, ""},
	{"ChildAt", (PyCFunction)Haiku_View_ChildAt, METH_VARARGS, ""},
	{"NextSibling", (PyCFunction)Haiku_View_NextSibling, METH_VARARGS, ""},
	{"PreviousSibling", (PyCFunction)Haiku_View_PreviousSibling, METH_VARARGS, ""},
	{"RemoveSelf", (PyCFunction)Haiku_View_RemoveSelf, METH_VARARGS, ""},
	{"Window", (PyCFunction)Haiku_View_Window, METH_VARARGS, ""},
	{"BeginRectTracking", (PyCFunction)Haiku_View_BeginRectTracking, METH_VARARGS, ""},
	{"EndRectTracking", (PyCFunction)Haiku_View_EndRectTracking, METH_VARARGS, ""},
	{"GetMouse", (PyCFunction)Haiku_View_GetMouse, METH_VARARGS, ""},
	{"WithRect", (PyCFunction)Haiku_View_WithRect, METH_VARARGS, ""},
	{"FindView", (PyCFunction)Haiku_View_FindView, METH_VARARGS, ""},
	{"Parent", (PyCFunction)Haiku_View_Parent, METH_VARARGS, ""},
	{"Bounds", (PyCFunction)Haiku_View_Bounds, METH_VARARGS, ""},
	{"Frame", (PyCFunction)Haiku_View_Frame, METH_VARARGS, ""},
	{"ConvertPointToScreen", (PyCFunction)Haiku_View_ConvertPointToScreen, METH_VARARGS, ""},
	{"ConvertPointFromScreen", (PyCFunction)Haiku_View_ConvertPointFromScreen, METH_VARARGS, ""},
	{"ConvertRectToScreen", (PyCFunction)Haiku_View_ConvertRectToScreen, METH_VARARGS, ""},
	{"ConvertRectFromScreen", (PyCFunction)Haiku_View_ConvertRectFromScreen, METH_VARARGS, ""},
	{"ConvertPointToParent", (PyCFunction)Haiku_View_ConvertPointToParent, METH_VARARGS, ""},
	{"ConvertPointFromParent", (PyCFunction)Haiku_View_ConvertPointFromParent, METH_VARARGS, ""},
	{"ConvertRectToParent", (PyCFunction)Haiku_View_ConvertRectToParent, METH_VARARGS, ""},
	{"ConvertRectFromParent", (PyCFunction)Haiku_View_ConvertRectFromParent, METH_VARARGS, ""},
	{"LeftTop", (PyCFunction)Haiku_View_LeftTop, METH_VARARGS, ""},
	{"ClipToPicture", (PyCFunction)Haiku_View_ClipToPicture, METH_VARARGS, ""},
	{"ClipToInversePicture", (PyCFunction)Haiku_View_ClipToInversePicture, METH_VARARGS, ""},
	{"SetDrawingMode", (PyCFunction)Haiku_View_SetDrawingMode, METH_VARARGS, ""},
	{"DrawingMode", (PyCFunction)Haiku_View_DrawingMode, METH_VARARGS, ""},
	{"SetBlendingMode", (PyCFunction)Haiku_View_SetBlendingMode, METH_VARARGS, ""},
	{"GetBlendingMode", (PyCFunction)Haiku_View_GetBlendingMode, METH_VARARGS, ""},
	{"SetPenSize", (PyCFunction)Haiku_View_SetPenSize, METH_VARARGS, ""},
	{"PenSize", (PyCFunction)Haiku_View_PenSize, METH_VARARGS, ""},
	{"SetViewCursor", (PyCFunction)Haiku_View_SetViewCursor, METH_VARARGS, ""},
	{"SetViewColor", (PyCFunction)Haiku_View_SetViewColor, METH_VARARGS, ""},
	{"SetViewColorWithRGBA", (PyCFunction)Haiku_View_SetViewColorWithRGBA, METH_VARARGS, ""},
	{"ViewColor", (PyCFunction)Haiku_View_ViewColor, METH_VARARGS, ""},
	{"ClearViewOverlay", (PyCFunction)Haiku_View_ClearViewOverlay, METH_VARARGS, ""},
	{"SetHighColor", (PyCFunction)Haiku_View_SetHighColor, METH_VARARGS, ""},
	{"SetHighColorWithRGBA", (PyCFunction)Haiku_View_SetHighColorWithRGBA, METH_VARARGS, ""},
	{"HighColor", (PyCFunction)Haiku_View_HighColor, METH_VARARGS, ""},
	{"SetLowColor", (PyCFunction)Haiku_View_SetLowColor, METH_VARARGS, ""},
	{"SetLowColorWithRGBA", (PyCFunction)Haiku_View_SetLowColorWithRGBA, METH_VARARGS, ""},
	{"LowColor", (PyCFunction)Haiku_View_LowColor, METH_VARARGS, ""},
	{"SetLineMode", (PyCFunction)Haiku_View_SetLineMode, METH_VARARGS, ""},
	{"LineJoinMode", (PyCFunction)Haiku_View_LineJoinMode, METH_VARARGS, ""},
	{"LineCapMode", (PyCFunction)Haiku_View_LineCapMode, METH_VARARGS, ""},
	{"LineMiterLimit", (PyCFunction)Haiku_View_LineMiterLimit, METH_VARARGS, ""},
	{"SetOrigin", (PyCFunction)Haiku_View_SetOrigin, METH_VARARGS, ""},
	{"SetOriginWithXY", (PyCFunction)Haiku_View_SetOriginWithXY, METH_VARARGS, ""},
	{"Origin", (PyCFunction)Haiku_View_Origin, METH_VARARGS, ""},
	{"PushState", (PyCFunction)Haiku_View_PushState, METH_VARARGS, ""},
	{"PopState", (PyCFunction)Haiku_View_PopState, METH_VARARGS, ""},
	{"MovePenTo", (PyCFunction)Haiku_View_MovePenTo, METH_VARARGS, ""},
	{"MovePenToXY", (PyCFunction)Haiku_View_MovePenToXY, METH_VARARGS, ""},
	{"MovePenBy", (PyCFunction)Haiku_View_MovePenBy, METH_VARARGS, ""},
	{"PenLocation", (PyCFunction)Haiku_View_PenLocation, METH_VARARGS, ""},
	{"StrokeLineFromPenLocation", (PyCFunction)Haiku_View_StrokeLineFromPenLocation, METH_VARARGS, ""},
	{"StrokeLine", (PyCFunction)Haiku_View_StrokeLine, METH_VARARGS, ""},
	{"BeginLineArray", (PyCFunction)Haiku_View_BeginLineArray, METH_VARARGS, ""},
	{"AddLine", (PyCFunction)Haiku_View_AddLine, METH_VARARGS, ""},
	{"EndLineArray", (PyCFunction)Haiku_View_EndLineArray, METH_VARARGS, ""},
	{"StrokePolygon", (PyCFunction)Haiku_View_StrokePolygon, METH_VARARGS, ""},
	{"StrokePolygonFromPointArray", (PyCFunction)Haiku_View_StrokePolygonFromPointArray, METH_VARARGS, ""},
	{"StrokePolygonFromPointArrayWithinBounds", (PyCFunction)Haiku_View_StrokePolygonFromPointArrayWithinBounds, METH_VARARGS, ""},
	{"FillPolygon", (PyCFunction)Haiku_View_FillPolygon, METH_VARARGS, ""},
	{"FillPolygonFromPointArray", (PyCFunction)Haiku_View_FillPolygonFromPointArray, METH_VARARGS, ""},
	{"FillPolygonFromPointArrayWithinBounds", (PyCFunction)Haiku_View_FillPolygonFromPointArrayWithinBounds, METH_VARARGS, ""},
	{"StrokeTriangle", (PyCFunction)Haiku_View_StrokeTriangle, METH_VARARGS, ""},
	{"StrokeTriangleWithinBounds", (PyCFunction)Haiku_View_StrokeTriangleWithinBounds, METH_VARARGS, ""},
	{"FillTriangle", (PyCFunction)Haiku_View_FillTriangle, METH_VARARGS, ""},
	{"FillTriangleWithinBounds", (PyCFunction)Haiku_View_FillTriangleWithinBounds, METH_VARARGS, ""},
	{"StrokeRect", (PyCFunction)Haiku_View_StrokeRect, METH_VARARGS, ""},
	{"FillRect", (PyCFunction)Haiku_View_FillRect, METH_VARARGS, ""},
	{"InvertRect", (PyCFunction)Haiku_View_InvertRect, METH_VARARGS, ""},
	{"StrokeRoundRect", (PyCFunction)Haiku_View_StrokeRoundRect, METH_VARARGS, ""},
	{"FillRoundRect", (PyCFunction)Haiku_View_FillRoundRect, METH_VARARGS, ""},
	{"StrokeEllipse", (PyCFunction)Haiku_View_StrokeEllipse, METH_VARARGS, ""},
	{"StrokeEllipseFromRect", (PyCFunction)Haiku_View_StrokeEllipseFromRect, METH_VARARGS, ""},
	{"FillEllipse", (PyCFunction)Haiku_View_FillEllipse, METH_VARARGS, ""},
	{"FillEllipseFromRect", (PyCFunction)Haiku_View_FillEllipseFromRect, METH_VARARGS, ""},
	{"StrokeArc", (PyCFunction)Haiku_View_StrokeArc, METH_VARARGS, ""},
	{"StrokeArcFromRect", (PyCFunction)Haiku_View_StrokeArcFromRect, METH_VARARGS, ""},
	{"FillArc", (PyCFunction)Haiku_View_FillArc, METH_VARARGS, ""},
	{"FillArcFromRect", (PyCFunction)Haiku_View_FillArcFromRect, METH_VARARGS, ""},
	{"StrokeBezier", (PyCFunction)Haiku_View_StrokeBezier, METH_VARARGS, ""},
	{"FillBezier", (PyCFunction)Haiku_View_FillBezier, METH_VARARGS, ""},
	{"StrokeShape", (PyCFunction)Haiku_View_StrokeShape, METH_VARARGS, ""},
	{"FillShape", (PyCFunction)Haiku_View_FillShape, METH_VARARGS, ""},
	{"CopyBits", (PyCFunction)Haiku_View_CopyBits, METH_VARARGS, ""},
	{"DrawChar", (PyCFunction)Haiku_View_DrawChar, METH_VARARGS, ""},
	{"DrawCharToPoint", (PyCFunction)Haiku_View_DrawCharToPoint, METH_VARARGS, ""},
	{"DrawString", (PyCFunction)Haiku_View_DrawString, METH_VARARGS, ""},
	{"DrawStringToPoint", (PyCFunction)Haiku_View_DrawStringToPoint, METH_VARARGS, ""},
	{"DrawStringWithLength", (PyCFunction)Haiku_View_DrawStringWithLength, METH_VARARGS, ""},
	{"DrawStringWithLengthToPoint", (PyCFunction)Haiku_View_DrawStringWithLengthToPoint, METH_VARARGS, ""},
	{"DrawStringToPointArray", (PyCFunction)Haiku_View_DrawStringToPointArray, METH_VARARGS, ""},
	{"DrawStringWithLengthToPointArray", (PyCFunction)Haiku_View_DrawStringWithLengthToPointArray, METH_VARARGS, ""},
	{"SetFont", (PyCFunction)Haiku_View_SetFont, METH_VARARGS, ""},
	{"GetFont", (PyCFunction)Haiku_View_GetFont, METH_VARARGS, ""},
	{"StringWidth", (PyCFunction)Haiku_View_StringWidth, METH_VARARGS, ""},
	{"StringWidthWithLength", (PyCFunction)Haiku_View_StringWidthWithLength, METH_VARARGS, ""},
	{"GetStringWidths", (PyCFunction)Haiku_View_GetStringWidths, METH_VARARGS, ""},
	{"SetFontSize", (PyCFunction)Haiku_View_SetFontSize, METH_VARARGS, ""},
	{"ForceFontAliasing", (PyCFunction)Haiku_View_ForceFontAliasing, METH_VARARGS, ""},
	{"GetFontHeight", (PyCFunction)Haiku_View_GetFontHeight, METH_VARARGS, ""},
	{"Invalidate", (PyCFunction)Haiku_View_Invalidate, METH_VARARGS, ""},
	{"InavlidateRect", (PyCFunction)Haiku_View_InavlidateRect, METH_VARARGS, ""},
	{"SetDiskMode", (PyCFunction)Haiku_View_SetDiskMode, METH_VARARGS, ""},
	{"BeginPicture", (PyCFunction)Haiku_View_BeginPicture, METH_VARARGS, ""},
	{"AppendToPicture", (PyCFunction)Haiku_View_AppendToPicture, METH_VARARGS, ""},
	{"EndPicture", (PyCFunction)Haiku_View_EndPicture, METH_VARARGS, ""},
	{"DrawPicture", (PyCFunction)Haiku_View_DrawPicture, METH_VARARGS, ""},
	{"DrawPictureToPoint", (PyCFunction)Haiku_View_DrawPictureToPoint, METH_VARARGS, ""},
	{"DrawPictureFromFile", (PyCFunction)Haiku_View_DrawPictureFromFile, METH_VARARGS, ""},
	{"DrawPictureAsync", (PyCFunction)Haiku_View_DrawPictureAsync, METH_VARARGS, ""},
	{"DrawPictureAsyncToPoint", (PyCFunction)Haiku_View_DrawPictureAsyncToPoint, METH_VARARGS, ""},
	{"DrawPictureAsyncFromFile", (PyCFunction)Haiku_View_DrawPictureAsyncFromFile, METH_VARARGS, ""},
	{"SetEventMask", (PyCFunction)Haiku_View_SetEventMask, METH_VARARGS, ""},
	{"EventMask", (PyCFunction)Haiku_View_EventMask, METH_VARARGS, ""},
	{"SetMouseEventMask", (PyCFunction)Haiku_View_SetMouseEventMask, METH_VARARGS, ""},
	{"SetFlags", (PyCFunction)Haiku_View_SetFlags, METH_VARARGS, ""},
	{"Flags", (PyCFunction)Haiku_View_Flags, METH_VARARGS, ""},
	{"SetResizingMode", (PyCFunction)Haiku_View_SetResizingMode, METH_VARARGS, ""},
	{"ResizingMode", (PyCFunction)Haiku_View_ResizingMode, METH_VARARGS, ""},
	{"MoveBy", (PyCFunction)Haiku_View_MoveBy, METH_VARARGS, ""},
	{"MoveTo", (PyCFunction)Haiku_View_MoveTo, METH_VARARGS, ""},
	{"ResizeBy", (PyCFunction)Haiku_View_ResizeBy, METH_VARARGS, ""},
	{"ResizeTo", (PyCFunction)Haiku_View_ResizeTo, METH_VARARGS, ""},
	{"ScrollBy", (PyCFunction)Haiku_View_ScrollBy, METH_VARARGS, ""},
	{"ScrollTo", (PyCFunction)Haiku_View_ScrollTo, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_View_MakeFocus, METH_VARARGS, ""},
	{"IsFocus", (PyCFunction)Haiku_View_IsFocus, METH_VARARGS, ""},
	{"Show", (PyCFunction)Haiku_View_Show, METH_VARARGS, ""},
	{"Hide", (PyCFunction)Haiku_View_Hide, METH_VARARGS, ""},
	{"IsHidden", (PyCFunction)Haiku_View_IsHidden, METH_VARARGS, ""},
	{"Flush", (PyCFunction)Haiku_View_Flush, METH_VARARGS, ""},
	{"Sync", (PyCFunction)Haiku_View_Sync, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_View_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_View_ResizeToPreferred, METH_VARARGS, ""},
	{"ScrollBar", (PyCFunction)Haiku_View_ScrollBar, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_View_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_View_GetSupportedSuites, METH_VARARGS, ""},
	{"IsPrinting", (PyCFunction)Haiku_View_IsPrinting, METH_VARARGS, ""},
	{"SetScale", (PyCFunction)Haiku_View_SetScale, METH_VARARGS, ""},
	{"Scale", (PyCFunction)Haiku_View_Scale, METH_VARARGS, ""},
	{"DrawAfterChildren", (PyCFunction)Haiku_View_DrawAfterChildren, METH_VARARGS, ""},
	{"HasHeightForWidth", (PyCFunction)Haiku_View_HasHeightForWidth, METH_VARARGS, ""},
	{"GetHeightForWidth", (PyCFunction)Haiku_View_GetHeightForWidth, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_View_InvalidateLayout, METH_VARARGS, ""},
	{"EnableLayoutInvalidation", (PyCFunction)Haiku_View_EnableLayoutInvalidation, METH_VARARGS, ""},
	{"DisableLayoutInvalidation", (PyCFunction)Haiku_View_DisableLayoutInvalidation, METH_VARARGS, ""},
	{"IsLayoutValid", (PyCFunction)Haiku_View_IsLayoutValid, METH_VARARGS, ""},
	{"ResetLayoutInvalidation", (PyCFunction)Haiku_View_ResetLayoutInvalidation, METH_VARARGS, ""},
	{"Layout", (PyCFunction)Haiku_View_Layout, METH_VARARGS, ""},
	{"Relayout", (PyCFunction)Haiku_View_Relayout, METH_VARARGS, ""},
	{"SetTooltipWithText", (PyCFunction)Haiku_View_SetTooltipWithText, METH_VARARGS, ""},
	{"ShowToolTip", (PyCFunction)Haiku_View_ShowToolTip, METH_VARARGS, ""},
	{"HideToolTip", (PyCFunction)Haiku_View_HideToolTip, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_View_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.View";
	type->tp_basicsize   = sizeof(Haiku_View_Object);
	type->tp_dealloc     = (destructor)Haiku_View_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_View_RichCompare;
	type->tp_methods     = Haiku_View_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Handler_PyType;
	type->tp_init        = (initproc)Haiku_View_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

