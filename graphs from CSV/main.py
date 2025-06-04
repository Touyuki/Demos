import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import gc

# 创建主窗口/GUIを宣言
root = tk.Tk()
root.title("CSVデータのグラフ表示")
root.geometry("800x600")

root.protocol("WM_DELETE_WINDOW", lambda:close_gui())

# 创建主Notebook（包含Tab 1, Tab 2, Tab 3）/ メインNotebookを作成
main_notebook = ttk.Notebook(root)
main_notebook.pack(expand=1, fill="both")

# 创建Tab页面 / タブ画面を宣言
tab1 = ttk.Frame(main_notebook)
tab2 = ttk.Frame(main_notebook)
tab3 = ttk.Frame(main_notebook)
tab4 = ttk.Frame(main_notebook)
tab5 = ttk.Frame(main_notebook)

# 将主Tab页面添加到主Notebook中 / メインNotebookにタブ画面を追加
main_notebook.add(tab1, text="データ取得")
main_notebook.add(tab2, text="グラフ作成1")
main_notebook.add(tab3, text="グラフ作成2")
main_notebook.add(tab4, text="グラフ表示1")
main_notebook.add(tab5, text="グラフ表示2")

original_data=[]
table_data_tab2 = []
table_data_tab3 = []
#------------------------------ tab1页面 数据读取 / タブ画面1 データ取得---------------------------
# 文件路径标签 / ラベル　ファイルパス
local_path_label = ttk.Label(tab1, text="CSVファイルパス:")
local_path_label.place(x=50, y=50)

# 文件路径输入框　/ 入力欄　ファイルパス
local_path_entry = ttk.Entry(tab1)
local_path_entry.place(x=150, y=50, width=500, height=25)

# 文件路径浏览按钮 / 参照ボタン
local_path_button = ttk.Button(tab1,text="参照", command=lambda:browse_csv())
local_path_button.place(x=700, y=50, width=80, height=25)

# 加载文件按钮　/ 読み込みボタン
load_data_button = ttk.Button(tab1, text="読み込み", command=lambda:load_csv())
load_data_button.place(x=500, y=480,width=80,height=25)

# 关闭程序按钮 / 終了ボタン
close_button_tab1 = ttk.Button(tab1, text="終了", command=lambda:close_gui())
close_button_tab1.place(x=620, y=480, width=80, height=25)

# 关闭程序 / 終了
def close_gui():
    # root.destroy()
    sys.exit(0)  # 确保完全退出程序 / 必ずプログラムを閉じる

# 浏览并选择csv文件 /　csvファイル参照
def browse_csv():
    file_path = filedialog.askopenfilename(
        title="CSVファイルを選択",
        filetypes=(("CSVファイル", "*.csv"), ("全部ファイル", "*.*"))
    )
    if file_path:
        local_path_entry.delete(0, tk.END)
        local_path_entry.insert(0, file_path)

all_funcnames = []
all_remarks = []

# 读取csv文件 / csvファイルの読み込み
def load_csv():
    global all_funcnames, all_remarks
    global original_data, table_data_tab2, table_data_tab3
    file_path = local_path_entry.get()
    if not file_path:
        messagebox.showerror("エラー", "csvファイルを選択してください")
        return
    try:
        df = pd.read_csv(file_path, header=None)
        original_data = []
        all_funcnames = []
        all_remarks = []

        # 获取全部备注 / コメントを取得
        all_remarks = df.iloc[0].tolist()
        all_remarks.pop(0)

        # 获取全部函数名 / 関数名を取得
        all_funcnames = df.iloc[1].tolist()
        all_funcnames.pop(0)

        # Treeview 初始化 / Treeviewの初期化
        # 清空Treeview1,清空Treeview2 / Treeview1,Treeview2をクリア
        for item in treeview_tab2.get_children():
            treeview_tab2.delete(item)
            table_data_tab2 = []

        for item in treeview_tab3.get_children():
            treeview_tab3.delete(item)
            table_data_tab3 = []

        original_data.append([])
        for i in range(len(all_remarks)):
            values = ["", "", all_funcnames[i], all_remarks[i]]
            original_data.append([])
            treeview_tab2.insert("", "end", values=values)
            table_data_tab2.append(values)

            values_second = ["", "", all_funcnames[i], all_remarks[i]]
            treeview_tab3.insert("", "end", values=values_second)
            table_data_tab3.append(values_second)

        for i in range(df.shape[0]):
            if i < 2:
                continue
            else:
                tmp_row_list = df.iloc[i].tolist()
                for j in range(len(tmp_row_list)):
                    original_data[j].append(convert_to_float(tmp_row_list[j]))

    except Exception as e:
            messagebox.showerror("エラー", f"CSVの読み込み処理が失敗しました: {str(e)}")

