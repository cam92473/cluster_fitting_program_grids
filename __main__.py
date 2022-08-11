import scipy.optimize as opt
import pandas as pd


class ChiSquared():
    def __init__(self):
        self.filenamevar = ""
        self.chosenstar = "     1-cluster fit     "
        self.checkedset = 0
        self.checked2set = 0
        self.checked3set = 0
        self.checked4set = 0
        self.checker1set = 1
        self.checker2set = 1
        self.checker3set = 1
        self.checker4set = 1
        self.checker5set = 0
        self.dset = "785000"
        self.sliderval1set = 0
        self.rownumberset = ""
        self.sliderstring1set = "log-log axes"
        self.model_chosen_set = "UVIT_HST"
        self.ulmethset = "Standard"

        self.starlist1 = ["0","0.75","N/A","N/A","N/A","N/A"]
        self.starlist2 = ["0","1.4","0","1.4","N/A","N/A"]
        self.starlist3 = ["0","1","0","1","0","0.7"]
        #UVIT_HST
        self.stardict1 = [["-2.5","0.3","0"],[".66",".90","0"],["0","1","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict2 = [["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict3 = [["-2.1","-0.1","0"],[".8",".9","0"],["0","1","0"],["-2.1","-0.1","0"],[".9","1.13","0"],["0","1","0"],["-2.1","0.3","0"],[".66",".8","0"]]
        #UVIT_SDSS_Spitzer
        self.stardict4 = [["-2.1","-0.1","0"],[".66",".90","0"],["0","1","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict5 = [["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict6 = [["-2.1","-0.1","0"],[".8",".9","0"],["0","1","0"],["-2.1","-0.1","0"],[".9","1.0","0"],["0","1","0"],["-2.1","-0.1","0"],[".66",".8","0"]]
        #UVIT_Johnson_GALEX
        self.stardict7 = [["-2.1","-0.1","0"],[".66",".90","0"],["0","1","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict8 = [["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["-2.1","-0.1","0"],[".66","1.01","0"],["0","2","0"],["N/A","N/A","N/A"],["N/A","N/A","N/A"]]
        self.stardict9 = [["-2.1","-0.1","0"],[".8",".9","0"],["0","1","0"],["-2.1","-0.1","0"],[".9","1.0","0"],["0","1","0"],["-2.1","-0.1","0"],[".66",".8","0"]]

        while True:
            self.intro_gui()
            self.buildGrid()
            self.extract_measured_flux()
            self.extract_ul()
            self.convert_to_AB()
            self.convert_to_bandflux()
            self.prepare_for_interpolation()
            self.minimize_chisq()
            self.find_param_errors()
            self.mysterious_function()
            self.display_all_results()
            self.save_output()

    ##orange

    def intro_gui(self):
        self.switch = False
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        mwin = tk.Tk()
        mwin.geometry("1260x940+520+50")
        mwin.title("Cluster Fitting")
        mwin.config(bg='alice blue')
        mwin.resizable(0,0)

        def collectfilename():
            from tkinter import messagebox
            if user_filename.get() == "":
                tk.messagebox.showinfo('Error', 'Please enter a filename.')
                return None
            else:
                moveon = False

                if "," in user_rownumber.get():
                    rowlist = user_rownumber.get().split(',')
                    for elem in rowlist:
                        try:
                            rowint = int(elem)
                        except:
                            tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                            return None
                        else:
                            introwlist = [int(i) for i in rowlist]
                            lowestelem = introwlist[0]
                            highestelem = introwlist[-1]
                            moveon = True

                elif ":" in user_rownumber.get():
                    rowlist = user_rownumber.get().split(':')
                    for elem in rowlist:
                        try:
                            rowint = int(elem)
                        except:
                            tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                            return None
                        else:
                            import numpy as np
                            introwlist = np.arange(int(rowlist[0]),int(rowlist[-1])+1).tolist()
                            lowestelem = introwlist[0]
                            highestelem = introwlist[-1]
                            moveon = True
                
                else:
                    try:
                        rowint = int(user_rownumber.get())
                    except:
                        tk.messagebox.showinfo('Error', 'Please enter the number of rows with the correct syntax.')
                        return None
                    else:
                        introwlist = [rowint]
                        lowestelem = rowint
                        highestelem = rowint
                        moveon = True

                if moveon == True:
                    try:
                        import pandas as pd
                        self.measuredata = pd.read_csv("{}".format(user_filename.get(),delimiter=","))
                        self.filenamevar = user_filename.get()
                    except:
                        tk.messagebox.showinfo('Error', "Could not find input file for measured fluxes. Please place the file in the program folder and try again.")
                        return None
                    else:   
                        if highestelem > len(self.measuredata)+1 or lowestelem < 2:
                            tk.messagebox.showinfo('Error', "Rows specified are out of range.")
                            return None
                        if (checker2.get() == 1 and weightedmeanvarname.get()[-4:] != ".csv") or (checker3.get() == 1 and gridname.get()[-4:] != ".csv"):
                            tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .csv extension.")
                            return None
                        elif checker4.get() == 1 and (imgname.get()[-4:] != ".png" and imgname.get()[-4:] != ".jpg"):
                            tk.messagebox.showinfo('Error', "The filenames specified are not allowed. Make sure to use the .png or .jpg extensions.")
                            return None
                        else:
                            try:
                                a = int(weightedmeanvarname.get()[0])
                                b = int(gridname.get()[0])
                                c = int(imgname.get()[0])
                                return None
                            except:
                                try:
                                    self.switch = True
                                    self.rows = [i-2 for i in introwlist]
                                    self.rownumberset = user_rownumber.get()

                                    self.dispresults = checker1.get()
                                    self.weightedmeanvarresults = checker2.get()
                                    self.gridresults = checker3.get()
                                    self.saveplots = checker4.get()
                                    self.plotscale = currentsliderval1.get()
                                    self.checker1set = checker1.get()
                                    self.checker2set = checker2.get()
                                    self.checker3set = checker3.get()
                                    self.checker4set = checker4.get()
                                    self.checker5set = checker5.get()
                                    self.checkedset = checked.get()
                                    self.checked2set = checked2.get()
                                    self.sliderval1set = currentsliderval1.get()
                                    self.sliderstring1set = sliderstring1.get()
                                    
                                    self.model_chosen = user_model_cho.get()
                                    self.model_chosen_set = user_model_cho.get()
                                    self.ulmeth = user_ulmeth.get()
                                    self.ulmethset = user_ulmeth.get()


                                    if checker2.get() == 1:
                                        self.weightedmeanvarname = weightedmeanvarname.get()
                                    if checker3.get() == 1:
                                        self.gridname = gridname.get()
                                    if checker4.get() == 1:
                                        self.imgfilename = imgname.get()
                                    if checker5.get() == 1:
                                        self.silent = True
                                    else:
                                        self.silent = False
                                    
                                    self.single_cluster = False
                                    self.double_cluster = False
                                    self.triple_cluster = False
                                    self.chosenstar = starno_chosen.get()

                                    try:
                                        self.d = float(user_d.get())
                                        self.dset = user_d.get()
                                    except:
                                        tk.messagebox.showinfo('Error', "Please enter a number for d.")
                                        return None

                                    if self.chosenstar == "     1-cluster fit     ":

                                        self.single_cluster = True

                                        self.Mbound1lo = float(user_Mbound1lo.get())
                                        self.Mbound1hi = float(user_Mbound1hi.get())
                                        
                                        self.Z1lowest = float(user_Z1lowest.get())
                                        self.Z1highest = float(user_Z1highest.get())
                                        self.Z1num = int(user_Z1num.get())
                                        if self.Z1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age1lowest = float(user_age1lowest.get())
                                        self.age1highest = float(user_age1highest.get())
                                        self.age1num = int(user_age1num.get())
                                        if self.age1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv1lowest = float(user_ebv1lowest.get())
                                        self.ebv1highest = float(user_ebv1highest.get())
                                        self.ebv1num = int(user_ebv1num.get())
                                        if self.ebv1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                         
                                        self.starlist1[0] = user_Mbound1lo.get()
                                        self.starlist1[1] = user_Mbound1hi.get()
                                        if user_model_cho.get() == "UVIT_HST":
                                            self.stardict1[0][0] = user_Z1lowest.get()
                                            self.stardict1[0][1] = user_Z1highest.get()
                                            self.stardict1[0][2] = user_Z1num.get()
                                            self.stardict1[1][0] = user_age1lowest.get()
                                            self.stardict1[1][1] = user_age1highest.get()
                                            self.stardict1[1][2] = user_age1num.get()
                                            self.stardict1[2][0] = user_ebv1lowest.get()
                                            self.stardict1[2][1] = user_ebv1highest.get()
                                            self.stardict1[2][2] = user_ebv1num.get()
                                        elif user_model_cho.get() == "UVIT_SDSS_Spitzer":
                                            self.stardict4[0][0] = user_Z1lowest.get()
                                            self.stardict4[0][1] = user_Z1highest.get()
                                            self.stardict4[0][2] = user_Z1num.get()
                                            self.stardict4[1][0] = user_age1lowest.get()
                                            self.stardict4[1][1] = user_age1highest.get()
                                            self.stardict4[1][2] = user_age1num.get()
                                            self.stardict4[2][0] = user_ebv1lowest.get()
                                            self.stardict4[2][1] = user_ebv1highest.get()
                                            self.stardict4[2][2] = user_ebv1num.get()
                                        elif user_model_cho.get() == "UVIT_Johnson_GALEX":
                                            self.stardict7[0][0] = user_Z1lowest.get()
                                            self.stardict7[0][1] = user_Z1highest.get()
                                            self.stardict7[0][2] = user_Z1num.get()
                                            self.stardict7[1][0] = user_age1lowest.get()
                                            self.stardict7[1][1] = user_age1highest.get()
                                            self.stardict7[1][2] = user_age1num.get()
                                            self.stardict7[2][0] = user_ebv1lowest.get()
                                            self.stardict7[2][1] = user_ebv1highest.get()
                                            self.stardict7[2][2] = user_ebv1num.get()

                                    elif self.chosenstar == "     2-cluster fit     ":
                                        
                                        self.double_cluster = True

                                        self.Mbound1lo = float(user_Mbound1lo.get())
                                        self.Mbound1hi = float(user_Mbound1hi.get())
                                        self.Mguess2 = float(user_Mguess2.get())
                                        self.Mbound2lo = float(user_Mbound2lo.get())
                                        self.Mbound2hi = float(user_Mbound2hi.get())
                                        
                                        self.Z1lowest = float(user_Z1lowest.get())
                                        self.Z1highest = float(user_Z1highest.get())
                                        self.Z1num = int(user_Z1num.get())
                                        if self.Z1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age1lowest = float(user_age1lowest.get())
                                        self.age1highest = float(user_age1highest.get())
                                        self.age1num = int(user_age1num.get())
                                        if self.age1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv1lowest = float(user_ebv1lowest.get())
                                        self.ebv1highest = float(user_ebv1highest.get())
                                        self.ebv1num = int(user_ebv1num.get())
                                        if self.ebv1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Z2lowest = float(user_Z2lowest.get())
                                        self.Z2highest = float(user_Z2highest.get())
                                        self.Z2num = int(user_Z2num.get())
                                        if self.Z2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age2lowest = float(user_age2lowest.get())
                                        self.age2highest = float(user_age2highest.get())
                                        self.age2num = int(user_age2num.get())
                                        if self.age2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv2lowest = float(user_ebv2lowest.get())
                                        self.ebv2highest = float(user_ebv2highest.get())
                                        self.ebv2num = int(user_ebv2num.get())
                                        if self.ebv2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')

                                        self.starlist2[0] = user_Mbound1lo.get()
                                        self.starlist2[1] = user_Mbound1hi.get()
                                        self.starlist2[2] = user_Mbound2lo.get()
                                        self.starlist2[3] = user_Mbound2hi.get()
                                        if user_model_cho.get() == "UVIT_HST":
                                            self.stardict2[0][0] = user_Z1lowest.get()
                                            self.stardict2[0][1] = user_Z1highest.get()
                                            self.stardict2[0][2] = user_Z1num.get()
                                            self.stardict2[1][0] = user_age1lowest.get()
                                            self.stardict2[1][1] = user_age1highest.get()
                                            self.stardict2[1][2] = user_age1num.get()
                                            self.stardict2[2][0] = user_ebv1lowest.get()
                                            self.stardict2[2][1] = user_ebv1highest.get()
                                            self.stardict2[2][2] = user_ebv1num.get()
                                            self.stardict2[3][0] = user_Z2lowest.get()
                                            self.stardict2[3][1] = user_Z2highest.get()
                                            self.stardict2[3][2] = user_Z2num.get()
                                            self.stardict2[4][0] = user_age2lowest.get()
                                            self.stardict2[4][1] = user_age2highest.get()
                                            self.stardict2[4][2] = user_age2num.get()
                                            self.stardict2[5][0] = user_ebv2lowest.get()
                                            self.stardict2[5][1] = user_ebv2highest.get()
                                            self.stardict2[5][2] = user_ebv2num.get()
                                        elif user_model_cho.get() == "UVIT_SDSS_Spitzer":
                                            self.stardict5[0][0] = user_Z1lowest.get()
                                            self.stardict5[0][1] = user_Z1highest.get()
                                            self.stardict5[0][2] = user_Z1num.get()
                                            self.stardict5[1][0] = user_age1lowest.get()
                                            self.stardict5[1][1] = user_age1highest.get()
                                            self.stardict5[1][2] = user_age1num.get()
                                            self.stardict5[2][0] = user_ebv1lowest.get()
                                            self.stardict5[2][1] = user_ebv1highest.get()
                                            self.stardict5[2][2] = user_ebv1num.get()
                                            self.stardict5[3][0] = user_Z2lowest.get()
                                            self.stardict5[3][1] = user_Z2highest.get()
                                            self.stardict5[3][2] = user_Z2num.get()
                                            self.stardict5[4][0] = user_age2lowest.get()
                                            self.stardict5[4][1] = user_age2highest.get()
                                            self.stardict5[4][2] = user_age2num.get()
                                            self.stardict5[5][0] = user_ebv2lowest.get()
                                            self.stardict5[5][1] = user_ebv2highest.get()
                                            self.stardict5[5][2] = user_ebv2num.get()
                                        elif user_model_cho.get() == "UVIT_Johnson_GALEX":
                                            self.stardict8[0][0] = user_Z1lowest.get()
                                            self.stardict8[0][1] = user_Z1highest.get()
                                            self.stardict8[0][2] = user_Z1num.get()
                                            self.stardict8[1][0] = user_age1lowest.get()
                                            self.stardict8[1][1] = user_age1highest.get()
                                            self.stardict8[1][2] = user_age1num.get()
                                            self.stardict8[2][0] = user_ebv1lowest.get()
                                            self.stardict8[2][1] = user_ebv1highest.get()
                                            self.stardict8[2][2] = user_ebv1num.get()
                                            self.stardict8[3][0] = user_Z2lowest.get()
                                            self.stardict8[3][1] = user_Z2highest.get()
                                            self.stardict8[3][2] = user_Z2num.get()
                                            self.stardict8[4][0] = user_age2lowest.get()
                                            self.stardict8[4][1] = user_age2highest.get()
                                            self.stardict8[4][2] = user_age2num.get()
                                            self.stardict8[5][0] = user_ebv2lowest.get()
                                            self.stardict8[5][1] = user_ebv2highest.get()
                                            self.stardict8[5][2] = user_ebv2num.get()

                                    elif self.chosenstar == "     3-cluster fit     ":

                                        self.triple_cluster = True

                                        self.Mbound1lo = float(user_Mbound1lo.get())
                                        self.Mbound1hi = float(user_Mbound1hi.get())
                                        self.Mbound2lo = float(user_Mbound2lo.get())
                                        self.Mbound2hi = float(user_Mbound2hi.get())
                                        self.Mbound3lo = float(user_Mbound3lo.get())
                                        self.Mbound3hi = float(user_Mbound3hi.get())

                                        self.Z1lowest = float(user_Z1lowest.get())
                                        self.Z1highest = float(user_Z1highest.get())
                                        self.Z1num = int(user_Z1num.get())
                                        if self.Z1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age1lowest = float(user_age1lowest.get())
                                        self.age1highest = float(user_age1highest.get())
                                        self.age1num = int(user_age1num.get())
                                        if self.age1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv1lowest = float(user_ebv1lowest.get())
                                        self.ebv1highest = float(user_ebv1highest.get())
                                        self.ebv1num = int(user_ebv1num.get())
                                        if self.ebv1num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Z2lowest = float(user_Z2lowest.get())
                                        self.Z2highest = float(user_Z2highest.get())
                                        self.Z2num = int(user_Z2num.get())
                                        if self.Z2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age2lowest = float(user_age2lowest.get())
                                        self.age2highest = float(user_age2highest.get())
                                        self.age2num = int(user_age2num.get())
                                        if self.age2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.ebv2lowest = float(user_ebv2lowest.get())
                                        self.ebv2highest = float(user_ebv2highest.get())
                                        self.ebv2num = int(user_ebv2num.get())
                                        if self.ebv2num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.Z3lowest = float(user_Z3lowest.get())
                                        self.Z3highest = float(user_Z3highest.get())
                                        self.Z3num = int(user_Z3num.get())
                                        if self.Z3num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')
                                        self.age3lowest = float(user_age3lowest.get())
                                        self.age3highest = float(user_age3highest.get())
                                        self.age3num = int(user_age3num.get())
                                        if self.age3num == 0:
                                            raise Exception('One of the grid dimensions has length 0. Please reenter the number of values.')

                                        self.starlist3[0] = user_Mbound1lo.get()
                                        self.starlist3[1] = user_Mbound1hi.get()
                                        self.starlist3[2] = user_Mbound2lo.get()
                                        self.starlist3[3] = user_Mbound2hi.get()
                                        self.starlist3[4] = user_Mbound3lo.get()
                                        self.starlist3[5] = user_Mbound3hi.get()

                                        if user_model_cho.get() == "UVIT_HST":
                                            self.stardict3[0][0] = user_Z1lowest.get()
                                            self.stardict3[0][1] = user_Z1highest.get()
                                            self.stardict3[0][2] = user_Z1num.get()
                                            self.stardict3[1][0] = user_age1lowest.get()
                                            self.stardict3[1][1] = user_age1highest.get()
                                            self.stardict3[1][2] = user_age1num.get()
                                            self.stardict3[2][0] = user_ebv1lowest.get()
                                            self.stardict3[2][1] = user_ebv1highest.get()
                                            self.stardict3[2][2] = user_ebv1num.get()
                                            self.stardict3[3][0] = user_Z2lowest.get()
                                            self.stardict3[3][1] = user_Z2highest.get()
                                            self.stardict3[3][2] = user_Z2num.get()
                                            self.stardict3[4][0] = user_age2lowest.get()
                                            self.stardict3[4][1] = user_age2highest.get()
                                            self.stardict3[4][2] = user_age2num.get()
                                            self.stardict3[5][0] = user_ebv2lowest.get()
                                            self.stardict3[5][1] = user_ebv2highest.get()
                                            self.stardict3[5][2] = user_ebv2num.get()
                                            self.stardict3[6][0] = user_Z3lowest.get()
                                            self.stardict3[6][1] = user_Z3highest.get()
                                            self.stardict3[6][2] = user_Z3num.get()
                                            self.stardict3[7][0] = user_age3lowest.get()
                                            self.stardict3[7][1] = user_age3highest.get()
                                            self.stardict3[7][2] = user_age3num.get()
                                        elif user_model_cho.get() == "UVIT_SDSS_Spitzer":
                                            self.stardict6[0][0] = user_Z1lowest.get()
                                            self.stardict6[0][1] = user_Z1highest.get()
                                            self.stardict6[0][2] = user_Z1num.get()
                                            self.stardict6[1][0] = user_age1lowest.get()
                                            self.stardict6[1][1] = user_age1highest.get()
                                            self.stardict6[1][2] = user_age1num.get()
                                            self.stardict6[2][0] = user_ebv1lowest.get()
                                            self.stardict6[2][1] = user_ebv1highest.get()
                                            self.stardict6[2][2] = user_ebv1num.get()
                                            self.stardict6[3][0] = user_Z2lowest.get()
                                            self.stardict6[3][1] = user_Z2highest.get()
                                            self.stardict6[3][2] = user_Z2num.get()
                                            self.stardict6[4][0] = user_age2lowest.get()
                                            self.stardict6[4][1] = user_age2highest.get()
                                            self.stardict6[4][2] = user_age2num.get()
                                            self.stardict6[5][0] = user_ebv2lowest.get()
                                            self.stardict6[5][1] = user_ebv2highest.get()
                                            self.stardict6[5][2] = user_ebv2num.get()
                                            self.stardict6[6][0] = user_Z3lowest.get()
                                            self.stardict6[6][1] = user_Z3highest.get()
                                            self.stardict6[6][2] = user_Z3num.get()
                                            self.stardict6[7][0] = user_age3lowest.get()
                                            self.stardict6[7][1] = user_age3highest.get()
                                            self.stardict6[7][2] = user_age3num.get()
                                        elif user_model_cho.get() == "UVIT_Johnson_GALEX":
                                            self.stardict9[0][0] = user_Z1lowest.get()
                                            self.stardict9[0][1] = user_Z1highest.get()
                                            self.stardict9[0][2] = user_Z1num.get()
                                            self.stardict9[1][0] = user_age1lowest.get()
                                            self.stardict9[1][1] = user_age1highest.get()
                                            self.stardict9[1][2] = user_age1num.get()
                                            self.stardict9[2][0] = user_ebv1lowest.get()
                                            self.stardict9[2][1] = user_ebv1highest.get()
                                            self.stardict9[2][2] = user_ebv1num.get()
                                            self.stardict9[3][0] = user_Z2lowest.get()
                                            self.stardict9[3][1] = user_Z2highest.get()
                                            self.stardict9[3][2] = user_Z2num.get()
                                            self.stardict9[4][0] = user_age2lowest.get()
                                            self.stardict9[4][1] = user_age2highest.get()
                                            self.stardict9[4][2] = user_age2num.get()
                                            self.stardict9[5][0] = user_ebv2lowest.get()
                                            self.stardict9[5][1] = user_ebv2highest.get()
                                            self.stardict9[5][2] = user_ebv2num.get()
                                            self.stardict9[6][0] = user_Z3lowest.get()
                                            self.stardict9[6][1] = user_Z3highest.get()
                                            self.stardict9[6][2] = user_Z3num.get()
                                            self.stardict9[7][0] = user_age3lowest.get()
                                            self.stardict9[7][1] = user_age3highest.get()
                                            self.stardict9[7][2] = user_age3num.get()

                                except Exception as e:
                                        print(e)
                                        tk.messagebox.showinfo('Error', "One or more parameters seem to have been entered incorrectly. Please reenter the values and try again.")
                                        return None
                                else:
                                    mwin.destroy()
        
        def openrows3():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help", "One of the components of the model flux is an interpolation term that performs a 2-D interpolation inside a grid whose axes are Z and log(age)/10. The term accepts a coordinate (Z, log(age)/10) and returns a flux for every filter, subsequently to be used in calcuating the model flux. One property of the data grid of fluxes is left as a choice to the user: its resolution. The program actually contains two grids which the user can choose between. The finer grid is a 13 X 19 grid, and the coarser grid is a 10 X 16 grid, whose ranges in Z and log(age)/10 are roughly the same. The coarser grid was introduced to prevent the optimizer from getting stuck (as it tends to when performing 2-cluster fits). The lower resolution of the grid seems to help remove any local dips in the fluxes, and makes the 2-D landscape more monotonic.")

        starno_chosen = tk.StringVar()
        checked=tk.IntVar()
        checked.set(self.checkedset)
        user_rownumber = tk.StringVar()
        user_rownumber.set(self.rownumberset)
        enterrownumberpack = tk.Frame(mwin)
        enterrownumberpack.place(x=37,y=235)
        enterrownumber = tk.Entry(enterrownumberpack,textvariable=user_rownumber,width=12)
        enterrownumber.pack(ipady=3)
        labelwhich = tk.Label(mwin,text="Read rows", bg="alice blue")
        labelwhich.place(x=39,y=205)
        def openrows():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","  •  Use csv row labelling (which should start at row 2)\n\n  •  Specify multiple rows with commas: 2,5,6\n\n  •  Specify a selection of rows with a colon: 3:8")
        def openrows2():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","The cluster distance d appears as a constant in the model flux formula:\n\nflux_mod = M*interp(age,Z)*(10[pc]/d[pc])^2*10^(-0.4*E(B-V)*(k(λ-V)+R(V)))\n\nNote that d must be in parsecs.")
        whichbutton = tk.Button(mwin,text="?",font=("TimesNewRoman 8"),command = openrows)
        whichbutton.place(x=117,y=236)
        enterdpack = tk.Frame(mwin,bg='alice blue')
        enterdpack.place(x=167,y=235)
        user_d = tk.StringVar()
        user_d.set(self.dset)
        enterd = tk.Entry(enterdpack,textvariable=user_d,width=12)
        enterd.pack(ipady=3)
        labelwhat = tk.Label(mwin,text="d",bg="alice blue")
        labelwhat.place(x=170,y=205)
        whatbutton = tk.Button(mwin,text="?"  ,font=("TimesNewRoman 8"),command = openrows2)
        whatbutton.place(x=247,y=236)
        canvas2 = tk.Canvas(mwin,relief=tk.RIDGE,bd=2,width=330,height=380,bg='azure2')
        canvas2.place(x=310,y=190)
        canvasline = tk.Canvas(mwin,bd=3,relief=tk.GROOVE,width=680,height=1000,bg='mint cream')
        canvasline.place(x=-20,y=590)
        canvasline2 = canvasline = tk.Canvas(mwin,bd=3,relief=tk.GROOVE,width=680,height=1060,bg='lavender')
        canvasline2.place(x=660,y=190)

        user_Mbound1lo = tk.DoubleVar()
        user_Mbound1hi = tk.DoubleVar()
        user_Mguess2 = tk.DoubleVar()
        user_Mbound2lo = tk.DoubleVar()
        user_Mbound2hi = tk.DoubleVar()
        user_Mbound3lo = tk.DoubleVar()
        user_Mbound3hi = tk.DoubleVar()

        ystar1labels = 670
        ystar1entries = 700
        ystar2labels = 750
        ystar2entries = 780
        ystar3labels = 830
        ystar3entries = 860
        ycheckbutton = 620

        lowerboundlabel = tk.Label(mwin,text="Lower bound",font="Arial 10 underline",bg="mint cream")
        lowerboundlabel.place(x=330,y=ystar1labels)
        upperboundlabel = tk.Label(mwin,text="Upper bound",font="Arial 10 underline",bg="mint cream")
        upperboundlabel.place(x=470,y=ystar1labels)

        label1 = tk.Label(mwin,text="log(M1)/10",font="Arial 10 underline",bg="mint cream")
        label1.place(x=50,y=ystar1labels+30)
        label2 = tk.Label(mwin,text="log(M2)/10",font="Arial 10 underline",bg="mint cream")
        label2.place(x=50,y=ystar2labels+30)
        label3 = tk.Label(mwin,text="log(M3)/10",font="Arial 10 underline",bg="mint cream")
        label3.place(x=50,y=ystar3labels+30)

        entrylowerbound1 = tk.Entry(mwin,textvariable=user_Mbound1lo,width=12)
        entrylowerbound1.place(x=330,y=ystar1entries)
        entryupperbound1 = tk.Entry(mwin,textvariable=user_Mbound1hi,width=12)
        entryupperbound1.place(x=470,y=ystar1entries)

        entrylowerbound2 = tk.Entry(mwin,textvariable=user_Mbound2lo,width=12)
        entrylowerbound2.place(x=330,y=ystar2entries)
        entryupperbound2 = tk.Entry(mwin,textvariable=user_Mbound2hi,width=12)
        entryupperbound2.place(x=470,y=ystar2entries)

        entrylowerbound3 = tk.Entry(mwin,textvariable=user_Mbound3lo,width=12)
        entrylowerbound3.place(x=330,y=ystar3entries)
        entryupperbound3 = tk.Entry(mwin,textvariable=user_Mbound3hi,width=12)
        entryupperbound3.place(x=470,y=ystar3entries)
        
        def enable(howmany):
            entrylowerbound1['state'] = tk.NORMAL
            entryupperbound1['state'] = tk.NORMAL
            if howmany == "2":
                entrylowerbound2['state'] = tk.NORMAL
                entryupperbound2['state'] = tk.NORMAL
            if howmany == "3":
                entrylowerbound2['state'] = tk.NORMAL
                entryupperbound2['state'] = tk.NORMAL
                entrylowerbound3['state'] = tk.NORMAL
                entryupperbound3['state'] = tk.NORMAL

        def disable(howmany):
            entrylowerbound1['state'] = tk.DISABLED
            entryupperbound1['state'] = tk.DISABLED
            if howmany == "2":
                entrylowerbound2['state'] = tk.DISABLED
                entryupperbound2['state'] = tk.DISABLED
            if howmany == "3":
                entrylowerbound2['state'] = tk.DISABLED
                entryupperbound2['state'] = tk.DISABLED
                entrylowerbound3['state'] = tk.DISABLED
                entryupperbound3['state'] = tk.DISABLED


        def stuff_vals():
            entrylist = [entrylowerbound1,entryupperbound1,entrylowerbound2,entryupperbound2,entrylowerbound3,entryupperbound3]
            if starno_chosen.get() == "     1-cluster fit     ":
                enable("3")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(self.starlist1[i]))
                disable("3")
                if checked.get() == 1:
                    enable("1")
            elif starno_chosen.get() == "     2-cluster fit     ":
                enable("3")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(self.starlist2[i]))
                disable("3")
                if checked.get() == 1:
                    enable("2")
            elif starno_chosen.get() == "     3-cluster fit     ":
                enable("3")
                for i,entry in enumerate(entrylist):
                    entry.delete(0,20)
                    entry.insert(0,"{}".format(self.starlist3[i]))
                disable("3")
                if checked.get() == 1:
                    enable("3")
        
        def openinfo():
            #info = tk.Toplevel()
            #info.geometry("900x560+600+250")
            #info.title("Info")
            #info.config(bg="white")
            #infolabel = tk.Label(info,bg="white",wraplength=800,justify=tk.LEFT,text="  This program uses chi-square minimization to find the best fit between the inputted flux data and a model flux function, whose form is specified by either 5 or 8 parameters, depending on the type of model selected (1-star or 2-star). For the single-star model, the model flux is determined at each data point in the input file (i.e. at each specified filter) by the log of the surface gravity log_g, the temperature T, the solar abundance (metallicity) Z, the stellar angular radius theta_r, and the interstellar reddening E(B-V). For the two-star model an additional three parameters are used to describe the cooler star: T_cool, theta_r_cool, and E_bv_cool, while the original five are relabeled with hot subscripts. In both models, theta_r appears as a quadratic term, while log_g, T, and Z are used to interpolate a flux value from a pre-existing data array that provides the \"filtered intrinsic model flux\" through each filter, given a point in those three coordinates. The filtered instrinsic model fluxes at each node (11-filter set) in the array were calculated beforehand using a similar array that provided the intrisic flux at each wavelength; namely, the calculations were done by integrating these intrinsic fluxes over the wavelengths of each filter (while also weighting by a model filter function). The final intrinsic filtered model flux (as a function of log_g, T, and Z, as well as the filter chosen) is a linear term in the current calculation. The final parameter, E(B-V), appears, along with a filter-dependent extinction factor k(λ-V), in a 10^(-0.4*E(B-V)(k(λ-V)-R_V)) term. (R_V is a constant, a parameter of the pre-calculated average extinction curve.)\n\n  If the model desired is single-star, one of these model calculations is done, wheras if the model is two-star, two of the calculations are done, with the cool-star calculation using the three new parameters. (The \"missing\" two are provided as constants in the program.) A chi-square minimization is performed, which in the two-star model involves finding the difference at every datapoint (filter) between the inputted data flux and the sum of the model fluxes for the hot and cool stars. The Python code used for the minimization process is Scipy's optimize.minimize (using the default method, with bounds and inital parameter guesses specified in this interface by the user). Errors for the best-fit parameters are found after the best fit is found, by varying the individual parameters about their best-fit values while fixing the others and stamping an upper error bound and a lower error bound when the chi-square value changes by 4.72 (for the single-star model) or by 9.14 (for the two-star model).")
            #infolabel.place(x=50,y=30)
            #info.mainloop()
            pass
        #helpgobutton = tk.Button(mwin,text="Info",font=("Arial",10),command = openinfo,pady=10,padx=35,bd=2)
        #helpgobutton.place(x=860,y=30)

        checker1 = tk.IntVar()
        checker1.set(self.checker1set)
        checker2 = tk.IntVar()
        checker2.set(self.checker2set)
        checker3 = tk.IntVar()
        checker3.set(self.checker3set)
        checker4 = tk.IntVar()
        checker4.set(self.checker4set)
        checker5 = tk.IntVar()
        checker5.set(self.checker5set)
        sliderstring1 = tk.StringVar()
        currentsliderval1 = tk.IntVar()
        currentsliderval1.set(self.sliderval1set)
        weightedmeanvarname = tk.StringVar()
        gridname = tk.StringVar()
        imgname = tk.StringVar()
        sliderstring1.set(self.sliderstring1set)
        def changesliderstring1(useless):
            if currentsliderval1.get() == 1:
                sliderstring1.set(" linear axes  ")
            elif currentsliderval1.get() == 0:
                sliderstring1.set("log-log axes")
        
        def grent1():
            if plotslider1['state'] == tk.NORMAL:
                plotslider1['state'] = tk.DISABLED
                sliderstring1.set("                     ")
                sliderlabel1.config(bg="gray95")
            elif plotslider1['state'] == tk.DISABLED:
                plotslider1['state'] = tk.NORMAL
                sliderlabel1.config(bg="white")
                if currentsliderval1.get() == 1:
                    sliderstring1.set(" linear axes  ")
                elif currentsliderval1.get() == 0:
                    sliderstring1.set("log-log axes")

        def grent2():
            if buttentry2['state'] == tk.NORMAL:
                buttentry2.delete(0,30)
                buttentry2['state'] = tk.DISABLED
            elif buttentry2['state'] == tk.DISABLED:
                buttentry2['state'] = tk.NORMAL
                buttentry2.insert(tk.END,"weighted_meanvar.csv")
        def grent3():
            if buttentry3['state'] == tk.NORMAL:
                buttentry3.delete(0,30)
                buttentry3['state'] = tk.DISABLED
            elif buttentry3['state'] == tk.DISABLED:
                buttentry3['state'] = tk.NORMAL
                buttentry3.insert(tk.END,"params_grid.csv")
        def grent4():
            if buttentry4['state'] == tk.NORMAL:
                buttentry4.delete(0,30)
                buttentry4['state'] = tk.DISABLED
            elif buttentry4['state'] == tk.DISABLED:
                buttentry4['state'] = tk.NORMAL
                buttentry4.insert(tk.END,"plot_so_rowX.png")

                
        checkbutt1 = tk.Checkbutton(mwin,text="Display results",variable=checker1,command=grent1,bg='azure2')
        plotslider1 = tk.Scale(mwin,from_=0,to=1,orient=tk.HORIZONTAL,showvalue=0,length=65,width=25,variable=currentsliderval1, command=changesliderstring1)
        plotslider1.place(x=500,y=240)
        grayframe1= tk.Frame(mwin,bg="gray95",bd=3)
        grayframe1.place(x=350,y=240)
        sliderlabel1 = tk.Label(grayframe1,textvariable=sliderstring1,padx=5,bg='white')
        sliderlabel1.pack()
        if currentsliderval1.get() == 0:
            plotslider1.set(0)
        if currentsliderval1 == 1:
            plotslider1.set(1)
        checkbutt2 = tk.Checkbutton(mwin,text="Save weighted mean and variance data",variable=checker2,command=grent2,bg='azure2')
        checkbutt3 = tk.Checkbutton(mwin,text="Save parameter grids",variable=checker3,command=grent3,bg='azure2')
        checkbutt4 = tk.Checkbutton(mwin,text="Save plot images (1 per source X)",variable=checker4,command=grent4,bg='azure2')
        checkbutt5 = tk.Checkbutton(mwin,text="Run silently",variable=checker5,bg='alice blue')
        buttentry2 = tk.Entry(mwin, textvariable = weightedmeanvarname, width=26)
        buttentry3 = tk.Entry(mwin, textvariable = gridname,width=26)
        buttentry4 = tk.Entry(mwin,textvariable = imgname,width=26)
        if checker2.get() == 0:
            buttentry2['state'] = tk.DISABLED
        if checker3.get() == 0:
            buttentry3['state'] = tk.DISABLED
        if checker4.get() == 0:
            buttentry4['state'] = tk.DISABLED
        checkbutt1.place(x=340,y=210)
        checkbutt2.place(x=340,y=310)
        checkbutt3.place(x=340,y=405)
        checkbutt4.place(x=340,y=500)
        checkbutt5.place(x=870,y=35)
        buttentry2.place(x=345,y=340)
        buttentry3.place(x=345,y=435)
        buttentry4.place(x=345,y=530)

        user_Z1lowest = tk.DoubleVar()
        user_Z1highest = tk.DoubleVar()
        user_Z1num = tk.IntVar()
        user_age1lowest = tk.DoubleVar()
        user_age1highest = tk.DoubleVar()
        user_age1num = tk.IntVar()
        user_ebv1lowest = tk.DoubleVar()
        user_ebv1highest = tk.DoubleVar()
        user_ebv1num = tk.IntVar()
        user_Z2lowest = tk.DoubleVar()
        user_Z2highest = tk.DoubleVar()
        user_Z2num = tk.IntVar()
        user_age2lowest = tk.DoubleVar()
        user_age2highest = tk.DoubleVar()
        user_age2num = tk.IntVar()
        user_ebv2lowest = tk.DoubleVar()
        user_ebv2highest = tk.DoubleVar()
        user_ebv2num = tk.IntVar()
        user_Z3lowest = tk.DoubleVar()
        user_Z3highest = tk.DoubleVar()
        user_Z3num = tk.IntVar()
        user_age3lowest = tk.DoubleVar()
        user_age3highest = tk.DoubleVar()
        user_age3num = tk.IntVar()
        xstarbentrieslo = 850
        xstarbentrieshi = 980
        xstarbentriesnum = 1110
        def infopopup():
            from tkinter import messagebox
            tk.messagebox.showinfo("Help","Values are evenly spaced, starting from the lowest value and including the highest value.")
        infobutton = tk.Button(mwin,text=" ? ",font=("TimesNewRoman 8"),command = infopopup)
        infobutton.place(x=xstarbentriesnum+100,y=240)
        lwbound = tk.Label(mwin,text="Lowest value",font="Arial 10 underline",bg="lavender").place(x=xstarbentrieslo-7,y=240)
        upbound = tk.Label(mwin,text="Highest value",font = "Arial 10 underline",bg="lavender").place(x=xstarbentrieshi-7,y=240)
        numberr = tk.Label(mwin,text="No. of values",font = "Arial 10 underline",bg="lavender").place(x=xstarbentriesnum-7,y=240)
        labelbZ1 = tk.Label(mwin,text="",bg="lavender")
        labelbZ1.place(x=xstarbentrieslo-150,y=290)
        entrybZ1lo = tk.Entry(mwin,textvariable=user_Z1lowest,width=10)
        entrybZ1lo.place(x=xstarbentrieslo,y=290)
        entrybZ1hi = tk.Entry(mwin,textvariable=user_Z1highest,width=10)
        entrybZ1hi.place(x=xstarbentrieshi,y=290)
        entrybZ1num = tk.Entry(mwin,textvariable=user_Z1num,width=10)
        entrybZ1num.place(x=xstarbentriesnum,y=290)
        labelbage1 = tk.Label(mwin,text="",bg="lavender")
        labelbage1.place(x=xstarbentrieslo-150,y=350)
        entrybage1lo = tk.Entry(mwin,textvariable=user_age1lowest,width=10)
        entrybage1lo.place(x=xstarbentrieslo,y=350)
        entrybage1hi = tk.Entry(mwin,textvariable=user_age1highest,width=10)
        entrybage1hi.place(x=xstarbentrieshi,y=350)
        entrybage1num = tk.Entry(mwin,textvariable=user_age1num,width=10)
        entrybage1num.place(x=xstarbentriesnum,y=350)
        labelbebv1 = tk.Label(mwin,text="",bg="lavender")
        labelbebv1.place(x=xstarbentrieslo-150,y=410)
        entrybebv1lo = tk.Entry(mwin,textvariable=user_ebv1lowest,width=10)
        entrybebv1lo.place(x=xstarbentrieslo,y=410)
        entrybebv1hi = tk.Entry(mwin,textvariable=user_ebv1highest,width=10)
        entrybebv1hi.place(x=xstarbentrieshi,y=410)
        entrybebv1num = tk.Entry(mwin,textvariable=user_ebv1num,width=10)
        entrybebv1num.place(x=xstarbentriesnum,y=410)
        labelbZ2 = tk.Label(mwin,text="",bg="lavender")
        labelbZ2.place(x=xstarbentrieslo-150,y=470)
        entrybZ2lo = tk.Entry(mwin,textvariable=user_Z2lowest,width=10)
        entrybZ2lo.place(x=xstarbentrieslo,y=470)
        entrybZ2hi = tk.Entry(mwin,textvariable=user_Z2highest,width=10)
        entrybZ2hi.place(x=xstarbentrieshi,y=470)
        entrybZ2num = tk.Entry(mwin,textvariable=user_Z2num,width=10)
        entrybZ2num.place(x=xstarbentriesnum,y=470)
        labelbage2 = tk.Label(mwin,text="",bg="lavender")
        labelbage2.place(x=xstarbentrieslo-150,y=530)
        entrybage2lo = tk.Entry(mwin,textvariable=user_age2lowest,width=10)
        entrybage2lo.place(x=xstarbentrieslo,y=530)
        entrybage2hi = tk.Entry(mwin,textvariable=user_age2highest,width=10)
        entrybage2hi.place(x=xstarbentrieshi,y=530)
        entrybage2num = tk.Entry(mwin,textvariable=user_age2num,width=10)
        entrybage2num.place(x=xstarbentriesnum,y=530)
        labelbebv2 = tk.Label(mwin,text="",bg="lavender")
        labelbebv2.place(x=xstarbentrieslo-150,y=590)
        entrybebv2lo = tk.Entry(mwin,textvariable=user_ebv2lowest,width=10)
        entrybebv2lo.place(x=xstarbentrieslo,y=590)
        entrybebv2hi = tk.Entry(mwin,textvariable=user_ebv2highest,width=10)
        entrybebv2hi.place(x=xstarbentrieshi,y=590)
        entrybebv2num = tk.Entry(mwin,textvariable=user_ebv2num,width=10)
        entrybebv2num.place(x=xstarbentriesnum,y=590)
        labelbZ3 = tk.Label(mwin,text="",bg="lavender")
        labelbZ3.place(x=xstarbentrieslo-150,y=650)
        entrybZ3lo = tk.Entry(mwin,textvariable=user_Z3lowest,width=10)
        entrybZ3lo.place(x=xstarbentrieslo,y=650)
        entrybZ3hi = tk.Entry(mwin,textvariable=user_Z3highest,width=10)
        entrybZ3hi.place(x=xstarbentrieshi,y=650)
        entrybZ3num = tk.Entry(mwin,textvariable=user_Z3num,width=10)
        entrybZ3num.place(x=xstarbentriesnum,y=650)
        labelbage3 = tk.Label(mwin,text="",bg="lavender")
        labelbage3.place(x=xstarbentrieslo-150,y=710)
        entrybage3lo = tk.Entry(mwin,textvariable=user_age3lowest,width=10)
        entrybage3lo.place(x=xstarbentrieslo,y=710)
        entrybage3hi = tk.Entry(mwin,textvariable=user_age3highest,width=10)
        entrybage3hi.place(x=xstarbentrieshi,y=710)
        entrybage3num = tk.Entry(mwin,textvariable=user_age3num,width=10)
        entrybage3num.place(x=xstarbentriesnum,y=710)
        
        checked2=tk.IntVar()
        checked2.set(self.checked2set)

        def enable2(howmany):
            entrybZ1lo['state'] = tk.NORMAL
            entrybZ1hi['state'] = tk.NORMAL
            entrybZ1num['state'] = tk.NORMAL
            entrybage1lo['state'] = tk.NORMAL
            entrybage1hi['state'] = tk.NORMAL
            entrybage1num['state'] = tk.NORMAL
            entrybebv1lo['state'] = tk.NORMAL
            entrybebv1hi['state'] = tk.NORMAL
            entrybebv1num['state'] = tk.NORMAL
            if howmany == "2":
                entrybZ2lo['state'] = tk.NORMAL
                entrybZ2hi['state'] = tk.NORMAL
                entrybZ2num['state'] = tk.NORMAL
                entrybage2lo['state'] = tk.NORMAL
                entrybage2hi['state'] = tk.NORMAL
                entrybage2num['state'] = tk.NORMAL
                entrybebv2lo['state'] = tk.NORMAL
                entrybebv2hi['state'] = tk.NORMAL
                entrybebv2num['state'] = tk.NORMAL
            if howmany == "3":
                entrybZ2lo['state'] = tk.NORMAL
                entrybZ2hi['state'] = tk.NORMAL
                entrybZ2num['state'] = tk.NORMAL
                entrybage2lo['state'] = tk.NORMAL
                entrybage2hi['state'] = tk.NORMAL
                entrybage2num['state'] = tk.NORMAL
                entrybebv2lo['state'] = tk.NORMAL
                entrybebv2hi['state'] = tk.NORMAL
                entrybebv2num['state'] = tk.NORMAL
                entrybZ3lo['state'] = tk.NORMAL
                entrybZ3hi['state'] = tk.NORMAL
                entrybZ3num['state'] = tk.NORMAL
                entrybage3lo['state'] = tk.NORMAL
                entrybage3hi['state'] = tk.NORMAL
                entrybage3num['state'] = tk.NORMAL

        def disable2(howmany):
            entrybZ1lo['state'] = tk.DISABLED
            entrybZ1hi['state'] = tk.DISABLED
            entrybZ1num['state'] = tk.DISABLED
            entrybage1lo['state'] = tk.DISABLED
            entrybage1hi['state'] = tk.DISABLED
            entrybage1num['state'] = tk.DISABLED
            entrybebv1lo['state'] = tk.DISABLED
            entrybebv1hi['state'] = tk.DISABLED
            entrybebv1num['state'] = tk.DISABLED
            if howmany == "2":
                entrybZ2lo['state'] = tk.DISABLED
                entrybZ2hi['state'] = tk.DISABLED
                entrybZ2num['state'] = tk.DISABLED
                entrybage2lo['state'] = tk.DISABLED
                entrybage2hi['state'] = tk.DISABLED
                entrybage2num['state'] = tk.DISABLED
                entrybebv2lo['state'] = tk.DISABLED
                entrybebv2hi['state'] = tk.DISABLED
                entrybebv2num['state'] = tk.DISABLED
            if howmany == "3":
                entrybZ2lo['state'] = tk.DISABLED
                entrybZ2hi['state'] = tk.DISABLED
                entrybZ2num['state'] = tk.DISABLED
                entrybage2lo['state'] = tk.DISABLED
                entrybage2hi['state'] = tk.DISABLED
                entrybage2num['state'] = tk.DISABLED
                entrybebv2lo['state'] = tk.DISABLED
                entrybebv2hi['state'] = tk.DISABLED
                entrybebv2num['state'] = tk.DISABLED
                entrybZ3lo['state'] = tk.DISABLED
                entrybZ3hi['state'] = tk.DISABLED
                entrybZ3num['state'] = tk.DISABLED
                entrybage3lo['state'] = tk.DISABLED
                entrybage3hi['state'] = tk.DISABLED
                entrybage3num['state'] = tk.DISABLED

        def stuff_vals2():
            entrybdict = [[entrybZ1lo,entrybZ1hi,entrybZ1num],[entrybage1lo,entrybage1hi,entrybage1num],[entrybebv1lo,entrybebv1hi,entrybebv1num],[entrybZ2lo,entrybZ2hi,entrybZ2num],[entrybage2lo,entrybage2hi,entrybage2num],[entrybebv2lo,entrybebv2hi,entrybebv2num],[entrybZ3lo,entrybZ3hi,entrybZ3num],[entrybage3lo,entrybage3hi,entrybage3num]]
            labelblistlist = [[labelbZ1,"log(Z)","log(Z_hot)","log(Z_old_1)"],[labelbage1,"log(age)/10","log(age_hot)/10","log(age_old_1)/10"],[labelbebv1,"E(B-V)","E(B-V)_hot","E(B-V)_old"],[labelbZ2,"","log(Z_cool)","log(Z_old_2)"],[labelbage2,"","log(age_cool)/10","log(age_old_2)/10"],[labelbebv2,"","E(B-V)_cool","E(B-V)_young"],[labelbZ3,"","","log(Z_young)"],[labelbage3,"","","log(age_young)/10"]]
            if user_model_cho.get() == "UVIT_HST":
                if starno_chosen.get() == "     1-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[1]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict1[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("1")
                elif starno_chosen.get() == "     2-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[2]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict2[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("2")
                elif starno_chosen.get() == "     3-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[3]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict3[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("3")

            elif user_model_cho.get() == "UVIT_SDSS_Spitzer":
                if starno_chosen.get() == "     1-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[1]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict4[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("1")
                elif starno_chosen.get() == "     2-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[2]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict5[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("2")
                elif starno_chosen.get() == "     3-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[3]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict6[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("3")
                        
            elif user_model_cho.get() == "UVIT_Johnson_GALEX":
                if starno_chosen.get() == "     1-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[1]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict7[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("1")
                elif starno_chosen.get() == "     2-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[2]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict8[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("2")
                elif starno_chosen.get() == "     3-cluster fit     ":
                    enable2("3")
                    for labelquad in labelblistlist:
                        labelquad[0].config(text="{}".format(labelquad[3]))
                    for i in range(8):
                        for j in range(3):
                            entry = entrybdict[i][j]
                            entry.delete(0,20)
                            entry.insert(0,"{}".format(self.stardict9[i][j]))
                    disable2("3")
                    if checked2.get() == 1:
                        enable2("3")

        def stuffy(useless):
            stuff_vals()
            stuff_vals2()
        
        def stuffyonly2(useless):
            stuff_vals2()


        def gray():
            if starno_chosen.get() == "     1-cluster fit     ":
                if entrylowerbound1['state'] == tk.NORMAL:
                    disable("1")
                elif entrylowerbound1['state'] == tk.DISABLED:
                    enable("1")
            elif starno_chosen.get() == "     2-cluster fit     ":
                if entrylowerbound1['state'] == tk.NORMAL:
                    disable("2")
                elif entrylowerbound1['state'] == tk.DISABLED:
                    enable("2")
            elif starno_chosen.get() == "     3-cluster fit     ":
                if entrylowerbound1['state'] == tk.NORMAL:
                    disable("3")
                elif entrylowerbound1['state'] == tk.DISABLED:
                    enable("3")
        
        def gray2():
            if starno_chosen.get() == "     1-cluster fit     ":
                if entrybZ1lo['state'] == tk.NORMAL:
                    disable2("1")
                elif entrybZ1lo['state'] == tk.DISABLED:
                    enable2("1")
            elif starno_chosen.get() == "     2-cluster fit     ":
                if entrybZ1lo['state'] == tk.NORMAL:
                    disable2("2")
                elif entrybZ1lo['state'] == tk.DISABLED:
                    enable2("2")
            elif starno_chosen.get() == "     3-cluster fit     ":
                if entrybZ1lo['state'] == tk.NORMAL:
                    disable2("3")
                elif entrybZ1lo['state'] == tk.DISABLED:
                    enable2("3")

        user_ulmeth = tk.StringVar()
        user_ulmeth.set(self.ulmethset)
        ulmethoptions = ["Standard","Limit"]
        labelulmeth = tk.Label(mwin,text="Upper limit calculation method",bg="alice blue")
        labelulmeth.place(x=37,y=320)
        ulmethmenu = tk.OptionMenu(mwin,user_ulmeth,*ulmethoptions)
        ulmethmenu.place(x=37,y=350)
        user_model_cho = tk.StringVar()
        user_model_cho.set(self.model_chosen_set)
        modelchooptions = ["UVIT_HST", "UVIT_SDSS_Spitzer", "UVIT_Johnson_GALEX"]
        modelcholabel = tk.Label(mwin,text="Model data filters",bg="alice blue")
        modelcholabel.place(x=38,y=410)
        modelchomenu = tk.OptionMenu(mwin,user_model_cho,*modelchooptions,command=stuffyonly2)
        modelchomenu.place(x=32,y=440)
        starlabel = tk.Label(mwin,text="Fitting method",bg="alice blue").place(x=38,y=500)
        starno_chosen.set(self.chosenstar)
        staroptions = ["     1-cluster fit     ","     2-cluster fit     ","     3-cluster fit     "]
        starmenu = tk.OptionMenu(mwin,starno_chosen,*staroptions,command=stuffy)
        starmenu.place(x=32,y=530)
        checkbutton = tk.Checkbutton(mwin,text="Edit bounds for log(M)",variable=checked,command=gray,bg="mint cream")
        checkbutton.place(x=10,y=ycheckbutton)
        checkbutton2 = tk.Checkbutton(mwin,text="Edit parameters grid",variable=checked2,command=gray2,bg="lavender")
        checkbutton2.place(x=680,y=200)
        
        user_filename = tk.StringVar()
        user_filename.set(self.filenamevar)
        enterfileneame = tk.Entry(mwin,textvariable = user_filename,width=72)
        enterfileneame.place(x=224,y=34)
        labeltop = tk.Label(mwin,text="Input measured flux file: ", bg='white',border=2,relief=tk.RIDGE,padx=6,pady=5)
        labeltop.place(x=35,y=29)

        gobutton = tk.Button(mwin,text="Fit data",font=("Arial",10),command = collectfilename,pady=10,padx=25,bd=2)
        gobutton.place(x=865,y=90)
        grent2()
        grent2()
        grent3()
        grent3()
        grent4()
        grent4()
        disable("3")
        disable2("3")
        stuffy(3)
        mwin.mainloop()

    ##

    def extract_measured_flux(self):
        assert self.switch == True, "Program terminated"

        '''print("self.Zguess1", self.Zguess1)
        print("self.ageguess1", self.ageguess1)
        print("self.Mguess1", self.Mguess1)
        print("self.ebvguess1", self.ebvguess1)
        print("self.Zguess2", self.Zguess2)
        print("self.ageguess2", self.ageguess2)
        print("self.Mguess2", self.Mguess2)
        print("self.ebvguess2", self.ebvguess2)

        print("self.Zbound1lo", self.Zbound1lo)
        print("self.Zbound1hi", self.Zbound1hi)
        print("self.agebound1lo", self.agebound1lo)
        print("self.agebound1hi", self.agebound1hi)
        print("self.Mbound1lo", self.Mbound1lo)
        print("self.Mbound1hi", self.Mbound1hi)
        print("self.ebvbound1lo", self.ebvbound1lo)
        print("self.ebvbound1hi", self.ebvbound1hi)
        print("self.Zbound2lo", self.Zbound2lo)
        print("self.Zbound2hi", self.Zbound2hi)
        print("self.agebound2lo", self.agebound2lo)
        print("self.agebound2hi", self.agebound2hi)
        print("self.Mbound2lo", self.Mbound2lo)
        print("self.Mbound2hi", self.Mbound2hi)
        print("self.ebvbound2lo", self.ebvbound2lo)
        print("self.ebvbound2hi", self.ebvbound2hi)'''


        if self.model_chosen == "UVIT_HST":

            import pandas as pd
            import numpy as np
            import tkinter as tk
            
            raw_columns = ["F148W_AB","F148W_err","F169M_AB","F169M_err","F172M_AB","F172M_err","N219M_AB","N219M_err","N279N_AB","N279N_err","f275w_vega","f275w_err","f336w_vega","f336w_err","f475w_vega","f475w_err","f814w_vega","f814w_err","f110w_vega","f110w_err","f160w_vega","f160w_err"]

            self.raw_magnitudes_frame = pd.DataFrame()
            for rawname in raw_columns:
                self.raw_magnitudes_frame["{}".format(rawname)] = ""

            savebadcols = []
            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_columns:
                    try:
                        curr_rowdict[colname] = self.measuredata.at[rowno,colname].item()
                    except:
                        curr_rowdict[colname] = -999
                        savebadcols.append(colname)
                self.raw_magnitudes_frame.loc[self.raw_magnitudes_frame.shape[0]] = curr_rowdict

            savebadcols = list(dict.fromkeys(savebadcols))
            badstr = ""
            for badcol in savebadcols:
                badstr += "{} or ".format(badcol)
            badstr = badstr[:-4]

            if len(badstr) != 0:
                import tkinter as tk
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Warning',"No entries found for {}. Do you wish to proceed?\n\n(These filters will not be fitted. If a single column is missing without its error or vice versa, you should double check the file for naming typos)".format(badstr))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"

            for rowind,row in self.raw_magnitudes_frame.iterrows():
                for colind,colelement in enumerate(row):
                    if colelement == -999:
                        self.raw_magnitudes_frame.iat[rowind,colind] = np.nan

        elif self.model_chosen == "UVIT_SDSS_Spitzer":
            
            import pandas as pd
            import numpy as np
            import tkinter as tk
            
            raw_columns = ["F148W_AB","F148W_err","F169M_AB","F169M_err","F172M_AB","F172M_err","N219M_AB","N219M_err","N279N_AB","N279N_err","u_prime","u_prime_err","g_prime","g_prime_err","r_prime","r_prime_err","i_prime","i_prime_err","z_prime","z_prime_err","IRAC1","IRAC1_err","IRAC2","IRAC2_err"]

            self.raw_magnitudes_frame = pd.DataFrame()
            for rawname in raw_columns:
                self.raw_magnitudes_frame["{}".format(rawname)] = ""

            savebadcols = []
            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_columns:
                    try:
                        curr_rowdict[colname] = self.measuredata.at[rowno,colname].item()
                    except:
                        curr_rowdict[colname] = -999
                        savebadcols.append(colname)
                self.raw_magnitudes_frame.loc[self.raw_magnitudes_frame.shape[0]] = curr_rowdict

            savebadcols = list(dict.fromkeys(savebadcols))
            badstr = ""
            for badcol in savebadcols:
                badstr += "{} or ".format(badcol)
            badstr = badstr[:-4]

            if len(badstr) != 0:
                import tkinter as tk
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Warning',"No entries found for {}. Do you wish to proceed?\n\n(These filters will not be fitted. If a single column is missing without its error or vice versa, you should double check the file for naming typos)".format(badstr))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"

            for rowind,row in self.raw_magnitudes_frame.iterrows():
                for colind,colelement in enumerate(row):
                    if colelement == -999:
                        self.raw_magnitudes_frame.iat[rowind,colind] = np.nan

        elif self.model_chosen == "UVIT_Johnson_GALEX":

            import pandas as pd
            import numpy as np
            import tkinter as tk
            
            raw_columns = ["F148W_AB","F148W_err","FUV","FUV_err","F169M_AB","F169M_err","F172M_AB","F172M_err","N219M_AB","N219M_err","NUV","NUV_err","N279N_AB","N279N_err","U_vega","U_err","B_vega","B_err","V_vega","V_err","R_vega","R_err","I_vega","I_err","J_vega","J_err","H_vega","H_err","K_vega","K_err"]

            self.raw_magnitudes_frame = pd.DataFrame()
            for rawname in raw_columns:
                self.raw_magnitudes_frame["{}".format(rawname)] = ""

            savebadcols = []
            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_columns:
                    try:
                        curr_rowdict[colname] = float(self.measuredata.at[rowno,colname])
                    except Exception as e:
                        curr_rowdict[colname] = -999
                        savebadcols.append(colname)
                self.raw_magnitudes_frame.loc[self.raw_magnitudes_frame.shape[0]] = curr_rowdict

            savebadcols = list(dict.fromkeys(savebadcols))
            badstr = ""
            for badcol in savebadcols:
                badstr += "{} or ".format(badcol)
            badstr = badstr[:-4]

            if len(badstr) != 0:
                import tkinter as tk
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Warning',"No entries found for {}. Do you wish to proceed?\n\n(These filters will not be fitted. If a single column is missing without its error or vice versa, you should double check the file for naming typos)".format(badstr))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"

            for rowind,row in self.raw_magnitudes_frame.iterrows():
                for colind,colelement in enumerate(row):
                    if colelement == -999:
                        self.raw_magnitudes_frame.iat[rowind,colind] = np.nan

        
    def convert_to_AB(self):
        if self.model_chosen == "UVIT_HST":
            self.ab_magnitudes_frame = self.raw_magnitudes_frame
            for col in self.ab_magnitudes_frame:
                    if col == "f275w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.496))
                    elif col == "f336w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.188))
                    elif col == "f475w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - 0.091)
                    elif col == "f814w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-0.427))
                    elif col == "f110w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-0.7595))
                    elif col == "f160w_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x - (-1.2514))
            
            self.ab_magnitudes_frame.rename(columns={"f275w_vega" : "f275w_AB", "f336w_vega" : "f336w_AB", "f475w_vega" : "f475w_AB", "f814w_vega" : "f814w_AB", "f110w_vega" : "f110w_AB", "f160w_vega" : "f160w_AB"}, inplace=True)
        
        elif self.model_chosen == "UVIT_SDSS_Spitzer":
            pass

        elif self.model_chosen == "UVIT_Johnson_GALEX": 
            self.ab_magnitudes_frame = self.raw_magnitudes_frame
            for col in self.ab_magnitudes_frame:
                    if col == "U_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 0.79)
                    elif col == "B_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + (-0.09))
                    elif col == "V_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 0.02)
                    elif col == "R_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 0.21)
                    elif col == "I_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 0.45)
                    elif col == "J_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 0.91)
                    elif col == "H_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 1.39)
                    elif col == "K_vega":
                        self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: x + 1.85)
            
            self.ab_magnitudes_frame.rename(columns={"U_vega" : "U_AB", "B_vega" : "B_AB", "V_vega" : "V_AB", "R_vega" : "R_AB", "I_vega" : "I_AB", "J_vega" : "J_AB", "H_vega" : "H_AB", "K_vega" : "K_AB"}, inplace=True)
    
    def extract_ul(self):

        if self.model_chosen == "UVIT_HST":
            import pandas as pd
            import numpy as np
            import tkinter as tk

            raw_limits = ["F148W_ul","F169M_ul","F172M_ul","N219M_ul","N279N_ul","f275w_ul","f336w_ul","f475w_ul","f814w_ul","f110w_ul","f160w_ul"]
            
            self.ul_frame = pd.DataFrame()
            for rawname in raw_limits:
                self.ul_frame["{}".format(rawname)] = ""

            saverowuls = []
            savecoluls = []
            badcoluls = []
            first_time = True
            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_limits:
                    try:
                        if self.measuredata.at[rowno,colname] == ">":
                            curr_rowdict[colname] = 1
                            savecoluls.append(colname)
                            saverowuls.append(str(rowno+2))
                        else:
                            curr_rowdict[colname] = 0
                    except:
                        curr_rowdict[colname] = np.nan
                        badcoluls.append(colname)
                self.ul_frame.loc[self.ul_frame.shape[0]] = curr_rowdict
                
                if first_time == True and len(badcoluls) > 0:
                    miniwin2 = tk.Tk()
                    miniwin2.geometry("10x10+800+500")
                    savebadcols2 = list(dict.fromkeys(badcoluls))
                    badstr2 = ""
                    for badcol2 in savebadcols2:
                        badstr2 += "{} or ".format(badcol2)
                    badstr2 = badstr2[:-4]
                    response2 = tk.messagebox.askquestion('Warning',"No upper limit columns found for {}. Do you wish to proceed?".format(badstr2))
                    if response2 == "yes":
                        miniwin2.destroy()
                        first_time = False
                    if response2 == "no":
                        assert response2 == "yes", "Program terminated"
            
            if len(savecoluls) > 0:
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Info',"Upper limits detected in columns {} in rows {}, respectively. If this sounds correct, click yes to continue.".format(", ".join(savecoluls),", ".join(saverowuls)))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"
        
        elif self.model_chosen == "UVIT_SDSS_Spitzer":
            import pandas as pd
            import numpy as np

            raw_limits = ["F14_ul","F16_ul","F17_ul","N2_ul","N27_ul","a1_ul","a2_ul","a3_ul","a4_ul","a5_ul","a6_ul","a7_ul"]
            
            self.ul_frame = pd.DataFrame()
            for rawname in raw_limits:
                self.ul_frame["{}".format(rawname)] = ""

            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_limits:
                  curr_rowdict[colname] = 0
                self.ul_frame.loc[self.ul_frame.shape[0]] = curr_rowdict

        elif self.model_chosen == "UVIT_Johnson_GALEX":
            import pandas as pd
            import numpy as np
            import tkinter as tk

            raw_limits = ["F148W_ul", "FUV_ul", "F169M_ul","F172M_ul","N219M_ul", "NUV_ul", "N279N_ul","U_ul","B_ul","V_ul","R_ul","I_ul","J_ul","H_ul","K_ul"]
            
            self.ul_frame = pd.DataFrame()
            for rawname in raw_limits:
                self.ul_frame["{}".format(rawname)] = ""

            saverowuls = []
            savecoluls = []
            badcoluls = []
            first_time = True
            for rowno in self.rows:
                curr_rowdict = {}
                for colname in raw_limits:
                    try:
                        if self.measuredata.at[rowno,colname] == ">":
                            curr_rowdict[colname] = 1
                            savecoluls.append(colname)
                            saverowuls.append(str(rowno+2))
                        else:
                            curr_rowdict[colname] = 0
                    except:
                        curr_rowdict[colname] = np.nan
                        badcoluls.append(colname)
                self.ul_frame.loc[self.ul_frame.shape[0]] = curr_rowdict
                
                if first_time == True and len(badcoluls) > 0:
                    miniwin2 = tk.Tk()
                    miniwin2.geometry("10x10+800+500")
                    savebadcols2 = list(dict.fromkeys(badcoluls))
                    badstr2 = ""
                    for badcol2 in savebadcols2:
                        badstr2 += "{} or ".format(badcol2)
                    badstr2 = badstr2[:-4]
                    response2 = tk.messagebox.askquestion('Warning',"No upper limit columns found for {}. Do you wish to proceed?".format(badstr2))
                    if response2 == "yes":
                        miniwin2.destroy()
                        first_time = False
                    if response2 == "no":
                        assert response2 == "yes", "Program terminated"
            
            if len(savecoluls) > 0:
                miniwin = tk.Tk()
                miniwin.geometry("10x10+800+500")
                response = tk.messagebox.askquestion('Info',"Upper limits detected in columns {} in rows {}, respectively. If this sounds correct, click yes to continue.".format(", ".join(savecoluls),", ".join(saverowuls)))
                if response == "yes":
                    miniwin.destroy()
                if response == "no":
                    assert response == "yes", "Program terminated"

    def convert_to_bandflux(self):

        if self.model_chosen == "UVIT_HST":

            self.filternames = ["F148W","F169M","F172M","N219M","N279N","f275w","f336w","f475w","f814w","f110w","f160w"]
            self.bandfluxes = pd.DataFrame()
            self.bandfluxerrors = pd.DataFrame()
            self.avgwvlist = [148.1, 160.8, 171.7, 219.6, 279.2, 270.4, 335.5, 477.3, 802.4, 1153.4, 1536.9]
            #self.avgwvlist = [150.2491,161.4697,170.856,199.1508,276.0,267.884375,336.8484,476.0,833.0,1096.7245,1522.1981]
            #self.allextinct = [5.52548923, 5.17258596, 5.0540947, 5.83766858, 3.49917568, 3.25288368, 1.95999799, 0.62151591, -1.44589933, -2.10914243, -2.51310314]
            self.allextinct = [5.62427152,  5.18640888,  5.04926289,  6.99406125,  3.15901211,  3.42340971, 1.97787612,  0.61008783, -1.33280758, -2.18810981, -2.52165626]

            for colind,col in enumerate(self.ab_magnitudes_frame):
                if colind%2 == 0:
                    self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: (10**(-0.4*(48.60+x)))*10**26)
                    self.bandfluxes["{}".format(col)] = self.ab_magnitudes_frame[col]
                elif colind%2 != 0:
                    for rowind in range(len(self.ab_magnitudes_frame[col])):
                        self.ab_magnitudes_frame.iloc[rowind,colind] = self.ab_magnitudes_frame.iloc[rowind,colind-1]*self.ab_magnitudes_frame.iloc[rowind,colind]/1.0857
                    self.bandfluxerrors["{}".format(col)] = self.ab_magnitudes_frame[col]
        
        elif self.model_chosen == "UVIT_SDSS_Spitzer":

            self.filternames = ["F148W","F169M","F172M","N219M","N279N","u_prime","g_prime","r_prime","i_prime","z_prime","IRAC1","IRAC2"]
            self.bandfluxes = pd.DataFrame()
            self.bandfluxerrors = pd.DataFrame()
            self.avgwvlist = [150.2491, 161.4697, 170.856, 199.1508, 276.0, 355.1, 468.6, 616.6, 748, 893, 3550, 4490]
            self.allextinct = [5.52548923,  5.17258596,  5.0540947,   5.83766858,  3.25288368,  1.74741802, 0.68710903, -0.42704846, -1.11016491, -1.64589927, -2.89828005, -2.93432827]
            for colind,col in enumerate(self.raw_magnitudes_frame):
                if colind%2 == 0:
                    self.bandfluxes["{}".format(col)] = self.raw_magnitudes_frame[col]
                elif colind%2 != 0:
                    self.bandfluxerrors["{}".format(col)] = self.raw_magnitudes_frame[col]

        elif self.model_chosen == "UVIT_Johnson_GALEX":

            self.filternames = ["F148W", "FUV", "F169M", "F172M", "N219M", "NUV", "N279N", "U", "B", "V", "R", "I", "J", "H", "K"]
            self.bandfluxes = pd.DataFrame()
            self.bandfluxerrors = pd.DataFrame()
            self.avgwvlist = [148.1, 152.8, 160.8, 171.7, 219.6, 227.1, 279.2, 373.5, 444.3, 548.3, 685.5, 863.7, 1230, 1640, 2200]
            self.allextinct = [5.62427152, 5.421872558991813, 5.18640888, 5.04926289, 6.99406125,  6.373666896159239, 3.15901211, 1.56625775, 0.90822229, 0.03461861, -0.81424956, -1.55160369, -2.2788131400496705, -2.575634456801791, -2.753247951200635]
            for colind,col in enumerate(self.ab_magnitudes_frame):
                if colind%2 == 0:
                    self.ab_magnitudes_frame[col] = self.ab_magnitudes_frame[col].apply(lambda x: (10**(-0.4*(48.60+x)))*10**26)
                    self.bandfluxes["{}".format(col)] = self.ab_magnitudes_frame[col]
                elif colind%2 != 0:
                    for rowind in range(len(self.ab_magnitudes_frame[col])):
                        self.ab_magnitudes_frame.iloc[rowind,colind] = self.ab_magnitudes_frame.iloc[rowind,colind-1]*self.ab_magnitudes_frame.iloc[rowind,colind]/1.0857
                    self.bandfluxerrors["{}".format(col)] = self.ab_magnitudes_frame[col]

    def buildGrid(self):
        import numpy as np

        if self.single_cluster == True:
            Z1vals = np.linspace(self.Z1lowest,self.Z1highest,self.Z1num)
            age1vals = np.linspace(self.age1lowest,self.age1highest,self.age1num)
            ebv1vals = np.linspace(self.ebv1lowest,self.ebv1highest,self.ebv1num)

            self.Z1grid,self.age1grid,self.ebv1grid = np.meshgrid(Z1vals,age1vals,ebv1vals,indexing='ij')

        elif self.double_cluster == True:
            Z1vals = np.linspace(self.Z1lowest,self.Z1highest,self.Z1num)
            age1vals = np.linspace(self.age1lowest,self.age1highest,self.age1num)
            ebv1vals = np.linspace(self.ebv1lowest,self.ebv1highest,self.ebv1num)
            Z2vals = np.linspace(self.Z2lowest,self.Z2highest,self.Z2num)
            age2vals = np.linspace(self.age2lowest,self.age2highest,self.age2num)
            ebv2vals = np.linspace(self.ebv2lowest,self.ebv2highest,self.ebv2num)

            self.Z1grid,self.age1grid,self.ebv1grid,self.Z2grid,self.age2grid,self.ebv2grid = np.meshgrid(Z1vals,age1vals,ebv1vals,Z2vals,age2vals,ebv2vals,indexing='ij')
        
        elif self.triple_cluster == True:
            Z1vals = np.linspace(self.Z1lowest,self.Z1highest,self.Z1num)
            age1vals = np.linspace(self.age1lowest,self.age1highest,self.age1num)
            ebv1vals = np.linspace(self.ebv1lowest,self.ebv1highest,self.ebv1num)
            Z2vals = np.linspace(self.Z2lowest,self.Z2highest,self.Z2num)
            age2vals = np.linspace(self.age2lowest,self.age2highest,self.age2num)
            ebv2vals = np.linspace(self.ebv2lowest,self.ebv2highest,self.ebv2num)
            Z3vals = np.linspace(self.Z3lowest,self.Z3highest,self.Z3num)
            age3vals = np.linspace(self.age3lowest,self.age3highest,self.age3num)

            self.Z1grid,self.age1grid,self.ebv1grid,self.Z2grid,self.age2grid,self.ebv2grid,self.Z3grid,self.age3grid = np.meshgrid(Z1vals,age1vals,ebv1vals,Z2vals,age2vals,ebv2vals,Z3vals,age3vals,indexing='ij')
        
    def prepare_for_interpolation(self):
        import pandas as pd
        import xarray as xr
        import numpy as np

        if self.model_chosen == "UVIT_HST":

            fluxdata = pd.read_csv("fluxpersolarmassUVIT_HST.csv")
            
            blankdata = np.zeros((13,19,11))

            row=0
            for Z in range(13):
                for age in range(19):
                    for filt in range(11):
                        blankdata[Z,age,filt] = fluxdata.iat[row,filt]
                    row += 1

            filleddata = blankdata

            zcoordlist = [-2.617,-2.36173,-2.11185,-1.86881,-1.62577,-1.37645,-1.12564,-0.87822,-0.63202,-0.38809,-0.14836,0.08353,0.303332]
            agecoordlist = [.66,.68,.70,.72,.74,.76,.78,.80,.82,.84,.86,.88,.90,.92,.94,.96,.98,1.0,1.2]
            filtercoordlist = [0,1,2,3,4,5,6,7,8,9,10]

            self.da = xr.DataArray(filleddata,coords=[("Z",zcoordlist),("Age",agecoordlist),("Filter",filtercoordlist)])

        elif self.model_chosen == "UVIT_SDSS_Spitzer":
            fluxdata = pd.read_csv("fluxpersolarmassSDSS_Spitzer.csv")
            
            blankdata = np.zeros((13,19,12))

            row=0
            for Z in range(13):
                for age in range(19):
                    for filt in range(12):
                        blankdata[Z,age,filt] = fluxdata.iat[row,filt]
                    row += 1

            filleddata = blankdata

            zcoordlist = [-2.617,-2.36173,-2.11185,-1.86881,-1.62577,-1.37645,-1.12564,-0.87822,-0.63202,-0.38809,-0.14836,0.08353,0.303332]
            agecoordlist = [.66,.68,.70,.72,.74,.76,.78,.80,.82,.84,.86,.88,.90,.92,.94,.96,.98,1.0,1.2]
            filtercoordlist = [0,1,2,3,4,5,6,7,8,9,10,11]

            self.da = xr.DataArray(filleddata,coords=[("Z",zcoordlist),("Age",agecoordlist),("Filter",filtercoordlist)])

        elif self.model_chosen == "UVIT_Johnson_GALEX":

            fluxdata = pd.read_csv("fluxpersolarmassUVIT_Johnson_GALEX.csv")
            
            blankdata = np.zeros((13,19,15))

            row=0
            for Z in range(13):
                for age in range(19):
                    for filt in range(15):
                        blankdata[Z,age,filt] = fluxdata.iat[row,filt]
                    row += 1

            filleddata = blankdata

            zcoordlist = [-2.617,-2.36173,-2.11185,-1.86881,-1.62577,-1.37645,-1.12564,-0.87822,-0.63202,-0.38809,-0.14836,0.08353,0.303332]
            agecoordlist = [.66,.68,.70,.72,.74,.76,.78,.80,.82,.84,.86,.88,.90,.92,.94,.96,.98,1.0,1.2]
            filtercoordlist = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]

            self.da = xr.DataArray(filleddata,coords=[("Z",zcoordlist),("Age",agecoordlist),("Filter",filtercoordlist)])

    ##blue

    def interpolate(self,Z,age,valid_filters_this_row):
        interpolist = []
        interpolated = self.da.interp(Z = Z, Age = age)
        for valid_filter in valid_filters_this_row:
            interpolist.append(interpolated.sel(Filter = valid_filter).data.item()*10**26)
        return interpolist
    
    def extinction(self,valid_filters_this_row):
        extinctlist = []
        for valid_filter in valid_filters_this_row:
            extinctlist.append(self.allextinct[valid_filter])
        return extinctlist

    def minichisqfunc_single(self,M1,Z1,age1,ebv1,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M = 10**(M1*10)

        mean_models = []
        interpolist = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models.append(true_M*interpolist[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - mean_models[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        mean_chisq = sum(summands)
        return mean_models, mean_chisq

    def minichisqfunc2_single(self,M1,Z1,age1,ebv1,valid_filters_this_row,ul_filters_this_row,curr_row):
        if self.silent is False:
            print("Fitting M1 to other mean parameters: Testing row {} with Z1, age1, M1, ebv1: ".format(self.rows[curr_row]+2), Z1,age1,M1,ebv1)

        true_M = 10**(M1*10)

        mean_models = []
        interpolist = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models.append(true_M*interpolist[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - mean_models[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        new_chisq = sum(summands)
        if self.silent is False:
            print("chisq: ", new_chisq)

        return new_chisq

    def minichisqfunc_double(self,M1,M2,Z1,age1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)

        mean_models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))
        
        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models1[i]+mean_models2[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -mean_models1[i]-mean_models2[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
        mean_chisq = sum(summands)
        return mean_models1, mean_models2, mean_chisq

    def minichisqfunc2_double(self,tup,Z1,age1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
        M1, M2 = tup

        if self.silent is False:
            print("Fitting Ms to other mean parameters: Testing row {} with Z1, age1, M1, ebv1, Z2, age2, M2, ebv2: ".format(self.rows[curr_row]+2), Z1,age1,M1,ebv1,Z2,age2,M2,ebv2)

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)

        mean_models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv2*(extinctolist2[i]+3.001))))
        
        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models1[i]+mean_models2[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -mean_models1[i]-mean_models2[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        new_chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",new_chisq)

        return new_chisq

    def minichisqfunc_triple(self,M_old_1,M_old_2,M_young,Z_old_1,age_old_1,ebv_old,Z_old_2,age_old_2,ebv_young,Z_young,age_young,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M_old_1 = 10**(M_old_1*10)
        true_M_old_2 = 10**(M_old_2*10)
        true_M_young = 10**(M_young*10)

        mean_models1 = []
        interpolist1 = self.interpolate(Z_old_1,age_old_1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(true_M_old_1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv_old*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(Z_old_2,age_old_2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(true_M_old_2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv_old*(extinctolist2[i]+3.001))))
        mean_models3 = []
        interpolist3 = self.interpolate(Z_young,age_young,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models3.append(true_M_young*interpolist3[i]*(10/self.d)**2*10**(-0.4*(ebv_young*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models1[i]+mean_models2[i]+mean_models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i]-mean_models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -mean_models1[i]-mean_models2[i]-mean_models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i]-mean_models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        mean_chisq = sum(summands)

        return mean_models1,mean_models2,mean_models3, mean_chisq

    def minichisqfunc2_triple(self,tup,Z_old_1,age_old_1,ebv_old,Z_old_2,age_old_2,ebv_young,Z_young,age_young,valid_filters_this_row,ul_filters_this_row,curr_row):

        M_old_1,M_old_2,M_young = tup

        if self.silent is False:
            print("Fitting Ms to other mean parameters: Testing row {} with Z1, age1, M1, ebv1, Z2, age2, M2, ebv2, Z3, age3, M3: ".format(self.rows[curr_row]+2), Z_old_1,age_old_1,M_old_1,ebv_old,Z_old_2,age_old_2,M_old_2,ebv_young,Z_young,age_young,M_young)

        true_M_old_1 = 10**(M_old_1*10)
        true_M_old_2 = 10**(M_old_2*10)
        true_M_young = 10**(M_young*10)

        mean_models1 = []
        interpolist1 = self.interpolate(Z_old_1,age_old_1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models1.append(true_M_old_1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv_old*(extinctolist1[i]+3.001))))
        mean_models2 = []
        interpolist2 = self.interpolate(Z_old_2,age_old_2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models2.append(true_M_old_2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv_old*(extinctolist2[i]+3.001))))
        mean_models3 = []
        interpolist3 = self.interpolate(Z_young,age_young,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            mean_models3.append(true_M_young*interpolist3[i]*(10/self.d)**2*10**(-0.4*(ebv_young*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if mean_models1[i]+mean_models2[i]+mean_models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i]-mean_models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -mean_models1[i]-mean_models2[i]-mean_models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - mean_models1[i]-mean_models2[i]-mean_models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        new_chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",new_chisq)

        return new_chisq

    def chisqfunc(self,M,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row):
        if self.silent is False:
            print("Testing row {} with log(Z), log(age)/10, log(M)/10, E_bv: ".format(self.rows[curr_row]+2), Z,age,M,ebv)

        true_M = 10**(M*10)

        models = []
        interpolist = self.interpolate(Z,age,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models.append(true_M*interpolist[i]*(10/self.d)**2*10**(-0.4*(ebv*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - models[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",chisq,"\n")

        return chisq

    def chisqfunc2(self,tup,Z1,age1,E_bv1,Z2,age2,E_bv2,valid_filters_this_row,ul_filters_this_row,curr_row):
        M1,M2 = tup
        if self.silent is False:
            print("Testing row {} with log(Z1), log(age1)/10, log(M1)/10, E_bv1, log(Z2), log(age2)/10, log(M2)/10, E_bv2: ".format(self.rows[curr_row]+2), Z1, age1, M1, E_bv1, Z2, age2, M2, E_bv2)

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -models1[i]-models2[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",chisq,"\n")
        return chisq

    def chisqfunc3(self,tup,Z_old_1,age_old_1,E_bv_old,Z_old_2,age_old_2,E_bv_new,Z_new,age_new,valid_filters_this_row,ul_filters_this_row,curr_row):
        M_old_1,M_old_2,M_new = tup
        if self.silent is False:
            print("Testing row {} with log(Z_old_1), log(age_old_1)/10, log(M_old_1)/10, E(B-V)_old, log(Z_old_2), log(age_old_2)/10, log(M_old_2)/10, E(B-V)_new, log(Z_new), log(age_new)/10, log(M_new)/10: ".format(self.rows[curr_row]+2),Z_old_1,age_old_1,M_old_1,E_bv_old,Z_old_2,age_old_2,M_old_2,E_bv_new,Z_new,age_new,M_new)

        true_M_old_1 = 10**(M_old_1*10)
        true_M_old_2 = 10**(M_old_2*10)
        true_M_new = 10**(M_new*10)

        models1 = []
        interpolist1 = self.interpolate(Z_old_1,age_old_1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M_old_1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(E_bv_old*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z_old_2,age_old_2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M_old_2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(E_bv_old*(extinctolist2[i]+3.001))))
        models3 = []
        interpolist3 = self.interpolate(Z_new,age_new,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models3.append(true_M_new*interpolist3[i]*(10/self.d)**2*10**(-0.4*(E_bv_new*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i]+models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -models1[i]-models2[i]-models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                
        chisq = sum(summands)
        if self.silent is False:
            print("chisq: ",chisq,"\n")
        return chisq
    
    def chisqfuncerror(self,M,mean_chi2,Z,age,E_bv,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M = 10**(M*10)

        models = []
        interpolist = self.interpolate(Z,age,valid_filters_this_row)
        extinctolist = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models.append(true_M*interpolist[i]*(10/self.d)**2*10**(-0.4*(E_bv*(extinctolist[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - models[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)


        chisq = sum(summands) - mean_chi2 - 4.28
        return chisq

    def chisqfunc2error_1(self,M1,mean_chi2,Z1,age1,E_bv1,Z2,age2,M2,E_bv2,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - models1[i]-models2[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands) - mean_chi2 - 9.32
        return chisq

    def chisqfunc2error_2(self,M2,mean_chi2,Z1,age1,M1,E_bv1,Z2,age2,E_bv2,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(E_bv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(E_bv2*(extinctolist2[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 - models1[i]-models2[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands) - mean_chi2 - 9.32
        return chisq

    def chisqfunc3error_1(self,M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)
        true_M3 = 10**(M3*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist2[i]+3.001))))
        models3 = []
        interpolist3 = self.interpolate(Z3,age3,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models3.append(true_M3*interpolist3[i]*(10/self.d)**2*10**(-0.4*(ebv2*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i]+models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -models1[i]-models2[i]-models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands) - mean_chi2 - 12.77
        return chisq

    def chisqfunc3error_2(self,M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)
        true_M3 = 10**(M3*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist2[i]+3.001))))
        models3 = []
        interpolist3 = self.interpolate(Z3,age3,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models3.append(true_M3*interpolist3[i]*(10/self.d)**2*10**(-0.4*(ebv2*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i]+models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -models1[i]-models2[i]-models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands) - mean_chi2 - 12.77
        return chisq

    def chisqfunc3error_3(self,M3,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row):

        true_M1 = 10**(M1*10)
        true_M2 = 10**(M2*10)
        true_M3 = 10**(M3*10)

        models1 = []
        interpolist1 = self.interpolate(Z1,age1,valid_filters_this_row)
        extinctolist1 =self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models1.append(true_M1*interpolist1[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist1[i]+3.001))))
        models2 = []
        interpolist2 = self.interpolate(Z2,age2,valid_filters_this_row)
        extinctolist2 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models2.append(true_M2*interpolist2[i]*(10/self.d)**2*10**(-0.4*(ebv1*(extinctolist2[i]+3.001))))
        models3 = []
        interpolist3 = self.interpolate(Z3,age3,valid_filters_this_row)
        extinctolist3 = self.extinction(valid_filters_this_row)
        for i in range(len(valid_filters_this_row)):
            models3.append(true_M3*interpolist3[i]*(10/self.d)**2*10**(-0.4*(ebv2*(extinctolist3[i]+3.001))))

        summands = []
        for i,valid_ind in enumerate(valid_filters_this_row):
            if valid_ind in ul_filters_this_row:
                if self.ulmeth == "Limit":
                    if models1[i]+models2[i]+models3[i] - self.bandfluxes.iat[curr_row,valid_ind] > 0:
                        summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)
                    else:
                        pass
                elif self.ulmeth == "Standard":
                    summands.append(((self.bandfluxes.iat[curr_row,valid_ind]/3 -models1[i]-models2[i]-models3[i])/(self.bandfluxes.iat[curr_row,valid_ind]/3))**2)
            else:
                summands.append(((self.bandfluxes.iat[curr_row,valid_ind] - models1[i]-models2[i]-models3[i])/self.bandfluxerrors.iat[curr_row,valid_ind])**2)

        chisq = sum(summands) - mean_chi2 - 12.77
        return chisq

    def minimize_chisq(self):
        import numpy as np
        from math import exp, sqrt
        from scipy.optimize import Bounds
        
        if self.single_cluster == True:
            bnds = Bounds([self.Mbound1lo],[self.Mbound1hi])
            x0 = np.array([(self.Mbound1lo+self.Mbound1hi)/2])    

            self.mean_Z1s = []
            self.mean_age1s = []
            self.mean_M1s = []
            self.mean_ebv1s = []
            
            self.var_Z1s = []
            self.var_age1s = []
            self.var_M1s = []
            self.var_ebv1s = []

            self.sigma_Z1s = []
            self.sigma_age1s = []
            self.sigma_M1s = []
            self.sigma_ebv1s = []

            self.gridM1s = []
            self.gridChisqs = []

            self.smallest_chi2s = []
            self.smallest_chi2_params = []

            self.newM1s = []
            self.newchi2s = []

            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1: 
                        ul_filters_this_row.append(valid_ind)

                gridChisq = np.zeros((self.Z1num,self.age1num,self.ebv1num))
                gridM = np.zeros((self.Z1num,self.age1num,self.ebv1num))
                Wtot = 0
                smallest_chi2 = 1e14
                smallest_chi2_params = np.zeros(4)
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            Z1 = self.Z1grid[i,j,k]
                            age1 = self.age1grid[i,j,k]
                            ebv1 = self.ebv1grid[i,j,k]
                            res = opt.minimize(self.chisqfunc, x0, args=(Z1,age1,ebv1,valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)
                            chi2 = res.fun
                            M1 = res.x[0]
                            gridChisq[i,j,k] = chi2
                            print("optimized chi2: ",chi2)
                            gridM[i,j,k] = M1
                            print("optimized log(M1)/10: ",M1)
                            print("\n")
                            if chi2 < smallest_chi2:
                                smallest_chi2 = chi2
                                smallest_chi2_params[0] = Z1
                                smallest_chi2_params[1] = age1
                                smallest_chi2_params[2] = M1
                                smallest_chi2_params[3] = ebv1

                self.smallest_chi2s.append(0)
                self.smallest_chi2s[curr_row] = smallest_chi2
                print("Smallest chi2 for row {}: {}".format(self.rows[curr_row]+2,smallest_chi2))
                self.smallest_chi2_params.append(0)
                self.smallest_chi2_params[curr_row] = smallest_chi2_params
                print("Associated parameter values: Z1 {}, age1 {}, M1 {}, ebv1 {}".format(smallest_chi2_params[0],smallest_chi2_params[1],smallest_chi2_params[2],smallest_chi2_params[3]))
                gridChisq -= smallest_chi2
                self.mean_Z1s.append(0)
                self.mean_age1s.append(0)
                self.mean_M1s.append(0)
                self.mean_ebv1s.append(0)
                
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num): 
                            Z1 = self.Z1grid[i,j,k]
                            age1 = self.age1grid[i,j,k]
                            M1 = gridM[i,j,k]
                            ebv1 = self.ebv1grid[i,j,k]
                            chi2 = gridChisq[i,j,k]

                            Wtot += exp(-chi2/2)
                            self.mean_Z1s[curr_row] += exp(-chi2/2)*Z1
                            self.mean_age1s[curr_row] += exp(-chi2/2)*age1
                            self.mean_M1s[curr_row] += exp(-chi2/2)*M1
                            self.mean_ebv1s[curr_row] += exp(-chi2/2)*ebv1
                                
                self.mean_Z1s[curr_row] /= Wtot
                self.mean_age1s[curr_row] /= Wtot
                self.mean_M1s[curr_row] /= Wtot
                self.mean_ebv1s[curr_row] /= Wtot

                print("weighted mean Z1 ", self.mean_Z1s[curr_row])
                print("weighted mean age1 ", self.mean_age1s[curr_row])
                print("weighted mean M1 ", self.mean_M1s[curr_row])
                print("weighted mean ebv1 ", self.mean_ebv1s[curr_row])

                self.var_Z1s.append(0)
                self.var_age1s.append(0)
                self.var_M1s.append(0)
                self.var_ebv1s.append(0)

                self.sigma_Z1s.append(0)
                self.sigma_age1s.append(0)
                self.sigma_M1s.append(0)
                self.sigma_ebv1s.append(0)

                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            Z1 = self.Z1grid[i,j,k]
                            age1 = self.age1grid[i,j,k]
                            M1 = gridM[i,j,k]
                            ebv1 = self.ebv1grid[i,j,k]
                            chi2 = gridChisq[i,j,k]

                            self.var_Z1s[curr_row] += exp(-chi2/2)*(Z1-self.mean_Z1s[curr_row])*(Z1-self.mean_Z1s[curr_row])
                            self.var_age1s[curr_row] += exp(-chi2/2)*(age1-self.mean_age1s[curr_row])*(age1-self.mean_age1s[curr_row])
                            self.var_M1s[curr_row] += exp(-chi2/2)*(M1-self.mean_M1s[curr_row])*(M1-self.mean_M1s[curr_row])
                            self.var_ebv1s[curr_row] += exp(-chi2/2)*(ebv1-self.mean_ebv1s[curr_row])*(ebv1-self.mean_ebv1s[curr_row])
                                
                gridChisq += smallest_chi2
                self.gridM1s.append(gridM.flatten())
                self.gridChisqs.append(gridChisq.flatten())
                                
                self.var_Z1s[curr_row] /= Wtot
                self.var_age1s[curr_row] /= Wtot
                self.var_M1s[curr_row] /= Wtot
                self.var_ebv1s[curr_row] /= Wtot

                self.sigma_Z1s[curr_row] = sqrt(self.var_Z1s[curr_row])
                self.sigma_age1s[curr_row] = sqrt(self.var_age1s[curr_row])
                self.sigma_M1s[curr_row] = sqrt(self.var_M1s[curr_row])
                self.sigma_ebv1s[curr_row] = sqrt(self.var_ebv1s[curr_row])

                print("weighted var Z1 ", self.var_Z1s[curr_row])
                print("sigma Z1 (sqrt weighted var Z1) ", self.sigma_Z1s[curr_row])
                print("weighted var age1 ", self.var_age1s[curr_row])
                print("sigma age1 (sqrt weighted var age1) ", self.sigma_age1s[curr_row])
                print("weighted var M1 ", self.var_M1s[curr_row])
                print("sigma M1 (sqrt weighted var M1) ", self.sigma_M1s[curr_row])
                print("weighted var ebv1 ", self.var_ebv1s[curr_row])
                print("sigma ebv1 (sqrt weighted var ebv1) ", self.sigma_ebv1s[curr_row])

                x02 = np.array([self.mean_M1s[curr_row]])
                res2 = opt.minimize(self.minichisqfunc2_single, x02, args=(self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)

                newchi2 = res2.fun
                newM1 = res2.x[0]

                print("chi2 of fitted M to other mean parameters: ", newchi2)
                print("fitted M1 to other mean parameters: ", newM1)

                self.newchi2s.append(newchi2)
                self.newM1s.append(newM1)
        
        elif self.double_cluster == True:
            bnds = Bounds([self.Mbound1lo,self.Mbound2lo],[self.Mbound1hi,self.Mbound2hi])
            x0 = np.array([(self.Mbound1lo+self.Mbound1hi)/2,(self.Mbound2lo+self.Mbound2hi)/2])
            self.mean_Z1s = []
            self.mean_age1s = []
            self.mean_M1s = []
            self.mean_ebv1s = []
            self.mean_Z2s = []
            self.mean_age2s = []
            self.mean_M2s = []
            self.mean_ebv2s = []
            
            self.var_Z1s = []
            self.var_age1s = []
            self.var_M1s = []
            self.var_ebv1s = []
            self.var_Z2s = []
            self.var_age2s = []
            self.var_M2s = []
            self.var_ebv2s = []

            self.sigma_Z1s = []
            self.sigma_age1s = []
            self.sigma_M1s = []
            self.sigma_ebv1s = []
            self.sigma_Z2s = []
            self.sigma_age2s = []
            self.sigma_M2s = []
            self.sigma_ebv2s = []

            self.gridM1s = []
            self.gridM2s = []
            self.gridChisqs = []

            self.smallest_chi2s = []
            self.smallest_chi2_params = []

            self.newM1s = []
            self.newM2s = []
            self.newchi2s = []
            
            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1: 
                        ul_filters_this_row.append(valid_ind)

                gridChisq = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num))
                gridM1 = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num))
                gridM2 = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num))
                Wtot = 0
                smallest_chi2 = 1e14
                smallest_chi2_params = np.zeros(8)
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num):
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        age1 = self.age1grid[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        Z2 = self.Z2grid[i,j,k,l,m,n]
                                        age2 = self.age2grid[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        res = opt.minimize(self.chisqfunc2, x0, args=(Z1,age1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)
                                        chi2 = res.fun
                                        M1 = res.x[0]
                                        M2 = res.x[1]
                                        gridChisq[i,j,k,l,m,n] = chi2
                                        print("optimized chi2: ",chi2)
                                        gridM1[i,j,k,l,m,n] = M1
                                        gridM2[i,j,k,l,m,n] = M2
                                        print("optimized log(M1)/10: ",M1)
                                        print("optimized log(M2)/10: ",M2)
                                        print("\n")
                                        if chi2 < smallest_chi2:
                                            smallest_chi2 = chi2
                                            smallest_chi2_params[0] = Z1
                                            smallest_chi2_params[1] = age1
                                            smallest_chi2_params[2] = M1
                                            smallest_chi2_params[3] = ebv1
                                            smallest_chi2_params[4] = Z2
                                            smallest_chi2_params[5] = age2
                                            smallest_chi2_params[6] = M2
                                            smallest_chi2_params[7] = ebv2

                self.smallest_chi2s.append(0)
                self.smallest_chi2s[curr_row] = smallest_chi2
                print("Smallest chi2 for row {}: {}".format(self.rows[curr_row]+2,smallest_chi2))
                self.smallest_chi2_params.append(0)
                self.smallest_chi2_params[curr_row] = smallest_chi2_params
                print("Associated parameter values: Z1 {}, age1 {}, M1 {}, ebv1 {}, Z2 {}, age2 {}, M2 {}, ebv2 {}".format(smallest_chi2_params[0],smallest_chi2_params[1],smallest_chi2_params[2],smallest_chi2_params[3],smallest_chi2_params[4],smallest_chi2_params[5],smallest_chi2_params[6],smallest_chi2_params[7]))
                gridChisq -= smallest_chi2
                self.mean_Z1s.append(0)
                self.mean_age1s.append(0)
                self.mean_M1s.append(0)
                self.mean_ebv1s.append(0)
                self.mean_Z2s.append(0)
                self.mean_age2s.append(0)
                self.mean_M2s.append(0)
                self.mean_ebv2s.append(0)
                
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num): 
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        age1 = self.age1grid[i,j,k,l,m,n]
                                        M1 = gridM1[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        Z2 = self.Z2grid[i,j,k,l,m,n]
                                        age2 = self.age2grid[i,j,k,l,m,n]
                                        M2 = gridM2[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        chi2 = gridChisq[i,j,k,l,m,n]

                                        Wtot += exp(-chi2/2)
                                        self.mean_Z1s[curr_row] += exp(-chi2/2)*Z1
                                        self.mean_age1s[curr_row] += exp(-chi2/2)*age1
                                        self.mean_M1s[curr_row] += exp(-chi2/2)*M1
                                        self.mean_ebv1s[curr_row] += exp(-chi2/2)*ebv1
                                        self.mean_Z2s[curr_row] += exp(-chi2/2)*Z2
                                        self.mean_age2s[curr_row] += exp(-chi2/2)*age2
                                        self.mean_M2s[curr_row] += exp(-chi2/2)*M2
                                        self.mean_ebv2s[curr_row] += exp(-chi2/2)*ebv2
                                
                self.mean_Z1s[curr_row] /= Wtot
                self.mean_age1s[curr_row] /= Wtot
                self.mean_M1s[curr_row] /= Wtot
                self.mean_ebv1s[curr_row] /= Wtot
                self.mean_Z2s[curr_row] /= Wtot
                self.mean_age2s[curr_row] /= Wtot
                self.mean_M2s[curr_row] /= Wtot
                self.mean_ebv2s[curr_row] /= Wtot

                print("weighted mean Z1 ", self.mean_Z1s[curr_row])
                print("weighted mean age1 ", self.mean_age1s[curr_row])
                print("weighted mean M1 ", self.mean_M1s[curr_row])
                print("weighted mean ebv1 ", self.mean_ebv1s[curr_row])
                print("weighted mean Z2 ", self.mean_Z2s[curr_row])
                print("weighted mean age2 ", self.mean_age2s[curr_row])
                print("weighted mean M2 ", self.mean_M2s[curr_row])
                print("weighted mean ebv2 ", self.mean_ebv2s[curr_row])

                self.var_Z1s.append(0)
                self.var_age1s.append(0)
                self.var_M1s.append(0)
                self.var_ebv1s.append(0)
                self.var_Z2s.append(0)
                self.var_age2s.append(0)
                self.var_M2s.append(0)
                self.var_ebv2s.append(0)

                self.sigma_Z1s.append(0)
                self.sigma_age1s.append(0)
                self.sigma_M1s.append(0)
                self.sigma_ebv1s.append(0)
                self.sigma_Z2s.append(0)
                self.sigma_age2s.append(0)
                self.sigma_M2s.append(0)
                self.sigma_ebv2s.append(0)

                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num):
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        Z1 = self.Z1grid[i,j,k,l,m,n]
                                        age1 = self.age1grid[i,j,k,l,m,n]
                                        M1 = gridM1[i,j,k,l,m,n]
                                        ebv1 = self.ebv1grid[i,j,k,l,m,n]
                                        Z2 = self.Z2grid[i,j,k,l,m,n]
                                        age2 = self.age2grid[i,j,k,l,m,n]
                                        M2 = gridM2[i,j,k,l,m,n]
                                        ebv2 = self.ebv2grid[i,j,k,l,m,n]
                                        chi2 = gridChisq[i,j,k,l,m,n]

                                        self.var_Z1s[curr_row] += exp(-chi2/2)*(Z1-self.mean_Z1s[curr_row])*(Z1-self.mean_Z1s[curr_row])
                                        self.var_age1s[curr_row] += exp(-chi2/2)*(age1-self.mean_age1s[curr_row])*(age1-self.mean_age1s[curr_row])
                                        self.var_M1s[curr_row] += exp(-chi2/2)*(M1-self.mean_M1s[curr_row])*(M1-self.mean_M1s[curr_row])
                                        self.var_ebv1s[curr_row] += exp(-chi2/2)*(ebv1-self.mean_ebv1s[curr_row])*(ebv1-self.mean_ebv1s[curr_row])
                                        self.var_Z2s[curr_row] += exp(-chi2/2)*(Z2-self.mean_Z2s[curr_row])*(Z2-self.mean_Z2s[curr_row])
                                        self.var_age2s[curr_row] += exp(-chi2/2)*(age2-self.mean_age2s[curr_row])*(age2-self.mean_age2s[curr_row])
                                        self.var_M2s[curr_row] += exp(-chi2/2)*(M2-self.mean_M2s[curr_row])*(M2-self.mean_M2s[curr_row])
                                        self.var_ebv2s[curr_row] += exp(-chi2/2)*(ebv2-self.mean_ebv2s[curr_row])*(ebv2-self.mean_ebv2s[curr_row])
                                
                gridChisq += smallest_chi2
                self.gridM1s.append(gridM1.flatten())
                self.gridM2s.append(gridM2.flatten())
                self.gridChisqs.append(gridChisq.flatten())
                                
                self.var_Z1s[curr_row] /= Wtot
                self.var_age1s[curr_row] /= Wtot
                self.var_M1s[curr_row] /= Wtot
                self.var_ebv1s[curr_row] /= Wtot
                self.var_Z2s[curr_row] /= Wtot
                self.var_age2s[curr_row] /= Wtot
                self.var_M2s[curr_row] /= Wtot
                self.var_ebv2s[curr_row] /= Wtot

                self.sigma_Z1s[curr_row] = sqrt(self.var_Z1s[curr_row])
                self.sigma_age1s[curr_row] = sqrt(self.var_age1s[curr_row])
                self.sigma_M1s[curr_row] = sqrt(self.var_M1s[curr_row])
                self.sigma_ebv1s[curr_row] = sqrt(self.var_ebv1s[curr_row])
                self.sigma_Z2s[curr_row] = sqrt(self.var_Z2s[curr_row])
                self.sigma_age2s[curr_row] = sqrt(self.var_age2s[curr_row])
                self.sigma_M2s[curr_row] = sqrt(self.var_M2s[curr_row])
                self.sigma_ebv2s[curr_row] = sqrt(self.var_ebv2s[curr_row])

                print("weighted var Z1 ", self.var_Z1s[curr_row])
                print("sigma Z1 (sqrt weighted var Z1) ", self.sigma_Z1s[curr_row])
                print("weighted var age1 ", self.var_age1s[curr_row])
                print("sigma age1 (sqrt weighted var age1) ", self.sigma_age1s[curr_row])
                print("weighted var M1 ", self.var_M1s[curr_row])
                print("sigma M1 (sqrt weighted var M1) ", self.sigma_M1s[curr_row])
                print("weighted var ebv1 ", self.var_ebv1s[curr_row])
                print("sigma ebv1 (sqrt weighted var ebv1) ", self.sigma_ebv1s[curr_row])
                print("weighted var Z2 ", self.var_Z2s[curr_row])
                print("sigma Z2 (sqrt weighted var Z2) ", self.sigma_Z2s[curr_row])
                print("weighted var age2 ", self.var_age2s[curr_row])
                print("sigma age2 (sqrt weighted var age2) ", self.sigma_age2s[curr_row])
                print("weighted var M2 ", self.var_M2s[curr_row])
                print("sigma M2 (sqrt weighted var M2) ", self.sigma_M2s[curr_row])
                print("weighted var ebv2 ", self.var_ebv2s[curr_row])
                print("sigma ebv2 (sqrt weighted var ebv2) ", self.sigma_ebv2s[curr_row])

                x02 = np.array([self.mean_M1s[curr_row],self.mean_M2s[curr_row]])
                res2 = opt.minimize(self.minichisqfunc2_double, x02, args=(self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)

                newchi2 = res2.fun
                newM1 = res2.x[0]
                newM2 = res2.x[1]

                print("chi2 of fitted Ms to other mean parameters: ", newchi2)
                print("fitted M1 to other mean parameters: ", newM1)
                print("fitted M2 to other mean parameters: ", newM2)

                self.newchi2s.append(newchi2)
                self.newM1s.append(newM1)
                self.newM2s.append(newM2)

        elif self.triple_cluster == True:
            bnds = Bounds([self.Mbound1lo,self.Mbound2lo,self.Mbound3lo],[self.Mbound1hi,self.Mbound2hi,self.Mbound3hi])
            x0 = np.array([(self.Mbound1lo+self.Mbound1hi)/2,(self.Mbound2lo+self.Mbound2hi)/2,(self.Mbound3lo+self.Mbound3hi)/2])
            self.mean_Z1s = []
            self.mean_age1s = []
            self.mean_M1s = []
            self.mean_ebv1s = []
            self.mean_Z2s = []
            self.mean_age2s = []
            self.mean_M2s = []
            self.mean_ebv2s = []
            self.mean_Z3s = []
            self.mean_age3s = []
            self.mean_M3s = []
            
            self.var_Z1s = []
            self.var_age1s = []
            self.var_M1s = []
            self.var_ebv1s = []
            self.var_Z2s = []
            self.var_age2s = []
            self.var_M2s = []
            self.var_ebv2s = []
            self.var_Z3s = []
            self.var_age3s = []
            self.var_M3s = []

            self.sigma_Z1s = []
            self.sigma_age1s = []
            self.sigma_M1s = []
            self.sigma_ebv1s = []
            self.sigma_Z2s = []
            self.sigma_age2s = []
            self.sigma_M2s = []
            self.sigma_ebv2s = []
            self.sigma_Z3s = []
            self.sigma_age3s = []
            self.sigma_M3s = []

            self.gridM1s = []
            self.gridM2s = []
            self.gridM3s = []
            self.gridChisqs = []

            self.smallest_chi2s = []
            self.smallest_chi2_params = []

            self.newM1s = []
            self.newM2s = []
            self.newM3s = []
            self.newchi2s = []
            
            for curr_row in range(self.bandfluxes.shape[0]): 
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1: 
                        ul_filters_this_row.append(valid_ind)

                gridChisq = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num,self.Z3num,self.age3num))
                gridM1 = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num,self.Z3num,self.age3num))
                gridM2 = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num,self.Z3num,self.age3num))
                gridM3 = np.zeros((self.Z1num,self.age1num,self.ebv1num,self.Z2num,self.age2num,self.ebv2num,self.Z3num,self.age3num))
                Wtot = 0
                smallest_chi2 = 1e14
                smallest_chi2_params = np.zeros(11)
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num):
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        for o in range(self.Z3num):
                                            for p in range(self.age3num):
                                                Z1 = self.Z1grid[i,j,k,l,m,n,o,p]
                                                age1 = self.age1grid[i,j,k,l,m,n,o,p]
                                                ebv1 = self.ebv1grid[i,j,k,l,m,n,o,p]
                                                Z2 = self.Z2grid[i,j,k,l,m,n,o,p]
                                                age2 = self.age2grid[i,j,k,l,m,n,o,p]
                                                ebv2 = self.ebv2grid[i,j,k,l,m,n,o,p]
                                                Z3 = self.Z3grid[i,j,k,l,m,n,o,p]
                                                age3 = self.age3grid[i,j,k,l,m,n,o,p]
                                                res = opt.minimize(self.chisqfunc3, x0, args=(Z1,age1,ebv1,Z2,age2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)
                                                chi2 = res.fun
                                                M1 = res.x[0]
                                                M2 = res.x[1]
                                                M3 = res.x[2]
                                                gridChisq[i,j,k,l,m,n,o,p] = chi2
                                                print("optimized chi2: ",chi2)
                                                gridM1[i,j,k,l,m,n,o,p] = M1
                                                gridM2[i,j,k,l,m,n,o,p] = M2
                                                gridM2[i,j,k,l,m,n,o,p] = M3
                                                print("optimized log(M1)/10: ",M1)
                                                print("optimized log(M2)/10: ",M2)
                                                print("optimized log(M3)/10: ",M3)
                                                print("\n")
                                                if chi2 < smallest_chi2:
                                                    smallest_chi2 = chi2
                                                    smallest_chi2_params[0] = Z1
                                                    smallest_chi2_params[1] = age1
                                                    smallest_chi2_params[2] = M1
                                                    smallest_chi2_params[3] = ebv1
                                                    smallest_chi2_params[4] = Z2
                                                    smallest_chi2_params[5] = age2
                                                    smallest_chi2_params[6] = M2
                                                    smallest_chi2_params[7] = ebv2
                                                    smallest_chi2_params[8] = Z3
                                                    smallest_chi2_params[9] = age3
                                                    smallest_chi2_params[10] = M3

                self.smallest_chi2s.append(0)
                self.smallest_chi2s[curr_row] = smallest_chi2
                print("Smallest chi2 for row {}: {}".format(self.rows[curr_row]+2,smallest_chi2))
                self.smallest_chi2_params.append(0)
                self.smallest_chi2_params[curr_row] = smallest_chi2_params
                print("Associated parameter values: Z1 {}, age1 {}, M1 {}, ebv1 {}, Z2 {}, age2 {}, M2 {}, ebv2 {}, Z3 {}, age3 {}, M3 {}".format(smallest_chi2_params[0],smallest_chi2_params[1],smallest_chi2_params[2],smallest_chi2_params[3],smallest_chi2_params[4],smallest_chi2_params[5],smallest_chi2_params[6],smallest_chi2_params[7],smallest_chi2_params[8],smallest_chi2_params[9],smallest_chi2_params[10]))
                gridChisq -= smallest_chi2
                self.mean_Z1s.append(0)
                self.mean_age1s.append(0)
                self.mean_M1s.append(0)
                self.mean_ebv1s.append(0)
                self.mean_Z2s.append(0)
                self.mean_age2s.append(0)
                self.mean_M2s.append(0)
                self.mean_ebv2s.append(0)
                self.mean_Z3s.append(0)
                self.mean_age3s.append(0)
                self.mean_M3s.append(0)
                
                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num): 
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        for o in range(self.Z3num): 
                                            for p in range(self.age3num):
                                                Z1 = self.Z1grid[i,j,k,l,m,n,o,p]
                                                age1 = self.age1grid[i,j,k,l,m,n,o,p]
                                                M1 = gridM1[i,j,k,l,m,n,o,p]
                                                ebv1 = self.ebv1grid[i,j,k,l,m,n,o,p]
                                                Z2 = self.Z2grid[i,j,k,l,m,n,o,p]
                                                age2 = self.age2grid[i,j,k,l,m,n,o,p]
                                                M2 = gridM2[i,j,k,l,m,n,o,p]
                                                ebv2 = self.ebv2grid[i,j,k,l,m,n,o,p]
                                                Z3 = self.Z3grid[i,j,k,l,m,n,o,p]
                                                age3 = self.age3grid[i,j,k,l,m,n,o,p]
                                                M3 = gridM3[i,j,k,l,m,n,o,p]
                                                chi2 = gridChisq[i,j,k,l,m,n,o,p]

                                                Wtot += exp(-chi2/2)
                                                self.mean_Z1s[curr_row] += exp(-chi2/2)*Z1
                                                self.mean_age1s[curr_row] += exp(-chi2/2)*age1
                                                self.mean_M1s[curr_row] += exp(-chi2/2)*M1
                                                self.mean_ebv1s[curr_row] += exp(-chi2/2)*ebv1
                                                self.mean_Z2s[curr_row] += exp(-chi2/2)*Z2
                                                self.mean_age2s[curr_row] += exp(-chi2/2)*age2
                                                self.mean_M2s[curr_row] += exp(-chi2/2)*M2
                                                self.mean_ebv2s[curr_row] += exp(-chi2/2)*ebv2
                                                self.mean_Z3s[curr_row] += exp(-chi2/2)*Z3
                                                self.mean_age3s[curr_row] += exp(-chi2/2)*age3
                                                self.mean_M3s[curr_row] += exp(-chi2/2)*M3                                                
                                
                self.mean_Z1s[curr_row] /= Wtot
                self.mean_age1s[curr_row] /= Wtot
                self.mean_M1s[curr_row] /= Wtot
                self.mean_ebv1s[curr_row] /= Wtot
                self.mean_Z2s[curr_row] /= Wtot
                self.mean_age2s[curr_row] /= Wtot
                self.mean_M2s[curr_row] /= Wtot
                self.mean_ebv2s[curr_row] /= Wtot
                self.mean_Z3s[curr_row] /= Wtot
                self.mean_age3s[curr_row] /= Wtot
                self.mean_M3s[curr_row] /= Wtot                

                print("weighted mean Z1 ", self.mean_Z1s[curr_row])
                print("weighted mean age1 ", self.mean_age1s[curr_row])
                print("weighted mean M1 ", self.mean_M1s[curr_row])
                print("weighted mean ebv1 ", self.mean_ebv1s[curr_row])
                print("weighted mean Z2 ", self.mean_Z2s[curr_row])
                print("weighted mean age2 ", self.mean_age2s[curr_row])
                print("weighted mean M2 ", self.mean_M2s[curr_row])
                print("weighted mean ebv2 ", self.mean_ebv2s[curr_row])
                print("weighted mean Z3 ", self.mean_Z3s[curr_row])
                print("weighted mean age3 ", self.mean_age3s[curr_row])
                print("weighted mean M3 ", self.mean_M3s[curr_row])                

                self.var_Z1s.append(0)
                self.var_age1s.append(0)
                self.var_M1s.append(0)
                self.var_ebv1s.append(0)
                self.var_Z2s.append(0)
                self.var_age2s.append(0)
                self.var_M2s.append(0)
                self.var_ebv2s.append(0)
                self.var_Z3s.append(0)
                self.var_age3s.append(0)
                self.var_M3s.append(0)             

                self.sigma_Z1s.append(0)
                self.sigma_age1s.append(0)
                self.sigma_M1s.append(0)
                self.sigma_ebv1s.append(0)
                self.sigma_Z2s.append(0)
                self.sigma_age2s.append(0)
                self.sigma_M2s.append(0)
                self.sigma_ebv2s.append(0)
                self.sigma_Z3s.append(0)
                self.sigma_age3s.append(0)
                self.sigma_M3s.append(0)        

                for i in range(self.Z1num):
                    for j in range(self.age1num):
                        for k in range(self.ebv1num):
                            for l in range(self.Z2num):
                                for m in range(self.age2num):
                                    for n in range(self.ebv2num):
                                        for o in range(self.Z3num): 
                                            for p in range(self.age3num):
                                                Z1 = self.Z1grid[i,j,k,l,m,n,o,p]
                                                age1 = self.age1grid[i,j,k,l,m,n,o,p]
                                                M1 = gridM1[i,j,k,l,m,n,o,p]
                                                ebv1 = self.ebv1grid[i,j,k,l,m,n,o,p]
                                                Z2 = self.Z2grid[i,j,k,l,m,n,o,p]
                                                age2 = self.age2grid[i,j,k,l,m,n,o,p]
                                                M2 = gridM2[i,j,k,l,m,n,o,p]
                                                ebv2 = self.ebv2grid[i,j,k,l,m,n,o,p]
                                                Z3 = self.Z3grid[i,j,k,l,m,n,o,p]
                                                age3 = self.age3grid[i,j,k,l,m,n,o,p]
                                                M3 = gridM3[i,j,k,l,m,n,o,p]                                        
                                                chi2 = gridChisq[i,j,k,l,m,n,o,p]

                                                self.var_Z1s[curr_row] += exp(-chi2/2)*(Z1-self.mean_Z1s[curr_row])*(Z1-self.mean_Z1s[curr_row])
                                                self.var_age1s[curr_row] += exp(-chi2/2)*(age1-self.mean_age1s[curr_row])*(age1-self.mean_age1s[curr_row])
                                                self.var_M1s[curr_row] += exp(-chi2/2)*(M1-self.mean_M1s[curr_row])*(M1-self.mean_M1s[curr_row])
                                                self.var_ebv1s[curr_row] += exp(-chi2/2)*(ebv1-self.mean_ebv1s[curr_row])*(ebv1-self.mean_ebv1s[curr_row])
                                                self.var_Z2s[curr_row] += exp(-chi2/2)*(Z2-self.mean_Z2s[curr_row])*(Z2-self.mean_Z2s[curr_row])
                                                self.var_age2s[curr_row] += exp(-chi2/2)*(age2-self.mean_age2s[curr_row])*(age2-self.mean_age2s[curr_row])
                                                self.var_M2s[curr_row] += exp(-chi2/2)*(M2-self.mean_M2s[curr_row])*(M2-self.mean_M2s[curr_row])
                                                self.var_ebv2s[curr_row] += exp(-chi2/2)*(ebv2-self.mean_ebv2s[curr_row])*(ebv2-self.mean_ebv2s[curr_row])
                                                self.var_Z3s[curr_row] += exp(-chi2/2)*(Z3-self.mean_Z3s[curr_row])*(Z3-self.mean_Z3s[curr_row])
                                                self.var_age3s[curr_row] += exp(-chi2/2)*(age3-self.mean_age3s[curr_row])*(age3-self.mean_age3s[curr_row])
                                                self.var_M3s[curr_row] += exp(-chi2/2)*(M3-self.mean_M3s[curr_row])*(M3-self.mean_M3s[curr_row])                                        
                                
                gridChisq += smallest_chi2
                self.gridM1s.append(gridM1.flatten())
                self.gridM2s.append(gridM2.flatten())
                self.gridM3s.append(gridM3.flatten())
                self.gridChisqs.append(gridChisq.flatten())
                                
                self.var_Z1s[curr_row] /= Wtot
                self.var_age1s[curr_row] /= Wtot
                self.var_M1s[curr_row] /= Wtot
                self.var_ebv1s[curr_row] /= Wtot
                self.var_Z2s[curr_row] /= Wtot
                self.var_age2s[curr_row] /= Wtot
                self.var_M2s[curr_row] /= Wtot
                self.var_ebv2s[curr_row] /= Wtot
                self.var_Z3s[curr_row] /= Wtot
                self.var_age3s[curr_row] /= Wtot
                self.var_M3s[curr_row] /= Wtot      

                self.sigma_Z1s[curr_row] = sqrt(self.var_Z1s[curr_row])
                self.sigma_age1s[curr_row] = sqrt(self.var_age1s[curr_row])
                self.sigma_M1s[curr_row] = sqrt(self.var_M1s[curr_row])
                self.sigma_ebv1s[curr_row] = sqrt(self.var_ebv1s[curr_row])
                self.sigma_Z2s[curr_row] = sqrt(self.var_Z2s[curr_row])
                self.sigma_age2s[curr_row] = sqrt(self.var_age2s[curr_row])
                self.sigma_M2s[curr_row] = sqrt(self.var_M2s[curr_row])
                self.sigma_ebv2s[curr_row] = sqrt(self.var_ebv2s[curr_row])
                self.sigma_Z3s[curr_row] = sqrt(self.var_Z3s[curr_row])
                self.sigma_age3s[curr_row] = sqrt(self.var_age3s[curr_row])
                self.sigma_M3s[curr_row] = sqrt(self.var_M3s[curr_row])          

                print("weighted var Z1 ", self.var_Z1s[curr_row])
                print("sigma Z1 (sqrt weighted var Z1) ", self.sigma_Z1s[curr_row])
                print("weighted var age1 ", self.var_age1s[curr_row])
                print("sigma age1 (sqrt weighted var age1) ", self.sigma_age1s[curr_row])
                print("weighted var M1 ", self.var_M1s[curr_row])
                print("sigma M1 (sqrt weighted var M1) ", self.sigma_M1s[curr_row])
                print("weighted var ebv1 ", self.var_ebv1s[curr_row])
                print("sigma ebv1 (sqrt weighted var ebv1) ", self.sigma_ebv1s[curr_row])
                print("weighted var Z2 ", self.var_Z2s[curr_row])
                print("sigma Z2 (sqrt weighted var Z2) ", self.sigma_Z2s[curr_row])
                print("weighted var age2 ", self.var_age2s[curr_row])
                print("sigma age2 (sqrt weighted var age2) ", self.sigma_age2s[curr_row])
                print("weighted var M2 ", self.var_M2s[curr_row])
                print("sigma M2 (sqrt weighted var M2) ", self.sigma_M2s[curr_row])
                print("weighted var ebv2 ", self.var_ebv2s[curr_row])
                print("sigma ebv2 (sqrt weighted var ebv2) ", self.sigma_ebv2s[curr_row])
                print("weighted var Z3 ", self.var_Z3s[curr_row])
                print("sigma Z3 (sqrt weighted var Z3) ", self.sigma_Z3s[curr_row])
                print("weighted var age3 ", self.var_age3s[curr_row])
                print("sigma age3 (sqrt weighted var age3) ", self.sigma_age3s[curr_row])
                print("weighted var M3 ", self.var_M3s[curr_row])
                print("sigma M3 (sqrt weighted var M3) ", self.sigma_M3s[curr_row])

                x02 = np.array([self.mean_M1s[curr_row],self.mean_M2s[curr_row],self.mean_M3s[curr_row]])
                res2 = opt.minimize(self.minichisqfunc2_triple, x02, args=(self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],self.mean_Z3s[curr_row],self.mean_age3s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row,), bounds=bnds)

                newchi2 = res2.fun
                newM1 = res2.x[0]
                newM2 = res2.x[1]
                newM3 = res2.x[2]

                print("chi2 of fitted Ms to other mean parameters: ", newchi2)
                print("fitted M1 to other mean parameters: ", newM1)
                print("fitted M2 to other mean parameters: ", newM2)
                print("fitted M3 to other mean parameters: ", newM3)

                self.newchi2s.append(newchi2)
                self.newM1s.append(newM1)
                self.newM2s.append(newM2)
                self.newM3s.append(newM3)

    ##

    def find_param_errors(self):
        import numpy as np

        if self.single_cluster == True:

            self.errorsallrows = []
            self.errornotes = []
            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)
                errorsthisrow = []
                errornotesthisrow = []
                Z = self.mean_Z1s[curr_row]
                age = self.mean_age1s[curr_row]
                M = self.mean_M1s[curr_row]
                ebv = self.mean_ebv1s[curr_row]
                mean_models, mean_chi2 = self.minichisqfunc_single(M,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row)
                #
                try:
                    Mlowererror = M - opt.root_scalar(self.chisqfuncerror, args=(mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound1lo,M]).root
                    Mlowernotes = "\n"
                except:
                    Mlowererror = "N/A"
                    if self.chisqfuncerror(M,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfuncerror(self.Mbound1lo,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row):
                        Mlowernotes = "cannot go low enough to\nchange chi^2 by 4.28"
                    elif self.chisqfuncerror(M,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfuncerror(self.Mbound1lo,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row):
                        Mlowernotes = "sitting at lower bound\n"
                try:
                    Muppererror = opt.root_scalar(self.chisqfuncerror, args=(mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M,self.Mbound1hi]).root - M
                    Muppernotes = "\n"
                except:
                    Muppererror = "N/A"
                    if self.chisqfuncerror(M,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfuncerror(self.Mbound1hi,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row):
                        Muppernotes = "cannot go high enough to\nchange chi^2 by 4.28"
                    elif self.chisqfuncerror(M,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfuncerror(self.Mbound1hi,mean_chi2,Z,age,ebv,valid_filters_this_row,ul_filters_this_row,curr_row):
                        Muppernotes = "sitting at upper bound\n"
                errorsthisrow.append([Mlowererror,Muppererror])
                errornotesthisrow.append([Mlowernotes,Muppernotes])
                #
                self.errorsallrows.append(errorsthisrow)
                self.errornotes.append(errornotesthisrow)


        elif self.double_cluster == True:
            self.errornotes = []
            self.errorsallrows = []
            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)
                errorsthisrow = []
                errornotesthisrow = []
                M1 = self.mean_M1s[curr_row]
                M2 = self.mean_M2s[curr_row]
                Z1 = self.mean_Z1s[curr_row]
                age1 = self.mean_age1s[curr_row]
                ebv1 = self.mean_ebv1s[curr_row]
                Z2 = self.mean_Z2s[curr_row]
                age2 = self.mean_age2s[curr_row]
                ebv2 = self.mean_ebv2s[curr_row]
                hotmodels, coolmodels, mean_chi2 = self.minichisqfunc_double(M1,M2,Z1,age1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row)
                #
                try:
                    M1lowererror = M1 - opt.root_scalar(self.chisqfunc2error_1, args=(mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound1lo,M1]).root
                    M1lowernotes = "\n"
                except:
                    M1lowererror = "N/A"
                    if self.chisqfunc2error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc2error_1(self.Mbound1lo,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M1lowernotes = "cannot go low enough\nto change chi^2 by 9.32"
                    elif self.chisqfunc2error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc2error_1(self.Mbound1lo, mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M1lowernotes = "sitting at lower bound\n"
                try:
                    M1uppererror = opt.root_scalar(self.chisqfunc2error_1, args=(mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M1,self.Mbound1hi]).root - M1
                    M1uppernotes = "\n"
                except:
                    M1uppererror = "N/A"
                    if self.chisqfunc2error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc2error_1(self.Mbound1hi,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M1uppernotes = "cannot go high enough\nto change chi^2 by 9.32"
                    elif self.chisqfunc2error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc2error_1(self.Mbound1hi,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M1uppernotes = "sitting at upper bound\n"
                errorsthisrow.append([M1lowererror,M1uppererror])
                errornotesthisrow.append([M1lowernotes,M1uppernotes])
                #
                try:
                    M2lowererror = M2 - opt.root_scalar(self.chisqfunc2error_2, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound2lo,M2]).root
                    M2lowernotes = "\n"
                except:
                    M2lowererror = "N/A"
                    if self.chisqfunc2error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc2error_2(self.Mbound2lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M2lowernotes = "cannot go low enough to\nchange chi^2 by 9.32"
                    elif self.chisqfunc2error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc2error_2(self.Mbound2lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M2lowernotes = "sitting at lower bound\n"
                try:
                    M2uppererror = opt.root_scalar(self.chisqfunc2error, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M2,self.Mbound2hi]).root - M2
                    M2uppernotes = "\n"
                except:
                    M2uppererror = "N/A"
                    if self.chisqfunc2error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc2error_2(self.Mbound2hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M2uppernotes = "cannot go high enough to\nchange chi^2 by 9.32"
                    elif self.chisqfunc2error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc2error_2(self.Mbound2hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M2uppernotes = "sitting at upper bound\n"
                errorsthisrow.append([M2lowererror,M2uppererror])
                errornotesthisrow.append([M2lowernotes,M2uppernotes])
                #
                self.errorsallrows.append(errorsthisrow)
                self.errornotes.append(errornotesthisrow)
        
        elif self.triple_cluster == True:
            self.errornotes = []
            self.errorsallrows = []
            for curr_row in range(self.bandfluxes.shape[0]):  
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)
                errorsthisrow = []
                errornotesthisrow = []
                
                M1 = self.mean_M1s[curr_row]
                M2 = self.mean_M2s[curr_row]
                M3 = self.mean_M3s[curr_row]
                Z1 = self.mean_Z1s[curr_row]
                age1 = self.mean_age1s[curr_row]
                ebv1 = self.mean_ebv1s[curr_row]
                Z2 = self.mean_Z2s[curr_row]
                age2 = self.mean_age2s[curr_row]
                ebv2 = self.mean_ebv2s[curr_row]
                Z3 = self.mean_Z3s[curr_row]
                age3 = self.mean_age3s[curr_row]
                old1models, old2models, youngmodels, mean_chi2 = self.minichisqfunc_triple(M1,M2,M3,Z1,age1,ebv1,Z2,age2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row)
                #
                try:
                    M_old_1lowererror = M1 - opt.root_scalar(self.chisqfunc3error_1, args=(mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound1lo,M1]).root
                    M_old_1lowernotes = "\n"
                except:
                    M_old_1lowererror = "N/A"
                    if self.chisqfunc3error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_1(self.Mbound1lo,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_1lowernotes = "cannot go low enough\nto change chi^2 by 12.77"
                    elif self.chisqfunc3error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_1(self.Mbound1lo,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_1lowernotes = "sitting at lower bound\n"
                try:
                    M_old_1uppererror = opt.root_scalar(self.chisqfunc3error_1, args=(mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M1,self.Mbound1hi]).root - M1
                    M_old_1uppernotes = "\n"
                except:
                    M_old_1uppererror = "N/A"
                    if self.chisqfunc3error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_1(self.Mbound1hi,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_1uppernotes = "cannot go high enough\nto change chi^2 by 12.77"
                    elif self.chisqfunc3error_1(M1,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_1(self.Mbound1hi,mean_chi2,Z1,age1,ebv1,Z2,age2,M2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_1uppernotes = "sitting at upper bound\n"
                errorsthisrow.append([M_old_1lowererror,M_old_1uppererror])
                errornotesthisrow.append([M_old_1lowernotes,M_old_1uppernotes])
                #
                try:
                    M_old_2lowererror = M2 - opt.root_scalar(self.chisqfunc3error_2, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound2lo,M2]).root
                    M_old_2lowernotes = "\n"
                except:
                    M_old_2lowererror = "N/A"
                    if self.chisqfunc3error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_2(self.Mbound2lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_2lowernotes = "cannot go low enough to\nchange chi^2 by 12.77"
                    elif self.chisqfunc3error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_2(self.Mbound2lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_2lowernotes = "sitting at lower bound\n"
                try:
                    M_old_2uppererror = opt.root_scalar(self.chisqfunc3error_2, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M2,self.Mbound2hi]).root - M2
                    M_old_2uppernotes = "\n"
                except:
                    M_old_2uppererror = "N/A"
                    if self.chisqfunc3error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_2(self.Mbound2hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_2uppernotes = "cannot go high enough to\nchange chi^2 by 12.77"
                    elif self.chisqfunc3error_2(M2,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_2(self.Mbound2hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,ebv2,Z3,age3,M3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_old_2uppernotes = "sitting at upper bound\n"
                errorsthisrow.append([M_old_2lowererror,M_old_2uppererror])
                errornotesthisrow.append([M_old_2lowernotes,M_old_2uppernotes])
                #
                try:
                    M_newlowererror = M3 - opt.root_scalar(self.chisqfunc3error_3, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[self.Mbound3lo,M3]).root
                    M_newlowernotes = "\n"
                except:
                    M_newlowererror = "N/A"
                    if self.chisqfunc3error_3(M3,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_3(self.Mbound3lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_newlowernotes = "cannot go low enough to\nchange chi^2 by 12.77"
                    elif self.chisqfunc3error_3(M3,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_3(self.Mbound3lo,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_newlowernotes = "sitting at lower bound\n"
                try:
                    M_newuppererror = opt.root_scalar(self.chisqfunc3error_3, args=(mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row),method="brentq",bracket=[M3,self.Mbound3hi]).root - M3
                    M_newuppernotes = "\n"
                except:
                    M_newuppererror = "N/A"
                    if self.chisqfunc3error_3(M3,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row) != self.chisqfunc3error_3(self.Mbound3hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_newuppernotes = "cannot go high enough to\nchange chi^2 by 12.77"
                    elif self.chisqfunc3error_3(M3,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row) == self.chisqfunc3error_3(self.Mbound3hi,mean_chi2,Z1,age1,M1,ebv1,Z2,age2,M2,ebv2,Z3,age3,valid_filters_this_row,ul_filters_this_row,curr_row):
                        M_newuppernotes = "sitting at upper bound\n"
                errorsthisrow.append([M_newlowererror,M_newuppererror])
                errornotesthisrow.append([M_newlowernotes,M_newuppernotes])
                #
                self.errorsallrows.append(errorsthisrow)
                self.errornotes.append(errornotesthisrow)

    def display_all_results(self):
        if self.dispresults == 1:
            if self.single_cluster == True:
                self.mean_fluxes = []
                self.mean_chi2s = []
                for curr_row in range(self.bandfluxes.shape[0]):
                    self.display_results_single(curr_row)
            elif self.double_cluster == True:
                self.mean_hotfluxes = []
                self.mean_coolfluxes = []
                self.mean_chi2s = []
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_double(curr_row)
            elif self.triple_cluster == True:
                self.mean_old1fluxes = []
                self.mean_old2fluxes = []
                self.mean_youngfluxes = []
                self.mean_chi2s = []
                for curr_row in range(self.bandfluxes.shape[0]): 
                    self.display_results_triple(curr_row)

    def mysterious_function(self):

        import numpy as np
        import pandas as pd 

        if self.single_cluster == True:
            
            models = self.bandfluxes.copy(deep=True)
            self.truefluxerrors = self.bandfluxerrors.copy(deep=True)

            for curr_row in range(self.bandfluxes.shape[0]):
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)

                model,mean_chi2 = self.minichisqfunc_single(self.mean_M1s[curr_row],self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
                used = 0 
                for colno,col in enumerate(models.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        models.iat[curr_row,colno] = model[used]
                        used += 1
                
                for colno, arraytup in enumerate(zip(self.bandfluxerrors.loc[curr_row,:],self.ul_frame.loc[curr_row,:],self.bandfluxes.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        self.truefluxerrors.iat[curr_row,colno] = (arraytup[0])
                    if arraytup[1] == 1:
                        if self.ulmeth == "Limit":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[0]*-3)
                        elif self.ulmeth == "Standard":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[2]*-1/3)
        
        elif self.double_cluster == True:
            hotmodels = self.bandfluxes.copy(deep=True)
            coolmodels = self.bandfluxes.copy(deep=True)
            self.truefluxerrors = self.bandfluxerrors.copy(deep=True)

            for curr_row in range(self.bandfluxes.shape[0]):
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)
    
                hot,cool,mean_chi2 = self.minichisqfunc_double(self.mean_M1s[curr_row], self.mean_M2s[curr_row], self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
                usedhot = 0
                usedcool = 0
                for colno,col in enumerate(hotmodels.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        hotmodels.iat[curr_row,colno] = hot[usedhot]
                        usedhot += 1
                for colno,col in enumerate(coolmodels.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        coolmodels.iat[curr_row,colno] = cool[usedcool]
                        usedcool += 1

                for colno, arraytup in enumerate(zip(self.bandfluxerrors.loc[curr_row,:],self.ul_frame.loc[curr_row,:],self.bandfluxes.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        self.truefluxerrors.iat[curr_row,colno] = (arraytup[0])
                    if arraytup[1] == 1:
                        if self.ulmeth == "Limit":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[0]*-3)
                        elif self.ulmeth == "Standard":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[2]*-1/3)
        
        elif self.triple_cluster == True:
            old_1_models = self.bandfluxes.copy(deep=True)
            old_2_models = self.bandfluxes.copy(deep=True)
            new_models = self.bandfluxes.copy(deep=True)
            self.truefluxerrors = self.bandfluxerrors.copy(deep=True)

            for curr_row in range(self.bandfluxes.shape[0]):
                valid_filters_this_row = []
                ul_filters_this_row = []
                for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        valid_filters_this_row.append(valid_ind)
                    if arraytup[1] == 1:
                        ul_filters_this_row.append(valid_ind)
    
                old1,old2,new,mean_chi2 = self.minichisqfunc_triple(self.mean_M1s[curr_row], self.mean_M2s[curr_row], self.mean_M3s[curr_row], self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],self.mean_Z3s[curr_row],self.mean_age3s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
                usedold1 = 0
                usedold2 = 0
                usednew = 0
                for colno,col in enumerate(old_1_models.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        old_1_models.iat[curr_row,colno] = old1[usedold1]
                        usedold1 += 1
                for colno,col in enumerate(old_2_models.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        old_2_models.iat[curr_row,colno] = old2[usedold2]
                        usedold2 += 1
                for colno,col in enumerate(new_models.loc[curr_row,:]):
                    if np.isnan(col) == False:
                        new_models.iat[curr_row,colno] = new[usednew]
                        usednew += 1

                for colno, arraytup in enumerate(zip(self.bandfluxerrors.loc[curr_row,:],self.ul_frame.loc[curr_row,:],self.bandfluxes.loc[curr_row,:])):
                    if np.isnan(arraytup[0]) == False:
                        self.truefluxerrors.iat[curr_row,colno] = (arraytup[0])
                    if arraytup[1] == 1:
                        if self.ulmeth == "Limit":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[0]*-3)
                        elif self.ulmeth == "Standard":
                            self.truefluxerrors.iat[curr_row,colno] = (arraytup[2]*-1/3)

    ##purple
    def save_output(self):

        import numpy as np
        import pandas as pd
        
        if self.weightedmeanvarresults == 1:
            
            if self.single_cluster == True:

                df1 = pd.DataFrame({
                    'row' : [i+2 for i in self.rows],
                    'weighted_mean_Z1' : self.mean_Z1s,
                    'sigma_Z1' : self.sigma_Z1s,
                    'weighted_mean_age1' : self.mean_age1s,
                    'sigma_age1' : self.sigma_age1s,
                    'weighted_mean_M1s' : self.mean_M1s,
                    'sigma_M1' : self.sigma_M1s,
                    'weighted_mean_ebv1' : self.mean_ebv1s,
                    'sigma_ebv1' : self.sigma_ebv1s,
                    'chi2_using_mean_parameters' : self.mean_chi2s,
                    'fitted_M1_to_mean_parameters' : self.newM1s,
                    'chi2_of_fitted_M1' : self.newchi2s})

                try:
                    df1.to_csv("{}".format(self.weightedmeanvarname),index=False)
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')  

        
            elif self.double_cluster == True:

                df1 = pd.DataFrame({
                    'row' : [i+2 for i in self.rows],
                    'weighted_mean_Z1' : self.mean_Z1s,
                    'sigma_Z1' : self.sigma_Z1s,
                    'weighted_mean_age1' : self.mean_age1s,
                    'sigma_age1' : self.sigma_age1s,
                    'weighted_mean_M1' : self.mean_M1s,
                    'sigma_M1' : self.sigma_M1s,
                    'weighted_mean_ebv1' : self.mean_ebv1s,
                    'sigma_ebv1' : self.sigma_ebv1s,
                    'weighted_mean_Z2' : self.mean_Z2s,
                    'sigma_Z2' : self.sigma_Z2s,
                    'weighted_mean_age2' : self.mean_age2s,
                    'sigma_age2' : self.sigma_age2s,
                    'weighted_mean_M2' : self.mean_M2s,
                    'sigma_M2' : self.sigma_M2s,
                    'weighted_mean_ebv2' : self.mean_ebv2s,
                    'sigma_ebv2' : self.sigma_ebv2s,
                    'chi2_using_mean_parameters' : self.mean_chi2s,
                    'fitted_M1_to_mean_parameters' : self.newM1s,
                    'fitted_M2_to_mean_parameters' : self.newM2s,
                    'chi2_of_fitted_Ms' : self.newchi2s})

                try:
                    df1.to_csv("{}".format(self.weightedmeanvarname),index=False)
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')  
                

            elif self.triple_cluster == True:

                df1 = pd.DataFrame({
                    'row' : [i+2 for i in self.rows],
                    'weighted_mean_Z1' : self.mean_Z1s,
                    'sigma_Z1' : self.sigma_Z1s,
                    'weighted_mean_age1' : self.mean_age1s,
                    'sigma_age1' : self.sigma_age1s,
                    'weighted_mean_M1' : self.mean_M1s,
                    'sigma_M1' : self.sigma_M1s,
                    'weighted_mean_ebv1' : self.mean_ebv1s,
                    'sigma_ebv1' : self.sigma_ebv1s,
                    'weighted_mean_Z2' : self.mean_Z2s,
                    'sigma_Z2' : self.sigma_Z2s,
                    'weighted_mean_age2' : self.mean_age2s,
                    'sigma_age2' : self.sigma_age2s,
                    'weighted_mean_M2' : self.mean_M2s,
                    'sigma_M2' : self.sigma_M2s,
                    'weighted_mean_ebv2' : self.mean_ebv2s,
                    'sigma_ebv2' : self.sigma_ebv2s,
                    'weighted_mean_Z3' : self.mean_Z3s,
                    'sigma_Z3' : self.sigma_Z3s,
                    'weighted_mean_age3' : self.mean_age3s,
                    'sigma_age3' : self.sigma_age3s,
                    'weighted_mean_M3' : self.mean_M3s,
                    'sigma_M3' : self.sigma_M3s,
                    'chi2_using_mean_parameters' : self.mean_chi2s,
                    'fitted_M1_to_mean_parameters' : self.newM1s,
                    'fitted_M2_to_mean_parameters' : self.newM2s,
                    'fitted_M3_to_mean_parameters' : self.newM3s,
                    'chi2_of_fitted_Ms' : self.newchi2s})

                try:
                    df1.to_csv("{}".format(self.weightedmeanvarname),index=False)
                except:
                    import tkinter as tk
                    from tkinter import messagebox
                    tk.messagebox.showerror('Error','An error occurred. This can happen if a file is open while trying to overwrite it. Please close any relevant files and try again.')  


        if self.gridresults == 1:

            if self.single_cluster == True:

                for curr_row in range(self.bandfluxes.shape[0]):

                    a = pd.DataFrame({
                        'log(Z)' : self.Z1grid.flatten(),
                        'log(age)/10' : self.age1grid.flatten(),
                        'log(M)/10' : self.gridM1s[curr_row],
                        'E(B-V)' : self.ebv1grid.flatten(),
                        'Chi_squared' : self.gridChisqs[curr_row]})
                    
                    parts = self.gridname.split(".")
                    numbered_gridname = parts[0] + str(self.rows[curr_row]+2) + "." + parts[1]

                    a.to_csv("{}".format(numbered_gridname),index=False)
            
            elif self.double_cluster == True:

                for curr_row in range(self.bandfluxes.shape[0]):

                    a = pd.DataFrame({
                        'log(Z_hot)' : self.Z1grid.flatten(),
                        'log(age_hot)/10' : self.age1grid.flatten(),
                        'log(M_hot)/10' : self.gridM1s[curr_row],
                        'E(B-V)_hot' : self.ebv1grid.flatten(),
                        'log(Z_cool)' : self.Z2grid.flatten(),
                        'log(age_cool)/10' : self.age2grid.flatten(),
                        'log(M_cool)/10' : self.gridM2s[curr_row],
                        'E(B-V)_cool' : self.ebv2grid.flatten(),
                        'Chi_squared' : self.gridChisqs[curr_row]})
                    
                    parts = self.gridname.split(".")
                    numbered_gridname = parts[0] + str(self.rows[curr_row]+2) + "." + parts[1]

                    a.to_csv("{}".format(numbered_gridname),index=False)

            elif self.triple_cluster == True:

                for curr_row in range(self.bandfluxes.shape[0]):

                    a = pd.DataFrame({
                        'log(Z_old1)' : self.Z1grid.flatten(),
                        'log(age_old2)/10' : self.age1grid.flatten(),
                        'log(M_old1)/10' : self.gridM1s[curr_row],
                        'E(B-V)_old1' : self.ebv1grid.flatten(),
                        'log(Z_old2)' : self.Z2grid.flatten(),
                        'log(age_old2)/10' : self.age2grid.flatten(),
                        'log(M_old2)/10' : self.gridM2s[curr_row],
                        'E(B-V)_young' : self.ebv2grid.flatten(),
                        'log(Z_old3)' : self.Z3grid.flatten(),
                        'log(age_old3)/10' : self.age3grid.flatten(),
                        'log(M_old3)/10' : self.gridM3s[curr_row],
                        'Chi_squared' : self.gridChisqs[curr_row]})
                    
                    parts = self.gridname.split(".")
                    numbered_gridname = parts[0] + str(self.rows[curr_row]+2) + "." + parts[1]

                    a.to_csv("{}".format(numbered_gridname),index=False)
    ##

    ##red

    def display_results_single(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Tk()
        topw.geometry("1460x900+250+20")
        topw.title("Optimization results")
        topw.resizable(0,0)
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        import numpy as np

        valid_filters_this_row = []
        ul_filters_this_row = []
        for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
            if np.isnan(arraytup[0]) == False:
                valid_filters_this_row.append(valid_ind)
            if arraytup[1] == 1:
                ul_filters_this_row.append(valid_ind)
        valid_notul_filters_this_row = [i for i in valid_filters_this_row if i not in ul_filters_this_row]

        valid_fluxes_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_notul_fluxes_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])
    
        valid_ul_fluxes_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_errors_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_notul_errors_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_ul_errors_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind]*-1)  

        valid_avgwv_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_notul_avgwv_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_ul_avgwv_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_actualfilters_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_actualfilters_this_row.append(self.filternames[valid_ind])

        fig = Figure(figsize=(8.4,4.8))
        abc = fig.add_subplot(111)
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        abc.errorbar(valid_notul_avgwv_this_row,valid_notul_fluxes_this_row,yerr=valid_notul_errors_this_row,fmt="o",color="orange")
        if self.model_chosen == "UVIT_HST":
            abc.errorbar(valid_ul_avgwv_this_row,valid_ul_fluxes_this_row,yerr=valid_ul_errors_this_row,uplims=True,fmt="o",color="green")
        mean_models, mean_chi2 = self.minichisqfunc_single(self.mean_M1s[curr_row],self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
        print("\nchi2 of mean parameters: ", mean_chi2,"\n")
        abc.plot(valid_avgwv_this_row,mean_models,color="blue")

        if self.plotscale == 1:
            pass

        if self.plotscale == 0:
            abc.set_xscale('log')
            abc.set_yscale('log')
            abc.set_xticks([140,200,500,1000,1500])
            abc.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(valid_actualfilters_this_row,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=220)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(valid_actualfilters_this_row,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=250)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=420)
        textbox3 = tk.Text(topw,height=5,width=30)
        for filtername,bfe in zip(valid_actualfilters_this_row,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=450)
        label4 = tk.Label(topw,text="Model fluxes (y, blue):")
        label4.place(x=50,y=620)
        textbox4 = tk.Text(topw,height=6,width=30)
        self.mean_fluxes.append(0)
        for filtername,mod in zip(valid_actualfilters_this_row,mean_models):
            self.mean_fluxes[curr_row] += mod
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(mod,'.8e')))
        print("total model flux using weighted mean parameters: {}".format(self.mean_fluxes[curr_row]))
        textbox4.place(x=50,y=650)
        groove = tk.Canvas(topw,width=215,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=405,y=655)
        label5 = tk.Label(topw,text="chi^2 value using \nweighted mean parameters")
        label5.place(x=425,y=665)
        label5a = tk.Label(topw,text="{}".format(format(mean_chi2,'.6e')),font=("Arial",12))
        label5a.place(x=445,y=725)
        self.mean_chi2s.append(0)
        self.mean_chi2s[curr_row] = mean_chi2

        import math
        Z_sticker1 = format(self.mean_Z1s[curr_row],'.6e')

        age_sticker1 = format(self.mean_age1s[curr_row],'.6e')

        M_sticker1 = format(self.mean_M1s[curr_row],'.6e')
        try:
            M_sticker2 = format(self.errorsallrows[curr_row][0][0],'.6')
        except:
            M_sticker2 = "       N/A       "
        try:
            M_sticker3 = format(self.errorsallrows[curr_row][0][1],'.6e')
        except:
            M_sticker3 = "       N/A       "
        M_sticker4 = self.errornotes[curr_row][0][0]
        M_sticker5 = self.errornotes[curr_row][0][1]

        ebv_sticker1 = format(self.mean_ebv1s[curr_row],'.6e')

        colpack1 = tk.Frame(topw)
        colpack1.place(x=650,y=600)
        colpack2 = tk.Frame(topw)
        colpack2.place(x=765,y=600)
        colpack3 = tk.Frame(topw)
        colpack3.place(x=900,y=600)
        colpack4 = tk.Frame(topw)
        colpack4.place(x=1020,y=600)
        colpack5 = tk.Frame(topw)
        colpack5.place(x=1180,y=600)
        colpack6 = tk.Frame(topw)
        colpack6.place(x=1290,y=600)
        parameterhead = tk.Label(colpack1,text="Parameter",bg="azure").pack(pady=10)
        parameter1 = tk.Label(colpack1,text="log(Z)").pack(pady=10)
        parameter2 = tk.Label(colpack1,text="log(age)/10").pack(pady=10)
        parameter3 = tk.Label(colpack1,text="log(M)/10").pack(pady=10)
        parameter4 = tk.Label(colpack1,text="E(B-V)").pack(pady=10)
        meanhead = tk.Label(colpack2,text="Weighted mean",bg="azure").pack(pady=10)
        mean1 = tk.Label(colpack2,text="{}".format(Z_sticker1)).pack(pady=10)
        mean2 = tk.Label(colpack2,text="{}".format(age_sticker1)).pack(pady=10)
        mean3 = tk.Label(colpack2,text="{}".format(M_sticker1)).pack(pady=10)
        mean4 = tk.Label(colpack2,text="{}".format(ebv_sticker1)).pack(pady=10)
        errlohead = tk.Label(colpack3,text="Lower error",bg="azure").pack(pady=10)
        errlo3 = tk.Label(colpack3,text="{}".format(M_sticker2)).pack(pady=10)
        noteslohead = tk.Label(colpack4,text="Lower error notes",bg="azure").pack(pady=10)
        noteslo3 = tk.Label(colpack4,text="{}".format(M_sticker4),font="Arial, 7").pack(pady=5)
        errhihead = tk.Label(colpack5,text="Upper error",bg="azure").pack(pady=10)
        errhi3 = tk.Label(colpack5,text="{}".format(M_sticker3)).pack(pady=10)
        noteshihead = tk.Label(colpack6,text="Upper error notes",bg="azure").pack(pady=10)
        noteshi3 = tk.Label(colpack6,text="{}".format(M_sticker5),font="Arial, 7").pack(pady=5)

        def closethesource():
            topw.destroy()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=423,y=830)
        topw.mainloop()

    
    def display_results_double(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Tk()
        topw.geometry("1460x900+250+20")
        topw.title("Optimization results")
        topw.resizable(0,0)
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        import numpy as np

        valid_filters_this_row = []
        ul_filters_this_row = []
        for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
            if np.isnan(arraytup[0]) == False:
                valid_filters_this_row.append(valid_ind)
            if arraytup[1] == 1:
                ul_filters_this_row.append(valid_ind)
        valid_notul_filters_this_row = [i for i in valid_filters_this_row if i not in ul_filters_this_row]

        valid_fluxes_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_notul_fluxes_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])
    
        valid_ul_fluxes_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_errors_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_notul_errors_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_ul_errors_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind]*-1)  

        valid_avgwv_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_notul_avgwv_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_ul_avgwv_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_actualfilters_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_actualfilters_this_row.append(self.filternames[valid_ind])
    
        fig = Figure(figsize=(8.4,4.8))
        abc = fig.add_subplot(111)
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        abc.errorbar(valid_notul_avgwv_this_row,valid_notul_fluxes_this_row,yerr=valid_notul_errors_this_row,fmt="o",color="orange")
        if self.model_chosen == "UVIT_HST":
            abc.errorbar(valid_ul_avgwv_this_row,valid_ul_fluxes_this_row,yerr=valid_ul_errors_this_row,uplims=True,fmt="o",color="green")
        hotmodels, coolmodels, mean_chi2 = self.minichisqfunc_double(self.mean_M1s[curr_row], self.mean_M2s[curr_row], self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
        print("\nchi2 of mean parameters: ", mean_chi2,"\n")
        abc.plot(valid_avgwv_this_row,hotmodels,color="red")
        abc.plot(valid_avgwv_this_row,coolmodels,color="blue")
        sumofmodels = [hotmodels[i] + coolmodels[i] for i in range(len(hotmodels))]
        abc.plot(valid_avgwv_this_row,sumofmodels,color="limegreen")

        if self.plotscale == 1:
            pass

        if self.plotscale == 0:
            abc.set_xscale('log')
            abc.set_yscale('log')
            abc.set_xticks([140,200,500,1000,1500])
            abc.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=6,width=30)
        for filtername,avgwv in zip(valid_actualfilters_this_row,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=195)
        textbox2 = tk.Text(topw,height=6,width=30)
        for filtername,bf in zip(valid_actualfilters_this_row,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=225)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=370)
        textbox3 = tk.Text(topw,height=5,width=30)
        for filtername,bfe in zip(valid_actualfilters_this_row,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=400)
        label4 = tk.Label(topw,text="Hot cluster model fluxes (y, red):")
        label4.place(x=50,y=545)
        textbox4 = tk.Text(topw,height=6,width=30)
        self.mean_hotfluxes.append(0)
        for filtername,hotmod in zip(valid_actualfilters_this_row,hotmodels):
            self.mean_hotfluxes[curr_row] += hotmod
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(hotmod,'.8e')))
        print("total hot model flux using weighted mean parameters: {}".format(self.mean_hotfluxes[curr_row]))
        textbox4.place(x=50,y=575)
        label5 = tk.Label(topw,text="Cool cluster model fluxes (y, blue):")
        label5.place(x=50,y=720)
        textbox5 = tk.Text(topw,height=6,width=30)
        self.mean_coolfluxes.append(0)
        for filtername,coolmod in zip(valid_actualfilters_this_row,coolmodels):
            self.mean_coolfluxes[curr_row] += coolmod
            textbox5.insert(tk.END,"{}      {}\n".format(filtername,format(coolmod,'.8e')))
        print("total cool model flux using weighted mean parameters: {}".format(self.mean_coolfluxes[curr_row]))
        textbox5.place(x=50,y=750)
        groove = tk.Canvas(topw,width=215,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=405,y=655)
        label5 = tk.Label(topw,text="chi^2 value using\n weighted mean parameters")
        label5.place(x=425,y=665)
        label5a = tk.Label(topw,text="{}".format(format(mean_chi2,'.6e')),font=("Arial",12))
        label5a.place(x=445,y=725)        
        self.mean_chi2s.append(0)
        self.mean_chi2s[curr_row] = mean_chi2

        import math
        Z_hot_sticker1 = format(self.mean_Z1s[curr_row],'.6e')

        age_hot_sticker1 = format(self.mean_age1s[curr_row],'.6e')

        M_hot_sticker1 = format(self.mean_M1s[curr_row],'.6e')
        try:
            M_hot_sticker2 = format(self.errorsallrows[curr_row][0][0],'.6')
        except:
            M_hot_sticker2 = "       N/A       "
        try:
            M_hot_sticker3 = format(self.errorsallrows[curr_row][0][1],'.6e')
        except:
            M_hot_sticker3 = "       N/A       "
        M_hot_sticker4 = self.errornotes[curr_row][0][0]
        M_hot_sticker5 = self.errornotes[curr_row][0][1]

        ebv_hot_sticker1 = format(self.mean_ebv1s[curr_row],'.6e')

        Z_cool_sticker1 = format(self.mean_Z2s[curr_row],'.6e')

        age_cool_sticker1 = format(self.mean_age2s[curr_row],'.6e')

        M_cool_sticker1 = format(self.mean_M2s[curr_row],'.6e')
        try:
            M_cool_sticker2 = format(self.errorsallrows[curr_row][1][0],'.6e')
        except:
            M_cool_sticker2 = "       N/A       "
        try:
            M_cool_sticker3 = format(self.errorsallrows[curr_row][1][1],'.6e')
        except:
            M_cool_sticker3 = "       N/A       "
        M_cool_sticker4 = self.errornotes[curr_row][1][0]
        M_cool_sticker5 = self.errornotes[curr_row][1][1]

        ebv_cool_sticker1 = format(self.mean_ebv2s[curr_row],'.6e')

        colpack1 = tk.Frame(topw)
        colpack1.place(x=650,y=600)
        colpack2 = tk.Frame(topw)
        colpack2.place(x=790,y=600)
        colpack3 = tk.Frame(topw)
        colpack3.place(x=910,y=600)
        colpack4 = tk.Frame(topw)
        colpack4.place(x=1020,y=600)
        colpack5 = tk.Frame(topw)
        colpack5.place(x=1180,y=600)
        colpack6 = tk.Frame(topw)
        colpack6.place(x=1290,y=600)
        parameterhead = tk.Label(colpack1,text="Parameter",bg="azure").pack(pady=3)
        parameter1 = tk.Label(colpack1,text="log(Z_hot)").pack(pady=3)
        parameter2 = tk.Label(colpack1,text="log(age_hot)/10").pack(pady=3)
        parameter3 = tk.Label(colpack1,text="log(M_hot)/10").pack(pady=3)
        parameter4 = tk.Label(colpack1,text="E(B-V)_hot").pack(pady=3)
        parameter5 = tk.Label(colpack1,text="log(Z_cool)").pack(pady=3)
        parameter6 = tk.Label(colpack1,text="log(age_cool)/10").pack(pady=3)
        parameter7 = tk.Label(colpack1,text="log(M_cool)/10").pack(pady=3)
        parameter8 = tk.Label(colpack1,text="E(B-V)_cool").pack(pady=3)
        meanhead = tk.Label(colpack2,text="Weighted mean",bg="azure").pack(pady=3)
        mean1 = tk.Label(colpack2,text="{}".format(Z_hot_sticker1)).pack(pady=3)
        mean2 = tk.Label(colpack2,text="{}".format(age_hot_sticker1)).pack(pady=3)
        mean3 = tk.Label(colpack2,text="{}".format(M_hot_sticker1)).pack(pady=3)
        mean4 = tk.Label(colpack2,text="{}".format(ebv_hot_sticker1)).pack(pady=3)
        mean5 = tk.Label(colpack2,text="{}".format(Z_cool_sticker1)).pack(pady=3)
        mean6 = tk.Label(colpack2,text="{}".format(age_cool_sticker1)).pack(pady=3)
        mean7 = tk.Label(colpack2,text="{}".format(M_cool_sticker1)).pack(pady=3)
        mean8 = tk.Label(colpack2,text="{}".format(ebv_cool_sticker1)).pack(pady=3)
        errlohead = tk.Label(colpack3,text="Lower error",bg="azure").pack(pady=3)
        errlo3 = tk.Label(colpack3,text="{}".format(M_hot_sticker2)).pack(pady=3)
        errlo7 = tk.Label(colpack3,text="{}".format(M_cool_sticker2)).pack(pady=3)
        noteslohead = tk.Label(colpack4,text="Lower error notes",bg="azure").pack(pady=3)
        noteslo3 = tk.Label(colpack4,text="{}".format(M_hot_sticker4),font="Arial, 6").pack()
        noteslo7 = tk.Label(colpack4,text="{}".format(M_cool_sticker4),font="Arial, 6").pack()
        errhihead = tk.Label(colpack5,text="Upper error",bg="azure").pack(pady=3)
        errhi3 = tk.Label(colpack5,text="{}".format(M_hot_sticker3)).pack(pady=3)
        errhi7 = tk.Label(colpack5,text="{}".format(M_cool_sticker3)).pack(pady=3)
        noteshihead = tk.Label(colpack6,text="Upper error notes",bg="azure").pack(pady=3)
        noteshi3 = tk.Label(colpack6,text="{}".format(M_hot_sticker5),font="Arial, 6").pack()
        noteshi7 = tk.Label(colpack6,text="{}".format(M_cool_sticker5),font="Arial, 6").pack()


        def closethesource():
            topw.destroy()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=423,y=830)
        topw.mainloop()

    def display_results_triple(self,curr_row):
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
        import tkinter as tk
        topw = tk.Tk()
        topw.geometry("1460x1000+250+0")
        topw.title("Optimization results")
        topw.resizable(0,0)
        
        import matplotlib
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        matplotlib.use('TkAgg')
        import numpy as np

        valid_filters_this_row = []
        ul_filters_this_row = []
        for valid_ind,arraytup in enumerate(zip(self.bandfluxes.loc[curr_row,:],self.ul_frame.loc[curr_row,:])):
            if np.isnan(arraytup[0]) == False:
                valid_filters_this_row.append(valid_ind)
            if arraytup[1] == 1:
                ul_filters_this_row.append(valid_ind)
        valid_notul_filters_this_row = [i for i in valid_filters_this_row if i not in ul_filters_this_row]

        valid_fluxes_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_notul_fluxes_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])
    
        valid_ul_fluxes_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_fluxes_this_row.append(self.bandfluxes.iat[curr_row,valid_ind])

        valid_errors_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_notul_errors_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind])

        valid_ul_errors_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_errors_this_row.append(self.truefluxerrors.iat[curr_row,valid_ind]*-1)  

        valid_avgwv_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_notul_avgwv_this_row = []
        for valid_ind in valid_notul_filters_this_row:
            valid_notul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_ul_avgwv_this_row = []
        for valid_ind in ul_filters_this_row:
            valid_ul_avgwv_this_row.append(self.avgwvlist[valid_ind])

        valid_actualfilters_this_row = []
        for valid_ind in valid_filters_this_row:
            valid_actualfilters_this_row.append(self.filternames[valid_ind])
    
        fig = Figure(figsize=(8.4,4.8))
        abc = fig.add_subplot(111)
        abc.scatter(valid_avgwv_this_row,valid_fluxes_this_row,color="orange")
        abc.set_xlabel("Wavelength [nm]")
        abc.set_ylabel("Flux [mJy]")
        abc.set_title("Source at row {}".format(self.rows[curr_row]+2))
        abc.errorbar(valid_notul_avgwv_this_row,valid_notul_fluxes_this_row,yerr=valid_notul_errors_this_row,fmt="o",color="orange")
        if self.model_chosen == "UVIT_HST":
            abc.errorbar(valid_ul_avgwv_this_row,valid_ul_fluxes_this_row,yerr=valid_ul_errors_this_row,uplims=True,fmt="o",color="green")
        old1models, old2models, youngmodels, mean_chi2 = self.minichisqfunc_triple(self.mean_M1s[curr_row], self.mean_M2s[curr_row], self.mean_M3s[curr_row], self.mean_Z1s[curr_row],self.mean_age1s[curr_row],self.mean_ebv1s[curr_row],self.mean_Z2s[curr_row],self.mean_age2s[curr_row],self.mean_ebv2s[curr_row],self.mean_Z3s[curr_row],self.mean_age3s[curr_row],valid_filters_this_row,ul_filters_this_row,curr_row)
        print("\nchi2 of mean parameters: ", mean_chi2,"\n")
        abc.plot(valid_avgwv_this_row,old1models,color="red")
        abc.plot(valid_avgwv_this_row,old2models,color="blue")
        abc.plot(valid_avgwv_this_row,youngmodels,color="m")
        sumofmodels = [old1models[i] + old2models[i] + youngmodels[i] for i in range(len(old1models))]
        abc.plot(valid_avgwv_this_row,sumofmodels,color="limegreen")

        if self.plotscale == 1:
            pass

        if self.plotscale == 0:
            abc.set_xscale('log')
            abc.set_yscale('log')
            abc.set_xticks([140,200,500,1000,1500])
            abc.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

        if self.saveplots == 1:
            saveimgname = self.imgfilename.replace("X","{}".format(self.rows[curr_row]+2))
            fig.savefig('{}'.format(saveimgname), bbox_inches='tight', dpi=150)

        canvas = FigureCanvasTkAgg(fig, master=topw)
        canvas.get_tk_widget().pack(anchor=tk.E)
        canvas.draw()

        label1 = tk.Label(topw,text="Average wavelength of each filter (x):")
        label1.place(x=50,y=20)
        textbox1 = tk.Text(topw,height=5,width=30)
        for filtername,avgwv in zip(valid_actualfilters_this_row,valid_avgwv_this_row):
            textbox1.insert(tk.END,"{}      {}\n".format(filtername,avgwv))
        textbox1.place(x=50,y=50)
        label2 = tk.Label(topw,text="Bandfluxes (y, orange):")
        label2.place(x=50,y=165)
        textbox2 = tk.Text(topw,height=5,width=30)
        for filtername,bf in zip(valid_actualfilters_this_row,valid_fluxes_this_row):
            textbox2.insert(tk.END,"{}      {}\n".format(filtername,format(bf,'.8e')))
        textbox2.place(x=50,y=195)
        label3 = tk.Label(topw,text="Bandflux errors:")
        label3.place(x=50,y=310)
        textbox3 = tk.Text(topw,height=5,width=30)
        for filtername,bfe in zip(valid_actualfilters_this_row,valid_errors_this_row):
            textbox3.insert(tk.END,"{}      {}\n".format(filtername,format(bfe,'.8e')))
        textbox3.place(x=50,y=340)
        label4 = tk.Label(topw,text="Old_1 cluster model fluxes (y, red):")
        label4.place(x=50,y=455)
        textbox4 = tk.Text(topw,height=5,width=30)
        self.mean_old1fluxes.append(0)
        for filtername,old1mod in zip(valid_actualfilters_this_row,old1models):
            self.mean_old1fluxes[curr_row] += old1mod
            textbox4.insert(tk.END,"{}      {}\n".format(filtername,format(old1mod,'.8e')))
        print("total old1 model flux using weighted mean parameters: {}".format(self.mean_old1fluxes[curr_row]))
        textbox4.place(x=50,y=485)
        label5 = tk.Label(topw,text="Old_2 cluster model fluxes (y, blue):")
        label5.place(x=50,y=600)
        textbox5 = tk.Text(topw,height=5,width=30)
        self.mean_old2fluxes.append(0)
        for filtername,old2mod in zip(valid_actualfilters_this_row,old2models):
            self.mean_old2fluxes[curr_row] += old2mod
            textbox5.insert(tk.END,"{}      {}\n".format(filtername,format(old2mod,'.8e')))
        print("total old2 model flux using weighted mean parameters: {}".format(self.mean_old2fluxes[curr_row]))
        textbox5.place(x=50,y=630)
        label6 = tk.Label(topw,text="Young cluster model fluxes (y, majenta):")
        label6.place(x=50,y=745)
        textbox6 = tk.Text(topw,height=5,width=30)
        self.mean_youngfluxes.append(0)
        for filtername,youngmod in zip(valid_actualfilters_this_row,youngmodels):
            self.mean_youngfluxes[curr_row] += youngmod
            textbox6.insert(tk.END,"{}      {}\n".format(filtername,format(youngmod,'.8e')))
        print("total young model flux using weighted mean parameters: {}".format(self.mean_youngfluxes[curr_row]))
        textbox6.place(x=50,y=775)
        groove = tk.Canvas(topw,width=215,height=120,bd=4,relief=tk.RIDGE)
        groove.place(x=405,y=655)
        label7 = tk.Label(topw,text="chi^2 value using \nweighted mean parameters")
        label7.place(x=425,y=665)
        label7a = tk.Label(topw,text="{}".format(format(mean_chi2,'.6e')),font=("Arial",12))
        label7a.place(x=445,y=725)
        self.mean_chi2s.append(0)
        self.mean_chi2s[curr_row] = mean_chi2
        import math
        Z_old_1_sticker1 = format(self.mean_Z1s[curr_row],'.6e')

        age_old_1_sticker1 = format(self.mean_age1s[curr_row],'.6e')

        M_old_1_sticker1 = format(self.mean_M1s[curr_row],'.6e')
        try:
            M_old_1_sticker2 = format(self.errorsallrows[curr_row][0][0],'.6')
        except:
            M_old_1_sticker2 = "       N/A       "
        try:
            M_old_1_sticker3 = format(self.errorsallrows[curr_row][0][1],'.6e')
        except:
            M_old_1_sticker3 = "       N/A       "
        M_old_1_sticker4 = self.errornotes[curr_row][0][0]
        M_old_1_sticker5 = self.errornotes[curr_row][0][1]

        ebv_old_sticker1 = format(self.mean_ebv1s[curr_row],'.6e')

        Z_old_2_sticker1 = format(self.mean_Z2s[curr_row],'.6e')

        age_old_2_sticker1 = format(self.mean_age2s[curr_row],'.6e')

        M_old_2_sticker1 = format(self.mean_M2s[curr_row],'.6e')
        try:
            M_old_2_sticker2 = format(self.errorsallrows[curr_row][1][0],'.6e')
        except:
            M_old_2_sticker2 = "       N/A       "
        try:
            M_old_2_sticker3 = format(self.errorsallrows[curr_row][1][1],'.6e')
        except:
            M_old_2_sticker3 = "       N/A       "
        M_old_2_sticker4 = self.errornotes[curr_row][1][0]
        M_old_2_sticker5 = self.errornotes[curr_row][1][1]

        ebv_new_sticker1 = format(self.mean_ebv2s[curr_row],'.6e')

        Z_new_sticker1 = format(self.mean_Z3s[curr_row],'.6e')

        age_new_sticker1 = format(self.mean_age3s[curr_row],'.6e')

        M_new_sticker1 = format(self.mean_M3s[curr_row],'.6e')
        try:
            M_new_sticker2 = format(self.errorsallrows[curr_row][2][0],'.6e')
        except:
            M_new_sticker2 = "       N/A       "
        try:
            M_new_sticker3 = format(self.errorsallrows[curr_row][2][1],'.6e')
        except:
            M_new_sticker3 = "       N/A       "
        M_new_sticker4 = self.errornotes[curr_row][2][0]
        M_new_sticker5 = self.errornotes[curr_row][2][1]

        colpack1 = tk.Frame(topw)
        colpack1.place(x=650,y=600)
        colpack2 = tk.Frame(topw)
        colpack2.place(x=790,y=600)
        colpack3 = tk.Frame(topw)
        colpack3.place(x=910,y=600)
        colpack4 = tk.Frame(topw)
        colpack4.place(x=1020,y=600)
        colpack5 = tk.Frame(topw)
        colpack5.place(x=1180,y=600)
        colpack6 = tk.Frame(topw)
        colpack6.place(x=1290,y=600)
        parameterhead = tk.Label(colpack1,text="Parameter",bg="azure").pack(pady=3)
        parameter1 = tk.Label(colpack1,text="log(Z_old_1)").pack(pady=3)
        parameter2 = tk.Label(colpack1,text="log(age_old_1)/10").pack(pady=3)
        parameter3 = tk.Label(colpack1,text="log(M_old_1)/10").pack(pady=3)
        parameter4 = tk.Label(colpack1,text="E(B-V)_old").pack(pady=3)
        parameter5 = tk.Label(colpack1,text="log(Z_old_2)").pack(pady=3)
        parameter6 = tk.Label(colpack1,text="log(age_old_2)/10").pack(pady=3)
        parameter7 = tk.Label(colpack1,text="log(M_old_2)/10").pack(pady=3)
        parameter8 = tk.Label(colpack1,text="E(B-V)_young").pack(pady=3)
        parameter9 = tk.Label(colpack1,text="log(Z_young)").pack(pady=3)
        parameter10 = tk.Label(colpack1,text="log(age_young)/10").pack(pady=3)
        parameter11 = tk.Label(colpack1,text="log(M_young)/10").pack(pady=3)
        meanhead = tk.Label(colpack2,text="Weighted mean",bg="azure").pack(pady=3)
        mean1 = tk.Label(colpack2,text="{}".format(Z_old_1_sticker1)).pack(pady=3)
        mean2 = tk.Label(colpack2,text="{}".format(age_old_1_sticker1)).pack(pady=3)
        mean3 = tk.Label(colpack2,text="{}".format(M_old_1_sticker1)).pack(pady=3)
        mean4 = tk.Label(colpack2,text="{}".format(ebv_old_sticker1)).pack(pady=3)
        mean5 = tk.Label(colpack2,text="{}".format(Z_old_2_sticker1)).pack(pady=3)
        mean6 = tk.Label(colpack2,text="{}".format(age_old_2_sticker1)).pack(pady=3)
        mean7 = tk.Label(colpack2,text="{}".format(M_old_2_sticker1)).pack(pady=3)
        mean8 = tk.Label(colpack2,text="{}".format(ebv_new_sticker1)).pack(pady=3)
        mean9 = tk.Label(colpack2,text="{}".format(Z_new_sticker1)).pack(pady=3)
        mean10 = tk.Label(colpack2,text="{}".format(age_new_sticker1)).pack(pady=3)
        mean11 = tk.Label(colpack2,text="{}".format(M_new_sticker1)).pack(pady=3)
        errlohead = tk.Label(colpack3,text="Lower error",bg="azure").pack(pady=3)
        errlo3 = tk.Label(colpack3,text="{}".format(M_old_1_sticker2)).pack(pady=3)
        errlo7 = tk.Label(colpack3,text="{}".format(M_old_2_sticker2)).pack(pady=3)
        errlo11 = tk.Label(colpack3,text="{}".format(M_new_sticker2)).pack(pady=3)
        noteslohead = tk.Label(colpack4,text="Lower error notes",bg="azure").pack(pady=3)
        noteslo3 = tk.Label(colpack4,text="{}".format(M_old_1_sticker4),font="Arial, 6").pack()
        noteslo7 = tk.Label(colpack4,text="{}".format(M_old_2_sticker4),font="Arial, 6").pack()
        noteslo11 = tk.Label(colpack4,text="{}".format(M_new_sticker4),font="Arial, 6").pack()
        errhihead = tk.Label(colpack5,text="Upper error",bg="azure").pack(pady=3)
        errhi3 = tk.Label(colpack5,text="{}".format(M_old_1_sticker3)).pack(pady=3)
        errhi7 = tk.Label(colpack5,text="{}".format(M_old_2_sticker3)).pack(pady=3)
        errhi11 = tk.Label(colpack5,text="{}".format(M_new_sticker3)).pack(pady=3)
        noteshihead = tk.Label(colpack6,text="Upper error notes",bg="azure").pack(pady=3)
        noteshi3 = tk.Label(colpack6,text="{}".format(M_old_1_sticker5),font="Arial, 6").pack()
        noteshi7 = tk.Label(colpack6,text="{}".format(M_old_2_sticker5),font="Arial, 6").pack()
        noteshi11 = tk.Label(colpack6,text="{}".format(M_new_sticker5),font="Arial, 6").pack()

        def closethesource():
            topw.destroy()
        byebyebutt = tk.Button(topw, bd=3, font="Arial 10", text="Next source",command=closethesource,padx=30,pady=5)
        byebyebutt.place(x=423,y=830)
        topw.mainloop()
    
    ##


go = ChiSquared()