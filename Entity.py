from collections import defaultdict
from pygame import Vector3, Vector2, Surface, mask, Rect
from typing import Any, Callable, Dict, List, Type, cast


# =====================================
# ENTITY SINGLETON METACLASS
# =====================================
class OldEntity(type):
    _instance = None
    _register: Dict[str, Any] = {}
    _entities: List[Any] = []
    _debug_mode: bool = False
    _debug_message: List[str] = []

    def __call__(cls, *args, **kwargs):
        object = super().__call__(*args, **kwargs)  # Create new instance

        OldEntity._debug_message.append(
            f"[DEBUG] Created: {object.name}"
        )  # Debug message for creation
        OldEntity._entities.append(object)  # Add to entities list
        OldEntity._register[object.name] = object  # Add to register

        return object

    def __new__(mcls, name, bases, namespace, **kwargs):
        namespace.setdefault(
            "name", name.lower()
        )  # Default name is class name in lowercase
        # Tag acts as a tree to organize assigned parents and children
        namespace.setdefault(
            "tag", "orphan entity"
        )  # Default tag is neither a parent nor a child
        namespace.setdefault(
            "position", Vector3(0, 0, 0)
        )  # Default position is (x, y, z) = (0, 0, 0) for 3D space and (x, y, z-index) = (0, 0, 0) for 2D space
        namespace.setdefault(
            "transform", Vector3(1, 1, 1)
        )  # Default transform is (scale_x, scale_y, scale_z) = (1, 1, 1) for 3D space and (scale_x, scale_y, 0) = (1, 1, 0) for 2D space
        namespace.setdefault(
            "rotation", Vector3(0, 0, 0)
        )  # Default rotation is (rot_x, rot_y, rot_z) = (0, 0, 0) for 3D space and (0, 0, rot_z) = (0, 0, 0) for 2D space
        namespace.setdefault("visible", True)  # Default visibility is True
        namespace.setdefault("active", True)  # Default activity is True

        # --- Default image for non OpenGL entities ---
        namespace.setdefault(
            "anchor", "topleft"
        )  # Default anchor is (x, y) = (0, 0) topleft corner
        namespace.setdefault("width", namespace["transform"].x)  # Default width is 16
        namespace.setdefault("height", namespace["transform"].y)  # Default height is 16
        namespace.setdefault(
            "image", Surface((namespace["width"], namespace["height"]))
        )  # Default surface is a blank surface of size (width, height)
        namespace.setdefault("color", (255, 255, 255))  # Default color is white
        namespace["image"].fill(
            namespace["color"]
        )  # Fill default surface with default color
        namespace.setdefault(
            "rect", namespace["image"].get_rect()
        )  # Default rect is the rect of the default surface
        setattr(
            namespace["rect"],
            namespace["anchor"],
            (namespace["position"].x, namespace["position"].y),
        )  # Set rect anchor to position
        namespace.setdefault(
            "mask", mask.from_surface(namespace["image"])
        )  # Default mask is the mask of the default surface

        # --- Default mesh for OpenGL entities ---
        # future i will add default values for OpenGL entities afterwards

        # --- Lifecycle methods ---
        def _refresh(self):
            """Refresh entity properties."""
            self.image.fill(self.color)  # Update image color
            self.rect = self.image.get_rect()  # Update rect
            setattr(
                self.rect, self.anchor, (self.position.x, self.position.y)
            )  # Set rect anchor to position
            self.mask = mask.from_surface(self.image)  # Update mask
            OldEntity._debug_message.append(
                f"[DEBUG] Refreshed: {self.name}"
            )  # Debug message for refresh

        # --- Inject lifecycle methods ---
        namespace.setdefault("refresh", _refresh)

        return super().__new__(mcls, name, bases, namespace)

    # =====================================
    # INITIALIZATION
    # =====================================
    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)
        if OldEntity._instance is None:
            OldEntity._instance = cls

    # =====================================
    # ENTITY MANAGEMENT
    # =====================================
    @classmethod
    def getRenderList(mcls) -> List[tuple[Surface, Rect]]:
        """Sort list of Surfaces and Rects

        Returns:
            List[tuple[Surface, Rect]]: List of
        """
        _render_list = []
        for entity in mcls._entities:
            entity.refresh()
            _render_list.append((entity.image, entity.rect))
        return _render_list

    @classmethod
    def get_instance(mcls):
        return mcls._instance

    @classmethod
    def all_entities(mcls):
        return mcls._entities

    @classmethod
    def find_by_tag(mcls, tag: str):
        return [
            entity for entity in mcls._entities if getattr(entity, "tag", None) == tag
        ]

    # =====================================
    # DEBUG CONFIGURATION
    # =====================================
    @classmethod
    def enable_debug(cls, state: bool = True):
        cls._debug_mode = state
        cls._debug_message.append(
            f"[DEBUG] Debug mode {'enabled' if state else 'disabled'}"
        )  # Debug message for enabling/disabling debug mode


class _ComponentMeta(type):
    _registry: Dict[str, Type["Component"]] = {}

    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)
        if name != "Component":
            mcls._registry[name] = cast(type[Component], cls)
        return cls


class Component(metaclass=_ComponentMeta):
    def __init_subclass__(cls, **kwargs) -> None:
        def decorator(function: Callable):
            if not hasattr(function, "_component_tags"):
                function._component_tags = []  # type: ignore[attr-defined]
            function._component_tags.append(cls)  # type: ignore[attr-defined]
            return function

        cls.__call__ = staticmethod(decorator)


class _EntityMeta(type):
    _entities: Dict[str, Type["Entity"]] = {}

    def __new__(mcls, name, bases, attrs):
        component_map = defaultdict(list)
        for attrs_name, attrs_value in attrs.items():
            if callable(attrs_value) and hasattr(attrs_value, "_component_tags"):
                for component_cls in attrs_value._component_tags:  # type: ignore[attr-defined]
                    component_map[attrs_name].append(component_cls)

        attrs["_components"] = dict(component_map)
        cls = super().__new__(mcls, name, bases, attrs)

        if name != "Entity":
            mcls._entities[name] = cast(type[Entity], cls)
        return cls


class Entity(metaclass=_EntityMeta):
    _id_conter: int = 0

    def __init__(self) -> None:
        Entity._id_conter += 1
        self.id = Entity._id_conter

    def update(self, _delta_time: float):
        pass

    def render(self):
        pass

    def info(self):
        components = {K: [C.__name__ for C in V] for K, V in self._components.items()}  # type: ignore[attr-defined]
        print(f"<{self.__class__.__name__} id ={self.id} components ={components}>")


# ============================================
# Example Components
# ============================================


class Transform(Component): ...


# ============================================
# Example Entity
# ============================================


class Player(Entity):
    @Transform()
    def __init__(self):
        super().__init__()
        print(f"Player {self.id} created")

    def update(self, dt):
        print(f"Player {self.id} updating physics dt={dt}")

    def render(self):
        print(f"Player {self.id} rendering")


if __name__ == "__main__":
    p1 = Player()
    p2 = Player()

    print("\nEntity component metadata:")
    p1.info()
    p2.info()

    print("\nUpdate/render cycle:")
    for e in [p1, p2]:
        e.update(0.016)
        e.render()
    print("\nTracked entity subclasses:")
    print(_EntityMeta._entities)