def convert_to_float(value):
    """数值转换"""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
#------------------------------ tab2页面 制作折线图1 / タブ2 グラフ作成1---------------------------
# 函数名称标签(显示筛选使用) / 関数名ラベル(フィルター機能)
function_filter_label_tab2 = ttk.Label(tab2, text="関数名")
function_filter_label_tab2.place(x=210,y=40)

# 函数名输入框内容 / 入力欄文字列を保存する変数
function_filter_text_tab2 = tk.StringVar()
# 绑定文本变化事件(使用*args忽略trace自动传入的3个参数) / フィルター機能設定(*argsでディフォルト引数を無視)
function_filter_text_tab2.trace("w", lambda *args:apply_filter(1))

# 函数名输入框 / 入力欄 関数名
function_filter_entry_tab2 = ttk.Entry(tab2, textvariable=function_filter_text_tab2)
function_filter_entry_tab2.place(x=280, y=40, width=160, height=25)

# 创建Treeview和滚动条 / Treeview、スクロールバー作成
y_scroll_tab2 = ttk.Scrollbar(tab2)

# 让滚动条不显示 / スクロールバーの非表示設定
# y_scroll_tab2.place()

treeview_label_tab2 = ttk.Label(tab2, text="関数")
treeview_label_tab2.place(x=85, y=90)

treeview_tab2 = ttk.Treeview(tab2, yscrollcommand=y_scroll_tab2)
treeview_tab2.place(x=130, y=100, width=550, height=280)

# 格式化列 / 列名を設定
treeview_tab2['columns'] = ["単体グラフ", "重ねグラフ","関数名", "コメント"]

# 隐藏第一列 / 一列目を非表示にする
treeview_tab2.column('#0', width=0, stretch=tk.NO)

treeview_tab2.column("単体グラフ", width=80, anchor='center')
treeview_tab2.column("重ねグラフ", width=80, anchor='center')
treeview_tab2.column("関数名", width=190, anchor="w")
treeview_tab2.column("コメント", width=190, anchor="w")

# 创建表头 / ヘッダ設定
treeview_tab2.heading("単体グラフ", text="単体グラフ")
treeview_tab2.heading("重ねグラフ", text="重ねグラフ")
treeview_tab2.heading("関数名", text="関数名")
treeview_tab2.heading("コメント", text="コメント")

y_scroll_tab2.config(command=treeview_tab2.yview)

treeview_tab2.bind("<ButtonRelease-1>", lambda event:on_tree_click_tab2(event))

# 绘图按钮 / グラフ作成ボタン
draw_graph_button_tab2 = ttk.Button(tab2, text="グラフ作成",command=lambda:draw_graph_tab2())
draw_graph_button_tab2.place(x=500, y=480,width=80,height=25)

# 关闭程序按钮 / 終了ボタン
close_button_tab2 = ttk.Button(tab2, text="終了", command=lambda:close_gui())
close_button_tab2.place(x=620, y=480, width=80, height=25)

# フィルター機能
def apply_filter(index):
    treeview_index=index

    filter_text = ""
    target_tree = None
    table_data = None

    if treeview_index == 1:
        filter_text = function_filter_entry_tab2.get()
        target_tree = treeview_tab2
        table_data = table_data_tab2
    else:
        filter_text = function_filter_entry_tab3.get()
        target_tree = treeview_tab3
        table_data = table_data_tab3

    # 清空Treeview / Treeviewをクリア
    for item in target_tree.get_children():
        target_tree.delete(item)

    for i in range(len(table_data)):
        tmp_values = table_data[i]

        tmp_funcname = tmp_values[2]
        if not filter_text or filter_text in tmp_funcname:
            target_tree.insert('', 'end', values=tmp_values)

