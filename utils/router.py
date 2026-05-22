def navigate(window, view):
    # Remove todos os widgets atuais e carrega a nova tela
    for widget in window.winfo_children():
        widget.destroy()
    view.show(window)
