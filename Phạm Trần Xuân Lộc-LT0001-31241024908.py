import pygame, sys
from PIL import Image
import random  # Thêm dòng này để sử dụng các chức năng ngẫu nhiên
import math
pygame.mixer.init()  # Khởi tạo hệ thống âm thanh của Pygame
pygame.mixer.music.load('fast-chiptune-instrumental-2-minute-boss-fight-254040.mp3')  # Đảm bảo bạn có file nhạc nền
pygame.mixer.music.set_volume(0.5)  # Điều chỉnh âm lượng nhạc nền
pygame.mixer.music.play(-1, 0.0)  # Phát nhạc nền liên tục (-1)
amplitude = 20  # Biên độ (độ nảy)
frequency = 0.1  # Tần số (tốc độ nảy)
time = 0  # Biến thời gian 
pygame.display.set_caption("3I Transformers") # đặt tên game
logo = pygame.image.load('logo.png') #đặt logo game
pygame.display.set_icon(logo) # hiển thị logo game

# Hàm tải các khung hình từ file GIF
def load_gif_frames(gif_path):
    """Load frames from a GIF file and convert them to Pygame surfaces."""
    gif = Image.open(gif_path)
    frames = []
    for frame in range(gif.n_frames):  # Lặp qua tất cả các frame trong GIF
        gif.seek(frame)
        rgba_frame = gif.convert("RGBA")  # Chuyển đổi sang định dạng RGBA
        frame_surface = pygame.image.frombuffer(
            rgba_frame.tobytes(), rgba_frame.size, "RGBA"
        )
        frames.append(frame_surface)  # Thêm frame vào danh sách
    return frames

# Hàm điều chỉnh vị trí xe nếu vượt quá các giới hạn màn hình
def correction(car, width, height):
    if car.left < 0:
        car.left = 0  # Đảm bảo xe không đi ra ngoài trái màn hình
    elif car.right > width:
        car.right = width  # Đảm bảo xe không đi ra ngoài phải màn hình
    if car.top < 90:
        car.top = 90  # Đảm bảo xe không đi ra ngoài trên màn hình
    elif car.bottom > 709:
        car.bottom = 709  # Đảm bảo xe không đi ra ngoài dưới màn hình

# Hàm khởi động lại game, phục vụ cho mỗi round
def reset_game(round=1):
    """Khởi động lại các biến trạng thái để bắt đầu round mới."""
    global car_health,car_rect, health_bar, collision_count, reward_visible, reward_collected, game_over, in_intro_screen, car, facing_right, in_round_two, in_round_three, dragon_health

    car = pygame.image.load('car.png')  # Tải ảnh xe
    car = pygame.transform.scale(car, (230, 250))  # Thay đổi kích thước xe
    car_rect = car.get_rect(center=(120, 350))  # Đặt vị trí xe
    facing_right = True  # Xe đang đối diện sang phải
    health_bar = car_health_imgs[2]  # Lấy ảnh thanh máu mặc định
    car_health = 3  # Xe có tổng cộng 3 phần máu
    dragon_health = 9  # Máu của con rồng
    fires = []  # Danh sách các đạn bắn ra
    collision_count = 0  # Số lần va chạm
    game_over = False  # Biến trạng thái thua game
    game_won = False  # Biến trạng thái thắng game
    in_intro_screen = False  # Biến trạng thái màn hình intro
    in_round_two = round == 2  # Đặt trạng thái round 2
    in_round_three = round == 3  # Đặt trạng thái round 3
    
# Khởi tạo Pygame
pygame.init()

# Biến điểm số
score = 0

# Font để hiển thị điểm
font = pygame.font.Font("pixel_font.ttf", 32)

# Tạo cửa sổ Pygame
screen = pygame.display.set_mode((1280, 800))  # Kích thước cửa sổ là 1280x800
clock = pygame.time.Clock()  # Khởi tạo đồng hồ game

# Hình nền intro
intro_bg = pygame.image.load('hình-nền-game.png')  # Tải hình nền intro
intro_bg = pygame.transform.scale(intro_bg, (1280, 800))  # Thay đổi kích thước hình nền intro

# Hình nền round 1
bg = pygame.image.load('background.png')  # Tải hình nền round 1
bg = pygame.transform.scale2x(bg)  # Thay đổi kích thước hình nền

# Hình nền khi thua
game_over_bg = pygame.image.load('lose.png')  # Tải hình nền khi thua
game_over_bg = pygame.transform.scale(game_over_bg, (1280, 800))  # Thay đổi kích thước hình nền khi thua

# Hình nền khi thắng
game_won_bg = pygame.image.load('optimus pixel with word _ You Win _.jpg')  # Tải hình nền khi thắng
game_won_bg = pygame.transform.scale(game_won_bg, (1280, 800))  # Thay đổi kích thước hình nền khi thắng

# Hình ảnh xe
car = pygame.image.load('car.png')  # Tải hình ảnh xe
car = pygame.transform.scale(car, (230, 250))  # Thay đổi kích thước xe
car_rect = car.get_rect(center=(120, 350))  # Đặt vị trí ban đầu của xe
car_mask = pygame.mask.from_surface(car)  # Tạo mặt nạ cho xe để kiểm tra va chạm
car_speed = 8  # Tốc độ di chuyển của xe

