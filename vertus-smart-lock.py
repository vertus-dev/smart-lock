import sys
import random
import os
import datetime
import locale
import time
import hashlib
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap, QFont, QKeySequence, QShortcut, QColor, QPainter, QBrush
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QFrame, QGridLayout, QGraphicsOpacityEffect, QComboBox,
                             QTextEdit, QProgressBar, QMessageBox)

# WebEngine için platform kontrolü
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage

    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False
    print("Uyarı: QtWebEngine mevcut değil. Web görüntüleme özellikleri devre dışı.")

try:
    locale.setlocale(locale.LC_ALL, 'tr_TR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'turkish')
    except:
        pass

# Platform kontrolü
IS_WINDOWS = sys.platform.startswith('win')
IS_LINUX = sys.platform.startswith('linux')
IS_MAC = sys.platform.startswith('darwin')


class OptimizedWebEnginePage(QWebEnginePage):
    def __init__(self, parent=None):
        super().__init__(parent)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        # JavaScript konsol mesajlarını gizle
        pass


class AppWindow(QMainWindow):
    def __init__(self, app_name, app_url, orientation="horizontal", parent=None):
        super().__init__(parent)
        self.parent = parent
        self.app_name = app_name
        self.app_url = app_url

        if orientation == "vertical":
            self.setFixedSize(400, 700)
        else:
            self.setFixedSize(1000, 600)

        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowTitleHint |
                            Qt.WindowType.WindowCloseButtonHint)
        self.setWindowTitle(f"Vertus OS - {app_name}")

        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        if WEBENGINE_AVAILABLE:
            try:
                self.browser = QWebEngineView()

                # Linux için sandbox ayarları
                if IS_LINUX:
                    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox --disable-gpu'

                self.browser.setPage(OptimizedWebEnginePage(self.browser))
                self.browser.setUrl(QtCore.QUrl(self.app_url))
                self.browser.setStyleSheet("QWebEngineView { border: none; background-color: white; }")

                settings = self.browser.settings()
                settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
                settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, False)
                settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, False)
                settings.setAttribute(QWebEngineSettings.WebAttribute.Accelerated2dCanvasEnabled, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
                settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, False)
                settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanAccessClipboard, False)
                settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, True)

                self.browser.page().setBackgroundColor(Qt.GlobalColor.white)
                layout.addWidget(self.browser)

            except Exception as e:
                print(f"WebEngine hatası: {e}")
                self.create_fallback_ui()
        else:
            self.create_fallback_ui()

    def create_fallback_ui(self):
        """WebEngine yoksa alternatif arayüz"""
        layout = self.centralWidget().layout()

        error_widget = QWidget()
        error_layout = QVBoxLayout(error_widget)

        icon_label = QLabel("🌐")
        icon_label.setStyleSheet("font-size: 64px; color: #3498db;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(icon_label)

        title_label = QLabel(f"{self.app_name}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50; margin: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(title_label)

        url_label = QLabel(f"URL: {self.app_url}")
        url_label.setStyleSheet("font-size: 14px; color: #7f8c8d; margin: 5px;")
        url_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_layout.addWidget(url_label)

        info_label = QLabel("Web görüntüleyici mevcut değil.\nURL'yi tarayıcınızda açmak için butona tıklayın.")
        info_label.setStyleSheet("font-size: 12px; color: #95a5a6; margin: 20px;")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setWordWrap(True)
        error_layout.addWidget(info_label)

        open_btn = QPushButton("Tarayıcıda Aç")
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        open_btn.clicked.connect(self.open_in_browser)
        error_layout.addWidget(open_btn)

        layout.addWidget(error_widget)

    def open_in_browser(self):
        """URL'yi sistem tarayıcısında açar"""
        try:
            if IS_WINDOWS:
                os.system(f'start "" "{self.app_url}"')
            elif IS_LINUX:
                os.system(f'xdg-open "{self.app_url}"')
            elif IS_MAC:
                os.system(f'open "{self.app_url}"')
        except Exception as e:
            print(f"Tarayıcı açma hatası: {e}")

    def closeEvent(self, event):
        if self.parent:
            self.parent.close_app_window(self.app_name)
        super().closeEvent(event)


class DeveloperNotification(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(380, 70)

        self.bg_frame = QFrame(self)
        self.bg_frame.setGeometry(0, 0, 380, 70)
        self.bg_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(41, 128, 185, 220);
                border-radius: 12px;
                border: 2px solid rgba(255, 255, 255, 150);
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.icon_label = QLabel("🔧")
        self.icon_label.setStyleSheet("QLabel { color: white; font-size: 24px; background-color: transparent; }")

        self.message_label = QLabel("Geliştirici: Yiğit Eritici")
        self.message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        self.message_label.setWordWrap(True)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.message_label, 1)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        if parent:
            self.move(parent.width() - 400, 20)

    def show_notification(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.start()
        self.show()

    def hide_notification(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()


class DeveloperTerminal(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("C:\\VERTUS\\DEV>")
        self.setFixedSize(800, 600)

        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowTitleHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
                color: #3498db;
                font-family: 'Lucida Console', 'Courier New', monospace;
            }
        """)

        self.authenticated = False
        self.login_prompt_active = False
        self.original_wallpaper = None
        self.password_mode = False
        self.actual_password = ""
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.terminal_output = QTextEdit()
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #000000;
                color: #3498db;
                border: none;
                font-family: 'Lucida Console', 'Courier New', monospace;
                font-size: 14px;
                padding: 10px;
            }
        """)
        self.terminal_output.setReadOnly(True)

        input_container = QWidget()
        input_container.setStyleSheet("background-color: #000000;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(10, 5, 10, 10)

        self.prompt_label = QLabel("C:\\VERTUS\\DEV>")
        self.prompt_label.setStyleSheet("""
            QLabel {
                color: #3498db;
                font-family: 'Lucida Console', 'Courier New', monospace;
                font-size: 14px;
                background-color: #000000;
            }
        """)

        self.command_input = QLineEdit()
        self.command_input.setStyleSheet("""
            QLineEdit {
                background-color: #000000;
                color: #3498db;
                border: none;
                font-family: 'Lucida Console', 'Courier New', monospace;
                font-size: 14px;
                selection-background-color: #154360;
            }
        """)
        self.command_input.returnPressed.connect(self.execute_command)
        self.command_input.textChanged.connect(self.on_text_changed)

        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.command_input)

        layout.addWidget(self.terminal_output)
        layout.addWidget(input_container)

        self.show_welcome_message()

    def on_text_changed(self, text):
        if self.password_mode:
            if text and not text.endswith('*'):
                if len(text) > len(self.actual_password):
                    new_char = text[-1]
                    self.actual_password += new_char
                elif len(text) < len(self.actual_password):
                    self.actual_password = self.actual_password[:-1]

                self.command_input.blockSignals(True)
                self.command_input.setText('*' * len(self.actual_password))
                self.command_input.blockSignals(False)

    def show_welcome_message(self):
        self.terminal_output.append("Microsoft Windows [Version 10.0.19044.1766]")
        self.terminal_output.append("(c) Microsoft Corporation. All rights reserved.")
        self.terminal_output.append("")
        self.terminal_output.append("C:\\VERTUS>cd DEV")
        self.terminal_output.append("")
        self.terminal_output.append("C:\\VERTUS\\DEV>vertus_dev --login")
        self.terminal_output.append("")
        self.terminal_output.append("VERTUS Developer Terminal v1.0")
        self.terminal_output.append("")

    def execute_command(self):
        command = self.command_input.text().strip()
        self.command_input.clear()

        if self.password_mode:
            actual_input = self.actual_password
            self.actual_password = ""
            self.password_mode = False
            self.handle_login(actual_input)
            return

        if self.login_prompt_active:
            self.handle_login(command)
            return

        self.terminal_output.append(f"C:\\VERTUS\\DEV>{command}")

        if command.lower() == "root":
            self.start_login_process()
        elif command.lower() == "help" or command == "?":
            self.show_help()
        elif command.lower() == "sysinfo" and self.authenticated:
            self.show_system_info()
        elif command.lower() == "exit":
            self.terminal_output.append("Terminal kapatılıyor...")
            self.restore_original_wallpaper()
            QTimer.singleShot(1000, self.close)
        elif command.lower() == "shutdown" and self.authenticated:
            self.terminal_output.append("Vertus Smart Lock kapatılıyor...")
            QTimer.singleShot(1000, sys.exit)
        elif command.lower() == "clear" or command.lower() == "cls":
            self.terminal_output.clear()
        elif command.lower() == "version" and self.authenticated:
            self.show_version()
        elif command.lower() == "status" and self.authenticated:
            self.show_status()
        elif command.lower() == "debug" and self.authenticated:
            self.show_debug_info()
        elif command.lower() == "browser" and self.authenticated:
            self.open_browser()
        else:
            self.terminal_output.append(f"'{command}' tanınmayan bir komut.")
            self.terminal_output.append("Yardım için 'help' yazın.")

        self.terminal_output.append("")

    def open_browser(self):
        if self.parent:
            self.parent.open_app_window("Tarayıcı", "https://renamc.xyz", "horizontal")

    def start_login_process(self):
        self.login_prompt_active = True
        self.terminal_output.append("Kullanıcı Adı: ")

    def handle_login(self, input_text):
        if "Kullanıcı Adı:" in self.terminal_output.toPlainText() and not hasattr(self, 'username'):
            self.username = input_text
            self.terminal_output.append(input_text)
            self.terminal_output.append("Şifre: ")
            self.password_mode = True
            self.actual_password = ""
            return

        if "Şifre:" in self.terminal_output.toPlainText() and not self.authenticated:
            password = input_text
            self.terminal_output.append("*" * len(password))
            self.terminal_output.append("")

            correct_password = "fAd473dC5BbCc+"
            if self.username == "developer" and password == correct_password:
                self.authenticated = True
                self.login_prompt_active = False
                self.password_mode = False
                self.actual_password = ""
                self.terminal_output.append("✅ Giriş başarılı!")
                self.terminal_output.append("Geliştirici: Yiğit Eritici")
                self.terminal_output.append("Sistem: Vertus OS Smart Lock v0.3.0")
                self.terminal_output.append("")
                self.terminal_output.append("Kullanılabilir komutlar için 'help' yazın.")

                self.change_to_developer_wallpaper()
                self.show_developer_notification()
            else:
                self.terminal_output.append("❌ Hatalı kullanıcı adı veya şifre!")
                self.terminal_output.append("")
                self.login_prompt_active = False
                self.password_mode = False
                self.actual_password = ""
                if hasattr(self, 'username'):
                    delattr(self, 'username')

        self.terminal_output.append("")

    def change_to_developer_wallpaper(self):
        if self.parent:
            self.original_wallpaper = getattr(self.parent, 'current_wallpaper', 'wallpaper.png')
            if os.path.exists("wallpaper2.png"):
                self.parent.current_wallpaper = "wallpaper2.png"
                self.parent.update()

    def restore_original_wallpaper(self):
        if self.parent and self.original_wallpaper:
            self.parent.current_wallpaper = self.original_wallpaper
            self.parent.update()
            if hasattr(self.parent, 'developer_notification'):
                self.parent.developer_notification.hide_notification()

    def show_developer_notification(self):
        if self.parent:
            self.parent.show_developer_login_notification()

    def closeEvent(self, event):
        self.restore_original_wallpaper()
        super().closeEvent(event)

    def show_help(self):
        if self.authenticated:
            help_text = """
Geliştirici Komutları:

help veya ?       - Bu yardım mesajını gösterir
sysinfo           - Sistem bilgilerini gösterir
version           - Versiyon bilgisi
status            - Sistem durumu
debug             - Hata ayıklama bilgileri
browser           - Tarayıcı uygulamasını açar
clear veya cls    - Ekranı temizler
shutdown          - Programı kapatır
exit              - Terminalden çıkış
"""
        else:
            help_text = """
Temel Komutlar:

root              - Geliştirici girişi yap
help veya ?       - Bu yardım mesajını gösterir
clear veya cls    - Ekranı temizler
exit              - Terminalden çıkış
"""
        self.terminal_output.append(help_text)

    def show_system_info(self):
        if not self.authenticated:
            self.terminal_output.append("Erişim reddedildi. Önce 'root' yazarak giriş yapın.")
            return

        self.terminal_output.append("=== SİSTEM BİLGİLERİ ===")
        self.terminal_output.append("Vertus OS Smart Lock v0.3.0")
        self.terminal_output.append("Geliştirici: Yiğit Eritici")
        self.terminal_output.append(f"Sistem Zamanı: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.terminal_output.append("")

    def show_version(self):
        if not self.authenticated:
            self.terminal_output.append("Erişim reddedildi.")
            return
        self.terminal_output.append("=== VERSİYON BİLGİSİ ===")
        self.terminal_output.append("Vertus OS Smart Lock v0.3.0")
        self.terminal_output.append("Geliştirici: Yiğit Eritici")
        self.terminal_output.append("")

    def show_status(self):
        if not self.authenticated:
            self.terminal_output.append("Erişim reddedildi.")
            return
        if self.parent:
            status = "AÇIK" if self.parent.is_unlocked else "KİLİTLİ"
            self.terminal_output.append("=== SİSTEM DURUMU ===")
            self.terminal_output.append(f"Tahta Durumu: {status}")
            self.terminal_output.append("")

    def show_debug_info(self):
        if not self.authenticated:
            self.terminal_output.append("Erişim reddedildi.")
            return
        self.terminal_output.append("=== HATA AYIKLAMA ===")
        self.terminal_output.append(f"Python: {sys.version}")
        self.terminal_output.append(f"PyQt6: {QtCore.PYQT_VERSION_STR}")
        self.terminal_output.append(f"WebEngine: {'Mevcut' if WEBENGINE_AVAILABLE else 'Mevcut Değil'}")
        self.terminal_output.append(f"Platform: {sys.platform}")
        self.terminal_output.append("")


class TimeBasedCrypto:
    @staticmethod
    def get_display_code(secret_key="vertus_okul_2024"):
        current_time = int(time.time() / 60)
        raw_code = f"{secret_key}{current_time}"
        hash_code = hashlib.md5(raw_code.encode()).hexdigest()

        numeric_hash = ""
        for char in hash_code:
            if char.isdigit():
                numeric_hash += char

        numeric_code = numeric_hash[:6]
        if len(numeric_code) < 6:
            numeric_code += str(current_time % 1000000).zfill(6 - len(numeric_code))

        return numeric_code[:6]

    @staticmethod
    def get_real_code(display_code):
        real_code = ""
        for char in display_code:
            if char.isdigit():
                digit = int(char)
                real_digit = (10 - digit) % 10
                real_code += str(real_digit)
        return real_code

    @staticmethod
    def verify_code(input_code, secret_key="vertus_okul_2024"):
        input_code = input_code.strip()
        if not input_code.isdigit() or len(input_code) != 6:
            return False

        current_time = int(time.time() / 60)
        valid_times = [current_time, current_time - 1, current_time + 1]

        for t in valid_times:
            display_code = TimeBasedCrypto.get_display_code_with_time(t, secret_key)
            real_code = TimeBasedCrypto.get_real_code(display_code)
            if input_code == real_code:
                return True
        return False

    @staticmethod
    def get_display_code_with_time(timestamp, secret_key="vertus_okul_2024"):
        raw_code = f"{secret_key}{timestamp}"
        hash_code = hashlib.md5(raw_code.encode()).hexdigest()

        numeric_hash = ""
        for char in hash_code:
            if char.isdigit():
                numeric_hash += char

        numeric_code = numeric_hash[:6]
        if len(numeric_code) < 6:
            numeric_code += str(timestamp % 1000000).zfill(6 - len(numeric_code))

        return numeric_code[:6]


class NotificationWidget(QWidget):
    def __init__(self, message, parent=None, is_error=False):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 80)

        self.bg_frame = QFrame(self)
        self.bg_frame.setGeometry(0, 0, 300, 80)

        if is_error:
            bg_color = "rgba(231, 76, 60, 220)"
            border_color = "rgba(255, 100, 100, 150)"
        else:
            bg_color = "rgba(50, 100, 150, 220)"
            border_color = "rgba(100, 180, 255, 150)"

        self.bg_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border-radius: 15px;
                border: 2px solid {border_color};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        self.message_label = QLabel(message)
        self.message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
            }
        """)
        self.message_label.setWordWrap(True)
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        if parent:
            self.move(parent.width() - 320, 20)

    def show_notification(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(lambda: QTimer.singleShot(2000, self.hide_notification))
        self.animation.start()
        self.show()

    def hide_notification(self):
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(800)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.finished.connect(self.close)
        self.animation.start()


class GlassFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(100, 150, 200, 40)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 15, 15)


class RoundedPixmapLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.radius = 12

    def setPixmap(self, pixmap):
        self.original_pixmap = pixmap
        self.update_rounded_pixmap()

    def update_rounded_pixmap(self):
        if hasattr(self, 'original_pixmap'):
            rounded = QPixmap(self.original_pixmap.size())
            rounded.fill(Qt.GlobalColor.transparent)

            painter = QPainter(rounded)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(QBrush(self.original_pixmap))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(0, 0, self.original_pixmap.width(),
                                    self.original_pixmap.height(), self.radius, self.radius)
            painter.end()

            super().setPixmap(rounded)


class AnimatedAppWidget(QWidget):
    def __init__(self, icon, name, app_url, orientation="horizontal", parent=None):
        super().__init__(parent)
        self.icon = icon
        self.name = name
        self.app_url = app_url
        self.orientation = orientation
        self.parent = parent
        self.setup_ui()
        self.setup_animation()

    def setup_ui(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(80, 80)
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.icon_container = QFrame()
        self.icon_container.setFixedSize(70, 70)
        self.icon_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.95);
                border-radius: 18px;
                border: 2px solid rgba(150, 180, 210, 0.6);
            }
        """)
        icon_layout = QVBoxLayout(self.icon_container)
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.setContentsMargins(8, 8, 8, 8)

        if os.path.exists(self.icon):
            self.icon_label = RoundedPixmapLabel()
            icon_pixmap = QPixmap(self.icon)
            scaled_pixmap = icon_pixmap.scaled(50, 50,
                                               Qt.AspectRatioMode.KeepAspectRatio,
                                               Qt.TransformationMode.SmoothTransformation)
            self.icon_label.setPixmap(scaled_pixmap)
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_layout.addWidget(self.icon_label)
        else:
            self.placeholder = QLabel("📱")
            self.placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.placeholder.setStyleSheet("font-size: 28px; color: #2c3e50;")
            icon_layout.addWidget(self.placeholder)

        layout.addWidget(self.icon_container)

    def setup_animation(self):
        self.animation = QPropertyAnimation(self.icon_container, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBack)

    def enterEvent(self, event):
        self.animate_hover(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_hover(False)
        super().leaveEvent(event)

    def animate_hover(self, hover):
        current_geom = self.icon_container.geometry()
        if hover:
            self.animation.setStartValue(current_geom)
            self.animation.setEndValue(QtCore.QRect(
                current_geom.x() - 2, current_geom.y() - 2,
                current_geom.width() + 4, current_geom.height() + 4
            ))
            self.icon_container.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 1.0);
                    border-radius: 18px;
                    border: 3px solid rgba(100, 180, 255, 0.8);
                }
            """)
        else:
            self.animation.setStartValue(current_geom)
            self.animation.setEndValue(QtCore.QRect(
                current_geom.x() + 2, current_geom.y() + 2,
                current_geom.width() - 4, current_geom.height() - 4
            ))
            self.icon_container.setStyleSheet("""
                QFrame {
                    background-color: rgba(255, 255, 255, 0.95);
                    border-radius: 18px;
                    border: 2px solid rgba(150, 180, 210, 0.6);
                }
            """)
        self.animation.start()

    def mousePressEvent(self, event):
        self.animate_click()
        self.open_app()
        super().mousePressEvent(event)

    def open_app(self):
        if self.parent:
            self.parent.open_app_window(self.name, self.app_url, self.orientation)

    def animate_click(self):
        scale_anim = QPropertyAnimation(self.icon_container, b"geometry")
        scale_anim.setDuration(100)
        scale_anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        current_geom = self.icon_container.geometry()
        scale_anim.setStartValue(current_geom)
        scale_anim.setEndValue(QtCore.QRect(
            current_geom.x() + 3, current_geom.y() + 3,
            current_geom.width() - 6, current_geom.height() - 6
        ))

        scale_back_anim = QPropertyAnimation(self.icon_container, b"geometry")
        scale_back_anim.setDuration(100)
        scale_back_anim.setEasingCurve(QEasingCurve.Type.OutBack)
        scale_back_anim.setStartValue(QtCore.QRect(
            current_geom.x() + 3, current_geom.y() + 3,
            current_geom.width() - 6, current_geom.height() - 6
        ))
        scale_back_anim.setEndValue(current_geom)

        scale_anim.finished.connect(scale_back_anim.start)
        scale_anim.start()


class FixedAnimatedButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event):
        self.animate_click()
        super().mousePressEvent(event)

    def animate_click(self):
        effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(150)
        animation.setStartValue(1.0)
        animation.setEndValue(0.6)
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        reverse_animation = QPropertyAnimation(effect, b"opacity")
        reverse_animation.setDuration(150)
        reverse_animation.setStartValue(0.6)
        reverse_animation.setEndValue(1.0)
        reverse_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        animation.finished.connect(reverse_animation.start)
        animation.start()


class SmartBoardLock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vertus OS - Akıllı Tahta Kilidi")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.showFullScreen()

        self.crypto = TimeBasedCrypto()
        self.animation = None
        self.unlock_duration = "sinirsiz"
        self.is_unlocked = False
        self.last_period_state = None
        self.terminal = None
        self.browser = None
        self.current_wallpaper = "wallpaper.png"
        self.developer_notification = None
        self.app_windows = {}

        self.setup_ui()
        self.setup_timers()
        self.block_all_shortcuts()

        QTimer.singleShot(1500, self.show_welcome_notification)

    def open_app_window(self, app_name, app_url, orientation="horizontal"):
        """Uygulama penceresini açar - DÜZELTİLMİŞ VERSİYON"""
        try:
            # Mevcut pencereleri kapat (güvenli şekilde)
            windows_to_close = []
            for window_name, window in self.app_windows.items():
                if window and window.isVisible():
                    windows_to_close.append(window_name)

            for window_name in windows_to_close:
                try:
                    window = self.app_windows.get(window_name)
                    if window:
                        window.close()
                        del self.app_windows[window_name]
                except KeyError:
                    # Pencere zaten kapatılmış olabilir, devam et
                    continue
                except Exception as e:
                    print(f"Pencere kapatma hatası {window_name}: {e}")

            # Yeni pencereyi aç
            app_window = AppWindow(app_name, app_url, orientation, self)
            self.app_windows[app_name] = app_window
            app_window.show()

            notification = NotificationWidget(f"✅ {app_name} açılıyor...", self)
            notification.show_notification()

        except Exception as e:
            print(f"Uygulama açma hatası: {e}")
            notification = NotificationWidget(f"❌ {app_name} açılamadı!", self, is_error=True)
            notification.show_notification()

    def close_app_window(self, app_name):
        """Uygulama penceresini kapat - DÜZELTİLMİŞ VERSİYON"""
        try:
            if app_name in self.app_windows:
                window = self.app_windows[app_name]
                if window:
                    window.close()
                del self.app_windows[app_name]
        except KeyError:
            # Pencere zaten kapatılmış
            pass
        except Exception as e:
            print(f"Pencere kapatma hatası: {e}")

    def show_developer_login_notification(self):
        self.developer_notification = DeveloperNotification(self)
        self.developer_notification.show_notification()

    def show_welcome_notification(self):
        notification = NotificationWidget("Vertus Smart Lock aktif!", self)
        notification.show_notification()

    def block_all_shortcuts(self):
        shortcuts = [
            Qt.Key.Key_Escape, Qt.Key.Key_F4, Qt.Key.Key_Tab,
            QKeySequence("Alt+F4"), QKeySequence("Ctrl+Alt+Delete"),
            QKeySequence("Alt+Tab"), QKeySequence("Ctrl+Esc"),
            QKeySequence("Win+D"), QKeySequence("Win+R"),
            QKeySequence("Ctrl+Shift+Esc")
        ]
        for shortcut in shortcuts:
            try:
                sc = QShortcut(shortcut, self)
                sc.activated.connect(self.ignore_shortcut)
            except:
                pass

    def ignore_shortcut(self):
        pass

    def setup_timers(self):
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        self.watchdog_timer = QTimer()
        self.watchdog_timer.timeout.connect(self.keep_fullscreen)
        self.watchdog_timer.start(1000)

        self.code_update_timer = QTimer()
        self.code_update_timer.timeout.connect(self.update_display_code)
        self.code_update_timer.start(1000)

        self.auto_lock_timer = QTimer()
        self.auto_lock_timer.timeout.connect(self.check_auto_lock)
        self.auto_lock_timer.start(1000)

    def check_auto_lock(self):
        period_name, _, _, _ = self.get_current_period()
        is_break = "Teneffüs" in period_name or "Öğle Arası" in period_name

        if is_break and self.is_unlocked:
            print(f"[AUTO-LOCK] {period_name} başladı, tahta kilitleniyor...")
            self.lock_device()
            notification = NotificationWidget(f"⏰ {period_name} başladı, tahta otomatik kilitlendi.", self)
            notification.show_notification()

        self.last_period_state = period_name

    def lock_device(self):
        print(f"[LOCK] Kilitleme başlatılıyor. Mevcut durum: is_unlocked={self.is_unlocked}")

        self.is_unlocked = False
        self.code_input.clear()

        if hasattr(self, 'opacity_effect'):
            self.opacity_effect.setOpacity(1.0)
        self.setGraphicsEffect(None)

        self.show()
        self.showNormal()
        self.showFullScreen()

        self.raise_()
        self.activateWindow()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.show()

        print(f"[LOCK] Kilitleme tamamlandı. Yeni durum: is_unlocked={self.is_unlocked}")

    def isLocked(self):
        return not self.is_unlocked

    def keep_fullscreen(self):
        if not self.isFullScreen() and self.isLocked():
            self.showFullScreen()

    def setup_ui(self):
        central_widget = QWidget()
        central_widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(main_layout)

        left_widget = self.create_left_panel()
        main_layout.addWidget(left_widget)

        self.center_widget = self.create_center_panel()
        main_layout.addWidget(self.center_widget, 1)

        right_widget = self.create_right_panel()
        main_layout.addWidget(right_widget)

        self.setup_bottom_right_widgets(central_widget)
        self.update_clock()
        self.update_display_code()

    def create_center_panel(self):
        widget = QWidget()
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.center_layout = QVBoxLayout(widget)
        self.center_layout.setContentsMargins(0, 0, 0, 25)
        self.center_layout.setSpacing(0)
        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        logo_version_container = QWidget()
        logo_version_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        logo_version_layout = QVBoxLayout(logo_version_container)
        logo_version_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_version_layout.setSpacing(8)
        logo_version_layout.setContentsMargins(0, 0, 0, 0)

        if os.path.exists("logo.png"):
            logo_label = QLabel()
            logo_pixmap = QPixmap("logo.png")
            logo_label.setPixmap(logo_pixmap.scaled(120, 120,
                                                    Qt.AspectRatioMode.KeepAspectRatio,
                                                    Qt.TransformationMode.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            logo_version_layout.addWidget(logo_label, alignment=Qt.AlignmentFlag.AlignCenter)

        version_label = QLabel("Vertus™ Smart Lock v0.3.0")
        version_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                padding: 0px;
            }
        """)
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_version_layout.addWidget(version_label, alignment=Qt.AlignmentFlag.AlignCenter)

        author_label = QLabel("- Yiğit Eritici")
        author_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 20px;
                font-weight: normal;
                background: transparent;
                padding: 0px;
            }
        """)
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_version_layout.addWidget(author_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.center_layout.addWidget(logo_version_container, alignment=Qt.AlignmentFlag.AlignCenter)
        self.center_layout.addStretch(1)

        return widget

    def create_left_panel(self):
        widget = QWidget()
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(50, 50, 0, 0)
        layout.setSpacing(30)

        code_frame = self.create_code_display_frame()
        layout.addWidget(code_frame, alignment=Qt.AlignmentFlag.AlignLeft)

        login_frame = self.create_login_frame()
        layout.addWidget(login_frame, alignment=Qt.AlignmentFlag.AlignLeft)

        return widget

    def create_code_display_frame(self):
        frame = GlassFrame()
        frame.setFixedSize(200, 200)
        layout = QVBoxLayout(frame)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("GÜVENLİK KODU")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
                background-color: rgba(52, 152, 219, 0.8);
                border-radius: 8px;
                padding: 8px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.code_display_label = QLabel()
        self.code_display_label.setFixedSize(150, 80)
        self.code_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.code_display_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.countdown_label = QLabel()
        self.countdown_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                font-weight: bold;
                background-color: rgba(100, 150, 200, 0.6);
                border-radius: 6px;
                padding: 6px;
            }
        """)
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.countdown_label)

        return frame

    def update_display_code(self):
        fake_code = self.crypto.get_display_code()
        seconds_left = 60 - (int(time.time()) % 60)

        if seconds_left <= 10:
            border_color = "#e74c3c"
            text_color = "#e74c3c"
            countdown_color = "#e74c3c"
        elif seconds_left <= 30:
            border_color = "#3498db"
            text_color = "#3498db"
            countdown_color = "#e0e0e0"
        else:
            border_color = "#5dade2"
            text_color = "#2c3e50"
            countdown_color = "#e0e0e0"

        self.code_display_label.setStyleSheet(f"""
            QLabel {{
                background-color: white;
                border-radius: 10px;
                border: 3px solid {border_color};
                color: {text_color};
                font-size: 28px;
                font-weight: bold;
                font-family: 'Courier New';
                padding: 5px;
            }}
        """)

        self.countdown_label.setStyleSheet(f"""
            QLabel {{
                color: {countdown_color};
                font-size: 12px;
                font-weight: bold;
                background-color: rgba(100, 150, 200, 0.6);
                border-radius: 6px;
                padding: 6px;
            }}
        """)

        self.code_display_label.setText(fake_code)
        self.countdown_label.setText(f"Kod {seconds_left}s sonra değişecek")

    def create_system_monitor_frame(self):
        frame = GlassFrame()
        frame.setFixedSize(220, 160)
        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("💻 SİSTEM İZLEME")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
                background-color: rgba(80, 130, 180, 0.9);
                border-radius: 8px;
                padding: 6px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        cpu_container = QWidget()
        cpu_layout = QHBoxLayout(cpu_container)
        cpu_layout.setContentsMargins(0, 5, 0, 5)

        cpu_label = QLabel("CPU:")
        cpu_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                font-weight: bold;
                min-width: 40px;
            }
        """)
        cpu_layout.addWidget(cpu_label)

        self.cpu_progress_bar = QWidget()
        self.cpu_progress_bar.setFixedHeight(15)
        self.cpu_progress_bar.setStyleSheet("""
            background-color: rgba(100, 100, 100, 0.5);
            border-radius: 7px;
            border: 1px solid rgba(150, 150, 150, 0.3);
        """)
        cpu_layout.addWidget(self.cpu_progress_bar)

        self.cpu_text = QLabel("45%")
        self.cpu_text.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 11px;
                min-width: 35px;
            }
        """)
        cpu_layout.addWidget(self.cpu_text)

        layout.addWidget(cpu_container)

        ram_container = QWidget()
        ram_layout = QHBoxLayout(ram_container)
        ram_layout.setContentsMargins(0, 5, 0, 5)

        ram_label = QLabel("RAM:")
        ram_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 12px;
                font-weight: bold;
                min-width: 40px;
            }
        """)
        ram_layout.addWidget(ram_label)

        self.ram_progress_bar = QWidget()
        self.ram_progress_bar.setFixedHeight(15)
        self.ram_progress_bar.setStyleSheet("""
            background-color: rgba(100, 100, 100, 0.5);
            border-radius: 7px;
            border: 1px solid rgba(150, 150, 150, 0.3);
        """)
        ram_layout.addWidget(self.ram_progress_bar)

        self.ram_text = QLabel("8.2GB")
        self.ram_text.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 11px;
                min-width: 35px;
            }
        """)
        ram_layout.addWidget(self.ram_text)

        layout.addWidget(ram_container)

        system_info = QLabel("Vertus OS v0.3.0")
        system_info.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                font-size: 10px;
                background-color: rgba(100, 150, 200, 0.3);
                border-radius: 6px;
                padding: 4px;
            }
        """)
        system_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(system_info)

        self.update_system_monitor()
        return frame

    def create_right_panel(self):
        widget = QWidget()
        widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 50, 50, 0)
        layout.setSpacing(15)

        schedule_frame = self.create_schedule_frame()
        layout.addWidget(schedule_frame, alignment=Qt.AlignmentFlag.AlignRight)

        apps_frame = GlassFrame()
        apps_frame.setFixedSize(220, 250)
        apps_layout = QVBoxLayout(apps_frame)
        apps_layout.setSpacing(10)
        apps_layout.setContentsMargins(15, 15, 15, 15)

        title_label = QLabel("UYGULAMALAR")
        title_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(80, 130, 180, 0.9);
                border-radius: 10px;
                padding: 8px;
                margin: 0px 0px 10px 0px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFixedHeight(40)
        apps_layout.addWidget(title_label)

        apps_grid = QGridLayout()
        apps_grid.setSpacing(15)
        apps_grid.setContentsMargins(10, 10, 10, 10)

        apps = [
            ("ai.png", "Copilot", "https://yigtii.github.io/copilot/", "vertical", 0, 0),
            ("360.png", "Microsoft Office 365", "https://yigtii.github.io/360/", "horizontal", 0, 1),
            ("hesapmakinesi.png", "Vertus Hesap Makinesi", "https://yigtii.github.io/hesap-makinesi/", "vertical", 1,
             0),
            ("eba.png", "Eba", "https://yigtii.github.io/eba/", "horizontal", 1, 1)
        ]

        for icon, name, url, orientation, row, col in apps:
            app_widget = AnimatedAppWidget(icon, name, url, orientation, self)
            apps_grid.addWidget(app_widget, row, col, Qt.AlignmentFlag.AlignCenter)

        apps_layout.addLayout(apps_grid)
        apps_layout.addStretch()

        layout.addWidget(apps_frame, alignment=Qt.AlignmentFlag.AlignRight)

        system_frame = self.create_system_monitor_frame()
        layout.addWidget(system_frame, alignment=Qt.AlignmentFlag.AlignRight)

        return widget

    def create_schedule_frame(self):
        frame = GlassFrame()
        frame.setFixedSize(220, 240)
        layout = QVBoxLayout(frame)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("📚 DERS PROGRAMI")
        title.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
                background-color: rgba(80, 130, 180, 0.9);
                border-radius: 8px;
                padding: 6px;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.schedule_icon = QLabel()
        self.schedule_icon.setFixedSize(80, 80)
        self.schedule_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_icon.setStyleSheet("font-size: 40px;")
        layout.addWidget(self.schedule_icon, alignment=Qt.AlignmentFlag.AlignCenter)

        self.schedule_label = QLabel()
        self.schedule_label.setStyleSheet("""
            QLabel {
                color: #e0e0e0;
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(100, 150, 200, 0.8);
                border-radius: 8px;
                padding: 8px;
            }
        """)
        self.schedule_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.schedule_label.setWordWrap(True)
        layout.addWidget(self.schedule_label)

        self.update_schedule_info()
        return frame

    def get_current_period(self):
        now = datetime.datetime.now()
        current_time = now.time()
        current_day = now.weekday()

        is_friday = current_day == 4

        if is_friday:
            periods = [
                ((8, 0), (8, 40), "1. Ders", "📖"),
                ((8, 40), (8, 50), "Teneffüs", "☕"),
                ((8, 50), (9, 30), "2. Ders", "📖"),
                ((9, 30), (9, 40), "Teneffüs", "☕"),
                ((9, 40), (10, 20), "3. Ders", "📖"),
                ((10, 20), (10, 30), "Teneffüs", "☕"),
                ((10, 30), (11, 10), "4. Ders", "📖"),
                ((11, 10), (11, 20), "Teneffüs", "☕"),
                ((11, 20), (12, 0), "5. Ders", "📖"),
                ((12, 0), (12, 5), "Teneffüs", "☕"),
                ((12, 5), (12, 45), "6. Ders", "📖"),
                ((12, 45), (13, 35), "Öğle Arası", "🍽️"),
                ((13, 35), (14, 15), "7. Ders", "📖"),
                ((14, 15), (14, 25), "Teneffüs", "☕"),
                ((14, 25), (15, 5), "8. Ders", "📖")
            ]
        else:
            periods = [
                ((8, 0), (8, 40), "1. Ders", "📖"),
                ((8, 40), (8, 50), "Teneffüs", "☕"),
                ((8, 50), (9, 30), "2. Ders", "📖"),
                ((9, 30), (9, 40), "Teneffüs", "☕"),
                ((9, 40), (10, 20), "3. Ders", "📖"),
                ((10, 20), (10, 30), "Teneffüs", "☕"),
                ((10, 30), (11, 10), "4. Ders", "📖"),
                ((11, 10), (11, 20), "Teneffüs", "☕"),
                ((11, 20), (12, 0), "5. Ders", "📖"),
                ((12, 0), (12, 45), "Öğle Arası", "🍽️"),
                ((12, 45), (13, 25), "6. Ders", "📖"),
                ((13, 25), (13, 35), "Teneffüs", "☕"),
                ((13, 35), (14, 15), "7. Ders", "📖"),
                ((14, 15), (14, 25), "Teneffüs", "☕"),
                ((14, 25), (15, 5), "8. Ders", "📖")
            ]

        for start, end, name, emoji in periods:
            start_time = datetime.time(start[0], start[1])
            end_time = datetime.time(end[0], end[1])

            if start_time <= current_time <= end_time:
                return name, emoji, start_time, end_time

        return "Okul Kapalı", "🚫", None, None

    def update_schedule_info(self):
        period_name, emoji, start_time, end_time = self.get_current_period()

        self.schedule_icon.setText(emoji)

        if start_time and end_time:
            time_left = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.now()
            minutes_left = max(0, int(time_left.total_seconds() // 60))

            self.schedule_label.setText(
                f"{period_name}\n"
                f"{start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}\n"
                f"Kalan: {minutes_left} dk"
            )
        else:
            self.schedule_label.setText(f"{period_name}\nOkul saatleri dışında")

    def create_login_frame(self):
        frame = GlassFrame()
        frame.setFixedSize(200, 470)
        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)

        self.code_input = QLineEdit()
        self.code_input.setMaxLength(6)
        self.code_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.code_input.setStyleSheet("""
            font-size: 20px;
            padding: 15px;
            border: 2px solid rgba(150, 180, 210, 0.8);
            border-radius: 10px;
            background-color: rgba(240, 240, 240, 0.95);
            color: #2c3e50;
            font-weight: bold;
        """)
        self.code_input.setValidator(QtGui.QIntValidator(0, 999999))
        layout.addWidget(self.code_input)

        numpad_layout = self.create_numpad()
        layout.addLayout(numpad_layout)

        duration_label = QLabel("Kilidi Açık Tut:")
        duration_label.setStyleSheet("""
            color: #e0e0e0;
            font-size: 12px;
            font-weight: bold;
            padding: 5px;
        """)
        duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(duration_label)

        self.unlock_duration_combobox = QComboBox()
        self.unlock_duration_combobox.addItems(["1 Ders", "Sınırsız"])
        self.unlock_duration_combobox.setStyleSheet("""
            QComboBox {
                background-color: rgba(240, 240, 240, 0.95);
                color: #2c3e50;
                font-size: 14px;
                font-weight: bold;
                padding: 8px;
                border: 2px solid rgba(150, 180, 210, 0.8);
                border-radius: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: rgba(240, 240, 240, 0.95);
                selection-background-color: rgba(100, 150, 200, 0.8);
                border: 2px solid rgba(150, 180, 210, 0.8);
                border-radius: 8px;
            }
        """)
        layout.addWidget(self.unlock_duration_combobox)

        self.submit_btn = FixedAnimatedButton("KİLİDİ AÇ")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(100, 150, 200, 0.9);
                color: #e0e0e0;
                font-size: 14px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid rgba(120, 170, 210, 0.8);
            }
            QPushButton:hover {
                background-color: rgba(120, 170, 210, 0.9);
            }
        """)
        self.submit_btn.clicked.connect(self.check_code)
        layout.addWidget(self.submit_btn)

        return frame

    def create_numpad(self):
        layout = QGridLayout()
        layout.setSpacing(8)

        numbers = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 1), ('⌫', 3, 2)
        ]

        for num, row, col in numbers:
            btn = FixedAnimatedButton(num)
            btn.setFixedSize(48, 48)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(200, 200, 200, 0.3);
                    color: #2c3e50;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 8px;
                    border: 1px solid rgba(180, 180, 180, 0.4);
                }
                QPushButton:hover {
                    background-color: rgba(220, 220, 220, 0.4);
                }
            """)

            if num == '⌫':
                btn.clicked.connect(self.delete_number)
            else:
                btn.clicked.connect(lambda checked, n=num: self.number_clicked(n))

            layout.addWidget(btn, row, col)
        return layout

    def setup_bottom_right_widgets(self, parent):
        self.bottom_right_container = QWidget(parent)
        self.bottom_right_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.bottom_right_container.setFixedSize(280, 80)

        container_layout = QHBoxLayout(self.bottom_right_container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(0, 0, 20, 20)

        datetime_container = QWidget()
        datetime_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        datetime_layout = QVBoxLayout(datetime_container)
        datetime_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        datetime_layout.setSpacing(2)
        datetime_layout.setContentsMargins(0, 0, 0, 0)

        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                font-size: 20px;
                font-weight: 300;
                font-family: 'Segoe UI Light', 'Arial';
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        datetime_layout.addWidget(self.time_label)

        self.date_label = QLabel()
        self.date_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.85);
                font-size: 11px;
                font-weight: 400;
                font-family: 'Segoe UI', 'Arial';
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        datetime_layout.addWidget(self.date_label)

        self.day_label = QLabel()
        self.day_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.75);
                font-size: 10px;
                font-weight: 400;
                font-family: 'Segoe UI', 'Arial';
                background: transparent;
                padding: 0px;
                margin: 0px;
            }
        """)
        self.day_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        datetime_layout.addWidget(self.day_label)

        container_layout.addWidget(datetime_container)

        if os.path.exists("dev.png"):
            self.dev_btn = QPushButton()
            self.dev_btn.setIcon(QtGui.QIcon("dev.png"))
            self.dev_btn.setIconSize(QtCore.QSize(48, 48))
            self.dev_btn.setFixedSize(60, 60)
            self.dev_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 30px;
                }
            """)
            self.dev_btn.clicked.connect(self.open_developer_terminal)
            container_layout.addWidget(self.dev_btn)

        if os.path.exists("kapa.png"):
            self.power_btn = QPushButton()
            self.power_btn.setIcon(QtGui.QIcon("kapa.png"))
            self.power_btn.setIconSize(QtCore.QSize(48, 48))
            self.power_btn.setFixedSize(60, 60)
            self.power_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.1);
                    border-radius: 30px;
                }
            """)
            self.power_btn.clicked.connect(self.shutdown_computer)
            container_layout.addWidget(self.power_btn)

        self.bottom_right_container.move(self.width() - 280, self.height() - 80)

    def open_developer_terminal(self):
        if self.terminal is None or not self.terminal.isVisible():
            self.terminal = DeveloperTerminal(self)

            screen_geometry = QApplication.primaryScreen().geometry()
            x = (screen_geometry.width() - self.terminal.width()) // 2
            y = (screen_geometry.height() - self.terminal.height()) // 2
            self.terminal.move(x, y)

            self.terminal.show()
            self.terminal.raise_()
            self.terminal.activateWindow()

            notification = NotificationWidget("🔧 Geliştirici terminali açıldı.", self)
            notification.show_notification()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'bottom_right_container'):
            self.bottom_right_container.move(self.width() - 280, self.height() - 80)

    def update_clock(self):
        self.update_schedule_info()
        self.update_datetime_display()
        self.update_system_monitor()

    def update_datetime_display(self):
        try:
            now = datetime.datetime.now()

            time_str = now.strftime("%H:%M")
            self.time_label.setText(time_str)

            try:
                turkish_months = {
                    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan",
                    5: "Mayıs", 6: "Haziran", 7: "Temmuz", 8: "Ağustos",
                    9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
                }

                day = now.day
                month = turkish_months[now.month]
                year = now.year

                date_str = f"{day} {month[:3]} {year}"
                self.date_label.setText(date_str)
            except:
                date_str = now.strftime("%d %b %Y")
                self.date_label.setText(date_str)

            try:
                turkish_days = {
                    0: "Pazartesi", 1: "Salı", 2: "Çarşamba", 3: "Perşembe",
                    4: "Cuma", 5: "Cumartesi", 6: "Pazar"
                }
                day_name = turkish_days[now.weekday()][:3]
                self.day_label.setText(day_name)
            except:
                day_name = now.strftime("%a")
                self.day_label.setText(day_name)

        except Exception as e:
            print(f"DateTime update error: {e}")
            if hasattr(self, 'time_label'):
                self.time_label.setText("12:00")
            if hasattr(self, 'date_label'):
                self.date_label.setText("1 Oca 2024")
            if hasattr(self, 'day_label'):
                self.day_label.setText("Paz")

    def update_system_monitor(self):
        try:
            import psutil

            cpu_percent = psutil.cpu_percent(interval=None)
            self.cpu_text.setText(f"{cpu_percent:.0f}%")

            memory = psutil.virtual_memory()
            ram_used_gb = memory.used / (1024 ** 3)
            ram_percent = memory.percent
            self.ram_text.setText(f"{ram_used_gb:.1f}GB")

            self.update_progress_bar(self.cpu_progress_bar, cpu_percent)
            self.update_progress_bar(self.ram_progress_bar, ram_percent)

        except ImportError:
            # psutil yoksa simüle edilmiş veriler
            cpu_percent = random.randint(20, 80)
            ram_gb = random.uniform(4.0, 12.0)
            ram_percent = random.randint(40, 85)

            self.cpu_text.setText(f"{cpu_percent}%")
            self.ram_text.setText(f"{ram_gb:.1f}GB")

            self.update_progress_bar(self.cpu_progress_bar, cpu_percent)
            self.update_progress_bar(self.ram_progress_bar, ram_percent)

        except Exception as e:
            print(f"System monitor error: {e}")

    def update_progress_bar(self, progress_widget, percentage):
        if percentage < 50:
            color = "rgba(100, 200, 100, 0.8)"
        elif percentage < 80:
            color = "rgba(255, 200, 100, 0.8)"
        else:
            color = "rgba(255, 100, 100, 0.8)"

        progress_widget.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {color},
                stop:{percentage / 100} {color},
                stop:{percentage / 100 + 0.01} rgba(100, 100, 100, 0.3),
                stop:1 rgba(100, 100, 100, 0.3));
            border-radius: 7px;
            border: 1px solid rgba(150, 150, 150, 0.3);
        """)

    def number_clicked(self, number):
        current = self.code_input.text()
        if len(current) < 6:
            self.code_input.setText(current + number)

    def delete_number(self):
        current = self.code_input.text()
        if current:
            self.code_input.setText(current[:-1])

    def check_code(self):
        if self.animation and self.animation.state() == QPropertyAnimation.State.Running:
            return

        input_code = self.code_input.text()
        if len(input_code) == 6:
            if self.crypto.verify_code(input_code):
                self.unlock_duration = self.unlock_duration_combobox.currentText().lower()
                self.is_unlocked = True

                notification = NotificationWidget("✅ Gerçek kod doğru! Tahta açılıyor...", self)
                notification.show_notification()

                self.hide()
                self.showMinimized()

                period_name, _, _, _ = self.get_current_period()
                if period_name == "Okul Kapalı":
                    self.unlock_duration = "sınırsız"
            else:
                self.code_input.clear()
                notification = NotificationWidget("❌ Hatalı kod! Telefondaki GERÇEK kodu girin.", self, is_error=True)
                notification.show_notification()

    def shutdown_computer(self):
        try:
            if IS_WINDOWS:
                os.system("shutdown /s /f /t 0")
            elif IS_LINUX:
                os.system("systemctl poweroff")
            elif IS_MAC:
                os.system("shutdown -h now")
        except:
            pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        try:
            if os.path.exists(self.current_wallpaper):
                wallpaper = QPixmap(self.current_wallpaper)
                scaled_wallpaper = wallpaper.scaled(
                    self.size(),
                    Qt.AspectRatioMode.IgnoreAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                painter.drawPixmap(0, 0, scaled_wallpaper)
            else:
                # Varsayılan gradient arkaplan
                gradient = QtGui.QLinearGradient(0, 0, self.width(), self.height())
                gradient.setColorAt(0, QColor(100, 150, 200, 180))
                gradient.setColorAt(1, QColor(50, 100, 150, 180))
                painter.setBrush(QBrush(gradient))
        except Exception as e:
            print(f"Wallpaper error: {e}")
            painter.setBrush(QBrush(QColor(100, 150, 200, 180)))
        finally:
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRect(self.rect())

    def closeEvent(self, event):
        if hasattr(self, 'animation') and self.animation and self.animation.state() == QPropertyAnimation.State.Running:
            event.accept()
        else:
            event.ignore()
            self.showFullScreen()


def check_dependencies():
    """Gerekli bağımlılıkları kontrol et"""
    missing_deps = []

    try:
        from PyQt6 import QtWebEngineWidgets
    except ImportError:
        missing_deps.append("PyQt6-WebEngine")

    if missing_deps:
        print("Eksik bağımlılıklar:", ", ".join(missing_deps))
        print("Ubuntu/Debian için kurulum:")
        print("sudo apt update")
        print("sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine python3-psutil")
        print("\nPardus için kurulum:")
        print("sudo apt update")
        print("sudo apt install python3-pyqt6 python3-pyqt6.qtwebengine python3-psutil")

        return False
    return True


if __name__ == "__main__":
    # Konsolu gizle (sadece Windows)
    if IS_WINDOWS:
        try:
            import ctypes

            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

    # Bağımlılıkları kontrol et
    if not check_dependencies():
        print("Gerekli bağımlılıklar eksik. Lütfen yukarıdaki komutlarla kurun.")
        sys.exit(1)

    app = QApplication(sys.argv)

    # High DPI desteği
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    # Linux için font ayarları
    if IS_LINUX:
        font = QFont("Ubuntu", 9)
    else:
        font = QFont("Segoe UI", 9)

    font.setHintingPreference(QFont.HintingPreference.PreferFullHinting)
    app.setFont(font)

    window = SmartBoardLock()
    sys.exit(app.exec())