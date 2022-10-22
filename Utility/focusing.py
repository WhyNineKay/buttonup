from buttonup.Elements.element import Element

class FocusedElements:
    def __init__(self) -> None:
        self._type_elements = set()

    @property
    def type_elements(self) -> list[Element]:
        return list(self._type_elements)

    def is_type_focused(self, element_type: Element) -> bool:
        """
        Is the type of element focused.
        :param element_type: The type of the element. Must be a subclass of Element.
        :return bool: If the element is focused.
        """

        # Use sets for performance
        return element_type in self._type_elements

    def add_focused_element(self, class_type) -> None:
        pass