/*
 * Automatically generated file
 */

class Custom_BTextView : public BTextView {
	public:
		Custom_BTextView(BRect frame, const char* name, BRect textRect, uint32 resizingMode, uint32 flags);
		Custom_BTextView(BRect frame, const char* name, BRect textRect, BFont* font, rgb_color* color, uint32 resizingMode, uint32 flags);
		Custom_BTextView(const char* name, uint32 flags);
		Custom_BTextView(const char* name, BFont* font, rgb_color* color, uint32 flags);
		Custom_BTextView(BMessage* archive);
		virtual ~Custom_BTextView();
		void AttachedToWindow();
		void DetachedFromWindow();
		void Draw(BRect updateRect);
		void MouseDown(BPoint point);
		void MouseUp(BPoint point);
		void MouseMoved(BPoint point, uint32 transit, BMessage* message);
		void WindowActivated(bool state);
		void KeyDown(const char* bytes, int32 numBytes);
		void Pulse();
		void FrameResized(float newWidth, float newHeight);
		void MessageReceived(BMessage* message);
		void AllAttached();
		void AllDetached();
		Haiku_CustomTextView_Object* python_object;
}; // Custom_BTextView
