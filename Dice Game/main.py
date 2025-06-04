import tkinter as tk
from tkinter import ttk
from tkinter import Label
import random
from tkinter import messagebox
from PIL import Image, ImageTk

# 创建主窗口
root = tk.Tk()
root.title("随机掷三个骰子")

# 设置窗口大小
root.geometry("750x600")

# 准备骰子的图像列表
dice_images = {
    1: "dice1.png",
    2: "dice2.png",
    3: "dice3.png",
    4: "dice4.png",
    5: "dice5.png",
    6: "dice6.png"
}

# 用于显示三个骰子的标签
dice_labels = []

play_score = 10000
boss_score = 100000000

# 判断3个点数是否相同
def judge_three_same(array, tmp_score, target_num, input_score):
    if array[0]==array[1] and array[1]==array[2] and target_num == array[0]:
        tmp_score = tmp_score + input_score * 200
    else:
        tmp_score = tmp_score - input_score
    return tmp_score

# 判断总数是否正确
def judge_sum(tmp_score,sum,target_num, input_score, num):
    if sum == target_num:
        tmp_score = tmp_score + input_score * num
    else:
        tmp_score = tmp_score - input_score
    return tmp_score

# 判断次数是否正确
def judge_times(array, tmp_score, target_num, input_score):
    tmp_times =0
    for i in range(3):
        if array[i] == target_num:
            tmp_times = tmp_times + 1

    if tmp_times == 0:
        tmp_score = tmp_score - input_score
    elif tmp_times == 1:
        tmp_score = tmp_score + input_score
    elif tmp_times == 2:
        tmp_score = tmp_score + input_score * 2
    elif tmp_times == 3:
        tmp_score = tmp_score + input_score * 6

    return  tmp_score

def can_convert_to_int(s):
    try:
        int(s)  # 尝试将字符串转换为整数
        return True  # 转换成功，返回 True
    except ValueError:
        return False  # 转换失败，返回 False

# 函数:消除所有输入框
def clear_entry():
    small_entry.delete(0, tk.END)
    large_entry.delete(0, tk.END)
    all_same_entry.delete(0, tk.END)
    three_one_entry.delete(0, tk.END)
    three_two_entry.delete(0, tk.END)
    three_three_entry.delete(0, tk.END)
    three_four_entry.delete(0, tk.END)
    three_five_entry.delete(0, tk.END)
    three_six_entry.delete(0, tk.END)
    sum_four_entry.delete(0, tk.END)
    sum_five_entry.delete(0, tk.END)
    sum_six_entry.delete(0, tk.END)
    sum_seven_entry.delete(0, tk.END)
    sum_eight_entry.delete(0, tk.END)
    sum_nine_entry.delete(0, tk.END)
    sum_ten_entry.delete(0, tk.END)
    sum_eleven_entry.delete(0, tk.END)
    sum_twelve_entry.delete(0, tk.END)
    sum_thirteen_entry.delete(0, tk.END)
    sum_fourteen_entry.delete(0, tk.END)
    sum_fifteen_entry.delete(0, tk.END)
    sum_sixteen_entry.delete(0, tk.END)
    sum_seveteen_entry.delete(0, tk.END)


