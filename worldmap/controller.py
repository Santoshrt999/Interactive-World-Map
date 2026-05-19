from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem

from .model import MapModel
from .view import MainWindow


class MapController:
    def __init__(self, model: MapModel, window: MainWindow):
        self.model = model
        self.window = window
        self.map_canvas = window.map_canvas
        self._connect_signals()

    def _connect_signals(self):
        self.window.search_input.textChanged.connect(self.on_search_text)
        self.window.search_results.itemClicked.connect(self.on_search_result_clicked)
        for mode, button in self.window.overlay_buttons.items():
            button.clicked.connect(lambda checked, m=mode: self.on_overlay_toggle(m))
        self.window.mode_toggle.clicked.connect(self.on_mode_toggle)
        self.map_canvas.viewChanged.connect(self.on_view_changed)
        self.map_canvas.inspectRequested.connect(self.on_inspect_requested)
        self.map_canvas.installEventFilter(self)

    def on_search_text(self, text: str) -> None:
        suggestions = self.model.search_suggestions(text)
        self.window.search_results.clear()
        for item in suggestions:
            list_item = QListWidgetItem(item["label"])
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.window.search_results.addItem(list_item)

    def on_search_result_clicked(self, item: QListWidgetItem) -> None:
        entry = item.data(Qt.ItemDataRole.UserRole)
        if not entry:
            return
        self.model.update_center(entry["lon"], entry["lat"])
        self.window.refresh_metrics()
        self.map_canvas.update()

    def on_overlay_toggle(self, mode: str) -> None:
        self.model.set_overlay(mode)
        for key, button in self.window.overlay_buttons.items():
            button.setChecked(key == mode)
        self.window.refresh_metrics()
        self.map_canvas.update()

    def on_mode_toggle(self) -> None:
        self.model.toggle_mode()
        self.window.refresh_metrics()
        self.map_canvas.update()

    def on_view_changed(self, lon: float, lat: float, zoom: int) -> None:
        self.window.refresh_metrics()

    def on_inspect_requested(self, lon: float, lat: float) -> None:
        feature = self.model.inspect_location(lon, lat)
        if feature:
            self.window.metrics_label.setText(
                f"{feature['properties']['name']}\n"
                f"Population: {feature['properties']['population']}M\n"
                f"Climate: {feature['properties']['climate']}°C\n"
                f"GDP: ${feature['properties']['gdp']}B"
            )
        else:
            self.window.metrics_label.setText("No region found at this location.")
