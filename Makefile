PRETTIER_ARGS=web/*.html web/*.css


all: check

help:
	@echo "Commands:"
	@echo ""
	@echo "  format    ejecuta prettier y formatea el HTML y CSS  automaticamente"
	@echo "  check     chequea el estilo de los archivos HTML y CSS"
	@echo "  plot      ejecuta el script para generar las grafica"
	@echo ""

check:
	prettier --check $(PRETTIER_ARGS)

format:
	prettier --write $(PRETTIER_ARGS)

plots:
	python code/datos-pais.py
