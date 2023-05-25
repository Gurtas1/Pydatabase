# Autor: Martin Klokočík

import sqlite3
import tkinter as tk


class Acomodation:
    class Table(tk.Canvas):
        def __init__(self, parent, column_names, rows, column_names2, rows2, acomodation_inst):
            super().__init__(parent, bg="floral white", highlightthickness=0)
            self.parent = parent
            self.acomodation_inst = acomodation_inst

            self.add_button = tk.Button(self, text="Add", command=self.button_click_add, bg="antique white", fg="black",
                                        font=("Helvetica", 8), borderwidth=3, relief="raised", padx=5, pady=2)
            self.delete_button = tk.Button(self, text="Delete", command=self.button_click_delete, bg="antique white",
                                           fg="black", font=("Helvetica", 8), borderwidth=3, relief="raised", padx=5,
                                           pady=2)
            self.filter_button = tk.Button(self, text="Filter", command=self.button_click_filter, bg="antique white",
                                           fg="black", font=("Helvetica", 8), borderwidth=3, relief="raised", padx=5,
                                           pady=2)
            self.clear_filter_button = tk.Button(self, text="Clear filter", command=self.button_click_clear_filter,
                                                 bg="antique white", fg="black", font=("Helvetica", 8), borderwidth=3,
                                                 relief="raised", padx=5, pady=2)
            self.sort_button = tk.Button(self, text="Sort/Unsort", command=self.button_click_sorting,
                                         bg="antique white", fg="black", font=("Helvetica", 8), borderwidth=3,
                                         relief="raised", padx=5, pady=2)

            self.clear_filter_button.pack(side="bottom")
            self.delete_button.pack(side="bottom")
            self.sort_button.pack(side="bottom")
            self.filter_button.pack(side="bottom")
            self.add_button.pack(side="bottom")

            self.display_table(column_names, rows, column_names2, rows2)

            self.pack(side="left", fill="both", expand=True)

        def table_update(self, by=None):
            if by == 'availability':
                column_names, rows, column_names2, rows2 = self.acomodation_inst.filtered_table()
            else:
                column_names, rows, column_names2, rows2 = self.acomodation_inst.interactive_table_get()

            self.text_widget.destroy()
            self.display_table(column_names, rows, column_names2, rows2)

        def display_table(self, column_names, rows, column_names2, rows2):
            self.text_widget = tk.Text(self, bg="floral white", fg="black", font=("Courier", 10), padx=10, pady=10)
            self.text_widget.pack(side="left", fill="both", expand=True)

            lengths = [len(name) for name in column_names]
            for row in rows:
                lengths = [max(length, len(str(item))) for length, item in zip(lengths, row)]

            lengths = [length + 2 for length in lengths]

            format_string = ' '.join('| {:^%d}' % l for l in lengths) + ' |\n'
            self.text_widget.insert("end", format_string.format(*column_names))
            self.text_widget.insert("end", '-' * (sum(lengths) + len(lengths) + 3 + 12) + "\n")

            for row in rows:
                self.text_widget.insert("end", format_string.format(*row))
                self.text_widget.insert("end", '-' * (sum(lengths) + len(lengths) + 3 + 12) + "\n")

            # second table
            self.text_widget.insert("end", "\n\n")

            lengths2 = [len(name) for name in column_names2]
            for row in rows2:
                lengths2 = [max(length, len(str(item))) for length, item in zip(lengths2, row)]

            lengths2 = [length + 2 for length in lengths2]

            format_string = ' '.join('| {:^%d}' % l for l in lengths2) + ' |\n'
            self.text_widget.insert("end", format_string.format(*column_names2))
            self.text_widget.insert("end", '-' * (sum(lengths2) + len(lengths2) + 3 + 8) + "\n")

            for row in rows2:
                self.text_widget.insert("end", format_string.format(*row))
                self.text_widget.insert("end", '-' * (sum(lengths2) + len(lengths2) + 3 + 8) + "\n")

            self.text_widget.configure(width=(sum(max(lengths, lengths2)) + len(max(lengths, lengths2)) + 50),
                                       height=40)

        def button_click_delete(self):
            add_window = tk.Toplevel()
            add_window.title("Remove Item")

            id_label = tk.Label(add_window, text="Item ID:")
            id_label.grid(row=0, column=0, padx=10, pady=5)
            id_entry = tk.Entry(add_window)
            id_entry.grid(row=0, column=1, padx=10, pady=5)

            self.submit_button = tk.Button(add_window, text="Submit",
                                           command=lambda: self.submit_remove(id_entry.get(), add_window))
            self.submit_button.grid(row=5, column=1, padx=10, pady=5)

        def button_click_add(self):
            add_window = tk.Toplevel()
            add_window.title("Add Item")

            name_label = tk.Label(add_window, text="Name:")
            name_label.grid(row=0, column=0, padx=10, pady=5)
            name_entry = tk.Entry(add_window)
            name_entry.grid(row=0, column=1, padx=10, pady=5)

            state_label = tk.Label(add_window, text="State:")
            state_label.grid(row=1, column=0, padx=10, pady=5)
            state_entry = tk.Entry(add_window)
            state_entry.grid(row=1, column=1, padx=10, pady=5)

            type_label = tk.Label(add_window, text="Type:")
            type_label.grid(row=2, column=0, padx=10, pady=5)
            type_entry = tk.Entry(add_window)
            type_entry.grid(row=2, column=1, padx=10, pady=5)

            services_label = tk.Label(add_window, text="Services:")
            services_label.grid(row=3, column=0, padx=10, pady=5)
            services_entry = tk.Entry(add_window)
            services_entry.grid(row=3, column=1, padx=10, pady=5)

            address_label = tk.Label(add_window, text="Address:")
            address_label.grid(row=4, column=0, padx=10, pady=5)
            address_entry = tk.Entry(add_window)
            address_entry.grid(row=4, column=1, padx=10, pady=5)

            ad_num_label = tk.Label(add_window, text="Number of adults:")
            ad_num_label.grid(row=5, column=0, padx=10, pady=5)
            ad_num_entry = tk.Entry(add_window)
            ad_num_entry.grid(row=5, column=1, padx=10, pady=5)

            ch_num_label = tk.Label(add_window, text="Number of children:")
            ch_num_label.grid(row=6, column=0, padx=10, pady=5)
            ch_num_entry = tk.Entry(add_window)
            ch_num_entry.grid(row=6, column=1, padx=10, pady=5)

            p_num_label = tk.Label(add_window, text="Number of pets:")
            p_num_label.grid(row=7, column=0, padx=10, pady=5)
            p_num_entry = tk.Entry(add_window)
            p_num_entry.grid(row=7, column=1, padx=10, pady=5)

            self.submit_button = tk.Button(add_window, text="Submit",
                                           command=lambda: self.submit_add(name_entry.get(), state_entry.get(),
                                                                           type_entry.get(), services_entry.get(),
                                                                           address_entry.get(), ad_num_entry.get(),
                                                                           ch_num_entry.get(), p_num_entry.get(),
                                                                           add_window))
            self.submit_button.grid(row=8, column=1, padx=10, pady=5)

        def button_click_filter(self):
            filt_window = tk.Toplevel()
            filt_window.title("Filter Items")

            adults_label = tk.Label(filt_window, text="Number of adults:")
            adults_label.grid(row=0, column=0, padx=10, pady=5)
            adults_entry = tk.Entry(filt_window)
            adults_entry.grid(row=0, column=1, padx=10, pady=5)

            children_label = tk.Label(filt_window, text="Number of children:")
            children_label.grid(row=1, column=0, padx=10, pady=5)
            children_entry = tk.Entry(filt_window)
            children_entry.grid(row=1, column=1, padx=10, pady=5)

            pets_label = tk.Label(filt_window, text="Number of pets:")
            pets_label.grid(row=2, column=0, padx=10, pady=5)
            pets_entry = tk.Entry(filt_window)
            pets_entry.grid(row=2, column=1, padx=10, pady=5)

            state_label = tk.Label(filt_window, text="Choose state:")
            state_label.grid(row=3, column=0, padx=10, pady=5)
            state_entry = tk.Entry(filt_window)
            state_entry.grid(row=3, column=1, padx=10, pady=5)

            type_label = tk.Label(filt_window, text="Choose type:")
            type_label.grid(row=4, column=0, padx=10, pady=5)
            type_entry = tk.Entry(filt_window)
            type_entry.grid(row=4, column=1, padx=10, pady=5)

            self.submit_button = tk.Button(filt_window, text="Submit",
                                           command=lambda: self.submit_filt(adults_entry.get(), children_entry.get(),
                                                                            pets_entry.get(), state_entry.get(),
                                                                            type_entry.get(), filt_window))
            self.submit_button.grid(row=5, column=1, padx=10, pady=5)

        def button_click_clear_filter(self):
            self.acomodation_inst.clear_filter()
            self.table_update()

        def button_click_sorting(self):
            sort_win = tk.Toplevel()
            sort_win.title("Sort item")

            table_label = tk.Label(sort_win, text='Choose table')
            table_label.grid(row=0, column=0, padx=10, pady=5)

            table_entry = tk.StringVar(sort_win)
            table_entry.set("hotels_evidence")
            table_menu = tk.OptionMenu(sort_win, table_entry, "hotels_evidence", "hotel_availability")
            table_menu.grid(row=0, column=1)

            column_label = tk.Label(sort_win, text='Choose column')
            column_label.grid(row=1, column=0, padx=10, pady=5)
            column_entry = tk.StringVar(sort_win)
            column_entry.set("state")
            column_menu = tk.OptionMenu(sort_win, column_entry, "id", "name", "state", "services", "availability",
                                        "free_places_for_adults", "free_places_for_children", "free_places_for_pets")
            column_menu.grid(row=1, column=1)

            order_label = tk.Label(sort_win, text='Choose order')
            order_label.grid(row=2, column=0, padx=10, pady=5)

            order_entry = tk.StringVar(sort_win)
            order_entry.set("ASC")
            order_menu = tk.OptionMenu(sort_win, order_entry, "ASC", "DESC")
            order_menu.grid(row=2, column=1)

            self.submit_button = tk.Button(sort_win, text="Submit",
                                           command=lambda: self.submit_sort(table_entry.get(), column_entry.get(),
                                                                            order_entry.get(), sort_win))
            self.submit_button.grid(row=3, column=1, padx=10, pady=5)

            self.unsort_button = tk.Button(sort_win, text="Unsort",
                                           command=lambda: self.submit_unsort(sort_win))
            self.unsort_button.grid(row=3, column=2, padx=10, pady=5)

        def submit_add(self, name_entry, state_entry, type_entry, services_entry, address_entry, ad_num_entry,
                       ch_num_entry, p_num_entry, window):
            self.acomodation_inst.add_item(name_entry, state_entry, type_entry, services_entry, address_entry,
                                           ad_num_entry, ch_num_entry, p_num_entry, )
            window.destroy()
            self.table_update()

        def submit_remove(self, id_entry, window):
            self.acomodation_inst.remove_item(id_entry)
            window.destroy()
            self.table_update()

        def submit_filt(self, adults_entry, children_entry, pets_entry, state_entry, type_entry, window):
            self.acomodation_inst.filter(adults_entry, children_entry, pets_entry, state_entry, type_entry)
            window.destroy()
            self.table_update('availability')

        def submit_sort(self, table, column, order, window):
            if table == 'hotel_availability':
                table2 = 'hotels_evidence'
            else:
                table2 = 'hotel_availability'
            column_names, rows, column_names2, rows2 = self.acomodation_inst.sort_table(table, table2, column, order)
            window.destroy()
            self.text_widget.destroy()
            if table == 'hotels_evidence':
                self.display_table(column_names, rows, column_names2, rows2)
            else:
                self.display_table(column_names2, rows2, column_names, rows)

        def submit_unsort(self, window):
            self.table_update()
            window.destroy()

    def __init__(self, database='hotels.db', load_new=None, table1_load=None, table2_load=None):
        if load_new is None:
            self.DB = sqlite3.connect(database)
            self.CUR = self.DB.cursor()
            self.DB.commit()
        elif load_new is not None:
            self.DB = sqlite3.connect(database)
            self.CUR = self.DB.cursor()

            self.CUR.execute("DELETE FROM hotels_evidence")
            with open(table1_load, 'r') as file:
                data = file.readlines()

            add = []
            for row in data:
                row = row.strip("()")
                row = row.strip("\n")
                row = row.split(',')
                for i in range(len(row)):
                    if i == (len(row) - 1):
                        row[i] = row[i][2:-2]
                    elif i == 0:
                        row[i] = row[i][1:-1]
                    else:
                        row[i] = row[i][2:-1]
                add.append(row)

            self.CUR.execute("DELETE FROM hotel_availability")
            with open(table2_load, 'r') as file:
                data = file.readlines()

            add2 = []
            for row in data:
                row = row.strip("()")
                row = row.strip("\n")
                row = row.split(',')
                for i in range(len(row)):
                    if i == (len(row) - 1):
                        row[i] = row[i][1:-1]
                    elif i == 0:
                        row[i] = row[i][1:-1]
                    else:
                        row[i] = row[i][1:]
                add2.append(row)

            for i in range(len(add)):
                self.add_item(str(add[i][0]), str(add[i][1]), str(add[i][2]), str(add[i][3]), str(add[i][4]),
                              add2[i][1], add2[i][2], add2[i][3])

            self.DB.commit()

    def add_item(self, name='not_given', state='not_given', type='not_given', services='not_given', address='not_given',
                 adults='not_given', children='not_given', pets='not_given', availability='-'):
        self.CUR.execute(
            "INSERT INTO hotels_evidence (name, state, type, services, address, availability) VALUES (?, ?, ?, ?, ?, ?)",
            (name, state, type, services, address, availability))
        self.CUR.execute(
            "INSERT INTO hotel_availability (name, free_places_for_adults, free_places_for_children, free_places_for_pets) VALUES (?, ?, ?, ?)",
            (name, int(adults), int(children), int(pets)))

        item_id = self.CUR.lastrowid
        self.DB.commit()
        print("Item with ID", item_id, "added successfully")

    def remove_item(self, item_id):
        self.CUR.execute("DELETE FROM hotels_evidence WHERE id=?", (item_id,))
        self.CUR.execute("DELETE FROM hotel_availability WHERE id=?", (item_id,))
        self.DB.commit()
        print("Item with ID", item_id, "removed successfully")

    def sort_table(self, table, table2, column, order='ASC'):
        column_names1 = []
        self.CUR.execute(f"PRAGMA table_info({table})")
        for columnv in self.CUR.fetchall():
            column_names1.append(columnv[1])

        self.CUR.execute(f"SELECT * FROM {table} ORDER BY {column} {order}")
        result = self.CUR.fetchall()

        column_names2 = []
        self.CUR.execute(f"PRAGMA table_info({table2})")
        for columnv in self.CUR.fetchall():
            column_names2.append(columnv[1])

        self.CUR.execute(f"SELECT * FROM {table2}")
        rows2 = self.CUR.fetchall()

        return column_names1, result, column_names2, rows2

    def filter(self, num_a, num_ch, num_p, st, ty):
        self.CUR.execute(
            "SELECT id, free_places_for_adults, free_places_for_children, free_places_for_pets FROM hotel_availability")
        result = self.CUR.fetchall()
        self.CUR.execute("SELECT state, type FROM hotels_evidence")
        result2 = self.CUR.fetchall()
        for i in range(len(result)):
            if ((len(num_a) != 0 and int(result[i][1]) >= int(num_a)) or (len(num_a) == 0)) and (
                    (len(num_ch) != 0 and int(result[i][2]) >= int(num_ch)) or (len(num_ch) == 0)) and (
                    (len(num_p) != 0 and int(result[i][3]) >= int(num_p)) or (len(num_p) == 0)) and (
                    (len(st) != 0 and result2[i][0] == st) or (len(st) == 0)) and (
                    (len(ty) != 0 and result2[i][1] == ty) or (len(ty) == 0)):
                self.assignment(result[i][0], 'available')
            else:
                self.assignment(result[i][0], 'unavailable')

    def clear_filter(self):
        self.CUR.execute("SELECT * FROM hotel_availability")
        result = self.CUR.fetchall()

        for row in result:
            self.assignment(row[0], '-')

    def filtered_table(self):
        column_names = []
        self.CUR.execute(f"PRAGMA table_info('hotels_evidence')")
        for column in self.CUR.fetchall():
            column_names.append(column[1])

        self.CUR.execute(f"SELECT * FROM hotels_evidence WHERE availability = 'available'")
        rows = self.CUR.fetchall()

        column_names2 = []
        self.CUR.execute(f"PRAGMA table_info('hotel_availability')")
        for column in self.CUR.fetchall():
            column_names2.append(column[1])

        self.CUR.execute(f"SELECT * FROM hotel_availability")
        rows2 = self.CUR.fetchall()

        return column_names, rows, column_names2, rows2

    def assignment(self, id, result):
        self.CUR.execute('UPDATE hotels_evidence SET availability = ? WHERE id = ?', (str(result), str(id)))

        self.DB.commit()

    def assign(self, table, id, column, result):
        self.CUR.execute(f'UPDATE {table} SET {column} = ? WHERE id = ?', (result, str(id)))

        self.DB.commit()

    def interactive_table(self):
        x, y, x2, y2 = self.interactive_table_get()
        root = tk.Tk()
        self.Table(root, x, y, x2, y2, self)
        root.mainloop()

    def interactive_table_get(self):
        column_names = []
        self.CUR.execute(f"PRAGMA table_info('hotels_evidence')")
        for column in self.CUR.fetchall():
            column_names.append(column[1])

        self.CUR.execute(f"SELECT * FROM hotels_evidence")
        rows = self.CUR.fetchall()

        column_names2 = []
        self.CUR.execute(f"PRAGMA table_info('hotel_availability')")
        for column in self.CUR.fetchall():
            column_names2.append(column[1])

        self.CUR.execute(f"SELECT * FROM hotel_availability")
        rows2 = self.CUR.fetchall()

        return column_names, rows, column_names2, rows2

    def vypis(self):
        self.CUR.execute('SELECT * FROM hotel_availability')
        table2_rows = self.CUR.fetchall()
        print("Obsah druhej tabuľky:")
        for row in table2_rows:
            print(row)
        self.CUR.execute('SELECT * FROM hotels_evidence')
        table2_rows = self.CUR.fetchall()
        print("Obsah prvej tabuľky:")
        for row in table2_rows:
            print(row)

    def save_to_file(self, table1, table2):
        self.CUR.execute("SELECT * FROM hotels_evidence")
        data = self.CUR.fetchall()

        with open(table1, 'w') as file:
            for row in data:
                file.write(str(row[1:-1]) + "\n")

        self.CUR.execute("SELECT * FROM hotel_availability")
        data = self.CUR.fetchall()

        with open(table2, 'w') as file:
            for row in data:
                file.write(str(row[1:]) + "\n")


database = Acomodation('hotels.db') #, True, 'table1.txt', 'table2.txt')  # if you want to read your own new tables use syntax Acomodation('hotels.db', True, 'first_table', 'second_table') #, True, 'table1.txt', 'table2.txt'
# database.add_item('Hotel Krásna Hôrka', 'Slovakia', 'hotel', 'pool/breakfast', 'Krásna hôrka 48', '15', '4', '10')        # adding item example
# database.assign('hotels_evidence', '123', 'state', 'France')        # modify item example
# database.remove_item(1)                                           # remove item example, param = id
database.interactive_table()  # turn on interface for work with tables
# database.save_to_file('table1.txt', 'table2.txt')                 # Use this for saving table to your txt files