# Tải thanh máu cho xe trong cả 3 round
car_health_imgs = [pygame.image.load(f'carhealth{i}.png') for i in range(3)]  # Tải ảnh thanh máu
car_health = 3  # Xe có tổng cộng 3 phần máu
health_bar = car_health_imgs[2]  # Lấy thanh máu đầy cho xe
health_bar_rect = health_bar.get_rect(center=(car_rect.centerx, car_rect.top))  # Đặt vị trí thanh máu

# Số lần va chạm (2 round đầu)
collision_count = 0
damage_timer = 0
damage_interval = 500  # Khoảng thời gian giữa các lần va chạm

# Phần thưởng (round 1)
reward_image = pygame.image.load('pixel_art_realistic-2.png.png')  # Tải phần thưởng
reward_image = pygame.transform.scale(reward_image, (150, 150))  # Thay đổi kích thước phần thưởng
reward_rect = reward_image.get_rect(center=(1280 - 60, 400))  # Đặt vị trí phần thưởng
reward_visible = True  # Phần thưởng đang hiển thị
reward_collected = False  # Phần thưởng chưa được nhận

# Tải và xử lý GIF laser (round 2)
laser_frames = load_gif_frames("LaserShot.gif")  # GIF laser

# Thông số về GIF laser (round 2)
laser_info = [
    {"frames": laser_frames, "x": car_rect.centerx, "y": car_rect.top, "speed": 10, "current_frame": 0, "frame_timer": 0},
]

laser_cooldown = 600  # Thời gian giữa các lần bắn laser (giây)
last_laser_time = 0  # Thời gian bắn laser lần cuối
laser_list = []  # Danh sách các laser đang hoạt động

# Tải và xử lý GIF nhân vật (round 2)
gif1_frames = load_gif_frames("2.gif")  # Tải GIF cho nhân vật 1
gif2_frames = load_gif_frames("1.gif")  # Tải GIF cho nhân vật 2
gif3_frames = load_gif_frames("3.gif")  # Tải GIF cho nhân vật 3
gif4_frames = load_gif_frames("4.gif")  # Tải GIF cho nhân vật 4
gif5_frames = load_gif_frames("5.gif")  # Tải GIF cho nhân vật 5

# Thông số về các GIF (round 2)
gif_info = [
    {"frames": gif1_frames, "x": 1280, "y": 185, "speed": -6, "current_frame": 0, "frame_timer": 0, "rect": pygame.Rect(1280, 185, 56, 73)},
    {"frames": gif2_frames, "x": 1280, "y": 440, "speed": -5, "current_frame": 0, "frame_timer": 0, "rect": pygame.Rect(1280, 440, 65, 73)},
    {"frames": gif3_frames, "x": 1280, "y": 538, "speed": -4, "current_frame": 0, "frame_timer": 0, "rect": pygame.Rect(1280, 538, 44, 73)},
    {"frames": gif4_frames, "x": 1280, "y": 280, "speed": -2, "current_frame": 0, "frame_timer": 0, "rect": pygame.Rect(1280, 280, 43, 73)},
    {"frames": gif5_frames, "x": 1280, "y": 363, "speed": -3, "current_frame": 0, "frame_timer": 0, "rect": pygame.Rect(1280, 363, 63, 73)},
]

# Vị trí ngẫu nhiên cho mỗi GIF (round 2)
def get_random_position():
    random_x = random.randint(1280, 1280+200)  # Đảm bảo GIF xuất hiện từ bên phải
    return random_x

# Danh sách lưu trạng thái GIF bị bắn trúng (round 2)
removed_gifs = []

# Tải GIFs cho vật cản (round 1)

obstacle_frames_down_2 = load_gif_frames("nv2(1).gif")
obstacle_frames_up_2 = load_gif_frames("nv2.gif")
obstacle_frames_down_3 = load_gif_frames("nv3.gif")
obstacle_frames_up_3 = load_gif_frames("nv3(1).gif")
obstacle_frames_down_4 = load_gif_frames("nv4.gif")
obstacle_frames_up_4 = load_gif_frames("nv4(1).gif")
obstacle_frames_down_1 = load_gif_frames("nv1.gif")  # Tải GIF vật cản 1
obstacle_frames_up_1 = load_gif_frames("nv1(1).gif")  # Tải GIF vật cản 1 khi ở vị trí khác
# (Tiếp tục tải các vật cản khác...)

# Vật cản (Round 1)
obstacles = []  # Danh sách chứa thông tin của các vật cản
road_top = 120  # Vị trí Y trên cùng của đường
road_bottom = 630  # Vị trí Y dưới cùng của đường
road_center_x = 640  # Tọa độ X trung tâm của đường
obstacle_count = 4  # Số lượng vật cản
vertical_spacing = (road_bottom - road_top) // (obstacle_count + 0.1)  # Khoảng cách dọc giữa các vật cản