# クリック事件を設定
def on_tree_click_tab2(event):
    """处理Treeview点击事件"""
    region = treeview_tab2.identify('region', event.x, event.y)
    if region == 'cell':
        column = treeview_tab2.identify_column(event.x)
        item = treeview_tab2.identify_row(event.y)

        # 如果点击的是第一列（选择列）/ 一列目がクリックされた場合
        if column == '#1':
            # 获取当前行的值 / 現在の行の値を取得
            values = list(treeview_tab2.item(item, 'values'))
            current_value = values[0]
            new_value = '○' if current_value == '' else ''
            values[0] = new_value

            # 更新Treeview中的行 / Treeviewの行を更新
            treeview_tab2.item(item, values=values)

            # 更新原始数据中的对应行 / 読み込んだデータを更新
            item_index = treeview_tab2.index(item)
            for i,data in enumerate(table_data_tab2):
                if i == item_index:
                    table_data_tab2[i]=values
                    break

        elif column == "#2":
            # 获取当前行的值 / 現在の行の値を取得
            values = list(treeview_tab2.item(item, 'values'))
            current_value = values[1]
            new_value = '○' if current_value == '' else ''
            values[1] = new_value

            # 更新Treeview中的行 / Treeviewの行を更新
            treeview_tab2.item(item, values=values)

            # 更新原始数据中的对应行 / 読み込んだデータを更新
            item_index = treeview_tab2.index(item)
            for i,data in enumerate(table_data_tab2):
                if i == item_index:
                    table_data_tab2[i]=values
                    break

#------------------------------ tab3页面 制作折线图2 / タブ3 グラフ作成2---------------------------
# 函数名称标签(显示筛选使用) /  関数名ラベル(フィルター機能)
function_filter_label_tab3 = ttk.Label(tab3, text="函数名")
function_filter_label_tab3.place(x=210,y=40)

# 函数名输入框内容 / 入力欄文字列を保存する変数
function_filter_text_tab3 = tk.StringVar()

# 绑定文本变化事件 / フィルター機能設定
function_filter_text_tab3.trace("w", lambda *args:apply_filter(2))

# 函数名输入框 / 入力欄 関数名
function_filter_entry_tab3 = ttk.Entry(tab3, textvariable=function_filter_text_tab3)
function_filter_entry_tab3.place(x=280, y=40, width=160, height=25)

# 创建Treeview和滚动条 / Treeview、スクロールバー作成
y_scroll_tab3 = ttk.Scrollbar(tab3)

# 让滚动条不显示 / スクロールバーの非表示設定
# y_scroll_tab2.place()

treeview_label_tab3 = ttk.Label(tab3, text="関数")
treeview_label_tab3.place(x=85, y=90)

treeview_tab3 = ttk.Treeview(tab3, yscrollcommand=y_scroll_tab3)
treeview_tab3.place(x=130, y=100, width=550, height=280)

# 格式化列 / 列名を設定
treeview_tab3['columns'] = ["Y軸(左)", "Y軸(右)","関数名", "コメント"]

# 隐藏第一列 / 一列目を非表示にする
treeview_tab3.column('#0', width=0, stretch=tk.NO)
treeview_tab3.column("Y軸(左)", width=80, anchor='center')
treeview_tab3.column("Y軸(右)", width=80, anchor='center')
treeview_tab3.column("関数名", width=190, anchor="w")
treeview_tab3.column("コメント", width=190, anchor="w")

# 创建表头 / ヘッダ設定
treeview_tab3.heading("Y軸(左)", text="Y軸(左)")
treeview_tab3.heading("Y軸(右)", text="Y軸(右)")
treeview_tab3.heading("関数名", text="関数名")
treeview_tab3.heading("コメント", text="コメント")

y_scroll_tab3.config(command=treeview_tab3.yview)

treeview_tab3.bind("<ButtonRelease-1>", lambda event:on_tree_click_tab3(event))

# 绘图按钮 / グラフ作成ボタン
draw_graph_button_tab3 = ttk.Button(tab3, text="グラフ作成", command=lambda:draw_graph_tab3())
draw_graph_button_tab3.place(x=500, y=480,width=80,height=25)

# 关闭程序按钮 / 終了ボタン
close_button_tab3 = ttk.Button(tab3, text="終了", command=lambda:close_gui())
close_button_tab3.place(x=620, y=480, width=80, height=25)

# クリック事件を設定
def on_tree_click_tab3(event):
    """处理Treeview点击事件"""
    region = treeview_tab3.identify('region', event.x, event.y)
    if region == 'cell':
        column = treeview_tab3.identify_column(event.x)
        item = treeview_tab3.identify_row(event.y)

        # 如果点击的是第一列（选择列）/ 一列目がクリックされた場合
        if column == '#1':
            # 获取当前行的值 / 現在の行の値を取得
            values = list(treeview_tab3.item(item, 'values'))
            current_value = values[0]
            if current_value == "":
                new_value_1 = '○'
                new_value_2 = ''
            else:
                new_value_1 = ''
                new_value_2 = ''

            values[0] = new_value_1
            values[1] = new_value_2

            # 更新Treeview中的行 / Treeviewの行を更新
            treeview_tab3.item(item, values=values)

            # 更新原始数据中的对应行 / 読み込んだデータを更新
            item_index = treeview_tab3.index(item)
            for i,data in enumerate(table_data_tab3):
                if i == item_index:
                    table_data_tab3[i]=values
                    break

        elif column == "#2":
            # 获取当前行的值 / 現在の行の値を取得
            values = list(treeview_tab3.item(item, 'values'))
            current_value = values[1]
            if current_value == "":
                new_value_2 = '○'
                new_value_1 = ''

            else:
                new_value_1 = ''
                new_value_2 = ''

            values[0] = new_value_1
            values[1] = new_value_2

            # 更新Treeview中的行 / Treeviewの行を更新
            treeview_tab3.item(item, values=values)

            # 更新原始数据中的对应行 / 読み込んだデータを更新
            item_index = treeview_tab3.index(item)
            for i,data in enumerate(table_data_tab3):
                if i == item_index:
                    table_data_tab3[i]=values
                    break

