import sys
from database import crear_tablas
from ui import App
from error_reporter import report_error

def manejar_excepciones(tipo, valor, tb):
    enviar_error(valor, tb)
    sys.__excepthook__(tipo, valor, tb)

sys.excepthook = manejar_excepciones

crear_tablas()

app = App()
app.mainloop()

