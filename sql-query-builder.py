import tkinter as tk
from tkinter import ttk, messagebox

class SQLQueryBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Query Builder")

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Table Name Input
        self.table_name_label = ttk.Label(self.main_frame, text="Table Name:")
        self.table_name_label.grid(row=0, column=0, sticky=tk.W)

        self.table_name_entry = ttk.Entry(self.main_frame)
        self.table_name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

        # Fields and Data Types
        self.fields_label = ttk.Label(self.main_frame, text="Fields and Data Types (comma-separated, e.g. name TEXT, age INT):")
        self.fields_label.grid(row=1, column=0, sticky=tk.W)

        self.fields_entry = ttk.Entry(self.main_frame)
        self.fields_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Filters Section (will dynamically populate based on fields)
        self.filters_frame = ttk.LabelFrame(self.main_frame, text="Filters (Optional)")
        self.filters_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Add Filters Button (to populate filters dropdowns based on input fields)
        self.add_filters_button = ttk.Button(self.main_frame, text="Add Filters", command=self.create_filters)
        self.add_filters_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Remove Duplicates Checkbox
        self.remove_duplicates = tk.BooleanVar()
        self.remove_duplicates_check = ttk.Checkbutton(self.main_frame, text="Remove Duplicates (DISTINCT)", variable=self.remove_duplicates)
        self.remove_duplicates_check.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Aliases Section
        self.aliases_label = ttk.Label(self.main_frame, text="Field Aliases (Return Field As, comma-separated, e.g. id AS user_id):")
        self.aliases_label.grid(row=5, column=0, sticky=tk.W)

        self.aliases_entry = ttk.Entry(self.main_frame)
        self.aliases_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

        # Generate Query Button
        self.generate_button = ttk.Button(self.main_frame, text="Generate SQL Query", command=self.generate_query)
        self.generate_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Query Display
        self.query_label = ttk.Label(self.main_frame, text="Generated SQL Query:")
        self.query_label.grid(row=7, column=0, sticky=tk.W)

        self.query_display = tk.Text(self.main_frame, height=5, width=50)
        self.query_display.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E))

        # Copy Button
        self.copy_button = ttk.Button(self.main_frame, text="Copy to Clipboard", command=self.copy_to_clipboard)
        self.copy_button.grid(row=9, column=0, columnspan=2, pady=10)

        # Placeholder for dynamically created filters
        self.filter_widgets = []

    def create_filters(self):
        # Clear any existing filters
        for widget in self.filter_widgets:
            widget.grid_forget()

        self.filter_widgets.clear()

        # Get the field and data type input
        fields_input = self.fields_entry.get().strip()
        if not fields_input:
            messagebox.showerror("Error", "Fields and Data Types are required!")
            return

        # Parse the fields and data types (comma-separated)
        fields = [field.strip().split()[0] for field in fields_input.split(',')]

        # Create dropdowns for each field for filtering
        operators = ["=", ">", "<", ">=", "<=", "!="]
        for idx, field in enumerate(fields):
            field_label = ttk.Label(self.filters_frame, text=field)
            field_label.grid(row=idx, column=0, sticky=tk.W)
            self.filter_widgets.append(field_label)

            operator_combobox = ttk.Combobox(self.filters_frame, values=operators)
            operator_combobox.grid(row=idx, column=1, sticky=(tk.W, tk.E))
            self.filter_widgets.append(operator_combobox)

            value_entry = ttk.Entry(self.filters_frame)
            value_entry.grid(row=idx, column=2, sticky=(tk.W, tk.E))
            self.filter_widgets.append(value_entry)

    def generate_query(self):
        table_name = self.table_name_entry.get().strip()
        fields_input = self.fields_entry.get().strip()
        aliases_input = self.aliases_entry.get().strip()
        distinct = self.remove_duplicates.get()

        if not table_name or not fields_input:
            messagebox.showerror("Error", "Table name and Fields are required!")
            return

        # Build the SELECT query
        fields = [field.strip().split()[0] for field in fields_input.split(',')]
        combined_fields = fields

        # If aliases are provided, apply them to fields
        if aliases_input:
            aliases = [alias.strip() for alias in aliases_input.split(',')]
            combined_fields = [f"{field} AS {alias}" if alias else field for field, alias in zip(fields, aliases)]

        distinct_clause = "DISTINCT " if distinct else ""
        query = f"SELECT {distinct_clause}{', '.join(combined_fields)} FROM {table_name}"

        # Add filtering conditions if any filters were provided
        filters = []
        for i in range(0, len(self.filter_widgets), 3):
            field = self.filter_widgets[i].cget("text")
            operator = self.filter_widgets[i + 1].get()
            value = self.filter_widgets[i + 2].get().strip()

            if operator and value:
                # If the value looks like a number, don't wrap it in quotes; otherwise, treat it as a string
                if value.replace('.', '', 1).isdigit():
                    filters.append(f"{field} {operator} {value}")
                else:
                    filters.append(f"{field} {operator} '{value}'")

        if filters:
            query += " WHERE " + " AND ".join(filters)

        # Display the generated query
        self.query_display.delete(1.0, tk.END)
        self.query_display.insert(tk.END, query)

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.query_display.get(1.0, tk.END).strip())
        messagebox.showinfo("Copied", "SQL query copied to clipboard!")


if __name__ == "__main__":
    root = tk.Tk()
    app = SQLQueryBuilder(root)
    root.mainloop()