# 函数：生成随机骰子
def roll_dice():
    global play_score,boss_score
    # 清空之前的图片
    for label in dice_labels:
        label.destroy()

    # 初始化
    input_small = 0
    input_large = 0
    input_all_same = 0
    input_three_one = 0
    input_three_two = 0
    input_three_three = 0
    input_three_four = 0
    input_three_five = 0
    input_three_six = 0
    input_sum_four = 0
    input_sum_five = 0
    input_sum_six = 0
    input_sum_seven = 0
    input_sum_eight = 0
    input_sum_nine = 0
    input_sum_ten = 0
    input_sum_eleven = 0
    input_sum_twelve = 0
    input_sum_thirteen = 0
    input_sum_fourteen = 0
    input_sum_fifteen = 0
    input_sum_sixteen = 0
    input_sum_seventeen = 0
    input_times_one = 0
    input_times_two = 0
    input_times_three = 0
    input_times_four = 0
    input_times_five = 0
    input_times_six = 0

    # 获取投入积分
    if can_convert_to_int(small_entry.get()):
        input_small = int(small_entry.get())

    if can_convert_to_int(large_entry.get()):
        input_large = int(large_entry.get())

    if can_convert_to_int(all_same_entry.get()):
        input_all_same = int(all_same_entry.get())

    if can_convert_to_int(three_one_entry.get()):
        input_three_one = int(three_one_entry.get())

    if can_convert_to_int(three_two_entry.get()):
        input_three_two = int(three_two_entry.get())

    if can_convert_to_int(three_three_entry.get()):
        input_three_three = int(three_three_entry.get())

    if can_convert_to_int(three_four_entry.get()):
        input_three_four = int(three_four_entry.get())

    if can_convert_to_int(three_five_entry.get()):
        input_three_five = int(three_five_entry.get())

    if can_convert_to_int(three_six_entry.get()):
        input_three_six = int(three_six_entry.get())

    if can_convert_to_int(sum_four_entry.get()):
        input_sum_four = int(sum_four_entry.get())

    if can_convert_to_int(sum_five_entry.get()):
        input_sum_five = int(sum_five_entry.get())

    if can_convert_to_int(sum_six_entry.get()):
        input_sum_six = int(sum_six_entry.get())

    if can_convert_to_int(sum_seven_entry.get()):
        input_sum_seven = int(sum_seven_entry.get())

    if can_convert_to_int(sum_eight_entry.get()):
        input_sum_eight = int(sum_eight_entry.get())

    if can_convert_to_int(sum_nine_entry.get()):
        input_sum_nine = int(sum_nine_entry.get())

    if can_convert_to_int(sum_ten_entry.get()):
        input_sum_ten = int(sum_ten_entry.get())

    if can_convert_to_int(sum_eleven_entry.get()):
        input_sum_eleven = int(sum_eleven_entry.get())

    if can_convert_to_int(sum_twelve_entry.get()):
        input_sum_twelve = int(sum_twelve_entry.get())

    if can_convert_to_int(sum_thirteen_entry.get()):
        input_sum_thirteen = int(sum_thirteen_entry.get())

    if can_convert_to_int(sum_fourteen_entry.get()):
        input_sum_fourteen = int(sum_fourteen_entry.get())

    if can_convert_to_int(sum_fifteen_entry.get()):
        input_sum_fifteen = int(sum_fifteen_entry.get())

    if can_convert_to_int(sum_sixteen_entry.get()):
        input_sum_sixteen = int(sum_sixteen_entry.get())

    if can_convert_to_int(sum_seveteen_entry.get()):
        input_sum_seventeen = int(sum_seveteen_entry.get())

    if can_convert_to_int(times_one_entry.get()):
        input_times_one = int(times_one_entry.get())

    if can_convert_to_int(times_two_entry.get()):
        input_times_two = int(times_two_entry.get())

    if can_convert_to_int(times_three_entry.get()):
        input_times_three = int(times_three_entry.get())

    if can_convert_to_int(times_four_entry.get()):
        input_times_four = int(times_four_entry.get())

    if can_convert_to_int(times_five_entry.get()):
        input_times_five = int(times_five_entry.get())

    if can_convert_to_int(times_six_entry.get()):
        input_times_six = int(times_six_entry.get())

    sum_score = 0
    result_array = []
    # 生成3个随机骰子的数字并显示它们的图片
    for i in range(3):
        dice_num = random.randint(1, 6)
        dice_img = Image.open(dice_images[dice_num])
        dice_img = dice_img.resize((100, 100))  # 调整图片大小
        dice_img_tk = ImageTk.PhotoImage(dice_img)

        # 创建标签并使用place精确设置位置
        label = Label(root, image=dice_img_tk)
        # 设置每个骰子的x坐标位置，每个间隔100像素，y坐标为60
        label.place(x=150 * (i + 1), y=60)
        label.image = dice_img_tk  # 保持对图片的引用
        dice_labels.append(label)

        sum_score = sum_score + dice_num
        result_array.append(dice_num)

    # 结果判断
    if input_small + input_large + input_all_same + input_three_one + input_three_two + input_three_three + input_three_four \
        + input_three_five + input_three_six + input_sum_four + input_sum_five + input_sum_six + input_sum_seven + input_sum_eight \
            + input_sum_nine + input_sum_ten + input_sum_eleven + input_sum_twelve + input_sum_thirteen + input_sum_fourteen + input_sum_fifteen \
            + input_sum_sixteen + input_sum_seventeen + input_times_one + input_times_two + input_times_three + input_times_four \
            + input_times_five + input_times_six > play_score:
        messagebox.showinfo("投入积分大于已有积分！")
        clear_entry()
        return

    if input_small > 0:
        if (not (result_array[0] == result_array[1] and result_array[1] == result_array[2])) and  sum_score < 11 :
            play_score = play_score + input_small
        else:
            play_score = play_score - input_small

    if input_large > 0:
        if (not (result_array[0] == result_array[1] and result_array[1] == result_array[2])) and  sum_score > 10 :
            play_score = play_score + input_large
        else:
            play_score = play_score - input_large

    if input_all_same > 0:
        if result_array[0] == result_array[1] and result_array[1] == result_array[2] :
            play_score = play_score + input_all_same * 33
        else:
            play_score = play_score - input_large

    # 豹子判断
    if input_three_one > 0:
        play_score = judge_three_same(result_array,play_score,1,input_three_one)

    if input_three_two > 0:
        play_score = judge_three_same(result_array,play_score,2,input_three_two)

    if input_three_three > 0:
        play_score = judge_three_same(result_array,play_score,3,input_three_three)

    if input_three_four > 0:
        play_score = judge_three_same(result_array,play_score,4,input_three_four)

    if input_three_five > 0:
        play_score = judge_three_same(result_array,play_score,5,input_three_five)

    if input_three_six > 0:
        play_score = judge_three_same(result_array,play_score,6,input_three_six)

    # 总分判断
    if input_sum_four > 0:
        play_score = judge_sum(play_score,sum_score,4,input_sum_four, 60)

    if input_sum_five > 0:
        play_score = judge_sum(play_score,sum_score,5,input_sum_five, 30)

    if input_sum_six > 0:
        play_score = judge_sum(play_score,sum_score,6,input_sum_six, 17)

    if input_sum_seven > 0:
        play_score = judge_sum(play_score,sum_score,7,input_sum_seven, 12)

    if input_sum_eight > 0:
        play_score = judge_sum(play_score,sum_score,8,input_sum_eight, 8)

    if input_sum_nine > 0:
        play_score = judge_sum(play_score,sum_score,9,input_sum_nine, 6)

    if input_sum_ten > 0:
        play_score = judge_sum(play_score,sum_score,10,input_sum_ten, 6)

    if input_sum_eleven > 0:
        play_score = judge_sum(play_score,sum_score,11,input_sum_eleven,6)

    if input_sum_twelve > 0:
        play_score = judge_sum(play_score,sum_score,12,input_sum_twelve, 6)

    if input_sum_thirteen > 0:
        play_score = judge_sum(play_score,sum_score,13,input_sum_thirteen, 8)

    if input_sum_fourteen > 0:
        play_score = judge_sum(play_score,sum_score,14,input_sum_fourteen, 12)

    if input_sum_fifteen > 0:
        play_score = judge_sum(play_score,sum_score,15,input_sum_fifteen, 17)

    if input_sum_sixteen > 0:
        play_score = judge_sum(play_score,sum_score,16,input_sum_sixteen, 30)

    if input_sum_seventeen > 0:
        play_score = judge_sum(play_score,sum_score,17,input_sum_seventeen,60)

    # 出现次数判断
    if input_times_one > 0:
        play_score = judge_times(result_array,play_score,1,input_times_one)

    if input_times_two > 0:
        play_score = judge_times(result_array,play_score,2,input_times_two)

    if input_times_three > 0:
        play_score = judge_times(result_array,play_score,3,input_times_three)

    if input_times_four > 0:
        play_score = judge_times(result_array,play_score,4,input_times_four)

    if input_times_five > 0:
        play_score = judge_times(result_array,play_score,5,input_times_five)

    if input_times_six > 0:
        play_score = judge_times(result_array,play_score,6,input_times_six)

    # 更新分数
    player_score_label.config(text=f"Score: {play_score}")

    boss_score = 100010000-play_score
    boss_score_label.config(text= f"Score: {boss_score}")

    # 判断胜负
    if play_score > 100000000:
        messagebox.showinfo("失败","您获胜了!!")
        play_score = 10000
        boss_score = 100000000
        if player_name_label.cget("text") == "Player":
            player_name_label.config(text="BOSS")
            boss_name_label.config(text="Player")
        else:
            player_name_label.config(text="Player")
            boss_name_label.config(text="BOSS")

        # 更新分数
        player_score_label.config(text=f"Score: {play_score}")

        boss_score = 100010000 - play_score
        boss_score_label.config(text=f"Score: {boss_score}")
    elif play_score == 0:
        messagebox.showinfo("失败","您输光了!!")
        play_score = 10000
        boss_score = 100000000
        # 更新分数
        player_score_label.config(text=f"Score: {play_score}")

        boss_score = 100010000 - play_score
        boss_score_label.config(text=f"Score: {boss_score}")

    clear_entry()

