/*
 * Automatically generated file
 */

#include "CustomApplication.h"

Custom_BApplication::Custom_BApplication(const char* signature, status_t* error)
	: BApplication(signature, error) {}

Custom_BApplication::Custom_BApplication(BMessage* archive)
	: BApplication(archive) {}

Custom_BApplication::~Custom_BApplication() {	
	// if we still have a python object,
	// remove ourselves from it
	if (python_object != NULL) {
		python_object->cpp_object = NULL;
		python_object->can_delete_cpp_object = false;
	}
}

bool Custom_BApplication::QuitRequested() {
	if (python_object == NULL) {
		return BApplication::QuitRequested();
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
} // Custom_BApplication::QuitRequested

void Custom_BApplication::Pulse() {
	if (python_object == NULL) {
		return BApplication::Pulse();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"Pulse", NULL);
	}
} // Custom_BApplication::Pulse

void Custom_BApplication::ReadyToRun() {
	if (python_object == NULL) {
		return BApplication::ReadyToRun();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"ReadyToRun", NULL);
	}
} // Custom_BApplication::ReadyToRun

void Custom_BApplication::MessageReceived(BMessage* message) {
	if (python_object == NULL) {
		return BApplication::MessageReceived(message);
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
} // Custom_BApplication::MessageReceived

void Custom_BApplication::ArgvReceived(int32 argc, char** argv) {
	if (python_object == NULL) {
		return BApplication::ArgvReceived(argc, argv);
	}
	else {
		// defs
		PyObject* py_argv; // from as_python_call()
		PyObject* py_argv_element;	// from array_arg_builder
		
		// set values
		py_argv = PyList_New(0);
		for (int i = 0; i < argc; i++) {
			py_argv_element = Py_BuildValue("s", argv[i]);
			PyList_Append(py_argv, py_argv_element);
		}
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"ArgvReceived", (char*)"s", py_argv);
	}
} // Custom_BApplication::ArgvReceived

void Custom_BApplication::AppActivated(bool active) {
	if (python_object == NULL) {
		return BApplication::AppActivated(active);
	}
	else {
		// defs
		PyObject* py_active; // from as_python_call()
		
		// set values
		py_active = Py_BuildValue("b", (active ? 1 : 0));
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"AppActivated", (char*)"O", py_active);
	}
} // Custom_BApplication::AppActivated

void Custom_BApplication::RefsReceived(BMessage* message) {
	if (python_object == NULL) {
		return BApplication::RefsReceived(message);
	}
	else {
		// defs
		Haiku_Message_Object* py_message; // from as_python_call()
		
		// set values
		py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
		py_message->cpp_object = (BMessage*)message;
		// we own this object, so we can delete it
		py_message->can_delete_cpp_object = true;
		
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"RefsReceived", (char*)"O", py_message);
	}
} // Custom_BApplication::RefsReceived

void Custom_BApplication::AboutRequested() {
	if (python_object == NULL) {
		return BApplication::AboutRequested();
	}
	else {
		// call the proper method
		PyObject_CallMethod((PyObject*)python_object, (char*)"AboutRequested", NULL);
	}
} // Custom_BApplication::AboutRequested