#------------------------------ tab4页面 制作折线图1 / タブ4 グラフ作成1---------------------------

canvas_frame = tk.Frame(tab4,height=400, width=800)
canvas_frame.pack(fill=tk.BOTH, expand=True)

# 主容器Canvas / Canvasを宣言
graph_canvas = tk.Canvas(canvas_frame)
graph_canvas.pack(side='left', fill='both', expand=True)

# 滚动条 / スクロールバー
graph_scrollbar = ttk.Scrollbar(canvas_frame,
                                orient='vertical',
                                command=graph_canvas.yview)

graph_scrollbar.pack(side='right', fill='y')
graph_canvas.configure(yscrollcommand=graph_scrollbar.set)

# 内部Frame用于放置图表 / 内部Frame(グラフ保存用)
graph_inner_frame = ttk.Frame(graph_canvas)
graph_canvas.create_window((0, 0),
                                window=graph_inner_frame,
                                anchor='nw',
                                width=1350)

# 绑定配置事件 / スクロール機能設定
graph_inner_frame.bind(
    "<Configure>",
    lambda e: graph_canvas.configure(
        scrollregion=graph_canvas.bbox("all")
        )
)

# マウススクロール設定追加
def _bind_mousewheel(event):
    """绑定鼠标滚轮事件"""
    graph_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# マウススクロール設定の取り消し
def _unbind_mousewheel(event):
    """解绑鼠标滚轮事件"""
    graph_canvas.unbind_all("<MouseWheel>")

# マウススクロール設定
def _on_mousewheel(event):
    """处理鼠标滚轮滚动"""
    graph_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


graph_canvas.bind("<Enter>", _bind_mousewheel)
graph_canvas.bind("<Leave>", _unbind_mousewheel)

# 底部控制面板 / 一番下のFrame設定
bottom_frame = tk.Frame(tab4)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

update_button_tab2 = ttk.Button(bottom_frame, text="更新", command= lambda :update_graph_tab2())
update_button_tab2.pack(pady=10)
graph_frames = []

