PYTHON=python3
PYINSTALLER=pyinstaller
FILE_NAME=main.py
WINDOWS_SOURCE=.\$(FILE_NAME)
LINUX_SOURCE=`pwd`/$(FILE_NAME)
WINDOWS_OUTPUT=.\output\windows
LINUX_OUTPUT=`pwd`/output/linux
WINDOWS_OPTIONS=--onefile --console
LINUX_OPTIONS=--onefile --console
CLEANING_FILE=clear.py

all: windows linux

windows:
	@echo "Сборка для Windows..."
	$(PYINSTALLER) $(WINDOWS_OPTIONS) $(WINDOWS_SOURCE) --distpath $(WINDOWS_OUTPUT)
	@echo "Запуск Windows-исполняемого файла..."
	$(WINDOWS_OUTPUT)\main.exe

linux:
	@echo "Сборка для Linux..."
	@echo "Установка необходимых пакетов..."
	@apt install -y python3 python3-pip make
	pip install --break-system-packages -r requirements.txt
	$(PYINSTALLER) $(LINUX_OPTIONS) $(LINUX_SOURCE) --distpath $(LINUX_OUTPUT)
	@echo "Готово"
	@echo "Собранный файл находится в $(LINUX_OUTPUT)"
	@echo "Запуск игры..."
	./$(LINUX_OUTPUT)/$(FILE_NAME)

clean:
	@echo "Очистка..."
	$(PYTHON) $(CLEANING_FILE)

.PHONY: all windows linux clean