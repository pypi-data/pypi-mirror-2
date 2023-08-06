/*
 * Automatically generated file
 */

#include "CustomWindow.h"

Custom_BWindow::Custom_BWindow(BRect frame, const char* title, window_type type, uint32 flags, uint32 workspaces)
	: BWindow(frame, title, type, flags, workspaces) {}

Custom_BWindow::Custom_BWindow(BRect frame, const char* title, window_look look, window_feel feel, uint32 flags, uint32 workspaces)
	: BWindow(frame, title, look, feel, flags, workspaces) {}

Custom_BWindow::Custom_BWindow(BMessage* archive)
	: BWindow(archive) {}

Custom_BWindow::~Custom_BWindow() {	
	// if we still have a python object,
	// remove ourselves from it
	if (python_object != NULL) {
		python_object->cpp_object = NULL;
		python_object->can_delete_cpp_object = false;
	}
}

void Custom_BWindow::MessageReceived(BMessage* message) {
	if (python_object == NULL) {
		return BWindow::MessageReceived(message);
	}
	else {
		// defs
		Haiku_Message_Object* py_message; // from as_python_call()
		
		// set values
		py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
		py_message->cpp_object = (BMessage*)message;
		// cannot delete this object; we do not own it
		py_message->can_delete_cpp_object = false;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MessageReceived", (char*)"O", py_message);
	}
} // Custom_BWindow::MessageReceived

void Custom_BWindow::FrameMoved(BPoint newPosition) {
	if (python_object == NULL) {
		return BWindow::FrameMoved(newPosition);
	}
	else {
		// defs
		Haiku_Point_Object* py_newPosition; // from as_python_call()
		
		// set values
		py_newPosition = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_newPosition->cpp_object = (BPoint*)&newPosition;
		// we own this object, so we can delete it
		py_newPosition->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"FrameMoved", (char*)"O", py_newPosition);
	}
} // Custom_BWindow::FrameMoved

void Custom_BWindow::WorkspacesChanged(uint32 oldWorkspaces, uint32 newWorkspaces) {
	if (python_object == NULL) {
		return BWindow::WorkspacesChanged(oldWorkspaces, newWorkspaces);
	}
	else {
		// defs
		PyObject* py_oldWorkspaces; // from as_python_call()
		PyObject* py_newWorkspaces; // from as_python_call()
		
		// set values
		py_oldWorkspaces = Py_BuildValue("k", oldWorkspaces);
		py_newWorkspaces = Py_BuildValue("k", newWorkspaces);
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"WorkspacesChanged", (char*)"kk", py_oldWorkspaces, py_newWorkspaces);
	}
} // Custom_BWindow::WorkspacesChanged

void Custom_BWindow::WorkspaceActivated(int32 workspaces, bool state) {
	if (python_object == NULL) {
		return BWindow::WorkspaceActivated(workspaces, state);
	}
	else {
		// defs
		PyObject* py_workspaces; // from as_python_call()
		PyObject* py_state; // from as_python_call()
		
		// set values
		py_workspaces = Py_BuildValue("l", workspaces);
		py_state = Py_BuildValue("b", (state ? 1 : 0));
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"WorkspaceActivated", (char*)"lO", py_workspaces, py_state);
	}
} // Custom_BWindow::WorkspaceActivated

void Custom_BWindow::FrameResized(float newWidth, float newHeight) {
	if (python_object == NULL) {
		return BWindow::FrameResized(newWidth, newHeight);
	}
	else {
		// defs
		PyObject* py_newWidth; // from as_python_call()
		PyObject* py_newHeight; // from as_python_call()
		
		// set values
		py_newWidth = Py_BuildValue("f", newWidth);
		py_newHeight = Py_BuildValue("f", newHeight);
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"FrameResized", (char*)"ff", py_newWidth, py_newHeight);
	}
} // Custom_BWindow::FrameResized

void Custom_BWindow::Zoom(BPoint origin, float width, float height) {
	if (python_object == NULL) {
		return BWindow::Zoom(origin, width, height);
	}
	else {
		// defs
		Haiku_Point_Object* py_origin; // from as_python_call()
		PyObject* py_width; // from as_python_call()
		PyObject* py_height; // from as_python_call()
		
		// set values
		py_origin = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_origin->cpp_object = (BPoint*)&origin;
		// we own this object, so we can delete it
		py_origin->can_delete_cpp_object = true;
		py_width = Py_BuildValue("f", width);
		py_height = Py_BuildValue("f", height);
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"Zoom", (char*)"Off", py_origin, py_width, py_height);
	}
} // Custom_BWindow::Zoom

void Custom_BWindow::ScreenChanged(BRect screenSize, color_space format) {
	if (python_object == NULL) {
		return BWindow::ScreenChanged(screenSize, format);
	}
	else {
		// defs
		Haiku_Rect_Object* py_screenSize; // from as_python_call()
		PyObject* py_format; // from as_python_call()
		
		// set values
		py_screenSize = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
		py_screenSize->cpp_object = (BRect*)&screenSize;
		// we own this object, so we can delete it
		py_screenSize->can_delete_cpp_object = true;
		py_format = Py_BuildValue("i", format);
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"ScreenChanged", (char*)"Oi", py_screenSize, py_format);
	}
} // Custom_BWindow::ScreenChanged

void Custom_BWindow::MenusBeginning() {
	if (python_object == NULL) {
		return BWindow::MenusBeginning();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MenusBeginning", NULL);
	}
} // Custom_BWindow::MenusBeginning

void Custom_BWindow::MenusEnded() {
	if (python_object == NULL) {
		return BWindow::MenusEnded();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MenusEnded", NULL);
	}
} // Custom_BWindow::MenusEnded

void Custom_BWindow::WindowActivated(bool state) {
	if (python_object == NULL) {
		return BWindow::WindowActivated(state);
	}
	else {
		// defs
		PyObject* py_state; // from as_python_call()
		
		// set values
		py_state = Py_BuildValue("b", (state ? 1 : 0));
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"WindowActivated", (char*)"O", py_state);
	}
} // Custom_BWindow::WindowActivated

bool Custom_BWindow::QuitRequested() {
	if (python_object == NULL) {
		return BWindow::QuitRequested();
	}
	else {
		// for returning to caller
		bool retval;
		PyObject* py_retval;	// from as_python_return()
		
		// call the proper method
		py_retval = PyObject_CallMethod((PyObject*)python_object, (char*)"QuitRequested", NULL);
		
		// process return
		retval = (bool)(PyObject_IsTrue(py_retval));
		
		return retval;
	}
} // Custom_BWindow::QuitRequested

