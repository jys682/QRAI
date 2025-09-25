# QR Code Generator with Image Overlay

PyQt5와 qrcode 라이브러리를 사용하여 URL과 이미지를 입력받아 중앙에 이미지를 삽입한 QR 코드를 생성하는 GUI 프로그램입니다.

## 🚀 주요 기능

### 📥 URL 입력란
- 사용자가 QR코드에 포함시킬 URL을 입력
- URL 유효성 검사 기능
- 빈 문자열 또는 유효하지 않은 URL 경고

### 🔘 URL 관련 버튼
- **URL 등록 버튼**: URL을 QR코드 생성 대상 데이터로 등록
- **URL 지우기 버튼**: URL 입력창 초기화

### 🖼 QR 코드 중앙에 삽입할 이미지 미리보기
- 사용자가 업로드한 이미지의 썸네일을 미리 확인
- 이미지가 없을 경우 플레이스홀더 이미지 표시
- 150x150 픽셀 크기의 미리보기

### 📤 이미지 업로드 / 지우기 버튼
- **업로드 버튼**: 파일 탐색기를 통해 이미지를 선택 (.png, .jpg, .jpeg, .bmp, .gif)
- **이미지 지우기 버튼**: 선택된 이미지 초기화

### 🧾 QR 코드 생성 버튼
- 입력된 URL과 이미지(있는 경우)를 기반으로 QR 코드 생성
- 중앙에 이미지 삽입
- 오류 허용 레벨 자동 조정 (ERROR_CORRECT_H)
- 이미지 리사이징 및 정렬 처리 포함

### 👁 QR 코드 미리보기
- 생성된 QR코드를 GUI 내에서 미리 확인
- 스크롤 가능한 미리보기 창
- 최대 400x400 픽셀 크기로 표시

### 📋 QR 코드 복사 & 저장 기능
- **클립보드 복사 버튼**: 생성된 QR 코드를 클립보드에 이미지로 복사
- **이미지로 저장 버튼**: QR 코드를 .png, .jpg 형식으로 저장 (파일 다이얼로그로 위치/이름 지정)

## 📋 요구사항

- Python 3.6 이상
- PyQt5
- Pillow (PIL)
- qrcode

## 🛠 설치 방법

1. 저장소 클론 또는 파일 다운로드
```bash
git clone <repository-url>
cd UtillMyQR
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 🚀 사용 방법

1. 프로그램 실행
```bash
python main.py
```

2. URL 입력
   - URL 입력창에 QR 코드로 만들고 싶은 URL을 입력
   - "URL 등록" 버튼을 클릭하여 URL을 등록

3. 이미지 업로드 (선택사항)
   - "이미지 업로드" 버튼을 클릭하여 중앙에 삽입할 이미지 선택
   - 미리보기 창에서 이미지를 확인

4. QR 코드 생성
   - "QR 코드 생성" 버튼을 클릭
   - 미리보기 창에서 생성된 QR 코드 확인

5. 저장 또는 복사
   - "클립보드에 복사": QR 코드를 클립보드에 복사
   - "이미지로 저장": QR 코드를 파일로 저장

## 🎨 특징

- **직관적인 GUI**: 사용하기 쉬운 인터페이스
- **실시간 미리보기**: 입력한 내용을 실시간으로 확인
- **이미지 오버레이**: QR 코드 중앙에 로고나 이미지 삽입
- **다양한 형식 지원**: PNG, JPEG, BMP, GIF 이미지 지원
- **오류 처리**: 사용자 친화적인 오류 메시지
- **반응형 레이아웃**: 창 크기 조정에 따른 적응형 UI

## 🔧 기술 스택

- **GUI Framework**: PyQt5
- **QR Code Generation**: qrcode (Python QR Code generator)
- **Image Processing**: Pillow (PIL)
- **URL Validation**: urllib.parse

## 📁 파일 구조

```
UtillMyQR/
├── main.py              # 메인 프로그램 파일
├── requirements.txt     # 필요한 패키지 목록
└── README.md           # 프로젝트 설명서
```

## 🐛 문제 해결

### 일반적인 문제들

1. **PyQt5 설치 오류**
   ```bash
   pip install PyQt5==5.15.10
   ```

2. **Pillow 설치 오류**
   ```bash
   pip install Pillow==10.0.1
   ```

3. **qrcode 설치 오류**
   ```bash
   pip install qrcode[pil]
   ```

### 지원되는 이미지 형식
- PNG (권장)
- JPEG/JPG
- BMP
- GIF

### QR 코드 오류 수정 레벨
- **H (High)**: 30% 오류 수정 (기본값)
- 중앙 이미지 삽입 시 높은 오류 수정 레벨 사용으로 QR 코드 가독성 보장

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

버그 리포트, 기능 요청, 풀 리퀘스트를 환영합니다!

## 📞 지원

문제가 있거나 질문이 있으시면 이슈를 생성해 주세요.
