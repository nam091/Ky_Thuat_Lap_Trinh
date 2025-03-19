from Module_StegaAnalysis import compare_images, analyse, show_pixel_examples
from lsb_lib.file_struct import ftypes, read_exif_data
import tkinter as tk
from tkinter import filedialog, messagebox

def gui():
    
    def run_compare():
        messagebox.showinfo("Hướng dẫn", "Chọn ảnh gốc và ảnh đã chỉnh sửa để so sánh hoặc phân tích.\n")
        original = filedialog.askopenfilename(title="Chọn ảnh gốc", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not original:
            return
        modified = filedialog.askopenfilename(title="Chọn ảnh đã chỉnh sửa", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not modified:
            return
        messagebox.showinfo("Hướng dẫn", "Chọn thư mục lưu kết quả default = './Image_Output'")
        output_dir = filedialog.askdirectory(title="Chọn thư mục lưu kết quả") or "./Image_Output"
        result_text.insert(tk.END, f"[+] Chỉ số khác nhau giữa hai ảnh:\n")
        try:
            for color in ['RGB', 'delta', 'gray', 'hsv', 'lab']:
                match_percentage = compare_images(original, modified, color, output_dir)
                result_text.insert(tk.END, f" - Màu {color}: {match_percentage:.2f}\n")
        
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def run_analysis():
        messagebox.showinfo("Hướng dẫn", "Chọn ảnh gốc và ảnh đã chỉnh sửa để so sánh hoặc phân tích.\n")
        original = filedialog.askopenfilename(title="Chọn ảnh gốc", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not original:
            return
        modified = filedialog.askopenfilename(title="Chọn ảnh đã chỉnh sửa", filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not modified:
            return
        
        try:
            plot_path = analyse(original, modified)
            result_text.insert(tk.END, f"Biểu đồ được lưu tại: {plot_path}\n")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def check_structure():
        file_path = filedialog.askopenfilename(title="Chọn file cần kiểm tra", filetypes=[("All files", "*.*")])
        if not file_path:
            return
        
        try:
            file_info = ftypes(file_path)
            result_text.insert(tk.END, f"Kiểu file: {file_info['file_type']}\n")
            result_text.insert(tk.END, f"Phần mở rộng: {file_info['extension']}\n")
            result_text.insert(tk.END, f"Kích cỡ của ảnh: {file_info['image_size'][0]}x{file_info['image_size'][1]} pixels\n")
            result_text.insert(tk.END, f"Kích thước file: {file_info['file size']} bytes\n")
            if file_info['suspicious']:
                result_text.insert(tk.END, "File có bất thường\n")
            else:
                result_text.insert(tk.END, "File không có gì bất thường\n")
            result_text.insert(tk.END, "\n".join(file_info['details']) + "\n")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
    
    def show_exif():
        file_path = filedialog.askopenfilename(title="Chọn file cần kiểm tra", filetypes=[("All files", "*.*")])
        if not file_path:
            return
        
        try:
            metadata = read_exif_data(file_path)
            if metadata is None:
                result_text.insert(tk.END, "Không tìm thấy metadata trong file.\n\n")
                return
                
            if isinstance(metadata, dict):
                for key, value in metadata.items():
                    if isinstance(value, dict):
                        result_text.insert(tk.END, f"{key}:\n")
                        for sub_key, sub_value in value.items():
                            result_text.insert(tk.END, f"  {sub_key}: {sub_value}\n")
                    else:
                        result_text.insert(tk.END, f"{key}: {value}\n")
            else:
                result_text.insert(tk.END, f"Metadata: {metadata}\n")
            result_text.insert(tk.END, "\n")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Error processing metadata: {str(e)}")
    
    def clear_results():
        result_text.delete(1.0, tk.END)
    
    root = tk.Tk()
    root.title("Steganography Analysis Tool")
    root.iconbitmap("./00_LOGO/KMA.ico")
    root.resizable(True, True)
    root.geometry("1000x500")
    
    # Frame chứa các nút chức năng
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Kiểm tra Metadata", command=show_exif, width=15).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Kiểm tra cấu trúc", command=check_structure, width=15).grid(row=0, column=1, padx=5)
    tk.Button(button_frame, text="So sánh ảnh", command=run_compare, width=15).grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Phân tích Entropy", command=run_analysis, width=15).grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Xóa kết quả", command=clear_results, width=15).grid(row=0, column=4, padx=5)
    # Khu vực hiển thị kết quả
    result_frame = tk.Frame(root)
    result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    result_text = tk.Text(result_frame, wrap=tk.WORD, bg="lightyellow", font=("Times New Roman", 18))
    result_text.pack(fill=tk.BOTH, expand=True)
    
    # Thanh cuộn cho khu vực kết quả
    scrollbar = tk.Scrollbar(result_text)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    result_text.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=result_text.yview)
    
    # Trạng thái
    status_bar = tk.Label(root, text="Nhóm 7 KTLT", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    root.mainloop()

if __name__ == "__main__":
    gui()