# 玩家分数显示
player_name_label = ttk.Label(root, text="Player",font=("Arial", 14))
player_name_label.place(x=10, y=10)

player_score_label = ttk.Label(root, text="Score: 10000",font=("Arial", 14))
player_score_label.place(x=10,y=35)

# boss分数显示
boss_name_label = ttk.Label(root, text="BOSS",font=("Arial", 14))
boss_name_label.place(x=570, y=10)

boss_score_label = ttk.Label(root, text="Score: 100000000",font=("Arial", 14))
boss_score_label.place(x=570, y=35)


# 结果倍率设置
# 小
small_label_line1 = ttk.Label(root, text="小(4-10)", font=("Arial", 11))
small_label_line2 = ttk.Label(root, text="1:1", font=("Arial", 11))
small_entry = ttk.Entry(root, font=("Arial", 10), width=10)

small_label_line1.place(x=10, y=200)
small_label_line2.place(x=10, y=225)
small_entry.place(x=76,y=200)

# 大
large_label_line1 = ttk.Label(root, text="大(11-17)", font=("Arial", 11))
large_label_line2 = ttk.Label(root, text="1:1", font=("Arial", 11))
large_entry = ttk.Entry(root, font=("Arial", 10), width=10)

large_label_line1.place(x=165, y=200)
large_label_line2.place(x=165, y=225)
large_entry.place(x=237,y=200)

