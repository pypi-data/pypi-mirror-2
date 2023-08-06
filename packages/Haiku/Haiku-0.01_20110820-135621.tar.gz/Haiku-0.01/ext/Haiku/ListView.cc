/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_ListViewConstants_PyMethods[] = {
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
//static int Haiku_ListView_init(Haiku_ListView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_ListView_init(Haiku_ListView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	list_view_type type;
	uint32 resizingMode = B_FOLLOW_LEFT | B_FOLLOW_TOP;
	uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Osi|kk", &py_frame, &name, &type, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new BListView(frame, name, type, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_ListView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ListView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ListView_Object* python_self;
	const char* name;
	list_view_type type = B_SINGLE_SELECTION_LIST;
	uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ListView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "s|ik", &name, &type, &flags);
	
	python_self->cpp_object = new BListView(name, type, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_ListView_newBareBones(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ListView_newBareBones(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ListView_Object* python_self;
	list_view_type type = B_SINGLE_SELECTION_LIST;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ListView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "|i", &type);
	
	python_self->cpp_object = new BListView(type);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_ListView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_ListView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_ListView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_ListView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BListView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_ListView_DESTROY(Haiku_ListView_Object* python_self);
static void Haiku_ListView_DESTROY(Haiku_ListView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_ListView_Instantiate(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Instantiate(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ListView_Archive(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Archive(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ListView_GetPreferredSize(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_GetPreferredSize(Haiku_ListView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_ListView_ResizeToPreferred(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ResizeToPreferred(Haiku_ListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_MakeFocus(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_MakeFocus(Haiku_ListView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SetFont(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SetFont(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ListView_ScrollTo(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ScrollTo(Haiku_ListView_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->ScrollTo(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_ScrollToPoint(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ScrollToPoint(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BPoint where;
	Haiku_Point_Object* py_where; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_where);
	if (py_where != NULL) {
		memcpy((void*)&where, (void*)((Haiku_Point_Object*)py_where)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->ScrollTo(where);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_AddItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_AddItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
		((Haiku_ListItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->AddItem(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_AddItemAtIndex(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_AddItemAtIndex(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	int32 index;
	
	PyArg_ParseTuple(python_args, "Ol", &py_item, &index);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
		((Haiku_ListItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->AddItem(item, index);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_RemoveItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_RemoveItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->RemoveItem(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_RemoveItemAtIndex(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_RemoveItemAtIndex(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	python_self->cpp_object->RemoveItem(index);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_RemoveItems(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_RemoveItems(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	int32 count;
	
	PyArg_ParseTuple(python_args, "ll", &index, &count);
	
	python_self->cpp_object->RemoveItems(index, count);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SetSelectionMessage(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SetSelectionMessage(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->SetSelectionMessage(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SetInvocationMessage(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SetInvocationMessage(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->SetInvocationMessage(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SelectionMessage(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SelectionMessage(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->SelectionMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_SelectionCommand(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SelectionCommand(Haiku_ListView_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->SelectionCommand();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_InvocationMessage(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_InvocationMessage(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->InvocationMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_InvocationCommand(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_InvocationCommand(Haiku_ListView_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->InvocationCommand();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_SetListType(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SetListType(Haiku_ListView_Object* python_self, PyObject* python_args) {
	list_view_type type;
	
	PyArg_ParseTuple(python_args, "i", &type);
	
	python_self->cpp_object->SetListType(type);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_ListType(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ListType(Haiku_ListView_Object* python_self, PyObject* python_args) {
	list_view_type retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->ListType();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_ItemAt(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ItemAt(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->ItemAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_IndexAtPoint(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_IndexAtPoint(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->IndexOf(point);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_IndexOf(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_IndexOf(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->IndexOf(item);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_FirstItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_FirstItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->FirstItem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_LastItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_LastItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->LastItem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_HasItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_HasItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->HasItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_CountItems(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_CountItems(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountItems();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_MakeEmpty(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_MakeEmpty(Haiku_ListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->MakeEmpty();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_IsEmpty(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_IsEmpty(Haiku_ListView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEmpty();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_Items(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Items(Haiku_ListView_Object* python_self, PyObject* python_args) {
	const BListItem** retval;
	PyObject* py_retval; // from generate_py()
	Haiku_ListItem_Object* py_retval_element;	// from array_arg_builder
	
	retval = python_self->cpp_object->Items();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = PyList_New(0);
	for (int i = 0; i < python_self->cpp_object->CountItems(); i++) {
		py_retval_element = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
		py_retval_element->cpp_object = (BListItem*)retval[i];
		// we own this object, so we can delete it
		py_retval_element->can_delete_cpp_object = true;
		PyList_Append(py_retval, (PyObject*)py_retval_element);
	}
	return py_retval;
}

//static PyObject* Haiku_ListView_InvalidateItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_InvalidateItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	python_self->cpp_object->InvalidateItem(index);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_ScrollToSelection(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ScrollToSelection(Haiku_ListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ScrollToSelection();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_Select(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Select(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	bool extend = false;
	PyObject* py_extend; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "l|O", &index, &py_extend);
	extend = (bool)(PyObject_IsTrue(py_extend));
	
	python_self->cpp_object->Select(index, extend);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SelectMultiple(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SelectMultiple(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 from;
	int32 to;
	bool extend = false;
	PyObject* py_extend; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "ll|O", &from, &to, &py_extend);
	extend = (bool)(PyObject_IsTrue(py_extend));
	
	python_self->cpp_object->Select(from, to, extend);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_IsItemSelected(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_IsItemSelected(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->IsItemSelected(index);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_CurrentSelection(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_CurrentSelection(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index = 0;
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|l", &index);
	
	retval = python_self->cpp_object->CurrentSelection(index);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_ListView_Invoke(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Invoke(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ListView_DeselectAll(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_DeselectAll(Haiku_ListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DeselectAll();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_DeselectExcept(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_DeselectExcept(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 exceptFrom;
	int32 exceptTo;
	
	PyArg_ParseTuple(python_args, "ll", &exceptFrom, &exceptTo);
	
	python_self->cpp_object->DeselectExcept(exceptFrom, exceptTo);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_Deselect(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_Deselect(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	python_self->cpp_object->Deselect(index);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListView_SwapItems(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_SwapItems(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 a;
	int32 b;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll", &a, &b);
	
	retval = python_self->cpp_object->SwapItems(a, b);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_MoveItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_MoveItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 from;
	int32 to;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll", &from, &to);
	
	retval = python_self->cpp_object->MoveItem(from, to);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_ReplaceItem(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ReplaceItem(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "lO", &index, &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->ReplaceItem(index, item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListView_ItemFrame(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ItemFrame(Haiku_ListView_Object* python_self, PyObject* python_args) {
	int32 index;
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->ItemFrame(index);
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_ListView_ResolveSpecifier(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_ResolveSpecifier(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_ListView_GetSupportedSuites(Haiku_ListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListView_GetSupportedSuites(Haiku_ListView_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_ListView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ListView_Object*)a)->cpp_object == ((Haiku_ListView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ListView_Object*)a)->cpp_object != ((Haiku_ListView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ListView_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_ListView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"BareBones", (PyCFunction)Haiku_ListView_newBareBones, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_ListView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_ListView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_ListView_Archive, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_ListView_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_ListView_ResizeToPreferred, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_ListView_MakeFocus, METH_VARARGS, ""},
	{"SetFont", (PyCFunction)Haiku_ListView_SetFont, METH_VARARGS, ""},
	{"ScrollTo", (PyCFunction)Haiku_ListView_ScrollTo, METH_VARARGS, ""},
	{"ScrollToPoint", (PyCFunction)Haiku_ListView_ScrollToPoint, METH_VARARGS, ""},
	{"AddItem", (PyCFunction)Haiku_ListView_AddItem, METH_VARARGS, ""},
	{"AddItemAtIndex", (PyCFunction)Haiku_ListView_AddItemAtIndex, METH_VARARGS, ""},
	{"RemoveItem", (PyCFunction)Haiku_ListView_RemoveItem, METH_VARARGS, ""},
	{"RemoveItemAtIndex", (PyCFunction)Haiku_ListView_RemoveItemAtIndex, METH_VARARGS, ""},
	{"RemoveItems", (PyCFunction)Haiku_ListView_RemoveItems, METH_VARARGS, ""},
	{"SetSelectionMessage", (PyCFunction)Haiku_ListView_SetSelectionMessage, METH_VARARGS, ""},
	{"SetInvocationMessage", (PyCFunction)Haiku_ListView_SetInvocationMessage, METH_VARARGS, ""},
	{"SelectionMessage", (PyCFunction)Haiku_ListView_SelectionMessage, METH_VARARGS, ""},
	{"SelectionCommand", (PyCFunction)Haiku_ListView_SelectionCommand, METH_VARARGS, ""},
	{"InvocationMessage", (PyCFunction)Haiku_ListView_InvocationMessage, METH_VARARGS, ""},
	{"InvocationCommand", (PyCFunction)Haiku_ListView_InvocationCommand, METH_VARARGS, ""},
	{"SetListType", (PyCFunction)Haiku_ListView_SetListType, METH_VARARGS, ""},
	{"ListType", (PyCFunction)Haiku_ListView_ListType, METH_VARARGS, ""},
	{"ItemAt", (PyCFunction)Haiku_ListView_ItemAt, METH_VARARGS, ""},
	{"IndexAtPoint", (PyCFunction)Haiku_ListView_IndexAtPoint, METH_VARARGS, ""},
	{"IndexOf", (PyCFunction)Haiku_ListView_IndexOf, METH_VARARGS, ""},
	{"FirstItem", (PyCFunction)Haiku_ListView_FirstItem, METH_VARARGS, ""},
	{"LastItem", (PyCFunction)Haiku_ListView_LastItem, METH_VARARGS, ""},
	{"HasItem", (PyCFunction)Haiku_ListView_HasItem, METH_VARARGS, ""},
	{"CountItems", (PyCFunction)Haiku_ListView_CountItems, METH_VARARGS, ""},
	{"MakeEmpty", (PyCFunction)Haiku_ListView_MakeEmpty, METH_VARARGS, ""},
	{"IsEmpty", (PyCFunction)Haiku_ListView_IsEmpty, METH_VARARGS, ""},
	{"Items", (PyCFunction)Haiku_ListView_Items, METH_VARARGS, ""},
	{"InvalidateItem", (PyCFunction)Haiku_ListView_InvalidateItem, METH_VARARGS, ""},
	{"ScrollToSelection", (PyCFunction)Haiku_ListView_ScrollToSelection, METH_VARARGS, ""},
	{"Select", (PyCFunction)Haiku_ListView_Select, METH_VARARGS, ""},
	{"SelectMultiple", (PyCFunction)Haiku_ListView_SelectMultiple, METH_VARARGS, ""},
	{"IsItemSelected", (PyCFunction)Haiku_ListView_IsItemSelected, METH_VARARGS, ""},
	{"CurrentSelection", (PyCFunction)Haiku_ListView_CurrentSelection, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_ListView_Invoke, METH_VARARGS, ""},
	{"DeselectAll", (PyCFunction)Haiku_ListView_DeselectAll, METH_VARARGS, ""},
	{"DeselectExcept", (PyCFunction)Haiku_ListView_DeselectExcept, METH_VARARGS, ""},
	{"Deselect", (PyCFunction)Haiku_ListView_Deselect, METH_VARARGS, ""},
	{"SwapItems", (PyCFunction)Haiku_ListView_SwapItems, METH_VARARGS, ""},
	{"MoveItem", (PyCFunction)Haiku_ListView_MoveItem, METH_VARARGS, ""},
	{"ReplaceItem", (PyCFunction)Haiku_ListView_ReplaceItem, METH_VARARGS, ""},
	{"ItemFrame", (PyCFunction)Haiku_ListView_ItemFrame, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_ListView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_ListView_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ListView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ListView";
	type->tp_basicsize   = sizeof(Haiku_ListView_Object);
	type->tp_dealloc     = (destructor)Haiku_ListView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ListView_RichCompare;
	type->tp_methods     = Haiku_ListView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_ListView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = PyTuple_Pack(2, &Haiku_View_PyType, &Haiku_Invoker_PyType);
}

