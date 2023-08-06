/*
 * Automatically generated file
 */

#include "CustomTextView.h"

Custom_BTextView::Custom_BTextView(BRect frame, const char* name, BRect textRect, uint32 resizingMode, uint32 flags)
	: BTextView(frame, name, textRect, resizingMode, flags) {}

Custom_BTextView::Custom_BTextView(BRect frame, const char* name, BRect textRect, BFont* font, rgb_color* color, uint32 resizingMode, uint32 flags)
	: BTextView(frame, name, textRect, font, color, resizingMode, flags) {}

Custom_BTextView::Custom_BTextView(const char* name, uint32 flags)
	: BTextView(name, flags) {}

Custom_BTextView::Custom_BTextView(const char* name, BFont* font, rgb_color* color, uint32 flags)
	: BTextView(name, font, color, flags) {}

Custom_BTextView::Custom_BTextView(BMessage* archive)
	: BTextView(archive) {}

Custom_BTextView::~Custom_BTextView() {	
	// if we still have a python object,
	// remove ourselves from it
	if (python_object != NULL) {
		python_object->cpp_object = NULL;
		python_object->can_delete_cpp_object = false;
	}
}

void Custom_BTextView::AttachedToWindow() {
	if (python_object == NULL) {
		return BTextView::AttachedToWindow();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"AttachedToWindow", NULL);
	}
} // Custom_BTextView::AttachedToWindow

void Custom_BTextView::DetachedFromWindow() {
	if (python_object == NULL) {
		return BTextView::DetachedFromWindow();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"DetachedFromWindow", NULL);
	}
} // Custom_BTextView::DetachedFromWindow

void Custom_BTextView::Draw(BRect updateRect) {
	if (python_object == NULL) {
		return BTextView::Draw(updateRect);
	}
	else {
		// defs
		Haiku_Rect_Object* py_updateRect; // from as_python_call()
		
		// set values
		py_updateRect = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
		py_updateRect->cpp_object = (BRect*)&updateRect;
		// we own this object, so we can delete it
		py_updateRect->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"Draw", (char*)"O", py_updateRect);
	}
} // Custom_BTextView::Draw

void Custom_BTextView::MouseDown(BPoint point) {
	if (python_object == NULL) {
		return BTextView::MouseDown(point);
	}
	else {
		// defs
		Haiku_Point_Object* py_point; // from as_python_call()
		
		// set values
		py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_point->cpp_object = (BPoint*)&point;
		// we own this object, so we can delete it
		py_point->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MouseDown", (char*)"O", py_point);
	}
} // Custom_BTextView::MouseDown

void Custom_BTextView::MouseUp(BPoint point) {
	if (python_object == NULL) {
		return BTextView::MouseUp(point);
	}
	else {
		// defs
		Haiku_Point_Object* py_point; // from as_python_call()
		
		// set values
		py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_point->cpp_object = (BPoint*)&point;
		// we own this object, so we can delete it
		py_point->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MouseUp", (char*)"O", py_point);
	}
} // Custom_BTextView::MouseUp

void Custom_BTextView::MouseMoved(BPoint point, uint32 transit, BMessage* message) {
	if (python_object == NULL) {
		return BTextView::MouseMoved(point, transit, message);
	}
	else {
		// defs
		Haiku_Point_Object* py_point; // from as_python_call()
		PyObject* py_transit; // from as_python_call()
		Haiku_Message_Object* py_message; // from as_python_call()
		
		// set values
		py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_point->cpp_object = (BPoint*)&point;
		// we own this object, so we can delete it
		py_point->can_delete_cpp_object = true;
		py_transit = Py_BuildValue("k", transit);
		py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
		py_message->cpp_object = (BMessage*)message;
		// we own this object, so we can delete it
		py_message->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"MouseMoved", (char*)"OkO", py_point, py_transit, py_message);
	}
} // Custom_BTextView::MouseMoved

void Custom_BTextView::WindowActivated(bool state) {
	if (python_object == NULL) {
		return BTextView::WindowActivated(state);
	}
	else {
		// defs
		PyObject* py_state; // from as_python_call()
		
		// set values
		py_state = Py_BuildValue("b", (state ? 1 : 0));
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"WindowActivated", (char*)"O", py_state);
	}
} // Custom_BTextView::WindowActivated

void Custom_BTextView::KeyDown(const char* bytes, int32 numBytes) {
	if (python_object == NULL) {
		return BTextView::KeyDown(bytes, numBytes);
	}
	else {
		// defs
		PyObject* py_bytes; // from as_python_call()
		
		// set values
		py_bytes = Py_BuildValue("s#", bytes, numBytes);
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"KeyDown", (char*)"s", py_bytes);
	}
} // Custom_BTextView::KeyDown

void Custom_BTextView::Pulse() {
	if (python_object == NULL) {
		return BTextView::Pulse();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"Pulse", NULL);
	}
} // Custom_BTextView::Pulse

void Custom_BTextView::FrameResized(float newWidth, float newHeight) {
	if (python_object == NULL) {
		return BTextView::FrameResized(newWidth, newHeight);
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
} // Custom_BTextView::FrameResized

void Custom_BTextView::MessageReceived(BMessage* message) {
	if (python_object == NULL) {
		return BTextView::MessageReceived(message);
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
} // Custom_BTextView::MessageReceived

void Custom_BTextView::AllAttached() {
	if (python_object == NULL) {
		return BTextView::AllAttached();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"AllAttached", NULL);
	}
} // Custom_BTextView::AllAttached

void Custom_BTextView::AllDetached() {
	if (python_object == NULL) {
		return BTextView::AllDetached();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"AllDetached", NULL);
	}
} // Custom_BTextView::AllDetached