# Tạo vật cản
for i in range(obstacle_count):
    start_x = road_center_x + (-1) ** i * 97 * (i + 1)  # Đặt vị trí ngẫu nhiên cho vật cản theo chiều ngang
    start_y = road_bottom - (i + 1) * vertical_spacing  # Đặt vị trí dọc cho vật cản
    direction = 1

    # Cập nhật các frames của từng vật cản
    if i == 0:
        frames_down = obstacle_frames_down_1
        frames_up = obstacle_frames_up_1
    elif i == 1:
        frames_down = obstacle_frames_down_2
        frames_up = obstacle_frames_up_2
    elif i == 2:
        frames_down = obstacle_frames_down_3
        frames_up = obstacle_frames_up_3
    else:
        frames_down = obstacle_frames_down_4
        frames_up = obstacle_frames_up_4

    obstacle_surface = frames_down[0]  # Lấy frame đầu tiên của vật cản
    obstacle_mask = pygame.mask.from_surface(obstacle_surface)  # Tạo mặt nạ cho vật cản để kiểm tra va chạm

    obstacles.append({
        "rect": obstacle_surface.get_rect(center=(start_x + 75, start_y + 100)),  # Vị trí vật cản
        "mask": obstacle_mask,  # Mặt nạ vật cản
        "direction": direction,  # Hướng di chuyển của vật cản
        "speed": 1,  # Tốc độ di chuyển của vật cản
        "frames_down": frames_down,  # Các frames vật cản khi xuống
        "frames_up": frames_up,  # Các frames vật cản khi lên
        "current_frame_index": 0,  # Chỉ số frame hiện tại
        "frames": frames_down  # Lấy các frame khi vật cản đang xuống
    })

# Biến trạng thái
in_intro_screen = True  # Màn hình intro
game_over = False  # Trạng thái thua game
game_won = False  # Trạng thái thắng game
frame_delay = 100  # Độ trễ giữa các frame
facing_right = True  # Xe đang hướng sang phải
reward_active = False  # Phần thưởng chưa được kích hoạt

# Đặt biến trạng thái cho từng vòng
in_round_one = True
in_round_two = False
in_round_three = False

#GIF round 3
dragon_frames = load_gif_frames("dragon.gif")
fire_frames = load_gif_frames("fire.gif")

# Tải thanh máu cho rồng (9 phần máu) (round 3)
health_bar_imgs = [pygame.image.load(f'health{i}.png') for i in range(9)]
fires = []
fire_speed = -5  # Tốc độ di chuyển của lửa
fire_interval = 1500  # Thời gian giữa các lần bắn lửa (ms)
last_fire_time = pygame.time.get_ticks()

# Rồng và lửa (round 3)
y_pos = 90  # Bắt đầu từ vị trí 90 (Vị trí ban đầu của rồng trên trục Y)
y_velocity = 3  # Tốc độ di chuyển của rồng (Rồng sẽ di chuyển với tốc độ 3 pixel mỗi lần cập nhật)
frame_index = 0  # Chỉ số frame hiện tại của rồng (Dùng để xác định frame nào đang được hiển thị trong GIF của rồng)
last_update_time = pygame.time.get_ticks()  # Thời gian của lần cập nhật cuối cùng (Lấy thời gian hiện tại để quản lý tốc độ cập nhật frame)

# Máu của rồng(round 3)
dragon_health = 9  # Tổng cộng 9 phần máu