def draw_graph_tab2():
    global graph_frames
    selected_columns_single = []
    selected_columns_complex = []

    frame_height = 350  # 每个图表Frame的高度 / 各グラフFrameの高さ
    frame_width = 800  # 每个图表Frame的宽度　/ 幅
    y_offset = 10  # 初始Y偏移 / Y方向の移動値

    # 获取选中数据 / 選択されたデータの取得
    for i in range(len(table_data_tab2)):
        item_data = table_data_tab2[i]
        if item_data[0] == "○":
            selected_columns_single.append(i)
        if item_data[1] == "○":
            selected_columns_complex.append(i)

    # 清除旧图表 / 既に作成されたグラフをクリア
    for widget in graph_inner_frame.winfo_children():
        widget.destroy()

    graph_frames = []

    if len(selected_columns_complex) + len(selected_columns_single) == 0:
        return

    # 设置内部Frame的初始高度 / 最初の高さを設定
    add_count = 0
    if len(selected_columns_complex)>0:
        add_count = 1

    total_height = (len(selected_columns_single) + add_count) * (frame_height + 10)
    graph_inner_frame.configure(height=total_height)

    # 为每个选中的列创建Frame和图表 / 一列ずつグラフを作成
    for i in selected_columns_single:
        # 函数名 / 関数名
        func_name = all_funcnames[i]

        # x,y值 / x,yの値
        x_values = []
        y_values = []

        for j in range(len(original_data[0])):
            x_values.append(original_data[0][j])
            y_values.append(original_data[i+1][j])

        # 创建主Frame / メインFrameを作成
        main_frame = ttk.Frame(graph_inner_frame)
        main_frame.place(x=10, y=y_offset, width=frame_width-30, height=frame_height)
        graph_frames.append(main_frame)

        # 创建图表Frame / グラフFrameを宣言
        graph_frame = ttk.Frame(main_frame)
        graph_frame.place(x=0, y=0, relwidth=0.73, relheight=1)

        # 创建控制Frame / コントロールFrameを宣言
        control_frame = ttk.Frame(main_frame)
        control_frame.place(relx=0.75, y=0, relwidth=0.27, relheight=1)

        # 创建图表 / グラフ作成
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(x_values, y_values,
                marker='o',
                linestyle='-',
                color='red',
                linewidth=2,
                markersize=5)

        # 设置图表属性 / 軸名を設定
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        plt.subplots_adjust(left=0.15)

        # 添加标题标签 / タイトル設定
        ax.set_title(func_name,
                     pad=0,  # 标题与图表的间距 / タイトルとグラフ間の距離
                     fontsize=12,
                     fontweight='bold')

        ax.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(pad=3.0)

        # 嵌入到Frame中 / Frameに追加
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=20, relwidth=1, relheight=0.9)

        # 存储图表对象 / グラフを保存
        setattr(main_frame, 'figure', fig)
        setattr(main_frame, 'axes', ax)

        # 添加坐标轴控制组件 / 範囲設定機能
        ttk.Label(control_frame, text="X軸範囲:", font=('Arial', 9, 'bold')).place(x=10, y=10)
        ttk.Label(control_frame, text="最小値:").place(x=10, y=40)
        x_min_var = tk.StringVar(value=f"{min(x_values):.2f}")
        x_min_entry = ttk.Entry(control_frame, textvariable=x_min_var, width=12)
        x_min_entry.place(x=80, y=40)

        ttk.Label(control_frame, text="最大値:").place(x=10, y=70)
        x_max_var = tk.StringVar(value=f"{max(x_values):.2f}")
        x_max_entry = ttk.Entry(control_frame, textvariable=x_max_var, width=12)
        x_max_entry.place(x=80, y=70)

        ttk.Label(control_frame, text="Y軸範囲:", font=('Arial', 9, 'bold')).place(x=10, y=110)
        ttk.Label(control_frame, text="最小値:").place(x=10, y=140)
        y_min_var = tk.StringVar(value=f"{min(y_values):.2f}")
        y_min_entry = ttk.Entry(control_frame, textvariable=y_min_var, width=12)
        y_min_entry.place(x=80, y=140)

        ttk.Label(control_frame, text="最大値:").place(x=10, y=170)
        y_max_var = tk.StringVar(value=f"{max(y_values):.2f}")
        y_max_entry = ttk.Entry(control_frame, textvariable=y_max_var, width=12)
        y_max_entry.place(x=80, y=170)

        # 存储控制变量 / コントロール変数を保存
        setattr(main_frame, 'x_min_var', x_min_var)
        setattr(main_frame, 'x_max_var', x_max_var)
        setattr(main_frame, 'y_min_var', y_min_var)
        setattr(main_frame, 'y_max_var', y_max_var)

        # 更新Y偏移 / Y軸の座標を更新
        y_offset += frame_height + 10

    # 复数绘图 / 重ねグラフの作成
    if len(selected_columns_complex) > 0:
        x_values_overlap = []
        y_values_overlap = []

        for i in range(len(selected_columns_complex)):
            y_values_overlap.append([])

        for i in range(len(original_data[0])):
            x_values_overlap.append(original_data[0][i])
            for j in range(len(selected_columns_complex)):
                y_values_overlap[j].append(original_data[selected_columns_complex[j] + 1][i])

        # 创建主Frame / メインFrameを作成
        main_frame_overlap = ttk.Frame(graph_inner_frame)
        main_frame_overlap.place(x=10, y=y_offset, width=frame_width - 30, height=frame_height)
        graph_frames.append(main_frame_overlap)

        # 创建图表Frame / グラフ用Frameを作成
        graph_frame_overlap = ttk.Frame(main_frame_overlap)
        graph_frame_overlap.place(x=0, y=0, relwidth=0.73, relheight=1)

        # 创建控制Frame / コントロール用Frameを作成
        control_frame_overlap = ttk.Frame(main_frame_overlap)
        control_frame_overlap.place(relx=0.75, y=0, relwidth=0.27, relheight=1)

        # 创建图表 / グラフを作成
        fig_overlap, ax_overlap = plt.subplots(figsize=(7, 4))
        for i in range(len(selected_columns_complex)):
            ax_overlap.plot(x_values_overlap, y_values_overlap[i],
                    marker='o',
                    linestyle='-',
                    color='red',
                    linewidth=2,
                    markersize=5)

        # 设置图表属性 / 軸名と距離の設定
        ax_overlap.set_xlabel("X")
        ax_overlap.set_ylabel("Y")
        plt.subplots_adjust(left=0.15)

        ax_overlap.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(pad=3.0)

        # 嵌入到Frame中 / Frameに追加
        canvas = FigureCanvasTkAgg(fig_overlap, master=graph_frame_overlap)
        canvas.draw()
        canvas.get_tk_widget().place(x=0, y=20, relwidth=1, relheight=0.9)

        # 存储图表对象 / グラフを保存
        setattr(main_frame_overlap, 'figure', fig_overlap)
        setattr(main_frame_overlap, 'axes', ax_overlap)

        # 添加坐标轴控制组件 / コントロール機能を追加
        ttk.Label(control_frame_overlap, text="X軸範囲:", font=('Arial', 9, 'bold')).place(x=10, y=10)
        ttk.Label(control_frame_overlap, text="最小値:").place(x=10, y=40)
        x_min_var = tk.StringVar(value=f"{min(x_values_overlap):.2f}")
        x_min_entry_overlap = ttk.Entry(control_frame_overlap, textvariable=x_min_var, width=12)
        x_min_entry_overlap.place(x=80, y=40)

        ttk.Label(control_frame_overlap, text="最大値:").place(x=10, y=70)
        x_max_var = tk.StringVar(value=f"{max(x_values_overlap):.2f}")
        x_max_entry_overlap = ttk.Entry(control_frame_overlap, textvariable=x_max_var, width=12)
        x_max_entry_overlap.place(x=80, y=70)

        y_min_overlap = 99
        y_max_overlap = 0
        for i in range(len(y_values_overlap)):
            tmp_y_min = min(y_values_overlap[i])
            tmp_y_max = max(y_values_overlap[i])

            if  y_min_overlap > tmp_y_min:
                y_min_overlap = tmp_y_min

            if y_max_overlap < tmp_y_max:
                y_max_overlap = tmp_y_max

        ttk.Label(control_frame_overlap, text="Y軸範囲:", font=('Arial', 9, 'bold')).place(x=10, y=110)
        ttk.Label(control_frame_overlap, text="最小値:").place(x=10, y=140)
        y_min_var = tk.StringVar(value=f"{y_min_overlap:.2f}")
        y_min_entry_overlap = ttk.Entry(control_frame_overlap, textvariable=y_min_var, width=12)
        y_min_entry_overlap.place(x=80, y=140)

        ttk.Label(control_frame_overlap, text="最大値:").place(x=10, y=170)
        y_max_var = tk.StringVar(value=f"{y_max_overlap:.2f}")
        y_max_entry_overlap = ttk.Entry(control_frame_overlap, textvariable=y_max_var, width=12)
        y_max_entry_overlap.place(x=80, y=170)

        # 存储控制变量 / コントロール変数を保存
        setattr(main_frame_overlap, 'x_min_var', x_min_var)
        setattr(main_frame_overlap, 'x_max_var', x_max_var)
        setattr(main_frame_overlap, 'y_min_var', y_min_var)
        setattr(main_frame_overlap, 'y_max_var', y_max_var)

    # 更新滚动区域 / スクロールエリアを更新
    graph_canvas.configure(scrollregion=graph_canvas.bbox("all"))
    graph_canvas.yview_moveto(0)

