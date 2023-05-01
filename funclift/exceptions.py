class FunctorValueError(Exception):
    """FunctorValueError is raised when a Functor does not contain a value."""

    __slots__ = ('functor',)

    def __init__(self, functor) -> None:
        super().__init__()
        self.functor = functor
