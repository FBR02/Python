import ux

if __name__ == "__main__":
    root = ux.tk.Tk()
    app = ux.MainApplication(root)
    app.grid(row=0, column=0)

    app.transmitBtn.bind('<ButtonPress-1>', app.start_tx)
    app.transmitBtn.bind('<ButtonRelease-1>', app.stop_tx)
    app.after(0, app.update_stats)


    root.mainloop()