# 豹子
all_same_label_line1 = ttk.Label(root, text="豹子", font=("Arial", 11))
all_same_label_line2 = ttk.Label(root, text="1:33", font=("Arial", 11))
all_same_entry =ttk.Entry(root, font=("Arial", 10), width=10)

all_same_label_line1.place(x=317, y=200)
all_same_label_line2.place(x=317, y=225)
all_same_entry.place(x=370,y=200)

# 1,1,1
three_one_label_line1 = ttk.Label(root, text="1,1,1", font=("Arial", 11))
three_one_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_one_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_one_label_line1.place(x=450, y=200)
three_one_label_line2.place(x=450, y=225)
three_one_entry.place(x=505,y=200)

# 2,2,2
three_two_label_line1 = ttk.Label(root, text="2,2,2", font=("Arial", 11))
three_two_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_two_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_two_label_line1.place(x=585, y=200)
three_two_label_line2.place(x=585, y=225)
three_two_entry.place(x=640,y=200)

# 3,3,3
three_three_label_line1 = ttk.Label(root, text="3,3,3", font=("Arial", 11))
three_three_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_three_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_three_label_line1.place(x=10, y=250)
three_three_label_line2.place(x=10, y=275)
three_three_entry.place(x=76,y=250)

# 4,4,4
three_four_label_line1 = ttk.Label(root, text="4,4,4", font=("Arial", 11))
three_four_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_four_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_four_label_line1.place(x=165, y=250)
three_four_label_line2.place(x=165, y=275)
three_four_entry.place(x=237,y=250)

