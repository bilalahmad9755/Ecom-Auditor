import webbrowser
from tkinter import *
from tkinter import filedialog
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import tkinter
import sys
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib import colors
from reportlab.lib.units import *


class TkinterCustomButton(tkinter.Frame):
    """ tkinter custom button with border, rounded corners and hover effect
        Arguments:  master= where to place button
                    bg_color= background color, None is standard,
                    fg_color= foreground color, blue is standard,
                    hover_color= foreground color, lightblue is standard,
                    border_color= foreground color, None is standard,
                    border_width= border thickness, 0 is standard,
                    command= callback function, None is standard,
                    width= width of button, 110 is standard,
                    height= width of button, 35 is standard,
                    corner_radius= corner radius, 10 is standard,
                    text_font= (<Name>, <Size>),
                    text_color= text color, white is standard,
                    text= text of button,
                    hover= hover effect, True is standard,
                    image= PIL.PhotoImage, standard is None"""

    def __init__(self,
                 bg_color=None,
                 fg_color="#2874A6",
                 hover_color="#5499C7",
                 border_color=None,
                 border_width=0,
                 command=None,
                 width=120,
                 height=40,
                 corner_radius=10,
                 text_font=None,
                 text_color="white",
                 text="CustomButton",
                 hover=True,
                 image=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if bg_color is None:
            self.bg_color = self.master.cget("bg")
        else:
            self.bg_color = bg_color

        self.fg_color = fg_color
        self.hover_color = hover_color
        self.border_color = border_color

        self.width = width
        self.height = height

        if corner_radius * 2 > self.height:
            self.corner_radius = self.height / 2
        elif corner_radius * 2 > self.width:
            self.corner_radius = self.width / 2
        else:
            self.corner_radius = corner_radius

        self.border_width = border_width

        if self.corner_radius >= self.border_width:
            self.inner_corner_radius = self.corner_radius - self.border_width
        else:
            self.inner_corner_radius = 0

        self.text = text
        self.text_color = text_color
        if text_font is None:
            if sys.platform == "darwin":  # macOS
                self.text_font = ("Avenir", 13)
            elif "win" in sys.platform:  # Windows
                self.text_font = ("Century Gothic", 11)
            else:
                self.text_font = "TkDefaultFont"
        else:
            self.text_font = text_font

        self.image = image

        self.function = command
        self.hover = hover

        self.configure(width=self.width, height=self.height)

        if sys.platform == "darwin" and self.function is not None:
            self.configure(cursor="pointinghand")

        self.canvas = tkinter.Canvas(master=self,
                                     highlightthicknes=0,
                                     background=self.bg_color,
                                     width=self.width,
                                     height=self.height)
        self.canvas.place(x=0, y=0)

        if self.hover is True:
            self.canvas.bind("<Enter>", self.on_enter)
            self.canvas.bind("<Leave>", self.on_leave)

        self.canvas.bind("<Button-1>", self.clicked)
        self.canvas.bind("<Button-1>", self.clicked)

        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.text_part = None
        self.text_label = None
        self.image_label = None

        self.draw()

    def draw(self):
        self.canvas.delete("all")
        self.canvas_fg_parts = []
        self.canvas_border_parts = []
        self.canvas.configure(bg=self.bg_color)

        # border button parts
        if self.border_width > 0:

            if self.corner_radius > 0:
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        0,
                                                                        self.corner_radius * 2,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        0,
                                                                        self.width,
                                                                        self.corner_radius * 2))
                self.canvas_border_parts.append(self.canvas.create_oval(0,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.corner_radius * 2,
                                                                        self.height))
                self.canvas_border_parts.append(self.canvas.create_oval(self.width - self.corner_radius * 2,
                                                                        self.height - self.corner_radius * 2,
                                                                        self.width,
                                                                        self.height))

            self.canvas_border_parts.append(self.canvas.create_rectangle(0,
                                                                         self.corner_radius,
                                                                         self.width,
                                                                         self.height - self.corner_radius))
            self.canvas_border_parts.append(self.canvas.create_rectangle(self.corner_radius,
                                                                         0,
                                                                         self.width - self.corner_radius,
                                                                         self.height))

        # inner button parts

        if self.corner_radius > 0:
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.border_width,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(
                self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                        self.border_width,
                                        self.width - self.border_width,
                                        self.border_width + self.inner_corner_radius * 2))
            self.canvas_fg_parts.append(self.canvas.create_oval(self.border_width,
                                                                self.height - self.border_width - self.inner_corner_radius * 2,
                                                                self.border_width + self.inner_corner_radius * 2,
                                                                self.height - self.border_width))
            self.canvas_fg_parts.append(
                self.canvas.create_oval(self.width - self.border_width - self.inner_corner_radius * 2,
                                        self.height - self.border_width - self.inner_corner_radius * 2,
                                        self.width - self.border_width,
                                        self.height - self.border_width))

        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width + self.inner_corner_radius,
                                                                 self.border_width,
                                                                 self.width - self.border_width - self.inner_corner_radius,
                                                                 self.height - self.border_width))
        self.canvas_fg_parts.append(self.canvas.create_rectangle(self.border_width,
                                                                 self.border_width + self.inner_corner_radius,
                                                                 self.width - self.border_width,
                                                                 self.height - self.inner_corner_radius - self.border_width))

        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        for part in self.canvas_border_parts:
            self.canvas.itemconfig(part, fill=self.border_color, width=0)

        # no image given
        if self.image is None:
            # create tkinter.Label with text
            self.text_label = tkinter.Label(master=self,
                                            text=self.text,
                                            font=self.text_font,
                                            bg=self.fg_color,
                                            fg=self.text_color)
            self.text_label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

            # bind events the the button click and hover events also to the text_label
            if self.hover is True:
                self.text_label.bind("<Enter>", self.on_enter)
                self.text_label.bind("<Leave>", self.on_leave)

            self.text_label.bind("<Button-1>", self.clicked)
            self.text_label.bind("<Button-1>", self.clicked)

            self.set_text(self.text)

        # use the given image
        else:
            # create tkinter.Label with image on it
            self.image_label = tkinter.Label(master=self,
                                             image=self.image,
                                             bg=self.fg_color)

            self.image_label.place(relx=0.5,
                                   rely=0.5,
                                   anchor=tkinter.CENTER)

            # bind events the the button click and hover events also to the image_label
            if self.hover is True:
                self.image_label.bind("<Enter>", self.on_enter)
                self.image_label.bind("<Leave>", self.on_leave)

            self.image_label.bind("<Button-1>", self.clicked)
            self.image_label.bind("<Button-1>", self.clicked)

    def configure_color(self, bg_color=None, fg_color=None, hover_color=None, text_color=None):
        if bg_color is not None:
            self.bg_color = bg_color
        else:
            self.bg_color = self.master.cget("bg")

        if fg_color is not None:
            self.fg_color = fg_color

            # change background color of image_label
            if self.image is not None:
                self.image_label.configure(bg=self.fg_color)

        if hover_color is not None:
            self.hover_color = hover_color

        if text_color is not None:
            self.text_color = text_color
            if self.text_part is not None:
                self.canvas.itemconfig(self.text_part, fill=self.text_color)

        self.draw()

    def set_text(self, text):
        if self.text_label is not None:
            self.text_label.configure(text=text)

    def on_enter(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.hover_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.hover_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.hover_color)

    def on_leave(self, event=0):
        for part in self.canvas_fg_parts:
            self.canvas.itemconfig(part, fill=self.fg_color, width=0)

        if self.text_label is not None:
            # change background color of image_label
            self.text_label.configure(bg=self.fg_color)

        if self.image_label is not None:
            # change background color of image_label
            self.image_label.configure(bg=self.fg_color)

    def clicked(self, event=0):
        if self.function is not None:
            self.function()
            self.on_leave()


