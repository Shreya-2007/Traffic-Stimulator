import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon


class WirelessSimulator:

    def __init__(self, root):

        self.root = root
        self.root.title(
            "Traffic-Aware Wireless Network Simulator"
        )
        self.root.geometry("1250x800")

        self.create_gui()

    # =========================================================
    # GUI
    # =========================================================

    def create_gui(self):

        # ---------------- TITLE ----------------

        title = tk.Label(
            self.root,
            text="TRAFFIC-AWARE WIRELESS NETWORK SIMULATOR",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(12, 3))

        subtitle = tk.Label(
            self.root,
            text="Dynamic Channel Allocation in Cellular Networks",
            font=("Arial", 11)
        )
        subtitle.pack()

        # ---------------- MAIN FRAME ----------------

        main_frame = tk.Frame(self.root)

        main_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # =====================================================
        # LEFT CONTROL PANEL
        # =====================================================

        control_frame = tk.LabelFrame(
            main_frame,
            text="Network Configuration",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )

        control_frame.pack(
            side="left",
            fill="y",
            padx=(0, 10)
        )

        # ---------------- CELLS ----------------

        tk.Label(
            control_frame,
            text="Number of Cells:"
        ).pack(anchor="w")

        self.cells_var = tk.IntVar(value=7)

        tk.Spinbox(
            control_frame,
            from_=3,
            to=7,
            textvariable=self.cells_var,
            width=15
        ).pack(
            anchor="w",
            pady=(2, 12)
        )

        # ---------------- USERS ----------------

        tk.Label(
            control_frame,
            text="Total Users:"
        ).pack(anchor="w")

        self.users_var = tk.IntVar(value=70)

        tk.Spinbox(
            control_frame,
            from_=7,
            to=200,
            textvariable=self.users_var,
            width=15
        ).pack(
            anchor="w",
            pady=(2, 12)
        )

        # ---------------- CHANNELS ----------------

        tk.Label(
            control_frame,
            text="Channels per Cell:"
        ).pack(anchor="w")

        self.channels_var = tk.IntVar(value=10)

        tk.Spinbox(
            control_frame,
            from_=1,
            to=50,
            textvariable=self.channels_var,
            width=15
        ).pack(
            anchor="w",
            pady=(2, 12)
        )

        # ---------------- TRAFFIC ----------------

        tk.Label(
            control_frame,
            text="Traffic Level:"
        ).pack(anchor="w")

        self.traffic_var = tk.StringVar(
            value="Medium"
        )

        ttk.Combobox(
            control_frame,
            textvariable=self.traffic_var,
            values=[
                "Low",
                "Medium",
                "High"
            ],
            state="readonly",
            width=13
        ).pack(
            anchor="w",
            pady=(2, 20)
        )

        # =====================================================
        # BUTTONS
        # =====================================================

        tk.Button(
            control_frame,
            text="START SIMULATION",
            command=self.start_simulation,
            width=18,
            pady=8
        ).pack(pady=5)

        tk.Button(
            control_frame,
            text="RESET",
            command=self.reset_simulation,
            width=18,
            pady=8
        ).pack(pady=5)

        # =====================================================
        # NETWORK STATISTICS
        # =====================================================

        stats_frame = tk.LabelFrame(
            control_frame,
            text="Network Statistics",
            font=("Arial", 10, "bold"),
            padx=10,
            pady=10
        )

        stats_frame.pack(
            fill="x",
            pady=15
        )

        self.active_users_label = tk.Label(
            stats_frame,
            text="Active Users: 0"
        )
        self.active_users_label.pack(
            anchor="w",
            pady=3
        )

        self.assigned_label = tk.Label(
            stats_frame,
            text="Allocated Channels: 0"
        )
        self.assigned_label.pack(
            anchor="w",
            pady=3
        )

        self.borrowed_label = tk.Label(
            stats_frame,
            text="Borrowed Channels: 0"
        )
        self.borrowed_label.pack(
            anchor="w",
            pady=3
        )

        self.blocked_label = tk.Label(
            stats_frame,
            text="Blocked Requests: 0"
        )
        self.blocked_label.pack(
            anchor="w",
            pady=3
        )

        self.utilization_label = tk.Label(
            stats_frame,
            text="Network Utilization: 0%"
        )
        self.utilization_label.pack(
            anchor="w",
            pady=3
        )

        self.interference_label = tk.Label(
            stats_frame,
            text="Interference: LOW",
            font=("Arial", 10, "bold")
        )
        self.interference_label.pack(
            anchor="w",
            pady=3
        )

        # =====================================================
        # CELL DETAILS
        # =====================================================

        cell_frame = tk.LabelFrame(
            control_frame,
            text="Cell Details",
            font=("Arial", 10, "bold")
        )

        cell_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "Cell",
            "Users",
            "Own",
            "Borrowed",
            "Allocated",
            "Blocked",
            "Load",
            "Status"
        )

        self.cell_table = ttk.Treeview(
            cell_frame,
            columns=columns,
            show="headings",
            height=8
        )

        headings = {
            "Cell": "Cell",
            "Users": "Users",
            "Own": "Own",
            "Borrowed": "Borrowed",
            "Allocated": "Allocated",
            "Blocked": "Blocked",
            "Load": "Load",
            "Status": "Status"
        }

        for column in columns:

            self.cell_table.heading(
                column,
                text=headings[column]
            )

        widths = {
            "Cell": 45,
            "Users": 45,
            "Own": 45,
            "Borrowed": 65,
            "Allocated": 65,
            "Blocked": 55,
            "Load": 55,
            "Status": 75
        }

        for column in columns:

            self.cell_table.column(
                column,
                width=widths[column]
            )

        self.cell_table.pack(
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # =====================================================
        # RIGHT VISUALIZATION
        # =====================================================

        graph_frame = tk.LabelFrame(
            main_frame,
            text="Cellular Network Visualization",
            font=("Arial", 11, "bold")
        )

        graph_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.figure, self.ax = plt.subplots(
            figsize=(7, 6)
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=graph_frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.draw_network()

    # =========================================================
    # SIMULATION
    # =========================================================

    def start_simulation(self):

        try:

            cells = int(
                self.cells_var.get()
            )

            total_users = int(
                self.users_var.get()
            )

            channels_per_cell = int(
                self.channels_var.get()
            )

            if cells < 3 or cells > 7:
                raise ValueError

            if total_users < cells:
                raise ValueError

            if channels_per_cell < 1:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid network parameters."
            )

            return

        # =====================================================
        # TRAFFIC FACTOR
        # =====================================================

        traffic = self.traffic_var.get()

        if traffic == "Low":

            factor = 0.55

        elif traffic == "Medium":

            factor = 0.85

        else:

            factor = 1.20

        # Active users

        active_users = int(
            total_users * factor
        )

        # =====================================================
        # DISTRIBUTE USERS BETWEEN CELLS
        # =====================================================

        cell_users = []

        weights = [
            random.uniform(0.5, 1.5)
            for _ in range(cells)
        ]

        weight_sum = sum(weights)

        for weight in weights:

            users = round(
                active_users *
                weight /
                weight_sum
            )

            cell_users.append(
                users
            )

        # Correct rounding difference

        difference = (
            active_users -
            sum(cell_users)
        )

        if difference != 0:

            cell_users[0] += difference

        # =====================================================
        # INITIAL CHANNEL ALLOCATION
        # =====================================================

        cell_data = []

        for i in range(cells):

            users = cell_users[i]

            own_allocated = min(
                users,
                channels_per_cell
            )

            blocked = max(
                0,
                users - own_allocated
            )

            cell_data.append({

                "users": users,

                "own_allocated":
                    own_allocated,

                "borrowed":
                    0,

                "allocated":
                    own_allocated,

                "blocked":
                    blocked,

                "spare":
                    channels_per_cell -
                    own_allocated

            })

        # =====================================================
        # FIND CELL NEIGHBORS
        # =====================================================

        neighbors = self.find_neighbors(
            cells
        )

        # =====================================================
        # DYNAMIC CHANNEL BORROWING
        # =====================================================

        total_borrowed = 0

        borrowing_messages = []

        # Check each cell for additional channel demand

        for i in range(cells):

            needed = (
                cell_data[i]["users"] -
                cell_data[i]["allocated"]
            )

            if needed <= 0:
                continue

            # Find neighboring cells with spare channels

            available_neighbors = []

            for neighbor in neighbors[i]:

                spare = cell_data[
                    neighbor
                ]["spare"]

                if spare > 0:

                    available_neighbors.append(
                        neighbor
                    )

            # Borrow from neighbors

            for neighbor in available_neighbors:

                if needed <= 0:
                    break

                spare = cell_data[
                    neighbor
                ]["spare"]

                borrowed = min(
                    needed,
                    spare
                )

                # Add borrowed channels

                cell_data[i]["borrowed"] += (
                    borrowed
                )

                cell_data[i]["allocated"] += (
                    borrowed
                )

                # Remove spare capacity
                # from neighboring cell

                cell_data[neighbor]["spare"] -= (
                    borrowed
                )

                needed -= borrowed

                total_borrowed += borrowed

                borrowing_messages.append(
                    f"BS-{i + 1} borrowed "
                    f"{borrowed} channel(s) "
                    f"from BS-{neighbor + 1}"
                )

            # Remaining blocked requests

            cell_data[i]["blocked"] = max(
                0,
                cell_data[i]["users"] -
                cell_data[i]["allocated"]
            )

        # =====================================================
        # CALCULATE LOAD AND STATUS
        # =====================================================

        total_allocated = 0
        total_blocked = 0

        for data in cell_data:

            data["load"] = (
                data["allocated"] /
                channels_per_cell
            ) * 100

            if data["load"] < 60:

                data["status"] = "NORMAL"

            elif data["load"] < 100:

                data["status"] = "BUSY"

            else:

                data["status"] = "CONGESTED"

            total_allocated += (
                data["allocated"]
            )

            total_blocked += (
                data["blocked"]
            )

        # =====================================================
        # NETWORK UTILIZATION
        # =====================================================

        total_channels = (
            cells *
            channels_per_cell
        )

        network_utilization = (
            total_allocated /
            total_channels
        ) * 100

        # =====================================================
        # INTERFERENCE
        # =====================================================

        if network_utilization < 50:

            interference = "LOW"

        elif network_utilization < 80:

            interference = "MEDIUM"

        else:

            interference = "HIGH"

        # =====================================================
        # UPDATE MAIN STATISTICS
        # =====================================================

        self.active_users_label.config(
            text=f"Active Users: {active_users}"
        )

        self.assigned_label.config(
            text=f"Allocated Channels: "
                 f"{total_allocated}"
        )

        self.borrowed_label.config(
            text=f"Borrowed Channels: "
                 f"{total_borrowed}"
        )

        self.blocked_label.config(
            text=f"Blocked Requests: "
                 f"{total_blocked}"
        )

        self.utilization_label.config(
            text=f"Network Utilization: "
                 f"{network_utilization:.1f}%"
        )

        self.interference_label.config(
            text=f"Interference: "
                 f"{interference}"
        )

        # =====================================================
        # UPDATE CELL TABLE
        # =====================================================

        self.update_cell_table(
            cell_data
        )

        # =====================================================
        # DRAW NETWORK
        # =====================================================

        self.draw_network(
            cells=cells,
            cell_data=cell_data
        )

        # =====================================================
        # SHOW BORROWING ACTIVITY
        # =====================================================

        if borrowing_messages:

            message = (
                "Dynamic Channel Allocation:\n\n"
                +
                "\n".join(
                    borrowing_messages
                )
            )

            messagebox.showinfo(
                "Channel Borrowing",
                message
            )

        else:

            messagebox.showinfo(
                "Channel Borrowing",
                "No channel borrowing was required."
            )

    # =========================================================
    # FIND NEIGHBORING CELLS
    # =========================================================

    def find_neighbors(self, cells):

        radius = 1.0

        dx = math.sqrt(3) * radius
        dy = 1.5 * radius

        positions = [

            (0, 0),

            (dx, 0),

            (dx / 2, dy),

            (-dx / 2, dy),

            (-dx, 0),

            (-dx / 2, -dy),

            (dx / 2, -dy)

        ]

        positions = positions[:cells]

        neighbors = [
            []
            for _ in range(cells)
        ]

        # Adjacent pointy-top hexagons
        # have center distance sqrt(3)

        neighbor_distance = dx

        for i in range(cells):

            for j in range(cells):

                if i == j:
                    continue

                x1, y1 = positions[i]
                x2, y2 = positions[j]

                distance = math.sqrt(
                    (x1 - x2) ** 2 +
                    (y1 - y2) ** 2
                )

                if abs(
                    distance -
                    neighbor_distance
                ) < 0.01:

                    neighbors[i].append(j)

        return neighbors

    # =========================================================
    # UPDATE CELL TABLE
    # =========================================================

    def update_cell_table(self, cell_data):

        # Clear old rows

        for item in self.cell_table.get_children():

            self.cell_table.delete(
                item
            )

        # Insert new data

        for i, data in enumerate(
            cell_data
        ):

            self.cell_table.insert(
                "",
                "end",
                values=(

                    f"BS-{i + 1}",

                    data["users"],

                    data["own_allocated"],

                    data["borrowed"],

                    data["allocated"],

                    data["blocked"],

                    f"{data['load']:.0f}%",

                    data["status"]

                )
            )

    # =========================================================
    # CREATE PERFECT HEXAGON
    # =========================================================

    def create_hexagon(
        self,
        cx,
        cy,
        radius
    ):

        points = []

        for i in range(6):

            angle = math.radians(
                60 * i + 30
            )

            x = (
                cx +
                radius *
                math.cos(angle)
            )

            y = (
                cy +
                radius *
                math.sin(angle)
            )

            points.append(
                (x, y)
            )

        return points

    # =========================================================
    # DRAW CELLULAR NETWORK
    # =========================================================

    def draw_network(
        self,
        cells=7,
        cell_data=None
    ):

        self.ax.clear()

        radius = 1.0

        # Exact spacing for pointy-top hexagons

        dx = math.sqrt(3) * radius
        dy = 1.5 * radius

        # =====================================================
        # 7-CELL HEXAGONAL CLUSTER
        # =====================================================

        positions = [

            # Center
            (0, 0),

            # Right
            (dx, 0),

            # Upper-right
            (dx / 2, dy),

            # Upper-left
            (-dx / 2, dy),

            # Left
            (-dx, 0),

            # Lower-left
            (-dx / 2, -dy),

            # Lower-right
            (dx / 2, -dy)

        ]

        positions = positions[:cells]

        # =====================================================
        # DRAW CELLS
        # =====================================================

        for i, (cx, cy) in enumerate(
            positions
        ):

            if cell_data is not None:

                data = cell_data[i]

                load = data["load"]

                status = data["status"]

                borrowed = data["borrowed"]

            else:

                load = 0

                status = "NORMAL"

                borrowed = 0

            # -------------------------------------------------
            # Hexagon
            # -------------------------------------------------

            points = self.create_hexagon(
                cx,
                cy,
                radius
            )

            hexagon = Polygon(
                points,
                closed=True,
                fill=False,
                edgecolor="black",
                linewidth=2
            )

            self.ax.add_patch(
                hexagon
            )

            # -------------------------------------------------
            # Base station
            # -------------------------------------------------

            self.ax.scatter(
                cx,
                cy,
                marker="^",
                s=160,
                zorder=5
            )

            # -------------------------------------------------
            # Base station label
            # -------------------------------------------------

            self.ax.text(
                cx,
                cy + 0.28,
                f"BS-{i + 1}",
                ha="center",
                va="center",
                fontsize=9,
                fontweight="bold",
                zorder=6
            )

            # -------------------------------------------------
            # CELL STATUS
            # -------------------------------------------------

            if cell_data is not None:

                self.ax.text(
                    cx,
                    cy - 0.15,
                    f"Load: {load:.0f}%",
                    ha="center",
                    va="center",
                    fontsize=8,
                    zorder=6
                )

                self.ax.text(
                    cx,
                    cy - 0.38,
                    status,
                    ha="center",
                    va="center",
                    fontsize=7,
                    fontweight="bold",
                    zorder=6
                )

                # Show borrowed channels

                if borrowed > 0:

                    self.ax.text(
                        cx,
                        cy - 0.57,
                        f"Borrowed: {borrowed}",
                        ha="center",
                        va="center",
                        fontsize=6,
                        zorder=6
                    )

        # =====================================================
        # MOBILE USERS
        # =====================================================

        if cell_data is not None:

            for i, data in enumerate(
                cell_data
            ):

                cx, cy = positions[i]

                users = data["users"]

                # Draw each user inside this cell

                for _ in range(users):

                    angle = random.uniform(
                        0,
                        2 * math.pi
                    )

                    distance = random.uniform(
                        0.1,
                        0.65
                    )

                    ux = (
                        cx +
                        distance *
                        math.cos(angle)
                    )

                    uy = (
                        cy +
                        distance *
                        math.sin(angle)
                    )

                    self.ax.scatter(
                        ux,
                        uy,
                        marker="o",
                        s=20,
                        zorder=4
                    )

        # =====================================================
        # GRAPH SETTINGS
        # =====================================================

        self.ax.set_title(
            "Cellular Network and Traffic Distribution",
            fontsize=13,
            fontweight="bold"
        )

        self.ax.set_aspect(
            "equal"
        )

        self.ax.set_xlim(
            -4.0,
            4.0
        )

        self.ax.set_ylim(
            -3.5,
            3.5
        )

        self.ax.axis(
            "off"
        )

        self.figure.tight_layout()

        self.canvas.draw()

    # =========================================================
    # RESET
    # =========================================================

    def reset_simulation(self):

        self.active_users_label.config(
            text="Active Users: 0"
        )

        self.assigned_label.config(
            text="Allocated Channels: 0"
        )

        self.borrowed_label.config(
            text="Borrowed Channels: 0"
        )

        self.blocked_label.config(
            text="Blocked Requests: 0"
        )

        self.utilization_label.config(
            text="Network Utilization: 0%"
        )

        self.interference_label.config(
            text="Interference: LOW"
        )

        # Clear table

        for item in self.cell_table.get_children():

            self.cell_table.delete(
                item
            )

        # Redraw empty network

        self.draw_network(
            cells=int(
                self.cells_var.get()
            ),
            cell_data=None
        )


# =============================================================
# MAIN PROGRAM
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WirelessSimulator(
        root
    )

    root.mainloop()