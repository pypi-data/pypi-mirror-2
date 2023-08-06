/*
 * Automatically generated file
 */

class Custom_BWindow : public BWindow {
	public:
		Custom_BWindow(BRect frame, const char* title, window_type type, uint32 flags, uint32 workspaces);
		Custom_BWindow(BRect frame, const char* title, window_look look, window_feel feel, uint32 flags, uint32 workspaces);
		Custom_BWindow(BMessage* archive);
		virtual ~Custom_BWindow();
		void MessageReceived(BMessage* message);
		void FrameMoved(BPoint newPosition);
		void WorkspacesChanged(uint32 oldWorkspaces, uint32 newWorkspaces);
		void WorkspaceActivated(int32 workspaces, bool state);
		void FrameResized(float newWidth, float newHeight);
		void Zoom(BPoint origin, float width, float height);
		void ScreenChanged(BRect screenSize, color_space format);
		void MenusBeginning();
		void MenusEnded();
		void WindowActivated(bool state);
		bool QuitRequested();
		Haiku_CustomWindow_Object* python_object;
}; // Custom_BWindow
