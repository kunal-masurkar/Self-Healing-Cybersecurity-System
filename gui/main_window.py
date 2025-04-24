import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
from datetime import datetime
from config import DATA_DIR, MODEL_PATH
from detector.anomaly_detector import anomaly_detector
from security.response import security_response
from utils.logger import logger
import os

class SecuritySystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Self-Healing Cybersecurity System")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure('TButton', padding=5)
        self.style.configure('TLabel', padding=5)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create status bar
        self.status_var = tk.StringVar()
        self.status_var.set("System Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.setup_gui()
        self.is_running = False
        self.update_thread = None

    def setup_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.dashboard_tab = ttk.Frame(self.notebook)
        self.monitoring_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.monitoring_tab, text="Monitoring")
        self.notebook.add(self.settings_tab, text="Settings")
        
        self.setup_dashboard()
        self.setup_monitoring()
        self.setup_settings()

    def setup_dashboard(self):
        # Control buttons
        control_frame = ttk.LabelFrame(self.dashboard_tab, text="System Controls", padding="10")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.start_button = ttk.Button(control_frame, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.train_button = ttk.Button(control_frame, text="Train Model", command=self.train_model)
        self.train_button.pack(side=tk.LEFT, padx=5)
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.dashboard_tab, text="System Statistics", padding="10")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Create statistics labels
        self.stats_vars = {
            "Total Anomalies": tk.StringVar(value="0"),
            "Blocked IPs": tk.StringVar(value="0"),
            "Model Status": tk.StringVar(value="Not Trained"),
            "Last Update": tk.StringVar(value="Never")
        }
        
        for label, var in self.stats_vars.items():
            frame = ttk.Frame(stats_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=f"{label}:").pack(side=tk.LEFT)
            ttk.Label(frame, textvariable=var).pack(side=tk.RIGHT)
        
        # Log display
        log_frame = ttk.LabelFrame(self.dashboard_tab, text="System Logs", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

    def setup_monitoring(self):
        # Blocked IPs list
        blocked_frame = ttk.LabelFrame(self.monitoring_tab, text="Blocked IPs", padding="10")
        blocked_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for blocked IPs
        columns = ("IP Address", "Block Time", "Reason", "Duration")
        self.blocked_tree = ttk.Treeview(blocked_frame, columns=columns, show="headings")
        
        for col in columns:
            self.blocked_tree.heading(col, text=col)
            self.blocked_tree.column(col, width=100)
        
        self.blocked_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(blocked_frame, orient=tk.VERTICAL, command=self.blocked_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.blocked_tree.configure(yscrollcommand=scrollbar.set)
        
        # Control buttons
        button_frame = ttk.Frame(blocked_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.unblock_button = ttk.Button(button_frame, text="Unblock Selected", command=self.unblock_selected)
        self.unblock_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = ttk.Button(button_frame, text="Refresh", command=self.update_blocked_list)
        self.refresh_button.pack(side=tk.LEFT, padx=5)

    def setup_settings(self):
        # Model settings
        model_frame = ttk.LabelFrame(self.settings_tab, text="Model Settings", padding="10")
        model_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Contamination level
        ttk.Label(model_frame, text="Contamination Level:").pack(anchor=tk.W)
        self.contamination_var = tk.DoubleVar(value=0.05)
        contamination_scale = ttk.Scale(model_frame, from_=0.01, to=0.5, variable=self.contamination_var, orient=tk.HORIZONTAL)
        contamination_scale.pack(fill=tk.X, pady=5)
        
        # Security settings
        security_frame = ttk.LabelFrame(self.settings_tab, text="Security Settings", padding="10")
        security_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Block duration
        ttk.Label(security_frame, text="Block Duration (seconds):").pack(anchor=tk.W)
        self.block_duration_var = tk.IntVar(value=3600)
        duration_entry = ttk.Entry(security_frame, textvariable=self.block_duration_var)
        duration_entry.pack(fill=tk.X, pady=5)
        
        # Save settings button
        save_button = ttk.Button(self.settings_tab, text="Save Settings", command=self.save_settings)
        save_button.pack(pady=10)

    def start_monitoring(self):
        if not self.is_running:
            # Check if model is trained
            if not os.path.exists(MODEL_PATH):
                response = messagebox.askyesno(
                    "Model Not Trained",
                    "The model needs to be trained before starting monitoring. Would you like to train it now?"
                )
                if response:
                    self.train_model()
                else:
                    messagebox.showwarning(
                        "Warning",
                        "Monitoring cannot start without a trained model. Please train the model first."
                    )
                    return
            
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_var.set("Monitoring Active")
            self.update_thread = threading.Thread(target=self.monitoring_loop)
            self.update_thread.daemon = True
            self.update_thread.start()

    def stop_monitoring(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_var.set("Monitoring Stopped")

    def monitoring_loop(self):
        while self.is_running:
            try:
                # Load and analyze data
                test_data = anomaly_detector.load_data()
                
                if test_data is not None:
                    results = anomaly_detector.predict(test_data)
                    if results is not None:
                        self.update_statistics(results)
                        self.process_anomalies(results)
                else:
                    # Even if no new data, update statistics to reflect current state
                    self.update_statistics({'anomalies': []})
                
                # Always update blocked list and force GUI refresh
                self.update_blocked_list()
                self.root.update()
                
                time.sleep(5)  # Update every 5 seconds
            except Exception as e:
                self.log_message(f"Error in monitoring loop: {str(e)}", "ERROR")
                time.sleep(5)

    def update_statistics(self, results):
        # Update anomalies count
        if 'anomalies' in results:
            self.stats_vars["Total Anomalies"].set(str(len(results['anomalies'])))
        
        # Update blocked IPs count - get directly from security_response
        blocked_ips = security_response.get_blocked_ips()
        self.stats_vars["Blocked IPs"].set(str(len(blocked_ips)))
        
        # Update last update timestamp
        self.stats_vars["Last Update"].set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Update model status
        if os.path.exists(MODEL_PATH):
            self.stats_vars["Model Status"].set("Trained")
        else:
            self.stats_vars["Model Status"].set("Not Trained")
        
        # Force GUI update
        self.root.update()

    def process_anomalies(self, results):
        for idx in results['anomalies']:
            malicious_ip = f"192.168.1.{100 + idx}"
            try:
                security_response.block_ip(
                    malicious_ip,
                    reason=f"Anomaly detected in row {idx} with score {results['scores'][idx]:.2f}"
                )
                self.log_message(f"Blocked IP {malicious_ip} due to anomaly", "INFO")
            except Exception as e:
                self.log_message(f"Failed to block IP {malicious_ip}: {str(e)}", "ERROR")

    def update_blocked_list(self):
        # Clear existing items
        for item in self.blocked_tree.get_children():
            self.blocked_tree.delete(item)
        
        # Add current blocked IPs
        for ip, info in security_response.get_blocked_ips().items():
            self.blocked_tree.insert("", tk.END, values=(
                ip,
                info['block_time'],
                info['reason'],
                f"{info['duration']}s" if 'duration' in info else "Permanent"
            ))

    def unblock_selected(self):
        selected = self.blocked_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an IP to unblock")
            return
        
        for item in selected:
            ip = self.blocked_tree.item(item)['values'][0]
            if security_response.unblock_ip(ip):
                self.log_message(f"Unblocked IP {ip}", "INFO")
            else:
                self.log_message(f"Failed to unblock IP {ip}", "ERROR")
        
        self.update_blocked_list()

    def train_model(self):
        try:
            self.status_var.set("Training Model...")
            self.root.update()
            
            # Train model using the imported singleton instance
            success = anomaly_detector.train()
            
            if success:
                # Verify model was saved
                if os.path.exists(MODEL_PATH):
                    self.status_var.set("Model Trained Successfully")
                    messagebox.showinfo("Success", "Model trained successfully!")
                else:
                    self.status_var.set("Model Training Failed")
                    messagebox.showerror("Error", "Model training completed but model file was not saved!")
            else:
                self.status_var.set("Model Training Failed")
                messagebox.showerror("Error", "Model training failed. Check logs for details.")
                
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
            self.status_var.set("Model Training Failed")
            messagebox.showerror("Error", f"Error training model: {str(e)}")

    def save_settings(self):
        try:
            # Update model configuration
            MODEL_CONFIG['contamination'] = self.contamination_var.get()
            
            # Update security configuration
            SECURITY_CONFIG['block_duration'] = self.block_duration_var.get()
            
            self.log_message("Settings saved successfully", "INFO")
            messagebox.showinfo("Success", "Settings saved successfully")
        except Exception as e:
            self.log_message(f"Error saving settings: {str(e)}", "ERROR")
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def log_message(self, message, level="INFO"):
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {level}: {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = SecuritySystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