class Auditor:
    file_path = ""
    data_frame = ""
    summary = {}
    vendor_record = ""
    vendor_audit_details = {}
    category_audit_details = {}
    vendor_name = ""
    v_report = ""
    commission_percentage = ""
    c_report = ""
    category_name = ""
    category_record = ""
    etc_commission = ""
    date = {'from': '', 'to': ''}

    def __init__(self):
        # ------------App_Window---------------------------
        self.audit_page = Tk()
        self.audit_page.title("Every Thing Covered Auditor (Anedea)")
        width = self.audit_page.winfo_screenwidth()
        height = self.audit_page.winfo_screenheight()
        self.audit_page.geometry("%dx%d" % (width, height))
        # self.audit_page['bg'] = ""
        # -------------------------------------------------
        self.browse_button = TkinterCustomButton(text="Browse", fg_color="blue2", hover_color="cyan3", corner_radius=10,
                                                 command=self.browse_file)
        self.save_pdf_button = TkinterCustomButton(text="Save PDF", fg_color="blue2", hover_color="cyan3",
                                                   corner_radius=10, command=self.create_save_pdf)
        self.select_vendor_button = TkinterCustomButton(text="Select Vendor", fg_color="blue2",
                                                        hover_color="cyan3",
                                                        corner_radius=10, command=self.select_vendor)
        self.exit_button = TkinterCustomButton(text="Exit", fg_color="blue2", hover_color="cyan3", corner_radius=10,
                                               command=self.exit)
        self.audit_button = TkinterCustomButton(text="Audit", fg_color="blue2", hover_color="cyan3", corner_radius=10,
                                                command=self.audit_category)
        self.file_path_label = Label(self.audit_page, text="File Path", width=30, height=1,
                                     font='bold', bg='tan1', fg="black")
        self.summary_label = Label(self.audit_page, text="Summary", width=30, height=1,
                                   font='bold', bg='blue2', fg="white")
        self.vendors_label = Label(self.audit_page, text="Vendors", width=30, height=1,
                                   font='bold', bg='blue2', fg="white")
        self.vendor_audit_label = Label(self.audit_page, text="Vendor Audit Report", width=30, height=1,
                                        font='bold', bg='blue2', fg="white")
        self.category_audit_label = Label(self.audit_page, text="Category Audit Report", width=30, height=1,
                                          font='bold', bg='blue2', fg="white")
        self.vendor_audit_report = Label(self.audit_page, text="", width=30, height=22,
                                         font='bold', bg='tan1', fg="black")
        self.category_audit_report = Label(self.audit_page, text="", width=30, height=22,
                                           font='bold', bg='tan1', fg="black")
        self.title = Label(self.audit_page, text="Every Thing Covered (ETC) powered by ANEDEA", width=68, height=3,
                           font=('bold', 16), bg='tan1', fg="black")
        self.vendor_box = Listbox(self.audit_page, height=10, width=30, bg="tan1", font="bold", fg="black",
                                  selectmode=SINGLE, selectforeground="white", selectbackground="cyan3")
        self.category_box = Listbox(self.audit_page, height=8, width=30, bg="tan1", font="bold", fg="black",
                                    selectmode=SINGLE, selectforeground="white", selectbackground="cyan3")
        self.summary_box = Listbox(self.audit_page, height=8, width=30, bg="tan1", font="bold", fg="black",
                                   selectforeground="white", selectbackground="cyan3")
        self.commission_label = Label(self.audit_page, text="Commission %", bg='blue2', width=30, height=1,
                                      font='bold', fg="white")
        self.category_label = Label(self.audit_page, text="Category", width=30, height=1,
                                    font='bold', bg='blue2', fg="white")
        self.etc_label = Label(self.audit_page, bg="tan1", text=" Etc Earnings", width=20, height=2,
                               font=('bold', 18), fg="black")
        self.vendor_label = Label(self.audit_page, bg="tan1", text="Vendor Earnings", width=20, height=2,
                                  font=('bold', 18), fg="black")
        self.total_earnings_label = Label(self.audit_page, bg="tan1", text="Total Earnings", width=20, height=2,
                                          font=('bold', 18), fg="black")
        self.commission = Entry(self.audit_page, width=20, bg="blue2", fg="white", borderwidth=0)
        self.title.place(x=350, y=10)
        self.etc_label.place(x=350, y=440)
        self.total_earnings_label.place(x=350, y=380)
        self.vendor_label.place(x=350, y=498)
        self.commission.place(x=425, y=360)
        self.commission_label.place(x=350, y=320)
        self.file_path_label.place(x=10, y=10)
        self.browse_button.place(x=100, y=50)
        self.vendors_label.place(x=10, y=320)
        self.summary_label.place(x=10, y=100)
        self.summary_box.place(x=10, y=140)
        self.vendor_box.place(x=10, y=360)
        self.vendor_audit_label.place(x=670, y=100)
        self.category_audit_label.place(x=1002, y=100)
        self.vendor_audit_report.place(x=670, y=140)
        self.category_audit_report.place(x=1002, y=140)
        self.select_vendor_button.place(x=100, y=580)
        self.save_pdf_button.place(x=770, y=580)
        self.exit_button.place(x=1095, y=580)
        self.category_box.place(x=350, y=140)
        self.category_label.place(x=350, y=100)
        self.audit_button.place(x=450, y=580)
        self.audit_page.mainloop()

    def load_file(self):
        self.data_frame = pd.read_csv(self.file_path)

    def show_category(self):
        self.category_box.delete(0, END)
        for vendor in self.vendor_record['Product type'].unique():
            self.category_box.insert(END, vendor)
        return True

    def select_vendor(self):
        if len(self.vendor_box.get(0, END)) == 0:
            messagebox.showwarning("Empty Vendor", "Browse CSV File!")
            return True
        elif self.vendor_box.curselection().__len__() == 0:
            messagebox.showwarning("Selection", "Vendor Not Selected!")
        else:
            self.audit_vendor()
            self.show_category()
            return True

    def make_audit_report(self):
        date = datetime.now().date()
        time = datetime.now().time()
        self.vendor_audit_details['vendor_name'] = self.vendor_name
        self.vendor_audit_details['category'] = len(self.vendor_record['Product type'].unique())
        self.vendor_audit_details['total_sales'] = round(self.vendor_record['Total sales'].sum(), 2)
        self.vendor_audit_details['net_sales'] = round(self.vendor_record['Net sales'].sum(), 2)
        self.vendor_audit_details['gross_sales'] = round(self.vendor_record['Gross sales'].sum(), 2)
        self.vendor_audit_details['taxes'] = round(self.vendor_record['Taxes'].sum(), 2)
        self.vendor_audit_details['products'] = len(self.vendor_record['Product'].unique())
        self.vendor_audit_details['quantity'] = self.vendor_record['Net quantity'].sum()
        self.vendor_audit_details['from'] = self.vendor_record['Date'].min()
        self.vendor_audit_details['to'] = self.vendor_record['Date'].max()
        self.v_report = "*** Every Thing Covered (ETC)*** \n" \
                        "*** Vendor Audit Report *** \n \n" \
                        "Vendor Name = %s \n" \
                        "Category = %s \n" \
                        "Products Sold = %s \n" \
                        "Quantity = %s \n" \
                        "Gross Sales = %s \n" \
                        "Net Sales = %s \n" \
                        "Taxes =  %s\n" \
                        "Total Sales = %s \n \n" \
                        "From: %s \n" \
                        "To: %s \n" \
                        "Report Generated on \n" \
                        "%s \n" \
                        "%s \n" \
                        "By: ETC Team" % (
                            self.vendor_audit_details['vendor_name'], self.vendor_audit_details['category'],
                            self.vendor_audit_details['products'],
                            self.vendor_audit_details['quantity'],
                            self.vendor_audit_details['gross_sales'], self.vendor_audit_details['net_sales'],
                            self.vendor_audit_details['taxes'], self.vendor_audit_details['total_sales'],
                            self.vendor_audit_details['from'], self.vendor_audit_details['to'], date, time)
        self.vendor_audit_report.config(text=self.v_report)
        return True

    def make_category_report(self):
        date = datetime.now().date()
        time = datetime.now().time()
        self.vendor_audit_details['vendor_name'] = self.vendor_name
        self.category_audit_details['category_name'] = self.category_name
        self.category_audit_details['items_sold'] = self.category_record['Net quantity'].sum()
        self.category_audit_details['net_sales'] = round(self.category_record['Net sales'].sum(), 2)
        self.category_audit_details['gross_sales'] = round(self.category_record['Gross sales'].sum(), 2)
        self.category_audit_details['taxes'] = round(self.category_record['Taxes'].sum(), 2)
        self.category_audit_details['total_sales'] = round(self.category_record['Total sales'].sum())
        self.category_audit_details['from'] = self.category_record['Date'].min()
        self.category_audit_details['to'] = self.category_record['Date'].max()
        self.c_report = "*** Every Thing Covered (ETC)*** \n" \
                        "*** Category Audit Report *** \n \n" \
                        "Vendor Name = %s \n" \
                        "Category Name = %s \n" \
                        "Quantity = %s \n" \
                        "Gross Sales = %s \n" \
                        "Net Sales = %s \n" \
                        "Taxes = %s \n" \
                        "Total Sales = %s \n" \
                        "ETC Commission(%s%s) =  %s\n" \
                        "Vendor Total =  %s\n" \
                        "From: %s \n" \
                        "To: %s \n" \
                        "Report Generated on \n" \
                        "%s \n" \
                        "%s \n" \
                        "By: ETC Team" % (
                            self.vendor_audit_details['vendor_name'], self.category_audit_details['category_name'],
                            self.category_audit_details['items_sold'],
                            self.category_audit_details['gross_sales'],
                            self.category_audit_details['net_sales'], self.category_audit_details['taxes'],
                            self.category_audit_details['total_sales'], self.commission_percentage, "%",
                            self.etc_commission, self.category_audit_details['after_commission_deduction'],
                            self.category_audit_details['from'], self.category_audit_details['to'], date, time)
        self.category_audit_report.config(text=self.c_report)
        return True

    def create_save_pdf(self):
        if self.vendor_audit_report.cget("text") == "" and self.category_audit_report.cget("text") == "":
            return messagebox.showerror("Report", "No Report to SAVE!")
        else:
            date = datetime.now().date()
            time = datetime.now().time()
            vendor_audit_data = [["Description", "Amount"],
                                 ["Vendor Name", self.vendor_audit_details['vendor_name']],
                                 ["Total Sales", self.vendor_audit_details['total_sales']],
                                 ["Net Sales", self.vendor_audit_details['net_sales']],
                                 ["Gross Sales", self.vendor_audit_details['gross_sales']],
                                 ["Taxes", self.vendor_audit_details['taxes']],
                                 ["Products", self.vendor_audit_details['products']],
                                 ["Quantity", self.vendor_audit_details['quantity']],
                                 ["Dated From", self.vendor_audit_details['from']],
                                 ["Dated To", self.vendor_audit_details['to']]
                                 ]
            category_audit_data = [["Description", "Amount"],
                                   ["Vendor Name", self.vendor_audit_details['vendor_name']],
                                   ["Category Name", self.category_audit_details['category_name']],
                                   ["Quantity", self.category_audit_details['items_sold']],
                                   ["Gross Sales", self.category_audit_details['gross_sales']],
                                   ["Net Sales", self.category_audit_details['net_sales']],
                                   ["Taxes", self.category_audit_details['taxes']],
                                   ["Total Sales", self.category_audit_details['total_sales']],
                                   [f"ETC Commission({self.commission_percentage}%)", self.etc_commission],
                                   ["Vendor Total", self.category_audit_details['after_commission_deduction']],
                                   ["Dated From", self.category_audit_details['from']],
                                   ["Dated To", self.category_audit_details['to']]
                                   ]

            report = SimpleDocTemplate("assets/report.pdf")
            etc_logo = Image("assets/ETC-LOGO--final.jpg", width=70, height=50)
            etc_logo.hAlign = "LEFT"
            anedea_logo = Image("assets/ANEDEA_LOGO.ico", width=80, height=20)
            anedea_logo.hAlign = "LEFT"
            styles = getSampleStyleSheet()
            table_style = [('GRID', (0, 0), (-1, -1), 1, colors.black)]
            report_title = Paragraph("Every Thing Covered", style=styles['h1'])
            report_subtitle = Paragraph("Powered By")
            abs_to_digi = Paragraph("Abstract to Digital")
            note = Paragraph("NOTE: Contact ETC Finance Executive in case of Ambiguity in Report within 2 days...",
                             style=styles["h5"])
            date = Paragraph(f"Report Issue Date : {date}")
            time = Paragraph(f"Report Issue Time : {time}")
            space = Spacer(1, 0.5*cm)

            vendor_report_title = Paragraph("Vendor Audit Report", style=styles["h3"])
            category_report_title = Paragraph("Category Audit Report", style=styles["h3"])

            vendor_audit_table = Table(data=vendor_audit_data, style=table_style, hAlign="CENTER")
            vendor_audit_table.hAlign = "LEFT"
            category_audit_table = Table(data=category_audit_data, style=table_style, hAlign="CENTER")
            category_audit_table.hAlign = "LEFT"
            report.build(
                [etc_logo, space, report_title, report_subtitle, space, anedea_logo, abs_to_digi, space,
                 vendor_report_title, vendor_audit_table, category_report_title,
                 category_audit_table, space, note, date, time])
            # loading pdf in web browser
            path = "assets/report.pdf"
            webbrowser.open_new(path)
            return True

    def audit_vendor(self):
        selected_index = self.vendor_box.curselection()[0]
        self.vendor_name = self.vendor_box.get(selected_index)
        is_vendor_record = self.data_frame['Product vendor'] == self.vendor_name
        self.vendor_record = self.data_frame[is_vendor_record]
        self.make_audit_report()
        return True

    def calculate_commission(self):
        self.commission_percentage = int(self.commission.get())
        total_earnings = round(self.category_record['Total sales'].sum())
        self.etc_commission = round((total_earnings * self.commission_percentage) / 100, 2)
        self.category_audit_details['after_commission_deduction'] = str(round(total_earnings - self.etc_commission))
        self.total_earnings_label.config(fg="blue3", text="Total = " + str(total_earnings))
        self.etc_label.config(fg="blue3", text="ETC = " + str(self.etc_commission))
        self.vendor_label.config(fg='blue3', text="Vendor = " +
                                                  self.category_audit_details['after_commission_deduction'])
        return True

    def audit_category(self):
        # if category box is empty
        if len(self.category_box.get(0, END)) == 0:
            messagebox.showwarning("Empty Category", "No Category Found!")
            return True
        # category box is full but not selected
        elif self.category_box.curselection().__len__() == 0:
            messagebox.showwarning('Category', "Category not Selected!")
        elif self.commission.get() == "":
            messagebox.showwarning("Empty Commission", "Enter Commission % ")
        else:
            selected_category_index = self.category_box.curselection()[0]
            self.category_name = self.category_box.get(selected_category_index)
            is_category_record = self.vendor_record['Product type'] == self.category_name
            self.category_record = self.vendor_record[is_category_record]
            self.calculate_commission()
            self.make_category_report()
            return True

    def show_vendors(self):
        for vendor in self.data_frame['Product vendor'].unique():
            self.vendor_box.insert(END, vendor)
        return True

    def show_summary(self):
        self.summary_box.insert(END, f" Total Record                        {self.summary['total_record']}")
        self.summary_box.insert(END, f" Total Sale                     {self.summary['total_sales']}")
        self.summary_box.insert(END, f" Gross Sale                    {self.summary['gross_sales']}")
        self.summary_box.insert(END, f" Net Sale                       {self.summary['net_sales']}")
        self.summary_box.insert(END, f" Total Taxes                  {self.summary['total_taxes']}")
        self.summary_box.insert(END, f" Total Products                     {self.summary['total_products']}")
        self.summary_box.insert(END, f" Sold Items                           {self.summary['sold_items']}")
        self.summary_box.insert(END, f" Vendors                              {self.summary['vendors']}")

    def get_summary(self):
        self.summary['total_record'] = len(self.data_frame.index) + 1
        self.summary['total_sales'] = round(self.data_frame['Total sales'].sum(), 2)
        self.summary['gross_sales'] = round(self.data_frame['Gross sales'].sum(), 2)
        self.summary['net_sales'] = round(self.data_frame['Net sales'].sum(), 2)
        self.summary['total_taxes'] = round(self.data_frame['Taxes'].sum(), 2)
        self.summary['total_products'] = len(self.data_frame['Product'].unique())
        self.summary['sold_items'] = round(self.data_frame['Net quantity'].sum())
        self.summary['vendors'] = len(self.data_frame['Product vendor'].unique())

        return True

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(initialdir="/home/bilalpython/Documents/anedea/Etc_Auditor/",
                                                    title="Select a File",
                                                    filetypes=(('Excel files', '*.csv*'),
                                                               ('All files', '*.*')
                                                               ),
                                                    )
        self.load_file()
        self.file_path_label.config(text=self.file_path)
        self.get_summary()
        self.show_summary()
        self.show_vendors()
        return True

    def exit(self):
        response = messagebox.askyesno("Exit", "Sure to Exit")
        if response:
            self.audit_page.destroy()
        else:
            return True


auditor = Auditor()
