#!/usr/bin/env python
# encoding: utf-8

import signal_lab as slab

import os
from os.path import basename
import pprint
import random
import wx
import wx.grid

import sys

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar

from matplotlib.backends.backend_wx import _load_bitmap

import pylab
import numpy as np

STATUSBAR = None

class CenterForm( pylab.Formatter):
    def __call__(self,*p,**kw):
#        print p,kw
        res = (p[0]*self.step)+self.origin
        if (res > 1000) or (res < 1/1000.): 
            return "%.2e"%res
        else:
            return str(res)
            
    
    def __init__(self,origin,step):
        self.origin=origin
        self.step = step


class HistForm( pylab.Formatter):
    def __call__(self,*p,**kw):
#        print p,kw
        res = (p[0]*self.step)+self.origin
        return str( res )
    
    def __init__(self,origin,step):
        self.origin=origin
        self.step = step


class PrefrenceFrame(wx.Frame):
    interp_choices = ['None', 'nearest', 'bilinear', 'bicubic',
        'spline16', 'spline36', 'hanning', 'hamming', 'hermite', 'kaiser',
        'quadric', 'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc',
        'lanczos', 'blackman']
    
    cmap_choices = [ "autumn","bone","cool","copper","flag","gray","hot","hsv","jet","pink","prism","spring","summer","winter","spectral" ]

    def __init__( self, mainframe ):
        wx.Frame.__init__(self, None, title="Preferences")
        p = wx.Panel(self)
        
        self.mainframe = mainframe
        hsizer = wx.BoxSizer( wx.VERTICAL )
        sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        hsizer.AddSpacer( 40)
        hsizer.Add( sizer, 10, wx.ALIGN_CENTER_HORIZONTAL )
        hsizer.AddSpacer( 40)
        
        hsizer.AddSpacer( 40)
        sizer.AddSpacer(40 )
        
        gsizer = wx.GridSizer( rows=12, cols=2 )

        rflag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT
        lflag = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT

#===============================================================================
#        
#===============================================================================

        textbox_tag = wx.StaticText( p, -1, "title" )
        textbox = wx.TextCtrl( p, size=(100,-1), style=wx.TE_PROCESS_ENTER )
        textbox.SetValue( self.mainframe.mpl_extras['title'] )

        gsizer.Add( textbox_tag, 1, lflag )
        gsizer.Add( textbox, 1, rflag )
        
        self.Bind(wx.EVT_TEXT_ENTER, self.on_title, textbox )
        
#===============================================================================
#        
#===============================================================================

        textbox_tag = wx.StaticText( p, -1, "xlabel" )
        textbox = wx.TextCtrl( p, size=(100,-1), style=wx.TE_PROCESS_ENTER )
        textbox.SetValue( self.mainframe.mpl_extras['xlabel'] )

        gsizer.Add( textbox_tag, 1, lflag )
        gsizer.Add( textbox, 1, rflag )
        
        self.Bind(wx.EVT_TEXT_ENTER, self.on_xlabel, textbox )
        
#===============================================================================
#        
#===============================================================================

        textbox_tag = wx.StaticText( p, -1, "ylabel" )
        textbox = wx.TextCtrl( p, size=(100,-1), style=wx.TE_PROCESS_ENTER )
        textbox.SetValue( self.mainframe.mpl_extras['ylabel'] )

        gsizer.Add( textbox_tag, 1, lflag )
        gsizer.Add( textbox, 1, rflag )
        
        self.Bind(wx.EVT_TEXT_ENTER, self.on_ylabel, textbox )
#===============================================================================
#        
#===============================================================================

        cmap_choice = wx.Choice( p ,-1, choices=self.cmap_choices )
        cmap_choice_tag = wx.StaticText( p ,-1, "cmap" )
        cmap = mainframe.options["cmap"].name
        idx = self.cmap_choices.index( cmap )
        cmap_choice.SetSelection( idx )

        gsizer.Add( cmap_choice_tag, 1, lflag )
        gsizer.Add( cmap_choice, 1, rflag )
        
        self.Bind(wx.EVT_CHOICE, self.on_cmap, cmap_choice )

