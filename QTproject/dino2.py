import arcade
import random
import os

# Настройки экрана
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Dino Game"

# Физика и движение
GRAVITY = 0.95
JUMP_SPEED = 30
MOVE_SPEED = 10


# Функция для корректных путей к ресурсам
def resource_path(relative_path):
    return os.path.join(os.path.abspath("."), relative_path)


class DinoGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_list = None
        self.obstacle_list = None
        self.ground_list = None
        self.game_over_list = None
        self.player = None

        self.game_over = False
        self.score = 0.0

        self.move_speed = MOVE_SPEED
        self.acceleration = 0.005  # плавное ускорение

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.obstacle_list = arcade.SpriteList()
        self.ground_list = arcade.SpriteList()
        self.game_over_list = arcade.SpriteList()

        # Земля
        for i in range(0, 2050, 135):
            ground = arcade.Sprite(resource_path("assets/floor.jpg"), scale=0.3)
            ground.center_x = i + 32
            ground.center_y = 50
            self.ground_list.append(ground)

        # Игрок
        self.player = arcade.Sprite(resource_path("assets/player.png"), scale=1)
        self.player.center_x = 300
        self.player.center_y = 60
        self.player_list.append(self.player)

        # Game Over
        game_over_sprite = arcade.Sprite(resource_path("assets/gameover.png"), scale=3)
        game_over_sprite.center_x = SCREEN_WIDTH // 2
        game_over_sprite.center_y = SCREEN_HEIGHT // 1.5
        self.game_over_list.append(game_over_sprite)

        # Физика
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player, self.ground_list, gravity_constant=GRAVITY
        )

        # Кактусы
        self.cactus_images = [
            resource_path("assets/cactus1.png"),
            resource_path("assets/cactus2.png"),
            resource_path("assets/cactus3.jpg"),
            resource_path("assets/cactus4.png"),
            resource_path("assets/cactus5.png"),
            resource_path("assets/cactus6.gif")
        ]

        self.last_obstacle_x = SCREEN_WIDTH

        # Сброс параметров
        self.game_over = False
        self.score = 0.0
        self.move_speed = MOVE_SPEED

    def spawn_obstacle(self):
        image = random.choice(self.cactus_images)
        obstacle = arcade.Sprite(image, scale=1)

        min_distance = 300
        extra = random.randint(0, 200)

        obstacle.center_x = self.last_obstacle_x + min_distance + extra
        obstacle.center_y = self.ground_list[0].top + obstacle.height / 2
        obstacle.change_x = -self.move_speed

        self.last_obstacle_x = obstacle.center_x
        self.obstacle_list.append(obstacle)

    def on_update(self, delta_time):
        if self.game_over:
            return

        # Ускорение и счёт
        self.move_speed += self.acceleration
        self.score += 0.1

        # Создание препятствий
        if len(self.obstacle_list) == 0:
            self.spawn_obstacle()
        else:
            last = self.obstacle_list[-1]
            if last.center_x < SCREEN_WIDTH:
                self.spawn_obstacle()

        # Двигаем препятствия
        self.obstacle_list.update()

        # Удаляем ушедшие за экран
        for obstacle in self.obstacle_list:
            if obstacle.right < 0:
                obstacle.remove_from_sprite_lists()

        # Физика
        self.physics_engine.update()

        # Столкновение
        if arcade.check_for_collision_with_list(self.player, self.obstacle_list):
            self.game_over = True
            self.move_speed = 0

    def on_draw(self):
        self.clear()
        self.ground_list.draw()
        self.obstacle_list.draw()
        self.player_list.draw()

        if self.game_over:
            self.game_over_list.draw()
            arcade.draw_text(
                "Нажмите R для новой игры",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 200,
                arcade.color.BLACK,
                font_size=50,
                anchor_x="center",
                font_name="Consolas"
            )
        else:
            arcade.draw_text(
                f"SCORE: {int(self.score)}",
                SCREEN_WIDTH - 50,
                SCREEN_HEIGHT - 70,
                arcade.color.BLACK,
                font_size=40,
                anchor_x="right",
                font_name="Consolas"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
        elif key == arcade.key.R and self.game_over:
            # Перезапуск игры
            self.setup()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:  # левая кнопка
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED


def main():
    game = DinoGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()