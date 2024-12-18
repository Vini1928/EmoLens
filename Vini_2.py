if __name__ == "__main__":
    root = tk.Tk()
    core_logic = EmoLensCore()
    app = FullUI(root, core_logic)
    root.mainloop()