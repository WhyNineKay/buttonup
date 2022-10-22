from .. Themes import themes


class Globs:
    def __init__(self) -> None:
        """Globals."""

        self._project_theme = themes.get_default_theme()
        self._focused_other = False

    @property
    def focused_other(self) -> bool:
        return self._focused_other

    @property
    def project_theme(self) -> themes.Theme:
        return self._project_theme

    @project_theme.setter
    def project_theme(self, value: themes.Theme | str) -> None:
        """
        Sets the project theme.
        :raises ValueError: if the theme is not a theme object.
        """
        if isinstance(value, str):
            theme = themes.get_theme(value)
            if value == "default":
                self._project_theme = themes.get_default_theme()
                return

            elif theme.name.lower() == "default":
                raise ValueError(f"invalid theme name: '{value}'.")

            else:
                self._project_theme = theme
                return

        if not isinstance(value, themes.Theme):
            raise ValueError("theme must be a valid theme.")
        else:
            self._project_theme = value


globs = Globs()
