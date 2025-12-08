import pygame
import sys
import asyncio

pygame.init()



clock = pygame.time.Clock()
async def main():
    WIDTH, HEIGHT = 600, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cookie Clicker")

    WHITE = (51, 204, 255)
    COOKIE_COLOR = (204, 153, 0)
    CHIP_COLOR = (90, 50, 30)
    GREEN = (0, 200, 0)
    RED = (200, 0, 0)
    BLACK = (0, 0, 0)

    font = pygame.font.SysFont('Courier', 30, bold=True)

    cookie_radius = 120
    cookie_pos = (WIDTH // 2, HEIGHT // 2)
    cookie_scale = 1.0
    target_scale = 1.0
    scale_speed_up = 0.05
    scale_speed_down = 0.1

    main_upgrade_pulse = 0
    shop_auto_pulse = 0
    shop_menu_pulse = 0
    shop_auto_up_pulse = 0
    main_shop_pulse = 0

    cookies = 0
    cookies_per_click = 1
    upgrade_cost = 50
    auto_click_cost = 100
    auto_click_enabled = False
    auto_click_power = 0.1
    auto_upgrade_cost = 200

    # Precompute chocolate chip positions
    chip_positions = [
        (-80, -60), (70, -50), (50, 60), (-60, 50), (0, -90), (80, 20), (-50, -20), (30, 80)
    ]
    chip_radius = 15

    # Screen states
    MAIN_SCREEN = 'main'
    SHOP_SCREEN = 'shop'
    current_screen = MAIN_SCREEN
    pending_screen = None
    screen_timer = 0
    screen_delay = 20
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if current_screen == MAIN_SCREEN:
                    dx = mouse_x - cookie_pos[0]
                    dy = mouse_y - cookie_pos[1]
                    if dx*dx + dy*dy <= cookie_radius*cookie_radius:
                        cookies += cookies_per_click
                        target_scale = 1.2

                    # Main upgrade button
                    if 20 <= mouse_x <= 300 and 520 <= mouse_y <= 580:
                        if cookies >= upgrade_cost:
                            cookies -= upgrade_cost
                            cookies_per_click += 1
                            upgrade_cost = int(upgrade_cost * 1.5)
                            main_upgrade_pulse = 5

                    # Shop button
                    if 320 <= mouse_x <= 500 and 520 <= mouse_y <= 580:
                        main_shop_pulse = 5
                        pending_screen = SHOP_SCREEN
                        screen_timer = screen_delay

                elif current_screen == SHOP_SCREEN:
                    # Auto click upgrade button
                    if 80 <= mouse_x <= 400 and 200 <= mouse_y <= 260:
                        if cookies >= auto_click_cost and not auto_click_enabled:
                            cookies -= auto_click_cost
                            auto_click_enabled = True
                            shop_auto_pulse = 5

                    # Auto click upgrade button (increase power)
                    if 80 <= mouse_x <= 400 and 280 <= mouse_y <= 340:
                        if cookies >= auto_upgrade_cost and auto_click_enabled:
                            cookies -= auto_upgrade_cost
                            auto_click_power += 0.1
                            auto_upgrade_cost = int(auto_upgrade_cost * 1.7)
                            shop_auto_up_pulse = 5

                    # Menu button
                    if 20 <= mouse_x <= 220 and 520 <= mouse_y <= 580:
                        shop_menu_pulse = 5
                        pending_screen = MAIN_SCREEN
                        screen_timer = screen_delay

        # Automatic clicks if enabled
        if auto_click_enabled:
            cookies += auto_click_power

        # Handle delayed screen transitions
        if pending_screen:
            if screen_timer > 0:
                screen_timer -= 1
            else:
                current_screen = pending_screen
                pending_screen = None

        # Animate cookie scale gradually
        if cookie_scale < target_scale:
            cookie_scale += scale_speed_up
            if cookie_scale >= target_scale:
                target_scale = 1.0
        elif cookie_scale > 1.0:
            cookie_scale -= scale_speed_down
            if cookie_scale < 1.0:
                cookie_scale = 1.0

        current_radius = int(cookie_radius * cookie_scale)

        # Draw background
        screen.fill(WHITE)

        if current_screen == MAIN_SCREEN:
            # Draw cookie
            pygame.draw.circle(screen, COOKIE_COLOR, cookie_pos, current_radius)
            for dx, dy in chip_positions:
                chip_x = int(cookie_pos[0] + dx * (current_radius / cookie_radius))
                chip_y = int(cookie_pos[1] + dy * (current_radius / cookie_radius))
                pygame.draw.circle(screen, CHIP_COLOR, (chip_x, chip_y), chip_radius)

            # Main upgrade button
            button_width = 280 + main_upgrade_pulse * 2
            button_height = 60 + main_upgrade_pulse * 2
            button_rect = pygame.Rect(20 - main_upgrade_pulse, 520 - main_upgrade_pulse, button_width, button_height)
            pygame.draw.rect(screen, GREEN, button_rect, border_radius=5)
            if main_upgrade_pulse > 0:
                main_upgrade_pulse -= 1
            upgrade_text = font.render(f"UPGRADE ({upgrade_cost})", True, BLACK)
            screen.blit(upgrade_text, (25, 530))

            # Shop button
            shop_width = 180 + main_shop_pulse * 2
            shop_height = 60 + main_shop_pulse * 2
            shop_rect = pygame.Rect(320 - main_shop_pulse, 520 - main_shop_pulse, shop_width, shop_height)
            pygame.draw.rect(screen, RED, shop_rect, border_radius=5)
            if main_shop_pulse > 0:
                main_shop_pulse -= 1
            shop_text = font.render("SHOP", True, BLACK)
            screen.blit(shop_text, (350, 530))

            # Cookie count
            count_text = font.render(f"Cookies: {int(cookies)}", True, BLACK)
            screen.blit(count_text, (20, 20))

        elif current_screen == SHOP_SCREEN:
            # Auto click upgrade button
            auto_width = 320 + shop_auto_pulse * 2
            auto_height = 60 + shop_auto_pulse * 2
            auto_rect = pygame.Rect(80 - shop_auto_pulse, 200 - shop_auto_pulse, auto_width, auto_height)
            pygame.draw.rect(screen, RED, auto_rect, border_radius=5)
            if shop_auto_pulse > 0:
                shop_auto_pulse -= 1
            auto_text = font.render(f"AUTO CLICK ({auto_click_cost})", True, BLACK)
            screen.blit(auto_text, (100, 210))

            # Auto click upgrade power button
            auto_up_width = 320 + shop_auto_up_pulse * 2
            auto_up_height = 60 + shop_auto_up_pulse * 2
            auto_up_rect = pygame.Rect(80 - shop_auto_up_pulse, 280 - shop_auto_up_pulse, auto_up_width, auto_up_height)
            pygame.draw.rect(screen, RED, auto_up_rect, border_radius=5)
            if shop_auto_up_pulse > 0:
                shop_auto_up_pulse -= 1
            auto_up_text = font.render(f"UPGRADE AUTO ({auto_upgrade_cost})", True, BLACK)
            screen.blit(auto_up_text, (100, 290))

            # Menu button
            menu_width = 200 + shop_menu_pulse * 2
            menu_height = 60 + shop_menu_pulse * 2
            menu_rect = pygame.Rect(20 - shop_menu_pulse, 520 - shop_menu_pulse, menu_width, menu_height)
            pygame.draw.rect(screen, GREEN, menu_rect, border_radius=5)
            if shop_menu_pulse > 0:
                shop_menu_pulse -= 1
            menu_text = font.render("MENU", True, BLACK)
            screen.blit(menu_text, (50, 530))

            # Cookie count
            count_text = font.render(f"Cookies: {int(cookies)}", True, BLACK)
            screen.blit(count_text, (20, 20))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)
asyncio.run(main())