# グラフを更新
def update_graph_tab2():
    global graph_frames
    for frame in graph_frames:
        try:
            ax = frame.axes

            # 获取输入框的值 / 入力された値を取得
            x_min = float(frame.x_min_var.get())
            x_max = float(frame.x_max_var.get())
            y_min = float(frame.y_min_var.get())
            y_max = float(frame.y_max_var.get())

            # 设置坐标轴范围 / XY軸範囲を更新
            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

            # 重绘图表 / グラフを作り直す
            frame.figure.canvas.draw()

        except ValueError:
            messagebox.showerror("エラー", "数値を入力してください")
            return
        except AttributeError:
            continue

#------------------------------ tab5页面 制作折线图2 / タブ5 グラフ作成2 ---------------------------
canvas_frame_tab3 = tk.Frame(tab5, height=400, width=800)
canvas_frame_tab3.pack(fill=tk.BOTH, expand=True)

# 主容器Canvas / Canvasを宣言
graph_canvas_tab3 = tk.Canvas(canvas_frame_tab3)
graph_canvas_tab3.pack(side='left', fill='both', expand=True)

# 内部Frame用于放置图表 / 内部Frameを宣言(グラフ保存用)
graph_inner_frame_tab3 = ttk.Frame(graph_canvas_tab3)
graph_canvas_tab3.create_window((0, 0),
                                window=graph_inner_frame_tab3,
                                anchor='nw',
                                width=1350)