# Vòng lặp game chính
running = True  # Biến để duy trì vòng lặp trò chơi
while running:  # Vòng lặp chính của trò chơi
    current_time = pygame.time.get_ticks()  # Lấy thời gian hiện tại theo mili giây

    # Điều chỉnh độ trễ giữa các frame tùy thuộc vào vòng chơi
    if in_round_one:
        frame_delay = 100  # Đặt giá trị frame_delay cho Round 1 (100 ms giữa các frame)
    elif in_round_two:
        frame_delay = 5  # Đặt giá trị frame_delay cho Round 2 (5 ms giữa các frame, làm cho game nhanh hơn)
    elif in_round_three:
        frame_delay = 100  # Đặt giá trị frame_delay cho Round 3 (100 ms giữa các frame)

    for event in pygame.event.get():  # Lấy tất cả sự kiện từ Pygame
        if event.type == pygame.QUIT:  # Kiểm tra sự kiện đóng cửa sổ trò chơi
            running = False  # Dừng vòng lặp game
            pygame.quit()  # Đóng thư viện pygame
            sys.exit()  # Thoát chương trình
        if event.type == pygame.KEYDOWN:  # Kiểm tra khi một phím được nhấn
            if in_intro_screen and event.key == pygame.K_SPACE:  # Nếu đang ở màn hình intro và nhấn SPACE
                in_intro_screen = False  # Chuyển sang trạng thái không phải màn hình intro
            elif game_over and event.key == pygame.K_RETURN:  # Nếu game over và nhấn Enter
                in_round_two = False  # Đảm bảo vòng 2 bị dừng lại
                in_round_three = False  # Đảm bảo vòng 3 bị dừng lại
                in_round_one = True  # Đảm bảo vòng 1 được bắt đầu lại
                car_health = 3  # Reset lại máu xe về 3
                score = 0  # Reset lại điểm số về 0
                reset_game(round=1)  # Gọi hàm reset game về vòng 1
                game_over = False  # Đặt trạng thái game_over là False
            elif game_won and event.key == pygame.K_RETURN:  # Nếu thắng game và nhấn Enter
                in_round_three = False  # Đảm bảo vòng 3 bị dừng lại
                in_round_one = True  # Đảm bảo vòng 1 được bắt đầu lại
                car_health = 3  # Reset lại máu xe về 3
                score = 0  # Reset lại điểm số về 0
                reset_game(round=1)  # Gọi hàm reset game về vòng 1
                game_won = False  # Đặt trạng thái game_won là False
                
    if in_intro_screen: ## Kiểm tra nếu đang ở màn hình intro
        screen.blit(intro_bg, (0, 0))  # Vẽ nền màn hình intro

    # Tính toán vị trí y của chữ "PRESS SPACE TO START" để tạo hiệu ứng nhảy
        y_pos = screen.get_height() - 70 + int(amplitude * math.sin(frequency * time))  # Vị trí y của chữ "nảy"

        # Vẽ chữ "PRESS SPACE TO START" ở giữa màn hình
        font = pygame.font.Font('pixel_font.ttf', 50)  # Tạo font chữ pixel từ file font đã tải
        text_surface = font.render("PRESS SPACE TO START", True, (255, 255, 255))  # Render chữ với màu trắng
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2+50, y_pos))  # Vị trí chữ đã có hiệu ứng nảy
        screen.blit(text_surface, text_rect)  # Vẽ chữ lên màn hình

        # Cập nhật thời gian cho hiệu ứng
        time += 1  # Tăng biến thời gian để hiệu ứng nảy hoạt động
    elif game_over:  # Kiểm tra nếu đang ở màn hình game over

        laser_list.clear()  # Xóa tất cả các laser
        fires.clear()  # Xóa tất cả lửa
        screen.blit(game_over_bg, (0, 0))  # Vẽ nền màn hình game over

        
        # Hiệu ứng nhảy cho chữ "PRESS ENTER TO START AGAIN" (chia thành 2 dòng)
        y_pos_game_over_line1 = screen.get_height() - 750 + int(amplitude * math.sin(frequency * time))  # Vị trí y của dòng 1
        y_pos_game_over_line2 = screen.get_height() - 700 + int(amplitude * math.sin(frequency * time))  # Vị trí y của dòng 2

        # Font chữ cho cả hai dòng
        font = pygame.font.Font('pixel_font.ttf', 30) # Tạo font chữ từ file pixel_font.ttf với kích thước 30

        # Dòng 1
        text_surface1 = font.render("PRESS ENTER TO", True, (255, 0, 0)) # Render dòng 1 với màu đỏ
        text_rect1 = text_surface1.get_rect(center=(screen.get_width() // 2 , y_pos_game_over_line1))  # Vị trí chữ dòng 1
        screen.blit(text_surface1, text_rect1)  # Vẽ dòng 1 lên màn hình

        # Dòng 2
        text_surface2 = font.render("START AGAIN", True, (255, 0, 0))  # Render dòng 2 với màu đỏ
        text_rect2 = text_surface2.get_rect(center=(screen.get_width() // 2 , y_pos_game_over_line2))  # Vị trí chữ dòng 2
        screen.blit(text_surface2, text_rect2)  # Vẽ dòng 2 lên màn hình

        # Cập nhật thời gian cho hiệu ứng
        time += 1  # Tăng biến thời gian để hiệu ứng nảy hoạt động
    elif game_won:  # Kiểm tra nếu trò chơi đã thắng
        screen.blit(game_won_bg, (0, 0))  # Vẽ nền màn hình khi thắng trò chơi

        # Tính toán vị trí y của chữ "PRESS SPACE TO START" để tạo hiệu ứng nhảy
        y_pos = screen.get_height() - 70 + int(amplitude * math.sin(frequency * time))  # Vị trí y của chữ "nảy"

        # Vẽ chữ "PRESS SPACE TO START" ở giữa màn hình
        font = pygame.font.Font('pixel_font.ttf', 45)  # Tạo font chữ pixel từ file font đã tải
        text_surface = font.render("PRESS ENTER TO START AGAIN ", True, (255, 255, 255))  # Render chữ với màu trắng
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2+50, y_pos))  # Vị trí chữ đã có hiệu ứng nảy
        screen.blit(text_surface, text_rect)  # Vẽ chữ lên màn hình

        # Cập nhật thời gian cho hiệu ứng
        time += 1  # Tăng biến thời gian để hiệu ứng nảy hoạt động

    elif in_round_two:  # Kiểm tra nếu đang ở vòng 2
    # Duyệt qua tất cả các đối tượng GIF trong danh sách gif_info
        for gif in gif_info[:]:  # Sao chép danh sách để tránh lỗi khi xóa
        # Tạo một đối tượng Rect từ thông tin của GIF (vị trí và kích thước)
            gif_rect = pygame.Rect(gif["x"], gif["y"], gif["frames"][0].get_width(), gif["frames"][0].get_height())
        
        # Kiểm tra va chạm giữa xe và GIF
        if car_rect.colliderect(gif_rect):
            # Kiểm tra xem vùng va chạm có thực sự xảy ra giữa xe và GIF hay không (dùng mask để so sánh)
            if car_mask.overlap(gif["mask"], (gif_rect.x - car_rect.x, gif_rect.y - car_rect.y)):
                # Kiểm tra thời gian để tránh việc bị trừ máu quá nhanh
                if current_time - damage_timer >= damage_interval:
                    damage_timer = current_time  # Cập nhật thời gian để tính lại
                    car_health -= 1  # Giảm máu xe khi va chạm
                    car_rect.x -= 100  # Lùi xe sau khi va chạm (di chuyển xe về phía trái)
                    
                    # Cập nhật thanh máu của xe
                    if car_health >= 0:
                        health_bar = car_health_imgs[car_health-1]  # Cập nhật thanh máu với số lượng máu còn lại

                # Kiểm tra nếu xe hết máu
                if car_health <= 0:
                    health_bar = car_health_imgs[0]  # Hiển thị thanh máu trống (xe không còn máu)
                    game_over = True  # Đặt trạng thái game_over là True để chuyển sang màn hình game over
        
        # Vẽ nền màn hình round 2
        screen.blit(bg, (0, 0))  # Vẽ nền của màn hình round 2 (bg là ảnh nền)

        # Cập nhật vị trí của thanh máu
        health_bar_rect.centerx = car_rect.centerx  # Đặt vị trí trung tâm của thanh máu trùng với trung tâm của xe
        health_bar_rect.bottom = car_rect.top + 70  # Đặt vị trí của thanh máu cách đầu xe 70 pixel

        # Vẽ thanh máu lên màn hình
        screen.blit(health_bar, health_bar_rect)  # Vẽ thanh máu ở vị trí đã cập nhật lên màn hình
    # Điều khiển xe
        keys = pygame.key.get_pressed() # Lấy trạng thái các phím bấm hiện tại
        if keys[pygame.K_UP]:
            car_rect.y -= car_speed # Giảm y để di chuyển lên (y càng nhỏ thì xe càng di chuyển lên)
    # Điều khiển di chuyển xe xuống (phím mũi tên xuống)
        if keys[pygame.K_DOWN]:
            car_rect.y += car_speed # Tăng y để di chuyển xuống
    # Điều khiển di chuyển xe sang trái (phím mũi tên trái)
        if keys[pygame.K_LEFT]:
            car_rect.x -= car_speed # Giảm x để di chuyển sang trái
            if facing_right:  # Nếu xe đang đối diện sang phải
                car = pygame.transform.flip(car, True, False) # Lật xe theo chiều ngang
                facing_right = False # Đánh dấu xe đang hướng sang trái
        if keys[pygame.K_RIGHT]:
            car_rect.x += car_speed # Tăng x để di chuyển sang phải
            if not facing_right: # Nếu xe đang đối diện sang trái
                car = pygame.transform.flip(car, True, False) # Lật xe theo chiều ngang
                facing_right = True  # Đánh dấu xe đang hướng sang phải

        # Điều chỉnh vị trí xe trong giới hạn
        correction(car_rect, 1280, 800)  # Hàm correction đảm bảo xe không ra khỏi màn hình (độ rộng 1280 và chiều cao 800)

        
        # Vẽ xe
        screen.blit(car, car_rect)
        # Cập nhật vị trí và frame cho tất cả các GIF
        for gif in gif_info[:]:  # Sao chép danh sách để tránh lỗi khi xóa
            gif["x"] += gif["speed"] # Cập nhật vị trí của GIF theo tốc độ của nó

        # Khi GIF ra khỏi màn hình bên trái, reset lại vị trí x ngẫu nhiên từ bên phải màn hình
            if gif["x"] < -100:  # Nếu GIF đã ra ngoài màn hình ở bên trái
                gif["x"] = get_random_position()  # Cập nhật lại vị trí ngẫu nhiên khi ra khỏi màn hình

        # Cập nhật frame
            gif["frame_timer"] += 1                     # Tăng bộ đếm thời gian của frame
            if gif["frame_timer"] >= frame_delay:       # Nếu đủ thời gian để chuyển frame
                gif["frame_timer"] = 0                  # Reset bộ đếm thời gian
                gif["current_frame"] = (gif["current_frame"] + 1) % len(gif["frames"]) # Chuyển sang frame kế tiếp, vòng lại khi hết frame
        # Tạo surface cho frame hiện tại
            gif_surface = gif["frames"][gif["current_frame"]] # Lấy frame hiện tại
            gif_rect = gif_surface.get_rect(topleft=(gif["x"], gif["y"]))  # Lấy rectangle của GIF tại vị trí (x, y)
    
        # Thêm mask cho GIF
            gif["mask"] = pygame.mask.from_surface(gif_surface)  # Tạo mask từ frame hiện tại

        # Vẽ GIF lên màn hình
            screen.blit(gif_surface, gif_rect)
            
            # Kiểm tra va chạm với laser
            for laser in laser_list[:]: # Duyệt qua tất cả các laser trong danh sách
                if laser["rect"].colliderect(gif_rect): # Kiểm tra xem laser có va chạm với GIF không
                    if gif in gif_info:  # Kiểm tra GIF vẫn tồn tại trong danh sách
                        removed_gifs.append({"gif": gif, "remove_time": current_time}) # Thêm GIF vào danh sách bị xóa và lưu thời gian xóa
                        gif_info.remove(gif)  # Xóa GIF nếu bị va chạm
                    if laser in laser_list:  # Kiểm tra laser vẫn tồn tại trước khi xóa
                        laser_list.remove(laser)  # Xóa laser sau va chạm
                    score += 200 # Tăng điểm cho người chơi khi laser va chạm với GIF

            # Giới hạn điểm tối đa của vòng 2
            if in_round_two and score > 4000:
                score = 4000

            # Vẽ điểm
            score_text = font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_text, (120, 1))
            # Khôi phục các GIF sau 1 giây
        for removed in removed_gifs[:]:  # Duyệt danh sách GIF bị xóa
            if current_time - removed["remove_time"] >= 1:  # Nếu đã đủ 1 giây
                new_gif = removed["gif"]
                new_gif["x"] = get_random_position()  # Cập nhật vị trí mới
                gif_info.append(new_gif)  # Thêm lại vào danh sách chính
                removed_gifs.remove(removed)  # Xóa khỏi danh sách tạm thời
                
    # Tự động bắn laser mỗi 0.5 giây
        if current_time - last_laser_time >= laser_cooldown: # Kiểm tra xem đã đủ thời gian để bắn laser chưa (0.5 giây)
            last_laser_time = current_time  # Cập nhật thời gian bắn laser để tránh bắn quá nhanh
            # Thêm laser vào danh sách laser_list, mỗi laser có rect, chỉ số frame, và bộ đếm thời gian cho frame
            laser_rect = pygame.Rect(car_rect.centerx + 0, car_rect.top + 110, laser_frames[0].get_width(), laser_frames[0].get_height())
            laser_list.append({"rect": laser_rect, "frame_index": 0, "frame_timer": 0})

    # Cập nhật và vẽ laser
        for laser in laser_list[:]: # Duyệt qua từng laser trong danh sách laser_list
            laser["rect"].x += 10 if facing_right else -10  # Laser di chuyển theo hướng xe
            laser["frame_timer"] += 1 # Tăng bộ đếm thời gian của frame
            # Kiểm tra nếu đã đủ thời gian để chuyển sang frame kế tiếp
            if laser["frame_timer"] >= frame_delay:
                laser["frame_timer"] = 0  # Reset bộ đếm thời gian
                laser["frame_index"] = (laser["frame_index"] + 1) % len(laser_frames) # Chuyển sang frame kế tiếp, vòng lại nếu hết

        # Vẽ laser
            screen.blit(laser_frames[laser["frame_index"]], laser["rect"])

        # Xóa laser nếu ra khỏi màn hình
            if laser["rect"].right < 0 or laser["rect"].left > 1280:
                laser_list.remove(laser) # Nếu laser ra khỏi màn hình, xóa nó khỏi danh sách laser
            # Chuyển sang vòng 3 khi điểm số đạt đủ yêu cầu
            in_round_one=False
            if score >= 4000 and not in_round_three:
                in_round_two = False # Dừng vòng 2
                in_round_three = True # Bắt đầu vòng 3
                reset_game(round=3)  # Gọi reset_game để chuyển sang vòng 3
                
    elif in_round_three:
        screen.blit(bg, (0, 0)) # Vẽ nền màn hình
        keys = pygame.key.get_pressed() # Lấy thông tin về các phím được nhấn
         

        if keys[pygame.K_UP]:
            car_rect.y -= car_speed # Di chuyển lên
        if keys[pygame.K_DOWN]:
            car_rect.y += car_speed # Di chuyển xuống
        if keys[pygame.K_LEFT]:
            car_rect.x -= car_speed # Di chuyển qua trái
            if facing_right:
                car = pygame.transform.flip(car, True, False) # Lật xe nếu đang hướng phải
                facing_right = False
        if keys[pygame.K_RIGHT]:
            car_rect.x += car_speed # Di chuyển qua phải
            if not facing_right:
                car = pygame.transform.flip(car, True, False)
                facing_right = True
        correction(car_rect, 1280, 800) # Điều chỉnh vị trí xe trong giới hạn
         
        # Vẽ xe
        screen.blit(car, car_rect)

         # Nếu rồng vẫn còn máu, tiếp tục di chuyển và vẽ rồng
        if dragon_health > 0:
        # Cập nhật vị trí GIF (rồng)
            y_pos += y_velocity # Cập nhật vị trí y của rồng

        # Giới hạn rồng trong phạm vi từ 90 đến 701
            if y_pos < 150:
                y_pos = 150 # Đặt vị trí y nếu quá thấp
                y_velocity *= -1  # Đổi chiều di chuyển
            elif y_pos + dragon_frames[0].get_height() > 630:
                y_pos = 630 - dragon_frames[0].get_height() # Đặt vị trí y nếu quá cao
                y_velocity *= -1  # Đổi chiều di chuyển

        # Cập nhật khung hình rồng
            if current_time - last_update_time > frame_delay:
                frame_index = (frame_index + 1) % len(dragon_frames) # Lấy frame kế tiếp theo vòng
                last_update_time = current_time # Cập nhật thời gian để tính cho frame tiếp theo

        # Vẽ rồng
            dragon_rect = pygame.Rect(
                1280 - dragon_frames[0].get_width(), # Đặt rồng ở bên phải màn hình
                y_pos,  # Vị trí y của rồng
                dragon_frames[0].get_width(), # Chiều rộng của rồng
                dragon_frames[0].get_height(), # Chiều cao của rồng
            )
            screen.blit(dragon_frames[frame_index], dragon_rect.topleft) # Vẽ khung hình của rồng

        # Vẽ thanh máu trên đầu rồng 
            health_bar_x = dragon_rect.centerx - health_bar_imgs[0].get_width() // 2 - 30 # Đặt vị trí x của thanh máu (canh giữa và điều chỉnh khoảng cách)
            health_bar_y = dragon_rect.top - 5 - health_bar_imgs[0].get_height() # Đặt vị trí y của thanh máu (ở trên đầu rồng)
            screen.blit(health_bar_imgs[dragon_health - 1], (health_bar_x, health_bar_y)) # Vẽ thanh máu trên màn hình tại vị trí đã tính

        # Kiểm tra thời gian xuất hiện lửa
        if current_time - last_fire_time > fire_interval and dragon_health > 0:
            fire_width, fire_height = fire_frames[0].get_size() # Lấy kích thước của lửa
            fire_x_pos = 1280 - dragon_frames[0].get_width() + 20 # Xác định vị trí x của lửa, cách rồng một khoảng nhất định
            fire_y_pos = y_pos + dragon_frames[0].get_height() // 2 # Xác định vị trí y của lửa, giữa thân rồng
            fires.append({"x": fire_x_pos, "y": fire_y_pos, "frame_index": 0})  # Thêm lửa vào danh sách fires
            last_fire_time = current_time # Cập nhật thời gian của lần xuất hiện lửa này
        # Cập nhật và vẽ lửa
        for fire in fires[:]:  # Duyệt qua danh sách các lửa
            fire["x"] += fire_speed  # Di chuyển lửa theo chiều x
            fire["frame_index"] = (fire["frame_index"] + 1) % len(fire_frames) # Cập nhật frame của lửa (đổi khung hình liên tục)

            fire_rect = pygame.Rect(fire["x"], fire["y"], fire_frames[0].get_width(), fire_frames[0].get_height()) # Tạo khung cho lửa
            fire_mask = pygame.mask.from_surface(fire_frames[fire["frame_index"]])  # Tạo mặt nạ cho lửa dựa trên khung hình hiện tại
            # Kiểm tra va chạm giữa xe và lửa
            if car_mask.overlap(fire_mask, (fire["x"] - car_rect.x, fire["y"] - car_rect.y)):
                fires.remove(fire) # Nếu có va chạm, xóa lửa
                car_health -= 1  # Giảm máu xe
            # Vẽ lửa lên màn hình
            screen.blit(fire_frames[fire["frame_index"]], (fire["x"], fire["y"]))
            # Nếu lửa ra ngoài màn hình, xóa nó
            if fire["x"] < 0:
                fires.remove(fire)
        # Vẽ thanh máu của xe
        if car_health > 0:
            car_health_x = car_rect.centerx - car_health_imgs[0].get_width() // 2  # Đặt vị trí x của thanh máu xe
            car_health_y = car_rect.top - 2  # Đặt vị trí y của thanh máu xe
            screen.blit(car_health_imgs[car_health -1 ], (car_health_x, car_health_y))  # Vẽ thanh máu lên màn hình
        else:
            # Khi xe chết, dừng việc bắn laser hiển thị hình ảnh khi xe chết

            screen.blit(game_over_bg, (1280 // 2 - game_over_bg.get_width() // 2, 800 // 2 - game_over_bg.get_height() // 2))  # Vẽ nền game over
            game_over = True  # Đánh dấu game đã kết thúc
             
        # Tự động bắn laser
        if current_time - last_laser_time >= laser_cooldown:
            last_laser_time = current_time # Cập nhật thời gian sau khi bắn laser
            laser_rect = pygame.Rect(
                car_rect.centerx, car_rect.top + 110,  # Vị trí bắn laser từ trên đầu xe
                laser_frames[0].get_width(), laser_frames[0].get_height() # Kích thước laser
            )
            laser_list.append({"rect": laser_rect, "frame_index": 0, "frame_timer": 0}) # Thêm laser vào danh sách


        # Cập nhật và vẽ laser
        for laser in laser_list[:]:
            laser["rect"].x += 10 if facing_right else -10  # Di chuyển laser theo hướng xe
            laser["frame_timer"] += 1 # Cập nhật thời gian của laser
            if laser["frame_timer"] >= 4:  # Nếu frame đã đủ, thay đổi khung hình của laser
                laser["frame_timer"] = 0
                laser["frame_index"] = (laser["frame_index"] + 1) % len(laser_frames)

            if dragon_health > 0 and laser["rect"].colliderect(dragon_rect):
                laser_list.remove(laser) # Xóa laser sau khi va chạm với rồng
                dragon_health -= 1  # Giảm máu rồng
                continue # Tiếp tục với laser tiếp theo

            screen.blit(laser_frames[laser["frame_index"]], laser["rect"]) # Vẽ laser lên màn hình

            if laser["rect"].right < 0 or laser["rect"].left > 1280:
                laser_list.remove(laser)  # Nếu laser ra khỏi màn hình, xóa nó
        
        # Nếu rồng chết
        if dragon_health == 0:
        # Hiển thị hình ảnh khi rồng bị đánh bại
            game_won = True
    else:
        # Vẽ hình nền
        screen.blit(bg, (0, 0))

        # Cập nhật và vẽ vật cản
        for obstacle in obstacles:
            obstacle["rect"].y += obstacle["speed"] * obstacle["direction"]  # Di chuyển vật cản theo trục y (tốc độ * hướng)

            if obstacle["rect"].bottom >= road_bottom: # Kiểm tra nếu vật cản chạm giới hạn dưới
                obstacle["direction"] = -1  # Đảo ngược hướng di chuyển (đi lên)
                obstacle["frames"] = obstacle["frames_up"] # Chuyển sang danh sách khung hình đi lên
            elif obstacle["rect"].top <= road_top:  # Kiểm tra nếu vật cản chạm giới hạn trên
                obstacle["direction"] = 1 # Đảo ngược hướng di chuyển (đi xuống)
                obstacle["frames"] = obstacle["frames_down"] # Chuyển sang danh sách khung hình đi xuống

            obstacle["current_frame_index"] = (pygame.time.get_ticks() // frame_delay) % len(obstacle["frames"]) # Cập nhật khung hình hiện tại dựa trên thời gian
            current_frame_image = obstacle["frames"][obstacle["current_frame_index"]] # Lấy khung hình hiện tại

            screen.blit(current_frame_image, obstacle["rect"]) #Vẽ vật cản  

        # Kiểm tra va chạm giữa xe và vật cản
        for obstacle in obstacles:
            if car_rect.colliderect(obstacle["rect"]): # Kiểm tra va chạm với vật cản
                if car_mask.overlap(obstacle["mask"], (obstacle["rect"].x - car_rect.x, obstacle["rect"].y - car_rect.y)): # Va chạm với mặt nạ
                    if current_time - damage_timer >= damage_interval:  # Đảm bảo không bị trừ máu liên tục
                        damage_timer = current_time
                        car_health -= 1  # Giảm máu xe 
                        car_rect.x -= 100 # Lùi lại 100 pixel khi va chạm
 
        # Cập nhật hình ảnh thanh máu
                        if car_health > 0:
                            health_bar = car_health_imgs[car_health - 1]
                        else:
                            health_bar = car_health_imgs[0]
                            game_over = True  # Kết thúc game nếu hết máu

        # Kiểm tra khi xe nhận phần thưởng
        if car_rect.colliderect(reward_rect) and reward_visible:
            
            reward_collected = True
            reward_visible = False
            reward_active = True  # Kích hoạt trạng thái phần thưởng
            score_added = False  # Đặt lại trạng thái cộng điểm

        # Kiểm tra khi xe đi qua x = 400
        if reward_active:
            
            if car_rect.left <= 50 and not score_added:
               
                score += 250 # Cộng điểm
                if in_round_one and score > 1000:
                    score = 1000
                score_added = True
                reward_active = False  # Tắt trạng thái phần thưởng

        # Khi xe rời khỏi giới hạn phần thưởng, phần thưởng xuất hiện trở lại
        if not car_rect.colliderect(reward_rect) and not reward_visible:
            reward_visible = True
            reward_collected = False

        # Vẽ phần thưởng
        if reward_visible:
            screen.blit(reward_image, reward_rect)

        # Vẽ xe
        screen.blit(car, car_rect)

        # Vẽ thanh máu
        health_bar_rect.centerx = car_rect.centerx # vị trí trung tâm của xe
        health_bar_rect.bottom = car_rect.top + 70 #vị trí trên của xe
        screen.blit(health_bar, health_bar_rect)

        # Hiển thị điểm
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (120, 1))

        # Điều khiển xe
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            car_rect.y -= car_speed
        if keys[pygame.K_DOWN]:
            car_rect.y += car_speed
        if keys[pygame.K_LEFT]:
            car_rect.x -= car_speed
            if facing_right:
                car = pygame.transform.flip(car, True, False)
                facing_right = False
        if keys[pygame.K_RIGHT]:
            car_rect.x += car_speed
            if not facing_right:
                car = pygame.transform.flip(car, True, False)
                facing_right = True
        # Điều chỉnh vị trí xe trong giới hạn
        correction(car_rect, 1280, 800)
        # Kiểm tra nếu điểm đạt 1000
        if score >= 1000 and not in_round_two:
            in_round_one = False
            in_round_two = True
            reset_game(round=2)  # Transition to round 2   
    pygame.display.update()
    clock.tick(120)