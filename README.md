# ButtonUp

(C) Scott Simpson 2026

A lightweight and capable Pygame UI library

*Game UI | Desktop Apps | Simulator/Debug UI*

### Overview
### Overview

Buttonup is built to stay simple without limiting capability. It offers a clean, intuitive API for creating and managing UI elements across game interfaces, desktop tools, and simulator/debug environments.

Rather than relying on a central UI manager, ButtonUp follows a user-owned approach where developers directly control and organize their elements. This keeps the system flexible, explicit, and easy to reason about as projects grow.

Each element follows a consistent structure, exposing `handle_event`, `update`, and `draw` methods. This makes integration with existing Pygame loops straightforward and predictable, while still allowing full control over behavior and rendering.


### Features
- ☑️ Modular and extensible design
- ☑️ Theming and styling support
- ☑️ Containers, layouts, alignments, etc.
- 🆗 RichText support
- 🔜 Keyboard navigation
- 🚫 Built-in animations and transitions. For now, buttonup will not support these.

### Example
**Button**
```python
import buttonup

button = buttonup.TextButton(
    x=10, y=20, text="Click me!"
)
button.draw(surface)
```
**A simple container**
```python
vbox = buttonup.VBox(
    x=50, y=50, spacing=5
)
vbox.add(button)
vbox.apply()
```

### Documentation
No documentation yet.
