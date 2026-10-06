import csv
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

CSV_FILE = "data.csv"


class CRUDApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_data_from_csv()

    def initUI(self):
        self.setWindowTitle("Data Management System")
        self.setGeometry(100, 100, 720, 520)

        # Apply Modern Dark Theme Styling
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 13px;
            }
            QLabel {
                font-weight: bold;
                color: #89b4fa;
            }
            QLineEdit {
                background-color: #313244;
                border: 2px solid #45475a;
                border-radius: 6px;
                padding: 6px 10px;
                color: #cdd6f4;
            }
            QLineEdit:focus {
                border: 2px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #11111b;
                font-weight: bold;
                border-radius: 6px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            #deleteBtn {
                background-color: #f38ba8;
                color: #11111b;
            }
            #deleteBtn:hover {
                background-color: #f5e0dc;
            }
            #clearBtn {
                background-color: #6c7086;
                color: #ffffff;
            }
            #clearBtn:hover {
                background-color: #9399b2;
            }
            QTableWidget {
                background-color: #181825;
                border: 1px solid #45475a;
                border-radius: 8px;
                gridline-color: #313244;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #45475a;
                color: #89b4fa;
            }
            QHeaderView::section {
                background-color: #313244;
                color: #89b4fa;
                font-weight: bold;
                padding: 6px;
                border: 1px solid #181825;
            }
        """)

        # Main Vertical Layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Title Label
        title_label = QLabel("CRUD Data Management System")
        title_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #cba6f7; padding-bottom: 5px;"
        )
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # --- Form Inputs Layout ---
        form_layout = QHBoxLayout()
        form_layout.setSpacing(10)

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter ID")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Name")

        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("Enter Role / Course")

        form_layout.addWidget(QLabel("ID:"))
        form_layout.addWidget(self.id_input)
        form_layout.addWidget(QLabel("Name:"))
        form_layout.addWidget(self.name_input)
        form_layout.addWidget(QLabel("Role:"))
        form_layout.addWidget(self.role_input)

        main_layout.addLayout(form_layout)

        # --- Action Buttons Layout ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.add_btn = QPushButton("Add Record")
        self.add_btn.clicked.connect(self.add_record)

        self.update_btn = QPushButton("Update Selected")
        self.update_btn.clicked.connect(self.update_record)

        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.clicked.connect(self.delete_record)

        self.clear_btn = QPushButton("Clear Fields")
        self.clear_btn.setObjectName("clearBtn")
        self.clear_btn.clicked.connect(self.clear_inputs)

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.update_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.clear_btn)

        main_layout.addLayout(btn_layout)

        # --- Data Table Setup ---
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Role / Course"])
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.cellClicked.connect(self.on_table_click)

        main_layout.addWidget(self.table)

        self.setLayout(main_layout)

    # --- CSV Operations (Persistence) ---
    def load_data_from_csv(self):
        """Loads record data from the CSV file into the QTableWidget."""
        self.table.setRowCount(0)
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Name", "Role"])
            return

        with open(CSV_FILE, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader, None)  # Skip header
            for row in reader:
                if row:
                    row_idx = self.table.rowCount()
                    self.table.insertRow(row_idx)
                    for col_idx, value in enumerate(row):
                        self.table.setItem(
                            row_idx, col_idx, QTableWidgetItem(value)
                        )

    def save_table_to_csv(self):
        """Saves current QTableWidget records to the CSV file."""
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Role"])
            for row in range(self.table.rowCount()):
                row_data = []
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                writer.writerow(row_data)

    # --- CRUD Functions ---
    def add_record(self):
        id_val = self.id_input.text().strip()
        name_val = self.name_input.text().strip()
        role_val = self.role_input.text().strip()

        if not id_val or not name_val or not role_val:
            QMessageBox.warning(
                self,
                "Input Warning",
                "Please fill in all input fields before adding a record.",
            )
            return

        row_idx = self.table.rowCount()
        self.table.insertRow(row_idx)
        self.table.setItem(row_idx, 0, QTableWidgetItem(id_val))
        self.table.setItem(row_idx, 1, QTableWidgetItem(name_val))
        self.table.setItem(row_idx, 2, QTableWidgetItem(role_val))

        self.save_table_to_csv()
        self.clear_inputs()
        QMessageBox.information(
            self, "Success", "Record added successfully!"
        )

    def update_record(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a record from the table to update.",
            )
            return

        self.table.setItem(
            selected_row, 0, QTableWidgetItem(self.id_input.text().strip())
        )
        self.table.setItem(
            selected_row, 1, QTableWidgetItem(self.name_input.text().strip())
        )
        self.table.setItem(
            selected_row, 2, QTableWidgetItem(self.role_input.text().strip())
        )

        self.save_table_to_csv()
        self.clear_inputs()
        QMessageBox.information(
            self, "Success", "Record updated successfully!"
        )

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(
                self,
                "Selection Required",
                "Please select a record from the table to delete.",
            )
            return

        self.table.removeRow(selected_row)
        self.save_table_to_csv()
        self.clear_inputs()
        QMessageBox.information(
            self, "Success", "Record deleted successfully!"
        )

    def on_table_click(self, row, column):
        """Populates the input fields when a row is selected in the table."""
        self.id_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.role_input.setText(self.table.item(row, 2).text())

    def clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.role_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CRUDApp()
    window.show()
    sys.exit(app.exec_())