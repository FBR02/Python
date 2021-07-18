#
# This app is intded to use while chasing an offroad race eg. the Baja 1000.
# This app pulls satelitte tracking information for the race organizers website and plucks the useful data out
# for us in a much lighter manner than loading all the graphics from the page.
# It also then takes some user input like where the support vehicle is located and does some ETA calculations to help estimate further info.
# This app will eventually also control the VHF radio allowing me to operate without assistance from regular sited people.
# The massive UI is intentional so that I can read the screen from a laptop while bouncing down the road.
#

import ux

if __name__ == "__main__":
    root = ux.tk.Tk()
    app = ux.MainApplication(root)
    app.grid(row=0, column=0)

    # WIP radio transmit control
    app.transmitBtn.bind('<ButtonPress-1>', app.start_tx)
    app.transmitBtn.bind('<ButtonRelease-1>', app.stop_tx)

    app.after(0, app.update_stats)
    root.mainloop()