# 底部控制面板 / 更新ボタンのFrame
bottom_frame_tab3 = tk.Frame(tab5)
bottom_frame_tab3.pack(side=tk.BOTTOM, fill=tk.X)

update_button_tab3 = ttk.Button(bottom_frame_tab3, text="更新", command= lambda :update_graph_tab3())
update_button_tab3.pack(pady=10)
graph_frames_tab3 = []

def draw_graph_tab3():
    global graph_frames_tab3
    selected_columns_left = []
    selected_columns_right = []

    frame_height = 350  # 每个图表Frame的高度 / 各グラフFrameの高さ
    frame_width = 800  # 每个图表Frame的宽度 / 各グラフFrameの幅
    y_offset_tab3 = 10  # 初始Y偏移 / Y方向の移動値

    # 获取选中数据 / 選択されたデータの取得
    for i in range(len(table_data_tab3)):
        item_data = table_data_tab3[i]
        if item_data[0] == "○":
            selected_columns_left.append(i)
        if item_data[1] == "○":
            selected_columns_right.append(i)

    # 清除旧图表 / 既に作成されたグラフをクリア
    for widget in graph_inner_frame_tab3.winfo_children():
        widget.destroy()

    graph_frames_tab3 = []

    if len(selected_columns_left) * len(selected_columns_right) == 0:
        return

    total_height = frame_height + 10
    graph_inner_frame_tab3.configure(height=total_height)

    x_values = []
    y_values_left = []
    y_values_right = []

    for i in range(len(selected_columns_left)):
        y_values_left.append([])

    for i in range(len(selected_columns_right)):
        y_values_right.append([])

    for i in range(len(original_data[0])):
        x_values.append(original_data[0][i])

        for j in range(len(selected_columns_left)):
            y_values_left[j].append(original_data[selected_columns_left[j] + 1][i])

        for j in range(len(selected_columns_right)):
            y_values_right[j].append(original_data[selected_columns_right[j] + 1][i])

    # 创建主Frame / メインFrameを作成
    main_frame_tab3 = ttk.Frame(graph_inner_frame_tab3)
    main_frame_tab3.place(x=10, y=y_offset_tab3, width=frame_width - 30, height=frame_height)
    graph_frames_tab3.append(main_frame_tab3)

    # 创建图表Frame / グラフFrameを宣言
    graph_frame_tab3 = ttk.Frame(main_frame_tab3)
    graph_frame_tab3.place(x=0, y=0, relwidth=0.73, relheight=1)

    # 创建控制Frame / コントロールFrameを宣言
    control_frame_tab3 = ttk.Frame(main_frame_tab3)
    control_frame_tab3.place(relx=0.75, y=0, relwidth=0.27, relheight=1)

    # 创建图表 / グラフ作成
    fig_tab3, ax_left = plt.subplots(figsize=(7, 4))
    ax_right = ax_left.twinx()

    for i in range(len(selected_columns_left)):
        ax_left.plot(x_values, y_values_left[i],
                        marker='o',
                        linestyle='-',
                        color='red',
                        linewidth=2,
                        markersize=5)

    for i in range(len(selected_columns_right)):
        ax_right.plot(x_values, y_values_right[i],
                        marker='o',
                        linestyle='-',
                        color='blue',
                        linewidth=2,
                        markersize=5)

    ax_left.set_xlabel("X")
    ax_left.set_ylabel("Y(L)")
    ax_right.set_ylabel("Y(R)")
    plt.subplots_adjust(left=0.12,right=0.80, bottom=0.15)

    # 嵌入到Frame中 / Frameに追加
    canvas = FigureCanvasTkAgg(fig_tab3, master=graph_frame_tab3)
    canvas.draw()
    canvas.get_tk_widget().place(x=0, y=20, relwidth=1, relheight=0.9)

    # 存储图表对象 / グラフを保存
    setattr(main_frame_tab3, 'figure', fig_tab3)
    setattr(main_frame_tab3, 'axes_left', ax_left)
    setattr(main_frame_tab3, 'axes_right', ax_right)

    # 添加坐标轴控制组件 / 範囲設定機能
    ttk.Label(control_frame_tab3, text="X軸範囲:", font=('Arial', 9, 'bold')).place(x=10, y=10)
    ttk.Label(control_frame_tab3, text="最小値:").place(x=10, y=40)
    x_min_var = tk.StringVar(value=f"{min(x_values):.2f}")
    x_min_entry = ttk.Entry(control_frame_tab3, textvariable=x_min_var, width=12)
    x_min_entry.place(x=80, y=40)

    ttk.Label(control_frame_tab3, text="最大値:").place(x=10, y=70)
    x_max_var = tk.StringVar(value=f"{max(x_values):.2f}")
    x_max_entry_overlap = ttk.Entry(control_frame_tab3, textvariable=x_max_var, width=12)
    x_max_entry_overlap.place(x=80, y=70)

    y_min_left = 999
    y_max_left = -999

    for i in range(len(y_values_left)):
        tmp_y_min = min(y_values_left[i])
        tmp_y_max = max(y_values_left[i])

        if y_min_left > tmp_y_min:
            y_min_left = tmp_y_min

        if y_max_left < tmp_y_max:
            y_max_left = tmp_y_max

    y_min_right = 999
    y_max_right = -999

    for i in range(len(y_values_right)):
        tmp_y_min2 = min(y_values_right[i])
        tmp_y_max2 = max(y_values_right[i])

        if y_min_right > tmp_y_min2:
            y_min_right = tmp_y_min2

        if y_max_right < tmp_y_max2:
            y_max_right = tmp_y_max2

    ttk.Label(control_frame_tab3, text="Y軸(左)範囲:", font=('Arial', 9, 'bold')).place(x=10, y=100)
    ttk.Label(control_frame_tab3, text="最小値:").place(x=10, y=130)
    y_min_var_left = tk.StringVar(value=f"{y_min_left:.2f}")
    y_min_entry_left = ttk.Entry(control_frame_tab3, textvariable=y_min_var_left, width=12)
    y_min_entry_left.place(x=80, y=130)

    ttk.Label(control_frame_tab3, text="最大値:").place(x=10, y=160)
    y_max_var_left = tk.StringVar(value=f"{y_max_left:.2f}")
    y_max_entry_left = ttk.Entry(control_frame_tab3, textvariable=y_max_var_left, width=12)
    y_max_entry_left.place(x=80, y=160)

    ttk.Label(control_frame_tab3, text="Y軸(右)範囲:", font=('Arial', 9, 'bold')).place(x=10, y=190)
    ttk.Label(control_frame_tab3, text="最小値:").place(x=10, y=220)
    y_min_var_right = tk.StringVar(value=f"{y_min_right:.2f}")
    y_min_entry_right = ttk.Entry(control_frame_tab3, textvariable=y_min_var_right, width=12)
    y_min_entry_right.place(x=80, y=220)

    ttk.Label(control_frame_tab3, text="最大値:").place(x=10, y=250)
    y_max_var_right = tk.StringVar(value=f"{y_max_right:.2f}")
    y_max_entry_right = ttk.Entry(control_frame_tab3, textvariable=y_max_var_right, width=12)
    y_max_entry_right.place(x=80, y=250)

    # 存储控制变量 / コントロール変数を保存
    setattr(main_frame_tab3, 'x_min_var', x_min_var)
    setattr(main_frame_tab3, 'x_max_var', x_max_var)
    setattr(main_frame_tab3, 'y_min_var_left', y_min_var_left)
    setattr(main_frame_tab3, 'y_max_var_left', y_max_var_left)
    setattr(main_frame_tab3, 'y_min_var_right', y_min_var_right)
    setattr(main_frame_tab3, 'y_max_var_right', y_max_var_right)

def update_graph_tab3():
    global graph_frames_tab3
    for frame in graph_frames_tab3:
        try:
            ax_left = frame.axes_left
            ax_right = frame.axes_right

            # 获取输入框的值 / 入力された値を取得
            x_min = float(frame.x_min_var.get())
            x_max = float(frame.x_max_var.get())
            y_min_left = float(frame.y_min_var_left.get())
            y_max_left = float(frame.y_max_var_left.get())
            y_min_right = float(frame.y_min_var_right.get())
            y_max_right = float(frame.y_max_var_right.get())

            # 设置坐标轴范围 / XY軸範囲を更新
            ax_left.set_xlim(x_min, x_max)
            ax_left.set_ylim(y_min_left, y_max_left)
            ax_right.set_ylim(y_min_right, y_max_right)

            # 重绘图表 / グラフを作り直す
            frame.figure.canvas.draw()

        except ValueError:
            messagebox.showerror("エラー", "数値を入力してください")
            return
        except AttributeError:
            continue

# 启动主事件循环 / メイン事件のループを起動
root.mainloop()