#===============================================================================
#        
#===============================================================================
        
        combobox = wx.Choice( p ,-1, choices=self.interp_choices )
        combobox_tag = wx.StaticText( p ,-1,"interpolation")
        idx = self.interp_choices.index(mainframe.options["interpolation"])
        combobox.SetSelection( idx )
        
        gsizer.Add( combobox_tag, 1, lflag )
        gsizer.Add( combobox, 1, rflag )
        
        self.Bind(wx.EVT_CHOICE, self.on_interpolation, combobox )
#===============================================================================
#        
#===============================================================================
        
        combobox= wx.ComboBox( p ,-1, choices=["",'None','auto','equal'] ,style=wx.TE_PROCESS_ENTER )
        combobox_tag = wx.StaticText( p ,-1,"aspect")
        combobox.SetValue( str(mainframe.options["aspect"]) )
        
        gsizer.Add( combobox_tag, 1, lflag )
        gsizer.Add( combobox, 1, rflag )
        
        self.Bind( wx.EVT_COMBOBOX, self.on_aspect, combobox )
        self.Bind( wx.EVT_TEXT_ENTER, self.on_aspect, combobox )
        
#===============================================================================
#        
#===============================================================================
        
        slider_tag = wx.StaticText( p ,-1,"alpha" )
        slider = wx.Slider( p ,-1  ,minValue=0, maxValue=100 ,size=(100,-1),style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        slider.SetValue( 100 )
        
        gsizer.Add( slider_tag, 1, lflag )
        gsizer.Add( slider, 1, rflag )

        self.Bind( wx.EVT_SLIDER, self.on_alpha, slider )

#===============================================================================
#        
#===============================================================================
        
        origin_tag = wx.StaticText( p ,-1, "origin" )
        origin_choice = wx.Choice( p ,-1 , choices=['None','upper','lower'] )
#        slider.SetValue( str( mainframe.a["alpha"] ) )
        
        gsizer.Add( origin_tag, 1, lflag )
        gsizer.Add( origin_choice, 1, rflag )
        
        self.Bind( wx.EVT_CHOICE, self.on_origin, origin_choice )

#===============================================================================
#       
        clim = self.mainframe.pylabimage.get_clim( )
        imin = self.mainframe.image.real.min() 
        imax = self.mainframe.image.real.max()
        
        drange = imax-imin
        minval = int((clim[0]-imin) / drange *100)
        if minval > 100: minval=100 
        if minval < 0: minval=0 
        maxval = int((clim[1]-imin) / drange *100)
        
        if maxval > 100: maxval=100 
        if maxval < 0: maxval=0 
#===============================================================================
        
        slider_tag = wx.StaticText( p ,-1,"clim max (%)" )
        slider = wx.Slider( p ,-1  ,minValue=0, maxValue=100 ,size=(100,-1),style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        
        self.cmax_slider = slider
        
        slider.SetValue( maxval )
        
        gsizer.Add( slider_tag, 1, lflag )
        gsizer.Add( slider, 1, rflag )
        
        self.Bind( wx.EVT_SLIDER, self.on_climmax, slider )
#===============================================================================
#        
#===============================================================================
        
        slider_tag = wx.StaticText( p ,-1,"clim min (%)" )
        slider = wx.Slider( p ,-1  ,minValue=0, maxValue=100 ,size=(100,-1),style=wx.SL_AUTOTICKS | wx.SL_LABELS)
        self.cmin_slider = slider
        slider.SetValue( minval )
        
        gsizer.Add( slider_tag, 1, lflag )
        gsizer.Add( slider, 1, rflag )
        
        self.Bind( wx.EVT_SLIDER, self.on_climmin, slider )

#===============================================================================
#        
#===============================================================================
        
        cb_tag = wx.StaticText( p ,-1,"Grid" )
        cb = wx.CheckBox( p ,-1 ,"Grid")
        
        gsizer.Add( cb_tag, 1, lflag )
        gsizer.Add( cb, 1, rflag )
        
        self.Bind( wx.EVT_CHECKBOX, self.on_grid, cb )

#===============================================================================
#        
#===============================================================================
        
        cb_tag = wx.StaticText( p ,-1,"Coords" )
        cb = wx.CheckBox( p ,-1 ,"Coords")
        cb.SetValue( True )
        
        gsizer.Add( cb_tag, 1, lflag )
        gsizer.Add( cb, 1, rflag )
        
        self.Bind( wx.EVT_CHECKBOX, self.on_coords, cb )

#===============================================================================
#        
#===============================================================================

        sizer.Add( gsizer, 10, wx.ALIGN_CENTER_HORIZONTAL )
        sizer.AddSpacer( 40 )
        
        p.SetSizer(hsizer)
        hsizer.Fit( self )

    def on_coords(self, event ):
        val = event.GetInt()
        self.mainframe.coords = bool(val)
        self.mainframe.draw_images()
        
    def on_exit(self, event):
        
        if self.main_frame:
            self.main_frame.Destroy( )
        self.Destroy( )

    def on_title(self,event):
        title = event.GetString()
        self.mainframe.mpl_extras['title'] = title
        self.mainframe.draw_images()
        
    def on_xlabel(self,event):
        xlabel = event.GetString()
        self.mainframe.mpl_extras['xlabel'] = xlabel
        self.mainframe.draw_images()
        
    def on_ylabel(self,event):
        ylabel = event.GetString()
        self.mainframe.mpl_extras['ylabel'] = ylabel
        self.mainframe.draw_images()
    
    def on_cmap(self,event):
        cmap = event.GetString()
        self.mainframe.options['cmap'] = getattr(pylab.cm, cmap)
        self.mainframe.draw_images()
        
    def on_interpolation(self,event):
        interp = event.GetString()
        self.mainframe.options['interpolation'] = interp
        self.mainframe.draw_images()
    
    def on_aspect(self,event):
        aspect = event.GetString()
        if aspect in ['auto','equal']:
            self.mainframe.options['aspect'] = aspect
        elif aspect == 'None':
            self.mainframe.options['aspect'] = None
        else:
            self.mainframe.options['aspect'] = float(aspect)
            
        self.mainframe.draw_images( )
            
            
        
    def on_alpha(self,event):
        alpha = float(event.GetInt())/100.0
        self.mainframe.options['alpha'] = alpha
            
        self.mainframe.draw_images( )
        
    def on_origin(self,event):
        origin = event.GetString()
        if origin == 'None':
            self.mainframe.options['origin'] = None
        else:
            self.mainframe.options['origin'] = origin
            
        self.mainframe.draw_images( )
    
    def on_climmax(self,event):
        clim = self.mainframe.pylabimage.get_clim( )
        
        imin = self.mainframe.image.real.min() 
        imax = self.mainframe.image.real.max()
        
        drange = imax-imin
        
        
        cmax = (event.GetInt()*drange/100.0)+imin
        
        if self.mainframe.options['clim'] is None:
            self.mainframe.options['clim'] = [ imin, 0]

        if cmax < self.mainframe.options['clim'][0]:
            self.cmax_slider.SetValue( self.cmin_slider.GetValue() )
            return 
        
        self.mainframe.options['clim'][1] = cmax
        
        self.mainframe.draw_images( )
        
    def on_climmin(self,event):
        clim = self.mainframe.pylabimage.get_clim( )
        
        imin = self.mainframe.image.real.min() 
        imax = self.mainframe.image.real.max()
        
        drange = imax-imin
        
        cmin = (event.GetInt()*drange/100.0)+imin
        
        if self.mainframe.options['clim'] is None:
            self.mainframe.options['clim'] = [0, imax]
            
        if cmin > self.mainframe.options['clim'][1]:
            self.cmin_slider.SetValue( self.cmax_slider.GetValue() )
            return 
        
        self.mainframe.options['clim'][0] = cmin
        
        self.mainframe.draw_images( )
    
    def on_grid(self,event):
        self.mainframe.mpl_extras['grid'] = bool( event.GetInt() ) 
        self.mainframe.draw_images( )
        
    
class MainFrame(wx.Frame):
    
    def __init__( self , sfiles, images, options ):
        
        self.coords  = True 
        self.pref_frame = None
        self.image_num = 0
        self.images = images
        self.sfiles = sfiles
        self.image = images[self.image_num][0]
        mpl_extras = images[self.image_num][1]
        
        self.data_view = np.real
        
        wx.Frame.__init__(self, None, title=mpl_extras.get('title',"RSF Viewer"))
        
        self.options = options
        self.mpl_extras= mpl_extras
        self.currimage = 0
        self.show_type = 'image'
        self.xsection = [0,0]
        self.xsection_arrows = []
        
        self.axes = {"image":None,"xsec":None,"hist":None}
        self.create_status_bar()
        self.create_menu( )
        self.create_main_panel( )
        
    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()
        
        global STATUSBAR
        STATUSBAR = self.statusbar 

    
    def create_main_panel(self):
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        
        sizer = wx.BoxSizer( wx.VERTICAL )
        
        hsizer = wx.BoxSizer( wx.HORIZONTAL )
        self.pbutton = wx.Button(p, -1, "Prev" )
        self.nbutton = wx.Button(p, -1, "Next" )
        self.rbox = wx.RadioBox( p, -1, "",  choices=["real","imag","abs"])
        
        hsizer.AddSpacer(5)
        hsizer.Add( self.pbutton, 0 , wx.ALIGN_CENTER_VERTICAL )
        hsizer.AddSpacer(5)
        hsizer.Add( self.nbutton, 0 ,wx.ALIGN_CENTER_VERTICAL )
        hsizer.AddSpacer(5)
        hsizer.Add( self.rbox, 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(5)
        hsizer.Add( wx.StaticText( p, -1 ,"Location" ) , 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(5)
        tbox1 = wx.TextCtrl( p, size=(100,-1), style=wx.TE_PROCESS_ENTER )
        hsizer.Add( tbox1 , 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(1)
        hsizer.Add( wx.StaticText( p, -1 ,"x" ) , 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(5)
        
        tbox2 = wx.TextCtrl( p, size=(100,-1), style=wx.TE_PROCESS_ENTER )
        hsizer.Add( tbox2 , 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(1)
        hsizer.Add( wx.StaticText( p, -1 ,"y" ) , 0  ,wx.ALIGN_CENTER_VERTICAL)
        hsizer.AddSpacer(5)
        
        self.Bind(wx.EVT_BUTTON, self.on_previmage, self.pbutton )
        self.Bind(wx.EVT_BUTTON, self.on_nextimage, self.nbutton )
        self.Bind(wx.EVT_RADIOBOX, self.on_rbox, self.rbox )
        
        sizer.AddSpacer(5)
        sizer.Add( hsizer, 0  )
        sizer.AddSpacer(5)
        
        # the layout
                
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigCanvas( p, -1, self.fig )
        
#        if image.ndim < 3:
#            self.axis = self.fig.add_subplot( 111 )
#        self.create_axes( )
        self.draw_images( )
        
        self.toolbar = NavigationToolbar( self.canvas )
        
        sizer.Add( self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        sizer.Add( self.toolbar, 0, wx.LEFT | wx.TOP | wx.GROW)
        
                
        p.SetSizer( sizer )
        sizer.Fit( self )
        
        self.canvas.mpl_connect('key_press_event', self.on_key )
    
    def on_nextimage(self,event):
        self.image_num+=1
        if self.image_num >= len(self.images):
            self.image_num=0
        self.image = self.images[self.image_num][0]
        self.mpl_extras = self.images[self.image_num][1]
        self.draw_images()

    def on_previmage( self, event ):
        self.image_num-=1
        if self.image_num < 0:
            self.image_num=len(self.images)-1
        self.image = self.images[self.image_num][0]
        self.mpl_extras = self.images[self.image_num][1]
        self.draw_images()

    def on_rbox(self ,event ):
        name = event.GetString()
        if name=='real':
            self.data_view = np.real
        if name=='imag':
            self.data_view = np.imag
        if name=='abs':
            self.data_view = np.abs
            
        self.draw_images( )
        
    def on_key(self,event):
        
        image = self.image
        if event.key =='right':
            self.xsection[1]+=1
        elif event.key =='left':
            self.xsection[1]-=1
        if event.key =='up':
            self.xsection[0]-=1
        elif event.key =='down':
            self.xsection[0]+=1
        elif event.key == 'enter':
            ee = self.enter_event( event)
            if ee:
                self.xsection = list( self.enter_event( event ) )
            
            
        if self.xsection[0] > image.shape[0]:
            self.xsection[0]=0
        if self.xsection[0] < 0:
            self.xsection[0]=image.shape[0]
            
        if self.xsection[1] > image.shape[1]:
            self.xsection[1]=0
        if self.xsection[1] < 0:
            self.xsection[1]=image.shape[1]
            
        self.draw_images( )
        
    def create_menu(self):
        self.menubar = wx.MenuBar( )
        
        menu_file = wx.Menu( )
        m_open = menu_file.Append(-1, "&Open\tCtrl-O", "Open new .RSF to view" )
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        self.Bind(wx.EVT_MENU, self.on_open_file, m_open)

        menu_file.AppendSeparator( )
        
        m_exit = menu_file.Append(-1, "&Close Window\tCtrl-W", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        
        menu_help = wx.Menu( )
        m_about = menu_help.Append(-1, "&About\tF1", "About the demo")
        self.Bind(wx.EVT_MENU, self.on_about, m_about)

        menu_image = wx.Menu( )
        self.m_imag = menu_image.Append(-1, "&Image\tCtrl-I", "Show Image" )
        self.m_xsec = menu_image.Append(-1, "&Cross Section\tCtrl-X", "Show Cross Section" )
        self.m_hist = menu_image.Append(-1, "&Histogram\tCtrl-U", "Show Histogram" )
        menu_image.AppendSeparator( )
        self.m_prev = menu_image.Append(-1, "&Previous\tCtrl-P", "Previous Image" )
        self.m_next = menu_image.Append(-1, "&Next\tCtrl-N", "Next Image" )
        
        self.Bind( wx.EVT_MENU, self.on_xsec, self.m_xsec )
        self.Bind( wx.EVT_MENU, self.on_imag, self.m_imag )
        self.Bind( wx.EVT_MENU, self.on_hist, self.m_hist )
        
        self.Bind(wx.EVT_MENU, self.on_prev, self.m_prev)
        self.Bind(wx.EVT_MENU, self.on_next, self.m_next)
                
        menu_window = wx.Menu( )
        self.m_win = menu_window.Append(-1, "&Preferences\tCtrl-,", "Preferences window" )
        self.m_sfin = menu_window.Append(-1, "&sfin", "rsf file attributes" )
        self.m_sfattr = menu_window.Append(-1, "&sfattr", "rsf file attributes" )
        self.Bind(wx.EVT_MENU, self.on_pref, self.m_win )
        self.Bind(wx.EVT_MENU, self.on_sfin, self.m_sfin )
        self.Bind(wx.EVT_MENU, self.on_sfattr, self.m_sfattr )
        
        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menu_help, "&Help")
        self.menubar.Append(menu_image, "&Image")
        self.menubar.Append(menu_window, "&Window")
        
        
        self.SetMenuBar(self.menubar)
        
    def  on_pref(self,event ):
        frame = PrefrenceFrame( self )
        frame.Show(True)
        frame.SetFocus( )
        self.pref_frame = frame


    
    def on_xsec( self, event ):
        self.image_change( 'xsec' )
        self.show_type = 'xsec' 
#        self.create_axes( )
        self.draw_images( ) 
        
    def on_imag( self, event ):
        self.image_change( 'image' )
        self.show_type = 'image' 
#        self.create_axes( )
        self.draw_images( ) 
        
    def on_hist( self, event ):
        self.image_change( 'hist' )
        self.show_type = 'hist'
#        self.create_axes( )
        self.draw_images( ) 
        
    def on_save_plot(self, event):
        file_choices = "PNG (*.png)|*.png"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            self.flash_status_message("Saved to %s" % path)
            
    def on_open_file(self , event ):
        file_choices = "RSF (*.rsf)|*.rsf"
        
        dlg = wx.FileDialog(
            self, 
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.OPEN )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            
            sfile = slab.File(path)
            sarray = np.asarray( sfile )
            env = slab.Environment([])
            extras = create_mpl_extras2D(env, sfile)
            self.images.append( (sarray, extras ) )
            self.sfiles.append( sfile )
            self.image_num = len(self.images)-1
            self.image = sarray
            self.mpl_extras = extras
            self.draw_images()
        
    def flash_status_message(self, msg, flash_len_ms=1500):
        self.statusbar.SetStatusText(msg)

    def on_exit(self, event):
        
        if self.pref_frame:
            self.pref_frame.Destroy( )
        self.Destroy( )
        
    def on_about(self, event):
        msg = """ 
        Author: Sean Ross-Ross
        
        RSF Viewer program
        """
        dlg = wx.MessageDialog(self, msg, "About", wx.OK)
        dlg.ShowModal( )
        dlg.Destroy()
        
    def on_sfin(self, event ):
        
        sfile = self.sfiles[self.image_num]
        msg = "in=%s\n" %sfile['in']
        msg += "esize=%s    type=%s    form=%s\n"%(sfile.esize,sfile.type, sfile.form)
        
        shape = sfile.shape
        step = sfile.step
        origin = sfile.origin
        labels = sfile.labels
        units = sfile.units
        
        for i in range( sfile.ndim ):
            msg += "n1=%s    d1=%s    o1=%s    label1=%s    unit1=%s\n"%( shape[i], step[i], origin[i], labels[i], units[i] )
        
        msg += "%s elements %s bytes" %( sfile.size, sfile.nbytes)
#            in="/Tools/toolboxes/rsf_stuff/datapath/moid.rsf@"
#            esize=4 type=float form=native 
#            n1=512         d1=0.004       o1=0          label1="Time" unit1="s" 
#            n2=512         d2=0.032       o2=0          label2="Lateral" unit2="km" 
#            262144 elements 1048576 bytes
        dlg = wx.MessageDialog(self, msg, "sfin:", wx.OK)
        dlg.ShowModal( )
        dlg.Destroy()
    def on_sfattr(self,event):
        
        image = self.images[self.image_num][0]
        armax =np.argmax( image )
        armin = np.argmin( image )
        msg = "*******************************************\n" 
        msg += "rms = %s\n" %np.sqrt( np.sum(image**2) / image.size )
        msg += "mean value = %s\n" %image.mean() 
        msg += "2-norm value = %s\n" %np.sum(image**2)**0.5
        msg += "variance = %s\n" %np.var( image )
        msg += "standard deviation = %s\n" %np.std( image )
        msg += "maximum value =  %s at %s %s\n" %(np.max( image ),armax%image.shape[0],armax/image.shape[0])
        msg += "minimum value = %s at %s %s\n" %(np.min( image ),armin%image.shape[0],armin/image.shape[0])
        msg += "number of nonzero samples = %s \n" %len(np.nonzero( image ))
        msg += "total number of samples = %s \n" %image.size
        msg += "*******************************************\n" 
        dlg = wx.MessageDialog(self, msg, "sfattr:", wx.OK)
        dlg.ShowModal( )
        dlg.Destroy()
        
    def on_prev(self,event):
        self.currimage-=1
        self.draw_images( )
        
    def on_next(self,event):
        
        self.currimage+=1
        self.draw_images( )
        
        
        
class MainFrame2D(MainFrame):
    
    def image_change(self,to):
        if self.show_type == 'image' and to=='hist':
            if self.axes['hist']:
                self.axes['hist'].invert_yaxis( )
    
    def enter_event(self,event):
        
        if self.axes['image'] and event.inaxes == self.axes['image']:
            x = int(event.xdata)
            y = int(event.ydata)
            return x,y
        
        if self.axes['xsec']:
            if event.inaxes == self.axes['xsec'][0]:
                x = int(event.xdata)
                y = int(event.ydata)
                return y,x
            elif event.inaxes == self.axes['xsec'][1]:
                x = self.xsection[0]
                y = int(event.xdata)
                
                return y,x
            elif event.inaxes == self.axes['xsec'][2]:
                x = int(event.xdata)
                y = self.xsection[1]
                return y,x
            else:
                return  self.xsection
        
    def create_axes(self):
        
        if self.axes['image'] is not None:
            self.axes['image'].set_visible(False)
                
        if self.axes['hist'] is not None:
           self.axes['hist'].set_visible(False)
           
        if self.axes['xsec'] is not None:
           self.axes['xsec'][0].set_visible(False)
           self.axes['xsec'][1].set_visible(False)
           self.axes['xsec'][2].set_visible(False)

        if self.show_type =='hist':
            if self.axes['hist'] is None:
                self.axes['hist'] = self.fig.add_subplot( 111 )
                self.axes['hist'].invert_yaxis( )
            self.axes['hist'].set_visible(True)
            return self.axes['hist']
        elif self.show_type =='image':
            if self.axes['image'] is None:
                self.axes['image'] = self.fig.add_subplot( 111 )
            self.axes['image'].set_visible(True)
            return self.axes['image']
        
        elif self.show_type =='xsec':
            if self.axes['xsec'] is None: 
                self.axes['xsec'] = (self.fig.add_subplot( 221 ),self.fig.add_subplot( 222 ),self.fig.add_subplot( 223 ))
            self.axes['xsec'][0].set_visible(True)
            self.axes['xsec'][1].set_visible(True)
            self.axes['xsec'][2].set_visible(True)
            return self.axes['xsec']
        else:
            raise NotImplementedError
        
        
       
    def draw_image(self, axes ):
        
        mpl_extras = self.mpl_extras
        options = self.options
        image = self.image
        
        pylabimage = axes.imshow( self.data_view(image) , **options )
        self.pylabimage=pylabimage 
        
        
        xlabel = mpl_extras.get( 'xlabel', None )
        if xlabel and self.coords:
            axes.set_xlabel( xlabel )
            
        ylabel = mpl_extras.get( 'ylabel', None )
        if xlabel and self.coords:
            axes.set_ylabel( ylabel )
            
        title = mpl_extras.get( 'title', None )
        if title:
            axes.set_title( title )
        
        if self.coords:
            axes.yaxis.set_major_formatter( CenterForm( mpl_extras['origin'][0], mpl_extras['step'][0] ) )
            axes.xaxis.set_major_formatter( CenterForm( mpl_extras['origin'][1], mpl_extras['step'][1] ) )
        
        grid = mpl_extras.get( 'grid', False )
        axes.grid( grid )
#            pylabimage.set_colorbar( pylabimage, axis )

    def draw_images(self):
        
        options = self.options.copy( )
        image = self.image
        mpl_extras = self.mpl_extras.copy( )
        
        image_axes = mpl_extras['image_axes']
        ndim = mpl_extras['ndim']
        
        
        axes = self.create_axes( )
        if self.show_type == 'hist':
            
#            histo = np.histogram( image , bins=100 , new=True)
#            hist = histo[0]
#            
            axes.clear( )
            
            ire = self.data_view(image.reshape(-1))
            if options['clim'] is not None:
                _mask = np.ma.masked_where((ire <= options['clim'][0]) | (ire > options['clim'][1]), ire, copy=False)
            else:
                _mask = ire
                
            pylabimage = axes.hist( _mask ,bins=mpl_extras['bins'] , histtype=mpl_extras['histtype'])
            
            
        
        elif self.show_type =='image':
            
            axes.clear( )   
            self.draw_image(axes)
            
        elif self.show_type =='xsec':
            axis1 = axes[0]
            axis2 = axes[1]
            axis3 = axes[2]
            
            axis1.clear( )   
            axis2.clear( )   
            axis3.clear( )
               
            self.draw_image( axis1 )
            
            for arr in self.xsection_arrows:
                try:
                    arr.remove()
                except:
                    pass
            
            self.xsection_arrows = [ ]


            arr = axis1.arrow( self.xsection[1], 0,  0, self.image.shape[0], ec='y' )
            self.xsection_arrows.append( arr )
            arr = axis1.arrow(  0, self.xsection[0],  self.image.shape[1], 0 , ec='y')
            self.xsection_arrows.append( arr )
            
            xlabel = mpl_extras.get( 'xlabel', None )
                
            ylabel = mpl_extras.get( 'ylabel', None )
                
            
            sec1 = self.data_view(self.image[self.xsection[0],:])
            pylabimage = axis2.plot( sec1.real , color='black' )
            pylabimage2 = axis2.plot( [self.xsection[1],self.xsection[1]],[sec1.min(),sec1.max()] ,color='y' )
            
            if self.coords:
                axis2.xaxis.set_major_formatter( CenterForm( mpl_extras['origin'][1], mpl_extras['step'][1] ) )
                axis2.set_xlabel( ylabel )
                
                axis2.set_title( "%s=%s"%(ylabel,self.xsection[0]) )
            else:
                axis2.set_title( "y=%s" %(self.xsection[0]))
                axis2.set_xlabel( "x-axis" )
            
#            arr = axis2.arrow(  0, 0 ,  1, 1 )
#            self.xsection_arrows.append( arr )
            
            sec2 = self.data_view(self.image[:,self.xsection[1]])
            pylabimage = axis3.plot( sec2.real , color='black')
            pylabimage2 = axis3.plot( [self.xsection[0],self.xsection[0]],[sec2.min(),sec2.max()] ,color='y' )
            
            if self.coords:
                axis3.xaxis.set_major_formatter( CenterForm( mpl_extras['origin'][0], mpl_extras['step'][0] ) )
                axis3.set_xlabel( xlabel )
                
                axis3.set_title( "%s=%s"%(xlabel,self.xsection[1]) )
            else:
                axis3.set_title( "x=%s" %(self.xsection[1]))
                axis3.set_xlabel( "y-axis" )
                

#            raise NotImplementedError("can't do 3d yet")
        
        self.canvas.draw( )
        
        
        

        
def main( sfiles, images, options  ):
    app = wx.PySimpleApp( )
#    if mpl_extras['ndim'] == 2:
    app.frame = MainFrame2D( sfiles, images, options )
#    else:
#        raise NotImplementedError
    
    app.frame.Show( )
    app.MainLoop( )


def create_mpl_options2D( env, sfile ):
    
    options = env.kw.copy()
    mpl_options = {}
    
    ## interpolation
    mpl_options['interpolation']=options.get('interpolation','nearest')
    
    ## cmap
    mpl_options['cmap'] = getattr(pylab.cm, options.get('cmap','jet') )
    
    ## aspect
    aspect = options.get('aspect','auto')
    try:
        aspect = float(aspect)
    except:
        if aspect not in ['auto','equal','None']:
            raise Exception("'aspect=' must be None | 'auto' | 'equal' | scalar")
        if aspect == 'None':
            aspect = None
    
    mpl_options['aspect'] = aspect
    
    ## alpha
    alpha = float(options.get('alpha','1'))
    mpl_options['alpha'] = alpha
    
    ## clim
    clim = eval(options.get('clim','None'))
    if clim:
        mpl_options['clim'] = list(clim)
    else:
        mpl_options['clim'] = None
        
    return mpl_options

def create_mpl_extras2D( env, sfile ):
    
    mpl_extras = {}
    mpl_extras['colorbar'] = env.kw.get('colorbar','y')
    if mpl_extras['colorbar'] not in ['y','n']:
        raise Exception( "'colorbar=' argument must be 'n' | 'y'")

    if sfile.labels:
        labels = sfile.labels
    else:
        labels = ["?","?"]
    if sfile.units:
        units = sfile.units
    else:
        units = ["?","?"]
    
    mpl_extras['xlabel'] = "%s (%s)" %(labels[1], units[1] )    
    mpl_extras['ylabel'] = "%s (%s)" %(labels[0], units[0] )
        
    mpl_extras['title'] =  env.kw.get('title', basename(sfile.header) )
     
    mpl_extras['origin'] = sfile.origin 
    mpl_extras['step'] = sfile.step 
    
    mpl_extras['grid'] = env.kw.get('grid', 'n' )
    if mpl_extras['grid'] =='y':
        mpl_extras['grid']= True
    else:
        mpl_extras['grid']= False
       
    mask = env.kw.get('mask')
    if not mask:
        mask = sfile.get( 'mask' ) 
    if mask:
        maskarray = np.asarray(slab.File(mask,env=env))
        image = np.ma.masked_where( maskarray , image )

    mpl_extras['ndim']= int(env.kw.get('ndim', str(sfile.ndim) ))
    mpl_extras['image_axes']= eval(env.kw.get('image_axes', "0" ) )
    mpl_extras['image_type']= env.kw.get('image_type', 'movie' )

    
    mpl_extras['bins']= int(env.kw.get('histbins', '200' ))
    mpl_extras['histtype']= env.kw.get('histtype', 'stepfilled' )
    
    
    return mpl_extras
    
def WriteOut( filename, name, options, extras ):
    
        if filename == "stdout":
            ofile = sys.stdout
        else:
            ofile = open(filename,'w')
            
        options['cmap'] = options['cmap'].name 
        
        ofile.write( "input=%r"%os.path.abspath(arg) )
        ofile.write( "\n\n" )
        print >> ofile,  "options={" 
        for item in options.items():
            print >> ofile, "    %r=%r," %item
        print >> ofile,  "}"
        print >> ofile
        print >> ofile,  "extras={" 
        for item in extras.items():
            print >> ofile, "    %r=%r," %item
        print >> ofile,  "}"
        
if __name__ == '__main__':
    
    
    env = slab.Environment( sys.argv )
    
    if "output" in env.kw:
        arg = env.args[0]
        sfile= slab.File(arg,env=env)
        WriteOut(env.kw['output'], arg, options, extras)
        raise SystemExit( )
    
    images=[ ]
    sfiles=[ ]
    for arg in env.args:
        sfile= slab.File(arg,env=env)
        sarray = np.asarray( sfile )
        extras = create_mpl_extras2D(env, sfile )
        images.append( (sarray,extras))
        sfiles.append( sfile )
    
    options = create_mpl_options2D(env, sfile)
    
    main( sfiles, images , options )
    