# 5,5,5
three_five_label_line1 = ttk.Label(root, text="5,5,5", font=("Arial", 11))
three_five_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_five_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_five_label_line1.place(x=317, y=250)
three_five_label_line2.place(x=317, y=275)
three_five_entry.place(x=370,y=250)

# 6,6,6
three_six_label_line1 = ttk.Label(root, text="6,6,6", font=("Arial", 11))
three_six_label_line2 = ttk.Label(root, text="1:200", font=("Arial", 11))
three_six_entry = ttk.Entry(root, font=("Arial", 10), width=10)

three_six_label_line1.place(x=450, y=250)
three_six_label_line2.place(x=450, y=275)
three_six_entry.place(x=505,y=250)

# 合计4
sum_four_label_line1 = ttk.Label(root, text="合计4", font=("Arial", 11))
sum_four_label_line2 = ttk.Label(root, text="1:60", font=("Arial", 11))
sum_four_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_four_label_line1.place(x=10, y=300)
sum_four_label_line2.place(x=10, y=317)
sum_four_entry.place(x=76,y=300)

# 合计5
sum_five_label_line1 = ttk.Label(root, text="合计5", font=("Arial", 11))
sum_five_label_line2 = ttk.Label(root, text="1:30", font=("Arial", 11))
sum_five_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_five_label_line1.place(x=165, y=300)
sum_five_label_line2.place(x=165, y=317)
sum_five_entry.place(x=237,y=300)

# 合计6
sum_six_label_line1 = ttk.Label(root, text="合计6", font=("Arial", 11))
sum_six_label_line2 = ttk.Label(root, text="1:17", font=("Arial", 11))
sum_six_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_six_label_line1.place(x=317, y=300)
sum_six_label_line2.place(x=317, y=317)
sum_six_entry.place(x=370,y=300)

# 合计7
sum_seven_label_line1 = ttk.Label(root, text="合计7", font=("Arial", 11))
sum_seven_label_line2 = ttk.Label(root, text="1:12", font=("Arial", 11))
sum_seven_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_seven_label_line1.place(x=450, y=300)
sum_seven_label_line2.place(x=450, y=317)
sum_seven_entry.place(x=505,y=300)

# 合计8
sum_eight_label_line1 = ttk.Label(root, text="合计8", font=("Arial", 11))
sum_eight_label_line2 = ttk.Label(root, text="1:8", font=("Arial", 11))
sum_eight_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_eight_label_line1.place(x=585, y=300)
sum_eight_label_line2.place(x=585, y=317)
sum_eight_entry.place(x=640,y=300)

# 合计9
sum_nine_label_line1 = ttk.Label(root, text="合计9", font=("Arial", 11))
sum_nine_label_line2 = ttk.Label(root, text="1:6", font=("Arial", 11))
sum_nine_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_nine_label_line1.place(x=10, y=350)
sum_nine_label_line2.place(x=10, y=375)
sum_nine_entry.place(x=76,y=350)

# 合计10
sum_ten_label_line1 = ttk.Label(root, text="合计10", font=("Arial", 11))
sum_ten_label_line2 = ttk.Label(root, text="1:6", font=("Arial", 11))
sum_ten_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_ten_label_line1.place(x=165, y=350)
sum_ten_label_line2.place(x=165, y=375)
sum_ten_entry.place(x=237,y=350)

# 合计11
sum_eleven_label_line1 = ttk.Label(root, text="合计11", font=("Arial", 11))
sum_eleven_label_line2 = ttk.Label(root, text="1:6", font=("Arial", 11))
sum_eleven_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_eleven_label_line1.place(x=317, y=350)
sum_eleven_label_line2.place(x=317, y=375)
sum_eleven_entry.place(x=370,y=350)

# 合计12
sum_twelve_label_line1 = ttk.Label(root, text="合计12", font=("Arial", 11))
sum_twelve_label_line2 = ttk.Label(root, text="1:6", font=("Arial", 11))
sum_twelve_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_twelve_label_line1.place(x=450, y=350)
sum_twelve_label_line2.place(x=450, y=375)
sum_twelve_entry.place(x=505,y=350)

