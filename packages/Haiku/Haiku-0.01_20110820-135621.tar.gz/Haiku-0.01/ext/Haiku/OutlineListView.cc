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
//static int Haiku_OutlineListView_init(Haiku_OutlineListView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_OutlineListView_init(Haiku_OutlineListView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
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
	
	python_self->cpp_object = new BOutlineListView(frame, name, type, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_OutlineListView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_OutlineListView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_OutlineListView_Object* python_self;
	const char* name;
	list_view_type type = B_SINGLE_SELECTION_LIST;
	uint32 flags = B_WILL_DRAW | B_FRAME_EVENTS | B_NAVIGABLE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_OutlineListView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "s|ik", &name, &type, &flags);
	
	python_self->cpp_object = new BOutlineListView(name, type, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_OutlineListView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_OutlineListView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_OutlineListView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_OutlineListView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BOutlineListView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_OutlineListView_DESTROY(Haiku_OutlineListView_Object* python_self);
static void Haiku_OutlineListView_DESTROY(Haiku_OutlineListView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_OutlineListView_Instantiate(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_Instantiate(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_OutlineListView_Archive(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_Archive(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_OutlineListView_AddUnder(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_AddUnder(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	BListItem* underItem;
	Haiku_ListItem_Object* py_underItem; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_item, &py_underItem);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	if (py_underItem != NULL) {
		underItem = ((Haiku_ListItem_Object*)py_underItem)->cpp_object;
	}
	
	python_self->cpp_object->AddUnder(item, underItem);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_AddItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_AddItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->AddItem(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_AddItemAtIndex(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_AddItemAtIndex(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	int32 fullListIndex;
	
	PyArg_ParseTuple(python_args, "Ol", &py_item, &fullListIndex);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->AddItem(item, fullListIndex);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_RemoveItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_RemoveItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->RemoveItem(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_RemoveItemAtIndex(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_RemoveItemAtIndex(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 fullListIndex;
	
	PyArg_ParseTuple(python_args, "l", &fullListIndex);
	
	python_self->cpp_object->RemoveItem(fullListIndex);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_RemoveItems(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_RemoveItems(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 fullListIndex;
	int32 count;
	
	PyArg_ParseTuple(python_args, "ll", &fullListIndex, &count);
	
	python_self->cpp_object->RemoveItems(fullListIndex, count);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_FullListItemAt(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListItemAt(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 fullListIndex;
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &fullListIndex);
	
	retval = python_self->cpp_object->FullListItemAt(fullListIndex);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListIndexAtPoint(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListIndexAtPoint(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->FullListIndexOf(point);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListIndexOf(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListIndexOf(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->FullListIndexOf(item);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListFirstItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListFirstItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->FullListFirstItem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListLastItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListLastItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->FullListLastItem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListHasItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListHasItem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->FullListHasItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListCountItems(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListCountItems(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FullListCountItems();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_FullListCurrentSelection(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListCurrentSelection(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 index = 0;
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|l", &index);
	
	retval = python_self->cpp_object->FullListCurrentSelection(index);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_MakeEmpty(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_MakeEmpty(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->MakeEmpty();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_FullListIsEmpty(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_FullListIsEmpty(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FullListIsEmpty();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_Superitem(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_Superitem(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->Superitem(item);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_OutlineListView_Expand(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_Expand(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->Expand(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_Collapse(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_Collapse(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* item;
	Haiku_ListItem_Object* py_item; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_ListItem_Object*)py_item)->cpp_object;
	}
	
	python_self->cpp_object->Collapse(item);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_IsExpanded(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_IsExpanded(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	int32 fullListIndex;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &fullListIndex);
	
	retval = python_self->cpp_object->IsExpanded(fullListIndex);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_ResolveSpecifier(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_ResolveSpecifier(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_OutlineListView_GetSupportedSuites(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_GetSupportedSuites(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_OutlineListView_ResizeToPreferred(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_ResizeToPreferred(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_GetPreferredSize(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_GetPreferredSize(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_OutlineListView_MakeFocus(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_MakeFocus(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_OutlineListView_CountItemsUnder(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_CountItemsUnder(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* under;
	Haiku_ListItem_Object* py_under; // from generate_py()
	bool oneLevelOnly;
	PyObject* py_oneLevelOnly; // from generate_py ()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_under, &py_oneLevelOnly);
	if (py_under != NULL) {
		under = ((Haiku_ListItem_Object*)py_under)->cpp_object;
	}
	oneLevelOnly = (bool)(PyObject_IsTrue(py_oneLevelOnly));
	
	retval = python_self->cpp_object->CountItemsUnder(under, oneLevelOnly);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_OutlineListView_ItemUnderAt(Haiku_OutlineListView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_OutlineListView_ItemUnderAt(Haiku_OutlineListView_Object* python_self, PyObject* python_args) {
	BListItem* underItem;
	Haiku_ListItem_Object* py_underItem; // from generate_py()
	bool oneLevelOnly;
	PyObject* py_oneLevelOnly; // from generate_py ()
	int32 index;
	BListItem* retval;
	Haiku_ListItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OOl", &py_underItem, &py_oneLevelOnly, &index);
	if (py_underItem != NULL) {
		underItem = ((Haiku_ListItem_Object*)py_underItem)->cpp_object;
	}
	oneLevelOnly = (bool)(PyObject_IsTrue(py_oneLevelOnly));
	
	retval = python_self->cpp_object->ItemUnderAt(underItem, oneLevelOnly, index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_ListItem_Object*)Haiku_ListItem_PyType.tp_alloc(&Haiku_ListItem_PyType, 0);
	py_retval->cpp_object = (BListItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_OutlineListView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_OutlineListView_Object*)a)->cpp_object == ((Haiku_OutlineListView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_OutlineListView_Object*)a)->cpp_object != ((Haiku_OutlineListView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_OutlineListView_PyMethods[] = {
	{"WithoutFrame", (PyCFunction)Haiku_OutlineListView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_OutlineListView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_OutlineListView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_OutlineListView_Archive, METH_VARARGS, ""},
	{"AddUnder", (PyCFunction)Haiku_OutlineListView_AddUnder, METH_VARARGS, ""},
	{"AddItem", (PyCFunction)Haiku_OutlineListView_AddItem, METH_VARARGS, ""},
	{"AddItemAtIndex", (PyCFunction)Haiku_OutlineListView_AddItemAtIndex, METH_VARARGS, ""},
	{"RemoveItem", (PyCFunction)Haiku_OutlineListView_RemoveItem, METH_VARARGS, ""},
	{"RemoveItemAtIndex", (PyCFunction)Haiku_OutlineListView_RemoveItemAtIndex, METH_VARARGS, ""},
	{"RemoveItems", (PyCFunction)Haiku_OutlineListView_RemoveItems, METH_VARARGS, ""},
	{"FullListItemAt", (PyCFunction)Haiku_OutlineListView_FullListItemAt, METH_VARARGS, ""},
	{"FullListIndexAtPoint", (PyCFunction)Haiku_OutlineListView_FullListIndexAtPoint, METH_VARARGS, ""},
	{"FullListIndexOf", (PyCFunction)Haiku_OutlineListView_FullListIndexOf, METH_VARARGS, ""},
	{"FullListFirstItem", (PyCFunction)Haiku_OutlineListView_FullListFirstItem, METH_VARARGS, ""},
	{"FullListLastItem", (PyCFunction)Haiku_OutlineListView_FullListLastItem, METH_VARARGS, ""},
	{"FullListHasItem", (PyCFunction)Haiku_OutlineListView_FullListHasItem, METH_VARARGS, ""},
	{"FullListCountItems", (PyCFunction)Haiku_OutlineListView_FullListCountItems, METH_VARARGS, ""},
	{"FullListCurrentSelection", (PyCFunction)Haiku_OutlineListView_FullListCurrentSelection, METH_VARARGS, ""},
	{"MakeEmpty", (PyCFunction)Haiku_OutlineListView_MakeEmpty, METH_VARARGS, ""},
	{"FullListIsEmpty", (PyCFunction)Haiku_OutlineListView_FullListIsEmpty, METH_VARARGS, ""},
	{"Superitem", (PyCFunction)Haiku_OutlineListView_Superitem, METH_VARARGS, ""},
	{"Expand", (PyCFunction)Haiku_OutlineListView_Expand, METH_VARARGS, ""},
	{"Collapse", (PyCFunction)Haiku_OutlineListView_Collapse, METH_VARARGS, ""},
	{"IsExpanded", (PyCFunction)Haiku_OutlineListView_IsExpanded, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_OutlineListView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_OutlineListView_GetSupportedSuites, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_OutlineListView_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_OutlineListView_GetPreferredSize, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_OutlineListView_MakeFocus, METH_VARARGS, ""},
	{"CountItemsUnder", (PyCFunction)Haiku_OutlineListView_CountItemsUnder, METH_VARARGS, ""},
	{"ItemUnderAt", (PyCFunction)Haiku_OutlineListView_ItemUnderAt, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_OutlineListView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.OutlineListView";
	type->tp_basicsize   = sizeof(Haiku_OutlineListView_Object);
	type->tp_dealloc     = (destructor)Haiku_OutlineListView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_OutlineListView_RichCompare;
	type->tp_methods     = Haiku_OutlineListView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_ListView_PyType;
	type->tp_init        = (initproc)Haiku_OutlineListView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

