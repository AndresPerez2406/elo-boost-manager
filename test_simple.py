try:
    import tkinter
    print("✅ Tkinter está instalado correctamente")
except ImportError:
    print("❌ Tkinter NO está en tu Python")

try:
    import customtkinter
    print("✅ CustomTkinter está instalado correctamente")
except ImportError:
    print("❌ CustomTkinter NO está instalado")