# ButtonUp

(C) Scott Simpson 2026

A lightweight but capable Pygame UI library

### Element
Every UI element inherits from an Element class. This class contains the following functions:
- `handle_event(event: pygame.event.Event)`: Called every frame to handle events.
- `update(dt: float)`: Called every frame to update logic.
- `draw(surface: pygame.Surface)`: Called every frame to draw the element on the given surface.

In the update loop, they are called in the order of `handle_event` -> `update` -> `draw`.

All logic in *buttonup* is abstracted and modularized into more base classes.

*These base classes are not meant to be used directly, but rather to be inherited from to create more specific elements.*

- `PositionalElement`: An element that handles positioning of an element, including setting, getting, validating, etc. Has properties like `x`, `y`, `pos`, etc.
  - `SizedElement`: An element that handles elements with a size. Does not support setting the size directly, only internally. Has properties like `width`, `height`, `size`, etc.
      - `ResizableElement`: An element which overrides `SizedElement`, which allows setting the size directly.
  - `InteractiveElement`: An element that handles interactive elements, such as buttons, text inputs, etc. Includes a built-in state system for HOVERED, CLICKED, INACTIVE, DISABLED, etc. Allows for callbacks such as `on_click`, `on_hover`, etc. Includes arg and kwargs values for callbacks, which are automatically passed in, to simplify element creation.

- `ThemedElement`: An element that handles loading and validating themes.
- `ContainerElement`: An element that can contain other elements. Handles adding, removing, and managing child elements. Does not handle layout.

These base classes can be combined to create more specific elements, such as a `Button` which inherits from `InteractiveElement`, `ThemedElement`, and `ResizableElement`, or a `Panel` which inherits from `ContainerElement` and `ThemedElement`.


### Theming & Styling

- 'Themes' define the colors of an element.
- 'Styles' define the visual appearance of an element, such as borders, font, padding, etc.

All 'style' values in elements can be set directly from the arguments when creating the Element.
Color values are automatically set from the theme (if provided, otherwise default theme), but can be updated by using properties.

Themes should be able to customize ALL colors of the element. 


### Ownership of Elements
Elements are designed to be hybrid, which means they can be used as standalone elements, or as part of a container. When an element is added to a container, the container becomes the 'owner' of the element. The owner is responsible for calling the element's `handle_event`, `update`, and `draw` functions. When an element is removed from a container, it becomes a standalone element again.

For example, the user can create a `Label` element and use it standalone.

But there is NO global 'UI manager' or other.

### Layout Elements
Layout elements allow for automatic positioning of elements.

- VBox - Vertical layout, which stacks elements vertically.
- HBox - Horizontal layout, which stacks elements horizontally.
- Grid - Grid layout, which arranges elements in a grid.

Layouts are designed to be dynamically sized, which means they will automatically adjust their size depending on the size of the children.

However, there must be a setting to allow for a fixed size (typically for the lowest level container). Therefore, a layout can be set to a `DYNAMIC` or `FIXED` size.

### Animations & Transitions
As of v1, there will be NO built-in animations and transitions.

### Performance
Performance is not a huge issue for buttonup. However, small common-sense optimizations like 'not rendering text every frame', etc. will be implemented.

### Code Quality
The code must be written with readability and maintainability in mind. This means using clear and descriptive variable names, consistent formatting, and thorough documentation. The code should also be modular and organized in a way that makes it easy to understand and modify.

### Scope
The scope of buttonup is to provide a simple and easy-to-use UI library for Pygame.

It must be capable for Dev Menus, simple game UIs, or full-fledged desktop apps. 

However, it is not meant to be a full-fledged UI library like Qt or GTK, and therefore will not include features such as advanced layout management, complex animations, or support for multiple platforms.

As of v1, it will only support mouse input, and basic keyboard input only for text input and special elements. There will be no support for gamepad input, touch input, or other input methods.


### Usability
The library should be designed with usability in mind. This means that it should be easy to learn and use, with clear documentation and examples. 

Every element should be able to be subclassed, and should be designed to be flexible and customizable, allowing users to create their own unique UI elements by inheriting from the base classes and overriding the necessary functions.

### Errors & Handling
Errors should be strict. If an error is encountered, it should be raised immediately with a clear and descriptive error message. This will help users identify and fix issues quickly.