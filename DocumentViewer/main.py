#
# This app takes video from a local webcam and then converts it in various ways to make it easier to read with my visual impairment.
# The intent of this app is to use a webcam mounted on an arm pointed down towards a desk and be able to read documents/mail.
# I am using a 4k cheap webcam off amazon with a built in light to help normalize lighting issues with documents.
#
import viewer

if __name__ == "__main__":
    # Initialize the class
    root = viewer.tk.Tk()
    app = viewer.Viewer(root)
    app.grid(row=0, column=0)

    #Escape key quits app
    app.parent.bind('<Escape>', lambda e: app.parent.quit())

    root.mainloop()