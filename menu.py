from tkinter import Tk, Label, Button, Frame, BOTH, Entry, Text, END, font
from CubicEquation import CubicEquation
from matrix import Matrix  # Import your Matrix class
from EigenSolver import get_eigenvectors, get_char_polynomial_coefs  # Import functions for eigenvalue calculations

class MatrixOperations:
    def __init__(self):
        self.result_text = None

    def compute_sum(self, matrix_a, matrix_b):
        return matrix_a.add(matrix_b)

    def add_matrices(self):
        self.create_input_window("Add Matrices", self.display_sum, dual_matrices=True)

    def display_sum(self):
        matrix_a = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        matrix_b = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_b_entries])
        sum_matrix = self.compute_sum(matrix_a, matrix_b)

        result = "Sum of Matrices:\n" + '\n'.join([' '.join(map(str, row)) for row in sum_matrix.data])
        self.display_result(result)

    # Helper method to display results
    def display_result(self, result):
        if self.result_text:
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, result + "\n")
    
    def inverse_matrix(self):
        self.create_input_window("Inverse Matrix", self.display_inverse)

    def display_inverse(self):
        matrix = Matrix([[float(entry.get()) for entry in self.inverse_matrix_entries]])
        try:
            inverse_matrix = matrix.inverse()
            result = "Inverse of Matrix:\n" + '\n'.join([' '.join(map(str, row)) for row in inverse_matrix.data])
            self.display_result(result)
        except ValueError:
            self.display_result("Error: Matrix is singular and cannot be inverted.")

    def multiply_matrices(self):
        self.create_input_window("Multiply Matrices", self.display_product, dual_matrices=True)
    
    def display_product(self):
        matrix_a = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        matrix_b = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_b_entries])
        product_matrix = matrix_a.multiply(matrix_b)

        result = "Product of Matrices:\n" + '\n'.join([' '.join(map(str, row)) for row in product_matrix.data])
        self.display_result(result)

    # Transpose Matrix
    def transpose_matrix(self):
        self.create_input_window("Transpose Matrix", self.display_transpose)

    def display_transpose(self):
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        transposed_matrix = matrix.transpose()
        result = "Transpose of Matrix:\n" + '\n'.join([' '.join(map(str, row)) for row in transposed_matrix.data])
        self.display_result(result)

    # Trace of Matrix
    def trace_matrix(self):
        self.create_input_window("Trace Matrix", self.display_trace)

    def display_trace(self):
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        trace_value = matrix.trace()
        result = f"Trace of Matrix: {trace_value}"
        self.display_result(result)

    # Determinant of Matrix
    def determinant_matrix(self):
        self.create_input_window("Determinant of Matrix", self.display_determinant)

    def display_determinant(self):
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        determinant_value = matrix.determinant()
        result = f"Determinant of Matrix: {determinant_value}"
        self.display_result(result)

    # Minor Matrix
    def minor_matrix(self):
        self.create_input_window("Minor Matrix", self.display_minor)

    def display_minor(self):
        row = int(self.row_entry.get()) - 1  # row index to remove
        col = int(self.col_entry.get()) - 1  # col index to remove
        matrix = Matrix([[float(entry.get()) for entry in row_entries] for row_entries in self.matrix_a_entries])
        minor_matrix = matrix.minor(row, col)
        result = "Minor Matrix:\n" + '\n'.join([' '.join(map(str, row)) for row in minor_matrix.data])
        self.display_result(result)

    # Cofactor Matrix
    def cofactor_matrix(self):
        self.create_input_window("Cofactor Matrix", self.display_cofactor)

    def display_cofactor(self):
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        cofactor_matrix = matrix.cofactor_matrix()
        result = "Cofactor Matrix:\n" + '\n'.join([' '.join(map(str, row)) for row in cofactor_matrix.data])
        self.display_result(result)

    # Scalar Multiply
    def scalar_multiply(self):
        self.create_input_window("Scalar Multiply", self.display_scalar_multiply)

    def display_scalar_multiply(self):
        scalar = float(self.scalar_entry.get())
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.matrix_a_entries])
        result_matrix = matrix.scalar_multiply(scalar)
        result = f"Matrix multiplied by {scalar}:\n" + '\n'.join([' '.join(map(str, row)) for row in result_matrix.data])
        self.display_result(result)


    # Adding operations for previously requested features:
    def eigenvalues_vectors(self):
        self.create_input_window("Eigenvalues & Eigenvectors", self.display_eigen)

    def display_eigen(self):
        matrix = Matrix([[float(entry.get()) for entry in row] for row in self.eigen_matrix_entries])
        c3, c2, c1, c0 = get_char_polynomial_coefs(matrix)
        eigenvalues = CubicEquation(c3, c2, c1, c0)
        eigenvectors = get_eigenvectors(matrix, eigenvalues)

        result = "Eigenvalues:\n" + ' '.join(map(str, eigenvalues)) + "\nEigenvectors:\n"
        for vector in eigenvectors:
            result += ' '.join(map(str, vector)) + "\n"
        self.display_result(result)

    def create_input_window(self, title, operation_callback, dual_matrices=False):
        self.gui_input = Tk()
        self.gui_input.title(title)
        self.gui_input.geometry("400x400" if not dual_matrices else "600x400")
        self.gui_input.resizable(False, False)
        self.gui_input.configure(bg="#f5f5f5")  # Light background color

        self.frame_input = Frame(self.gui_input, bg="#f5f5f5")
        self.frame_input.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Title with a larger font
        Label(self.frame_input, text=title, font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#333").grid(row=0, column=0, columnspan=3, pady=10)

        # Matrix A Entries
        Label(self.frame_input, text="Matrix A (3x3)", font=("Helvetica", 12), bg="#f5f5f5").grid(row=1, column=0, padx=5)
        self.matrix_a_entries = []
        for i in range(3):
            row_entries = []
            for j in range(3):
                entry = Entry(self.frame_input, width=5, font=("Helvetica", 12), bd=2)
                entry.grid(row=i + 2, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.matrix_a_entries.append(row_entries)

        # Matrix B (optional for dual matrices like addition and multiplication)
        if dual_matrices:
            Label(self.frame_input, text="Matrix B (3x3)", font=("Helvetica", 12), bg="#f5f5f5").grid(row=1, column=3, padx=5)
            self.matrix_b_entries = []
            for i in range(3):
                row_entries = []
                for j in range(3):
                    entry = Entry(self.frame_input, width=5, font=("Helvetica", 12), bd=2)
                    entry.grid(row=i + 2, column=j + 3, padx=5, pady=5)
                    row_entries.append(entry)
                self.matrix_b_entries.append(row_entries)

        # Results section
        Label(self.frame_input, text="Results:", font=("Helvetica", 12, "bold"), bg="#f5f5f5").grid(row=6, column=0, columnspan=4, pady=10)
        self.result_text = Text(self.frame_input, height=8, width=40, font=("Helvetica", 12), bg="#e8f4f8", fg="#333")
        self.result_text.grid(row=7, column=0, columnspan=6, pady=5)

        # Compute Button
        Button(self.frame_input, text="Compute", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5, command=operation_callback).grid(row=8, column=2, pady=10)

class Menu:
    def __init__(self):
        # Main window setup
        gui_menu = Tk()
        gui_menu.title('Matrix Operations Menu')
        gui_menu.geometry('400x650')
        gui_menu.resizable(False, False)
        
        # Set a game-like background color
        gui_menu.configure(bg="#2E3440")  # Dark background like in games

        # Frame for menu content
        frame_menu = Frame(gui_menu, bg="#2E3440")
        frame_menu.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Title label with game-like font and color
        title_font = font.Font(family="Verdana", size=20, weight="bold")
        Label(frame_menu, text="Matrix Operations", font=title_font, bg="#2E3440", fg="#8FBCBB").pack(pady=20)

        operations = MatrixOperations()

        # Custom button styling for a "game-like" feel
        button_font = font.Font(family="Verdana", size=12, weight="bold")
        button_style = {
            "bg": "#88C0D0", "fg": "#2E3440", "activebackground": "#5E81AC", 
            "font": button_font, "relief": "raised", "bd": 5, "width": 20, "height": 1
        }

        # Game-style Buttons
        Button(frame_menu, text="Add Matrices", **button_style, command=operations.add_matrices).pack(pady=10)
        Button(frame_menu, text="Inverse Matrix", **button_style, command=operations.inverse_matrix).pack(pady=10)
        Button(frame_menu, text="Multiply Matrices", **button_style, command=operations.multiply_matrices).pack(pady=10)
        Button(frame_menu, text="Transpose Matrix", **button_style, command=operations.transpose_matrix).pack(pady=10)
        Button(frame_menu, text="Trace Matrix", **button_style, command=operations.trace_matrix).pack(pady=10)
        Button(frame_menu, text="Determinant", **button_style, command=operations.determinant_matrix).pack(pady=10)
        Button(frame_menu, text="Minor Matrix", **button_style, command=operations.minor_matrix).pack(pady=10)
        Button(frame_menu, text="Cofactor Matrix", **button_style, command=operations.cofactor_matrix).pack(pady=10)
        Button(frame_menu, text="Scalar Multiply", **button_style, command=operations.scalar_multiply).pack(pady=10)
        Button(frame_menu, text="Eigenvalues & Vectors", **button_style, command=operations.eigenvalues_vectors).pack(pady=10)

        gui_menu.mainloop()

if __name__ == "__main__":
    Menu()
