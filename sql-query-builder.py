import tkinter as tk
from tkinter import ttk, messagebox

class SQLQueryBuilderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Query Builder")

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Query Type
        self.query_type_label = ttk.Label(self.main_frame, text="Select Query Type:")
        self.query_type_label.grid(row=0, column=0, sticky=tk.W)

        self.query_type = tk.StringVar()
        self.query_type_combobox = ttk.Combobox(self.main_frame, textvariable=self.query_type, values=["SELECT", "INSERT", "UPDATE", "DELETE"])
        self.query_type_combobox.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Table Name Input
        self.table_name_label = ttk.Label(self.main_frame, text="Table Name:")
        self.table_name_label.grid(row=1, column=0, sticky=tk.W)

        self.table_name_entry = ttk.Entry(self.main_frame)
        self.table_name_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Field Inputs
        self.fields_label = ttk.Label(self.main_frame, text="Fields (comma-separated):")
        self.fields_label.grid(row=2, column=0, sticky=tk.W)

        self.fields_entry = ttk.Entry(self.main_frame)
        self.fields_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

        # Aliases Input (Optional)
        self.aliases_label = ttk.Label(self.main_frame, text="Field Aliases (comma-separated, e.g. id AS author_id):")
        self.aliases_label.grid(row=3, column=0, sticky=tk.W)

        self.aliases_entry = ttk.Entry(self.main_frame)
        self.aliases_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

        # Condition Inputs (Optional)
        self.conditions_label = ttk.Label(self.main_frame, text="Conditions (Optional, WHERE):")
        self.conditions_label.grid(row=4, column=0, sticky=tk.W)

        self.conditions_entry = ttk.Entry(self.main_frame)
        self.conditions_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

        # Values Input (For INSERT/UPDATE)
        self.values_label = ttk.Label(self.main_frame, text="Values (For INSERT/UPDATE):")
        self.values_label.grid(row=5, column=0, sticky=tk.W)

        self.values_entry = ttk.Entry(self.main_frame)
        self.values_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

        # Sorting Inputs (For SELECT)
        self.sort_by_label = ttk.Label(self.main_frame, text="Sort By (For SELECT):")
        self.sort_by_label.grid(row=6, column=0, sticky=tk.W)

        self.sort_by_entry = ttk.Entry(self.main_frame)
        self.sort_by_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))

        self.sort_order_label = ttk.Label(self.main_frame, text="Sort Order (ASC/DESC):")
        self.sort_order_label.grid(row=7, column=0, sticky=tk.W)

        self.sort_order = tk.StringVar()
        self.sort_order_combobox = ttk.Combobox(self.main_frame, textvariable=self.sort_order, values=["ASC", "DESC"])
        self.sort_order_combobox.grid(row=7, column=1, sticky=(tk.W, tk.E))

        # Remove Duplicates Checkbox
        self.remove_duplicates = tk.BooleanVar()
        self.remove_duplicates_check = ttk.Checkbutton(self.main_frame, text="Remove Duplicates (DISTINCT)", variable=self.remove_duplicates)
        self.remove_duplicates_check.grid(row=8, column=0, columnspan=2, sticky=tk.W)

        # Generate Query Button
        self.generate_button = ttk.Button(self.main_frame, text="Generate SQL Query", command=self.generate_query)
        self.generate_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Query Display
        self.query_label = ttk.Label(self.main_frame, text="Generated SQL Query:")
        self.query_label.grid(row=10, column=0, sticky=tk.W)

        self.query_display = tk.Text(self.main_frame, height=5, width=50)
        self.query_display.grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Copy Button
        self.copy_button = ttk.Button(self.main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=12, column=0, columnspan=2, pady=10)

    def generate_query(self):
        query_type = self.query_type.get().upper()
        table_name = self.table_name_entry.get().strip()
        fields = self.fields_entry.get().strip()
        aliases = self.aliases_entry.get().strip()
        conditions = self.conditions_entry.get().strip()
        values = self.values_entry.get().strip()
        sort_by = self.sort_by_entry.get().strip()
        sort_order = self.sort_order.get().upper()
        distinct = self.remove_duplicates.get()

        if not table_name:
            messagebox.showerror("Error", "Table name is required!")
            return

        query = ""
        if query_type == "SELECT":
            if not fields:
                messagebox.showerror("Error", "Fields are required for SELECT queries!")
                return

            # Combine fields and aliases
            fields_list = fields.split(",")
            aliases_list = aliases.split(",") if aliases else []
            combined_fields = []

            # Merge fields with aliases
            for idx, field in enumerate(fields_list):
                field = field.strip()
                alias = aliases_list[idx].strip() if idx < len(aliases_list) and aliases_list[idx] else None
                combined_fields.append(f"{field} AS {alias}" if alias else field)

            distinct_clause = "DISTINCT " if distinct else ""
            query = f"SELECT {distinct_clause}{', '.join(combined_fields)} FROM {table_name}"

            if conditions:
                query += f" WHERE {conditions}"
            if sort_by:
                order = "ASC" if sort_order == "" else sort_order
                query += f" ORDER BY {sort_by} {order}"
        elif query_type == "INSERT":
            if not fields or not values:
                messagebox.showerror("Error", "Fields and Values are required for INSERT queries!")
                return
            query = f"INSERT INTO {table_name} ({fields}) VALUES ({values})"
        elif query_type == "UPDATE":
            if not fields or not values:
                messagebox.showerror("Error", "Fields and Values are required for UPDATE queries!")
                return
            query = f"UPDATE {table_name} SET {fields} = {values}"
            if conditions:
                query += f" WHERE {conditions}"
        elif query_type == "DELETE":
            query = f"DELETE FROM {table_name}"
            if conditions:
                query += f" WHERE {conditions}"
        else:
            messagebox.showerror("Error", "Please select a valid query type!")
            return

        # Display the generated query
        self.query_display.delete(1.0, tk.END)
        self.query_display.insert(tk.END, query)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.query_display.get(1.0, tk.END).strip())
        messagebox.showinfo("Copied", "SQL query copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLQueryBuilderApp(root)
    root.mainloop()