# 合计13
sum_thirteen_label_line1 = ttk.Label(root, text="合计13", font=("Arial", 11))
sum_thirteen_label_line2 = ttk.Label(root, text="1:8", font=("Arial", 11))
sum_thirteen_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_thirteen_label_line1.place(x=585, y=350)
sum_thirteen_label_line2.place(x=585, y=375)
sum_thirteen_entry.place(x=640,y=350)

# 合计14
sum_fourteen_label_line1 = ttk.Label(root, text="合计14", font=("Arial", 11))
sum_fourteen_label_line2 = ttk.Label(root, text="1:12", font=("Arial", 11))
sum_fourteen_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_fourteen_label_line1.place(x=10, y=400)
sum_fourteen_label_line2.place(x=10, y=425)
sum_fourteen_entry.place(x=76,y=400)

# 合计15
sum_fifteen_label_line1 = ttk.Label(root, text="合计15", font=("Arial", 11))
sum_fifteen_label_line2 = ttk.Label(root, text="1:17", font=("Arial", 11))
sum_fifteen_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_fifteen_label_line1.place(x=165, y=400)
sum_fifteen_label_line2.place(x=165, y=425)
sum_fifteen_entry.place(x=237,y=400)

# 合计16
sum_sixteen_label_line1 = ttk.Label(root, text="合计16", font=("Arial", 11))
sum_sixteen_label_line2 = ttk.Label(root, text="1:30", font=("Arial", 11))
sum_sixteen_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_sixteen_label_line1.place(x=317, y=400)
sum_sixteen_label_line2.place(x=317, y=425)
sum_sixteen_entry.place(x=370,y=400)

# 合计17
sum_seveteen_label_line1 = ttk.Label(root, text="合计17", font=("Arial", 11))
sum_seveteen_label_line2 = ttk.Label(root, text="1:60", font=("Arial", 11))
sum_seveteen_entry = ttk.Entry(root, font=("Arial", 10), width=10)

sum_seveteen_label_line1.place(x=450, y=400)
sum_seveteen_label_line2.place(x=450, y=425)
sum_seveteen_entry.place(x=505,y=400)

# 1(1/2/3)
times_one_label_line1 = ttk.Label(root, text="1(1/2/3)", font=("Arial", 11))
times_one_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_one_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_one_label_line1.place(x=10, y=450)
times_one_label_line2.place(x=10, y=475)
times_one_entry.place(x=76,y=450)

# 2(1/2/3)
times_two_label_line1 = ttk.Label(root, text="2(1/2/3)", font=("Arial", 11))
times_two_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_two_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_two_label_line1.place(x=165, y=450)
times_two_label_line2.place(x=165, y=475)
times_two_entry.place(x=237,y=450)

# 3(1/2/3)
times_three_label_line1 = ttk.Label(root, text="3(1/2/3)", font=("Arial", 11))
times_three_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_three_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_three_label_line1.place(x=317, y=450)
times_three_label_line2.place(x=317, y=475)
times_three_entry.place(x=370,y=450)

# 4(1/2/3)
times_four_label_line1 = ttk.Label(root, text="4(1/2/3)", font=("Arial", 11))
times_four_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_four_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_four_label_line1.place(x=450, y=450)
times_four_label_line2.place(x=450, y=475)
times_four_entry.place(x=505,y=450)

# 5(1/2/3)
times_five_label_line1 = ttk.Label(root, text="5(1/2/3)", font=("Arial", 11))
times_five_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_five_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_five_label_line1.place(x=585, y=450)
times_five_label_line2.place(x=585, y=475)
times_five_entry.place(x=640,y=450)

# 6(1/2/3)
times_six_label_line1 = ttk.Label(root, text="6(1/2/3)", font=("Arial", 11))
times_six_label_line2 = ttk.Label(root, text="1:1/2/6", font=("Arial", 11))
times_six_entry = ttk.Entry(root, font=("Arial", 10), width=10)

times_six_label_line1.place(x=10, y=500)
times_six_label_line2.place(x=10, y=525)
times_six_entry.place(x=76,y=500)

# 创建按钮，点击时掷骰子
roll_button = tk.Button(root, text="掷三个骰子", command=roll_dice)
roll_button.place(x=320, y=550)  # 设置按钮的位置


# 运行主循环
root.mainloop()
