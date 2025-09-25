#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
QR Code Generator with Image Overlay
PyQt5 기반의 URL과 이미지를 입력받아 중앙에 이미지를 삽입한 QR 코드를 생성하는 GUI 프로그램
"""

import sys
import os
import tempfile
from urllib.parse import urlparse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QFileDialog, QMessageBox, QFrame, QTextEdit,
                             QScrollArea, QGroupBox, QGridLayout, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon, QPalette, QColor, QClipboard
from PIL import Image
import qrcode
from qrcode.image.pil import PilImage
import io


class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.url = ""
        self.image_path = ""
        self.qr_code_image = None
        self.init_ui()
        
    def init_ui(self):
        """GUI 초기화"""
        self.setWindowTitle("QR Code Generator with Image Overlay")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(800, 600)
        
        # 메인 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 제목
        title_label = QLabel("QR Code Generator with Image Overlay")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)
        
        # URL 입력 섹션
        url_group = self.create_url_section()
        main_layout.addWidget(url_group)
        
        # 이미지 업로드 섹션
        image_group = self.create_image_section()
        main_layout.addWidget(image_group)
        
        # QR 코드 생성 버튼
        generate_btn = QPushButton("🧾 QR 코드 생성")
        generate_btn.setFont(QFont("Arial", 12, QFont.Bold))
        generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #7f8c8d;
            }
        """)
        generate_btn.clicked.connect(self.generate_qr_code)
        main_layout.addWidget(generate_btn)
        
        # QR 코드 미리보기 섹션
        preview_group = self.create_preview_section()
        main_layout.addWidget(preview_group)
        
        # 저장/복사 버튼 섹션
        action_group = self.create_action_section()
        main_layout.addWidget(action_group)
        
        # 상태바
        self.statusBar().showMessage("준비됨")
        
    def create_url_section(self):
        """URL 입력 섹션 생성"""
        group = QGroupBox("📥 URL 입력")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QVBoxLayout(group)
        
        # URL 입력창
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        self.url_input.setFont(QFont("Arial", 11))
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.url_input)
        
        # URL 관련 버튼들
        url_btn_layout = QHBoxLayout()
        
        self.register_url_btn = QPushButton("URL 등록")
        self.register_url_btn.setStyleSheet(self.get_button_style("#27ae60"))
        self.register_url_btn.clicked.connect(self.register_url)
        url_btn_layout.addWidget(self.register_url_btn)
        
        self.clear_url_btn = QPushButton("URL 지우기")
        self.clear_url_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        self.clear_url_btn.clicked.connect(self.clear_url)
        url_btn_layout.addWidget(self.clear_url_btn)
        
        url_btn_layout.addStretch()
        layout.addLayout(url_btn_layout)
        
        return group
        
    def create_image_section(self):
        """이미지 업로드 섹션 생성"""
        group = QGroupBox("🖼 이미지 업로드")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QVBoxLayout(group)
        
        # 이미지 미리보기와 버튼을 위한 레이아웃
        image_layout = QHBoxLayout()
        
        # 이미지 미리보기
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(150, 150)
        self.image_preview.setStyleSheet("""
            QLabel {
                border: 2px dashed #bdc3c7;
                border-radius: 8px;
                background-color: #f8f9fa;
                color: #6c757d;
            }
        """)
        self.image_preview.setAlignment(Qt.AlignCenter)
        self.image_preview.setText("이미지 미리보기\n(150x150)")
        image_layout.addWidget(self.image_preview)
        
        # 버튼들
        btn_layout = QVBoxLayout()
        
        self.upload_btn = QPushButton("📤 이미지 업로드")
        self.upload_btn.setStyleSheet(self.get_button_style("#3498db"))
        self.upload_btn.clicked.connect(self.upload_image)
        btn_layout.addWidget(self.upload_btn)
        
        self.clear_image_btn = QPushButton("🗑 이미지 지우기")
        self.clear_image_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        self.clear_image_btn.clicked.connect(self.clear_image)
        btn_layout.addWidget(self.clear_image_btn)
        
        btn_layout.addStretch()
        image_layout.addLayout(btn_layout)
        layout.addLayout(image_layout)
        
        return group
        
    def create_preview_section(self):
        """QR 코드 미리보기 섹션 생성"""
        group = QGroupBox("👁 QR 코드 미리보기")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QVBoxLayout(group)
        
        # 스크롤 가능한 미리보기 영역
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(200)
        
        self.qr_preview = QLabel()
        self.qr_preview.setAlignment(Qt.AlignCenter)
        self.qr_preview.setStyleSheet("""
            QLabel {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                color: #6c757d;
                min-height: 200px;
            }
        """)
        self.qr_preview.setText("QR 코드가 여기에 표시됩니다")
        
        scroll_area.setWidget(self.qr_preview)
        layout.addWidget(scroll_area)
        
        return group
        
    def create_action_section(self):
        """저장/복사 버튼 섹션 생성"""
        group = QGroupBox("📋 QR 코드 저장 및 복사")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QHBoxLayout(group)
        
        self.copy_btn = QPushButton("📋 클립보드에 복사")
        self.copy_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        layout.addWidget(self.copy_btn)
        
        self.save_btn = QPushButton("💾 이미지로 저장")
        self.save_btn.setStyleSheet(self.get_button_style("#f39c12"))
        self.save_btn.clicked.connect(self.save_qr_code)
        self.save_btn.setEnabled(False)
        layout.addWidget(self.save_btn)
        
        return group
        
    def get_button_style(self, color):
        """버튼 스타일 생성"""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color, 0.8)};
            }}
            QPushButton:disabled {{
                background-color: #bdc3c7;
                color: #7f8c8d;
            }}
        """
        
    def darken_color(self, color, factor=0.9):
        """색상을 어둡게 만들기"""
        # 간단한 색상 어둡게 만들기 (실제로는 더 정교한 색상 변환이 필요)
        color_map = {
            "#3498db": "#2980b9",
            "#27ae60": "#229954",
            "#e74c3c": "#c0392b",
            "#9b59b6": "#8e44ad",
            "#f39c12": "#e67e22"
        }
        return color_map.get(color, color)
        
    def validate_url(self, url):
        """URL 유효성 검사"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
            
    def register_url(self):
        """URL 등록"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "경고", "URL을 입력해주세요.")
            return
            
        if not self.validate_url(url):
            QMessageBox.warning(self, "경고", "유효한 URL을 입력해주세요.\n예: https://example.com")
            return
            
        self.url = url
        self.statusBar().showMessage(f"URL 등록됨: {url}")
        QMessageBox.information(self, "성공", f"URL이 등록되었습니다:\n{url}")
        
    def clear_url(self):
        """URL 지우기"""
        self.url_input.clear()
        self.url = ""
        self.statusBar().showMessage("URL이 지워졌습니다")
        
    def upload_image(self):
        """이미지 업로드"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "이미지 선택", 
            "", 
            "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            try:
                # 이미지 로드 및 미리보기
                pixmap = QPixmap(file_path)
                if pixmap.isNull():
                    QMessageBox.warning(self, "오류", "이미지 파일을 읽을 수 없습니다.")
                    return
                    
                # 썸네일 생성
                scaled_pixmap = pixmap.scaled(
                    150, 150, 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.image_preview.setPixmap(scaled_pixmap)
                
                self.image_path = file_path
                self.statusBar().showMessage(f"이미지 업로드됨: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"이미지 업로드 중 오류가 발생했습니다:\n{str(e)}")
                
    def clear_image(self):
        """이미지 지우기"""
        self.image_preview.clear()
        self.image_preview.setText("이미지 미리보기\n(150x150)")
        self.image_path = ""
        self.statusBar().showMessage("이미지가 지워졌습니다")
        
    def generate_qr_code(self):
        """QR 코드 생성"""
        if not self.url:
            QMessageBox.warning(self, "경고", "먼저 URL을 등록해주세요.")
            return
            
        try:
            self.statusBar().showMessage("QR 코드 생성 중...")
            
            # 기본 QR 코드 생성
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(self.url)
            qr.make(fit=True)
            
            # QR 코드 이미지 생성
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # 이미지가 있는 경우 중앙에 삽입
            if self.image_path:
                qr_image = self.add_image_to_qr_center(qr_image, self.image_path)
            
            # PIL 이미지를 QPixmap으로 변환
            self.qr_code_image = qr_image
            
            # 미리보기에 표시
            self.display_qr_preview(qr_image)
            
            # 버튼 활성화
            self.copy_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            
            self.statusBar().showMessage("QR 코드 생성 완료")
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"QR 코드 생성 중 오류가 발생했습니다:\n{str(e)}")
            self.statusBar().showMessage("QR 코드 생성 실패")
            
    def add_image_to_qr_center(self, qr_image, image_path):
        """QR 코드 중앙에 이미지 삽입"""
        try:
            # QR 코드 크기
            qr_width, qr_height = qr_image.size
            
            # 중앙 이미지 크기 계산 (QR 코드의 약 20-25%)
            overlay_size = min(qr_width, qr_height) // 5
            
            # 오버레이 이미지 로드 및 리사이즈
            overlay = Image.open(image_path)
            overlay = overlay.convert("RGBA")
            overlay = overlay.resize((overlay_size, overlay_size), Image.Resampling.LANCZOS)
            
            # 중앙 위치 계산
            x = (qr_width - overlay_size) // 2
            y = (qr_height - overlay_size) // 2
            
            # 배경을 흰색으로 설정 (QR 코드와 동일)
            if qr_image.mode != 'RGBA':
                qr_image = qr_image.convert('RGBA')
            
            # 이미지 합성
            qr_image.paste(overlay, (x, y), overlay)
            
            return qr_image
            
        except Exception as e:
            QMessageBox.warning(self, "경고", f"이미지 삽입 중 오류가 발생했습니다:\n{str(e)}")
            return qr_image
            
    def display_qr_preview(self, qr_image):
        """QR 코드 미리보기 표시"""
        try:
            # PIL 이미지를 QPixmap으로 변환
            img_byte_arr = io.BytesIO()
            qr_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            pixmap = QPixmap()
            pixmap.loadFromData(img_byte_arr)
            
            # 미리보기 크기에 맞게 조정
            preview_size = 400
            scaled_pixmap = pixmap.scaled(
                preview_size, preview_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.qr_preview.setPixmap(scaled_pixmap)
            
        except Exception as e:
            QMessageBox.warning(self, "경고", f"미리보기 표시 중 오류가 발생했습니다:\n{str(e)}")
            
    def copy_to_clipboard(self):
        """클립보드에 복사"""
        if self.qr_code_image:
            try:
                # PIL 이미지를 클립보드용으로 변환
                img_byte_arr = io.BytesIO()
                self.qr_code_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                pixmap = QPixmap()
                pixmap.loadFromData(img_byte_arr)
                
                clipboard = QApplication.clipboard()
                clipboard.setPixmap(pixmap)
                
                self.statusBar().showMessage("QR 코드가 클립보드에 복사되었습니다")
                QMessageBox.information(self, "성공", "QR 코드가 클립보드에 복사되었습니다!")
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"클립보드 복사 중 오류가 발생했습니다:\n{str(e)}")
                
    def save_qr_code(self):
        """QR 코드를 파일로 저장"""
        if self.qr_code_image:
            try:
                file_path, _ = QFileDialog.getSaveFileName(
                    self,
                    "QR 코드 저장",
                    "qr_code.png",
                    "PNG 파일 (*.png);;JPEG 파일 (*.jpg);;모든 파일 (*.*)"
                )
                
                if file_path:
                    self.qr_code_image.save(file_path)
                    self.statusBar().showMessage(f"QR 코드가 저장되었습니다: {file_path}")
                    QMessageBox.information(self, "성공", f"QR 코드가 저장되었습니다:\n{file_path}")
                    
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일 저장 중 오류가 발생했습니다:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 다크 테마 설정 (선택사항)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    # app.setPalette(palette)  # 다크 테마 사용하려면 주석 해제
    
    window = QRCodeGenerator()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
