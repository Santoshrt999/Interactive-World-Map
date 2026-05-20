import math
import numpy as np
import moderngl
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QImage
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtOpenGLWidgets import QOpenGLWidget

from .model import MapModel, TILE_SIZE


class GlassPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(
            "background: rgba(18, 22, 34, 0.72); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px;"
        )


class MapCanvas(QOpenGLWidget):
    viewChanged = pyqtSignal(float, float, int)
    inspectRequested = pyqtSignal(float, float)
    hoverRequested = pyqtSignal(float, float)

    def __init__(self, model: MapModel, parent=None):
        super().__init__(parent)
        self.model = model
        self.last_pos = QPoint()
        self.dragging = False
        self.pan_velocity = [0.0, 0.0]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setMouseTracking(True)
        self.tile_program = None
        self.globe_program = None
        self.line_program = None
        self.quad_vao = None
        self.globe_vao = None
        self.sphere_vertex_count = 0

    def initializeGL(self):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = moderngl.BLEND_DEFAULT
        self._build_shaders()
        self._build_geometry()

    def _build_shaders(self):
        self.tile_program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_position;
                uniform vec2 u_offset;
                uniform vec2 u_scale;
                out vec2 v_uv;
                void main() {
                    v_uv = in_position * 0.5 + 0.5;
                    vec2 pos = in_position * u_scale + u_offset;
                    gl_Position = vec4(pos, 0.0, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                uniform sampler2D u_texture;
                in vec2 v_uv;
                out vec4 f_color;
                void main() {
                    f_color = texture(u_texture, v_uv);
                }
            """,
        )
        self.globe_program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                uniform mat4 u_mvp;
                out vec3 v_position;
                void main() {
                    v_position = in_position;
                    gl_Position = u_mvp * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                in vec3 v_position;
                out vec4 f_color;
                void main() {
                    float brightness = dot(normalize(v_position), vec3(0.0, 0.8, 0.6));
                    float shade = 0.16 + 0.84 * brightness;
                    f_color = vec4(vec3(0.10, 0.40, 0.82) * shade, 1.0);
                }
            """,
        )
        self.line_program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec3 in_position;
                uniform mat4 u_mvp;
                void main() {
                    gl_Position = u_mvp * vec4(in_position, 1.0);
                }
            """,
            fragment_shader="""
                #version 330
                uniform vec4 u_color;
                out vec4 f_color;
                void main() {
                    f_color = u_color;
                }
            """,
        )

    def _build_geometry(self):
        quad = np.array(
            [
                -1.0,
                -1.0,
                1.0,
                -1.0,
                -1.0,
                1.0,
                1.0,
                1.0,
            ], dtype="f4"
        )
        self.quad_vbo = self.ctx.buffer(quad.tobytes())
        self.quad_vao = self.ctx.simple_vertex_array(self.tile_program, self.quad_vbo, "in_position")
        self._build_globe_geometry(32, 64)

    def _build_globe_geometry(self, lat_steps: int, lon_steps: int):
        vertices = []
        for i in range(lat_steps + 1):
            theta = math.pi * (i / lat_steps - 0.5)
            for j in range(lon_steps + 1):
                phi = 2.0 * math.pi * j / lon_steps
                x = math.cos(theta) * math.cos(phi)
                y = math.sin(theta)
                z = math.cos(theta) * math.sin(phi)
                vertices.extend((x, y, z))
        vertices = np.array(vertices, dtype="f4")
        indices = []
        for i in range(lat_steps):
            for j in range(lon_steps + 1):
                indices.append(i * (lon_steps + 1) + j)
                indices.append((i + 1) * (lon_steps + 1) + j)
        self.sphere_vertex_count = len(indices)
        self.globe_vbo = self.ctx.buffer(vertices.tobytes())
        self.globe_ibo = self.ctx.buffer(np.array(indices, dtype="i4").tobytes())
        self.globe_vao = self.ctx.vertex_array(
            self.globe_program,
            [(self.globe_vbo, "3f", "in_position")],
            self.globe_ibo,
        )

    def resizeGL(self, width: int, height: int):
        self.ctx.viewport = (0, 0, width, height)

    def paintGL(self):
        self.ctx.clear(0.05, 0.08, 0.14, 1.0)
        if self.model.mode == "projection":
            self._draw_projection()
        else:
            self._draw_globe()
        self._draw_feature_overlays()
        self._draw_highlights()
        self._draw_notifications()

    def _draw_projection(self):
        width = self.width()
        height = self.height()
        z = int(self.model.zoom)
        center_x, center_y = self.model.lonlat_to_tile(self.model.center_lon, self.model.center_lat, z)
        half_tiles_x = width / TILE_SIZE / 2.0 + 1.5
        half_tiles_y = height / TILE_SIZE / 2.0 + 1.5
        x_start = int(math.floor(center_x - half_tiles_x))
        x_end = int(math.ceil(center_x + half_tiles_x))
        y_start = int(math.floor(center_y - half_tiles_y))
        y_end = int(math.ceil(center_y + half_tiles_y))
        for tx in range(x_start, x_end + 1):
            for ty in range(y_start, y_end + 1):
                tile = self.model.fetch_tile_image(tx % (2**z), ty % (2**z), z)
                texture = self._texture_from_qimage(tile)
                texture.use(0)
                self.tile_program["u_texture"].value = 0
                x_center = (tx - center_x) * TILE_SIZE + width / 2.0
                y_center = (ty - center_y) * TILE_SIZE + height / 2.0
                x_ndc = (x_center / width) * 2.0 - 1.0
                y_ndc = 1.0 - (y_center / height) * 2.0
                self.tile_program["u_offset"].value = (x_ndc, y_ndc)
                self.tile_program["u_scale"].value = (TILE_SIZE / width, TILE_SIZE / height)
                self.quad_vao.render(moderngl.TRIANGLE_STRIP)
                texture.release()

    def _draw_globe(self):
        self.ctx.enable(moderngl.DEPTH_TEST)
        aspect = self.width() / max(self.height(), 1)
        projection = self._perspective(45.0, aspect, 0.1, 100.0)
        view = self._look_at((0.0, 0.0, 2.8), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
        mvp = projection @ view
        self.globe_program["u_mvp"].write(mvp.astype("f4").tobytes())
        self.globe_vao.render(mode=moderngl.TRIANGLE_STRIP)
        self.ctx.disable(moderngl.DEPTH_TEST)

    def _draw_feature_overlays(self):
        if self.model.mode == "projection":
            self.ctx.disable(moderngl.DEPTH_TEST)
            identity = np.eye(4, dtype="f4")
            for feature in self.model.features:
                fill_color = self.model.get_overlay_color(feature)
                outline_color = (0.90, 0.92, 0.98, 0.75)
                for ring in self._feature_rings(feature):
                    vertices = self._build_ring_vertices(ring)
                    if vertices.size < 9:
                        continue
                    vbo = self.ctx.buffer(vertices.tobytes())
                    vao = self.ctx.simple_vertex_array(self.line_program, vbo, "in_position")
                    self.line_program["u_mvp"].write(identity.tobytes())
                    self.line_program["u_color"].value = fill_color
                    vao.render(mode=moderngl.TRIANGLE_FAN)
                    self.line_program["u_color"].value = outline_color
                    vao.render(mode=moderngl.LINE_LOOP)
                    vbo.release()
        else:
            self.ctx.disable(moderngl.DEPTH_TEST)
            aspect = self.width() / max(self.height(), 1)
            mvp = self._perspective(45.0, aspect, 0.1, 100.0) @ self._look_at((0.0, 0.0, 2.8), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
            for feature in self.model.features:
                fill_color = self.model.get_overlay_color(feature)
                outline_color = (0.98, 0.98, 1.0, 0.82)
                self.line_program["u_mvp"].write(mvp.astype("f4").tobytes())
                for ring in self._feature_rings(feature):
                    vertices = self._build_globe_ring(ring)
                    if vertices.size < 9:
                        continue
                    vbo = self.ctx.buffer(vertices.tobytes())
                    vao = self.ctx.simple_vertex_array(self.line_program, vbo, "in_position")
                    self.line_program["u_color"].value = fill_color
                    vao.render(mode=moderngl.TRIANGLE_FAN)
                    self.line_program["u_color"].value = outline_color
                    vao.render(mode=moderngl.LINE_LOOP)
                    vbo.release()

    def _draw_highlights(self):
        highlight = self.model.selected_feature or self.model.hovered_feature
        if not highlight:
            return
        color = (1.00, 0.96, 0.30, 0.98) if self.model.selected_feature else (1.00, 1.00, 1.00, 0.7)
        border = (1.00, 0.60, 0.10, 0.95) if self.model.selected_feature else (0.98, 0.98, 0.98, 0.85)
        if self.model.mode == "projection":
            self.line_program["u_mvp"].write(np.eye(4, dtype="f4").tobytes())
            for ring in self._feature_rings(highlight):
                vertices = self._build_ring_vertices(ring)
                if vertices.size < 9:
                    continue
                vbo = self.ctx.buffer(vertices.tobytes())
                vao = self.ctx.simple_vertex_array(self.line_program, vbo, "in_position")
                self.line_program["u_color"].value = color
                vao.render(mode=moderngl.TRIANGLE_FAN)
                self.line_program["u_color"].value = border
                vao.render(mode=moderngl.LINE_LOOP)
                vbo.release()
        else:
            aspect = self.width() / max(self.height(), 1)
            mvp = self._perspective(45.0, aspect, 0.1, 100.0) @ self._look_at((0.0, 0.0, 2.8), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))
            self.line_program["u_mvp"].write(mvp.astype("f4").tobytes())
            for ring in self._feature_rings(highlight):
                vertices = self._build_globe_ring(ring)
                if vertices.size < 9:
                    continue
                vbo = self.ctx.buffer(vertices.tobytes())
                vao = self.ctx.simple_vertex_array(self.line_program, vbo, "in_position")
                self.line_program["u_color"].value = color
                vao.render(mode=moderngl.TRIANGLE_FAN)
                self.line_program["u_color"].value = border
                vao.render(mode=moderngl.LINE_LOOP)
                vbo.release()

    def _feature_rings(self, feature):
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            return geometry["coordinates"]
        if geometry["type"] == "MultiPolygon":
            return [ring for polygon in geometry["coordinates"] for ring in polygon]
        return []

    def _build_ring_vertices(self, ring) -> np.ndarray:
        width = self.width()
        height = self.height()
        z = int(self.model.zoom)
        center_x, center_y = self.model.lonlat_to_tile(self.model.center_lon, self.model.center_lat, z)
        vertices = []
        for lon, lat in ring:
            px, py = self._project_tile_coordinates(lon, lat, z)
            x_norm = (px - center_x * TILE_SIZE) / width * 2.0
            y_norm = 1.0 - (py - center_y * TILE_SIZE) / height * 2.0
            vertices.extend([x_norm, y_norm, 0.0])
        if not vertices:
            return np.array([], dtype="f4")
        return np.array(vertices, dtype="f4")

    def _build_globe_ring(self, ring) -> np.ndarray:
        vertices = []
        for lon, lat in ring:
            x = math.cos(math.radians(lat)) * math.cos(math.radians(lon))
            y = math.sin(math.radians(lat))
            z = math.cos(math.radians(lat)) * math.sin(math.radians(lon))
            vertices.extend([x, y, z])
        if not vertices:
            return np.array([], dtype="f4")
        return np.array(vertices, dtype="f4")

    @staticmethod
    def _project_tile_coordinates(lon: float, lat: float, zoom: int) -> tuple[float, float]:
        x, y = MapModel.lonlat_to_tile(lon, lat, zoom)
        return x * TILE_SIZE, y * TILE_SIZE

    def _texture_from_qimage(self, qimage: QImage) -> moderngl.Texture:
        qimage = qimage.convertToFormat(QImage.Format.Format_RGBA8888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.constBits()
        ptr.setsize(qimage.byteCount())
        texture = self.ctx.texture((width, height), 4, ptr.asstring())
        texture.build_mipmaps()
        return texture

    def _perspective(self, fov: float, aspect: float, near: float, far: float) -> np.ndarray:
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        return np.array(
            [
                [f / aspect, 0.0, 0.0, 0.0],
                [0.0, f, 0.0, 0.0],
                [0.0, 0.0, (far + near) / (near - far), -1.0],
                [0.0, 0.0, (2.0 * far * near) / (near - far), 0.0],
            ],
            dtype="f4",
        )

    @staticmethod
    def _look_at(eye, target, up) -> np.ndarray:
        eye = np.array(eye, dtype="f4")
        target = np.array(target, dtype="f4")
        up = np.array(up, dtype="f4")
        z = eye - target
        z /= np.linalg.norm(z)
        x = np.cross(up, z)
        x /= np.linalg.norm(x)
        y = np.cross(z, x)
        mat = np.eye(4, dtype="f4")
        mat[0, :3] = x
        mat[1, :3] = y
        mat[2, :3] = z
        trans = np.eye(4, dtype="f4")
        trans[:3, 3] = -eye
        return mat @ trans

    def mousePressEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.last_pos = event.position().toPoint()
            self.dragging = True
            self.pan_velocity = [0.0, 0.0]

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.position().toPoint() - self.last_pos
            self.last_pos = event.position().toPoint()
            self.pan_velocity = [delta.x() * 0.1, delta.y() * 0.1]
            self._pan(delta.x(), delta.y())
        else:
            lon, lat = self._screen_to_lonlat(event.position().x(), event.position().y())
            self.hoverRequested.emit(lon, lat)

    def wheelEvent(self, event):
        amount = int(event.angleDelta().y() / 120)
        self.model.update_zoom(amount)
        self.viewChanged.emit(self.model.center_lon, self.model.center_lat, self.model.zoom)
        self.update()

    def mouseDoubleClickEvent(self, event):
        x = event.position().x()
        y = event.position().y()
        lon, lat = self._screen_to_lonlat(x, y)
        self.inspectRequested.emit(lon, lat)

    def _screen_to_lonlat(self, x: float, y: float) -> tuple[float, float]:
        width = self.width()
        height = self.height()
        z = int(self.model.zoom)
        center_x, center_y = self.model.lonlat_to_tile(self.model.center_lon, self.model.center_lat, z)
        pixel_x = center_x * TILE_SIZE + (x - width / 2.0)
        pixel_y = center_y * TILE_SIZE + (y - height / 2.0)
        lon = pixel_x / TILE_SIZE / (2**z) * 360.0 - 180.0
        n = math.pi - 2.0 * math.pi * pixel_y / (TILE_SIZE * 2**z)
        lat = math.degrees(math.atan(math.sinh(n)))
        return lon, lat

    def _pan(self, dx: float, dy: float) -> None:
        longitude_delta = -dx * (360.0 / (TILE_SIZE * 2**self.model.zoom))
        latitude_delta = dy * (180.0 / (TILE_SIZE * 2**self.model.zoom))
        self.model.update_center(self.model.center_lon + longitude_delta, self.model.center_lat + latitude_delta)
        self.viewChanged.emit(self.model.center_lon, self.model.center_lat, self.model.zoom)
        self.update()

    def _animate(self):
        if not self.dragging and (abs(self.pan_velocity[0]) > 0.1 or abs(self.pan_velocity[1]) > 0.1):
            self._pan(self.pan_velocity[0], self.pan_velocity[1])
            self.pan_velocity[0] *= 0.88
            self.pan_velocity[1] *= 0.88
        self.update()

    def _draw_notifications(self):
        notice = self.model.get_notification()
        if not notice:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)
        painter.setPen(QColor(200, 220, 255))
        painter.setFont(QFont("Segoe UI", 10))
        painter.drawText(18, self.height() - 18, notice)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self, model: MapModel):
        super().__init__()
        self.model = model
        self.setWindowTitle("Interactive World Atlas")
        self.setMinimumSize(1280, 800)
        self.setStyleSheet("background: #0b0f18; color: #e6ecff;")
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(18, 18, 18, 18)
        main_layout.setSpacing(18)

        self.map_canvas = MapCanvas(self.model, self)
        self.map_canvas.setStyleSheet("border-radius: 24px;")

        self.sidebar = GlassPanel(self)
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(16)

        title = QLabel("World Atlas")
        title.setStyleSheet("font-size: 28px; font-weight: 700; color: #f8fafc;")
        subtitle = QLabel("Geospatial analytics dashboard with polished map overlays")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("font-size: 13px; color: #cbd5e1;")
        sidebar_layout.addWidget(title)
        sidebar_layout.addWidget(subtitle)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search countries, cities, or regions…")
        self.search_input.setStyleSheet(
            "background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); border-radius: 14px; padding: 12px; color: #eef2ff;"
        )
        sidebar_layout.addWidget(self.search_input)

        self.search_results = QListWidget()
        self.search_results.setMaximumHeight(160)
        self.search_results.setStyleSheet(
            "background: rgba(9, 13, 24, 0.92); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; color: #e2e8f0;"
        )
        sidebar_layout.addWidget(self.search_results)

        self.stats_card = GlassPanel(self)
        stats_layout = QHBoxLayout(self.stats_card)
        stats_layout.setSpacing(12)
        self.population_card = self._make_stat_tile("Total Population", "—")
        self.climate_card = self._make_stat_tile("Avg Temp", "—")
        self.gdp_card = self._make_stat_tile("Total GDP", "—")
        stats_layout.addWidget(self.population_card.parent())
        stats_layout.addWidget(self.climate_card.parent())
        stats_layout.addWidget(self.gdp_card.parent())
        sidebar_layout.addWidget(self.stats_card)

        controls_card = GlassPanel(self)
        controls_layout = QVBoxLayout(controls_card)
        controls_layout.setSpacing(12)
        filter_label = QLabel("Overlay filters")
        filter_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #e2e8f0;")
        controls_layout.addWidget(filter_label)
        self.overlay_buttons = {}
        for label, mode in [("Population", "population"), ("Climate", "climate"), ("GDP", "gdp")]:
            button = QPushButton(label)
            button.setCheckable(True)
            button.setStyleSheet(
                "QPushButton { padding: 12px; border-radius: 14px; background: rgba(255,255,255,0.08); color: #cbd5e1; }"
                "QPushButton:checked { background: rgba(96, 165, 250, 0.96); color: #ffffff; }"
            )
            if mode == self.model.overlay_mode:
                button.setChecked(True)
            self.overlay_buttons[mode] = button
            controls_layout.addWidget(button)
        sidebar_layout.addWidget(controls_card)

        self.mode_toggle = QPushButton("Toggle Globe / Projection")
        self.mode_toggle.setStyleSheet(
            "padding: 12px; border-radius: 14px; background: rgba(255,255,255,0.08); color: #e2e8f0;"
        )
        sidebar_layout.addWidget(self.mode_toggle)

        self.legend_label = QLabel(self._legend_text())
        self.legend_label.setWordWrap(True)
        self.legend_label.setStyleSheet("font-size: 12px; color: #dbeafe;")
        sidebar_layout.addWidget(self.legend_label)

        self.detail_title = QLabel("Selected region details")
        self.detail_title.setStyleSheet("font-size: 16px; font-weight: 600; color: #ffffff;")
        self.detail_stats = QLabel("Double-click a country or city to inspect the overlay details.")
        self.detail_stats.setWordWrap(True)
        self.detail_stats.setStyleSheet("font-size: 13px; color: #dbeafe;")
        sidebar_layout.addWidget(self.detail_title)
        sidebar_layout.addWidget(self.detail_stats)

        self.notice_label = QLabel("")
        self.notice_label.setWordWrap(True)
        self.notice_label.setStyleSheet("font-size: 12px; color: #a5b4fc;")
        sidebar_layout.addWidget(self.notice_label)
        sidebar_layout.addStretch(1)

        main_layout.addWidget(self.map_canvas, stretch=3)
        main_layout.addWidget(self.sidebar, stretch=1)
        self.setCentralWidget(central)

    def _make_stat_tile(self, title: str, value: str) -> QLabel:
        tile = GlassPanel(self)
        tile.setMinimumWidth(120)
        tile.setStyleSheet(
            "background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); border-radius: 18px;"
        )
        layout = QVBoxLayout(tile)
        layout.setContentsMargins(16, 14, 16, 14)
        label = QLabel(title)
        label.setStyleSheet("font-size: 11px; color: #9ca3af;")
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 20px; font-weight: 700; color: #f8fafc;")
        layout.addWidget(label)
        layout.addWidget(value_label)
        return value_label

    def _legend_text(self) -> str:
        return (
            f"Overlay: {self.model.get_overlay_label()}\n"
            "Color intensity represents the current metric range. "
            "Hover over a region for instant details. Double-click to select."
        )

    def refresh_metrics(self) -> None:
        self.population_card.setText(f"{self.model.total_population():.0f} M")
        self.climate_card.setText(f"{self.model.average_climate():.1f}°C")
        self.gdp_card.setText(f"${self.model.total_gdp():.0f} B")
        self.legend_label.setText(self._legend_text())
        selected = self.model.selected_feature or self.model.hovered_feature
        if selected:
            props = selected["properties"]
            self.detail_title.setText(props.get("name", "Region details"))
            self.detail_stats.setText(
                f"Population: {props.get('population', 0)} M\n"
                f"Climate: {props.get('climate', 0.0):.1f}°C\n"
                f"GDP: ${props.get('gdp', 0.0):.1f} B\n"
                f"Current overlay: {self.model.get_overlay_label()}"
            )
        else:
            self.detail_title.setText("Selected region details")
            self.detail_stats.setText("Double-click a country or city to inspect the overlay details.")
        self.notice_label.setText(self.model.get_notification() or "")
