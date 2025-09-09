import pygame
import sys
from darwin import app as a


def main():
    """Main function to start the Darwin application"""
    try:
        app = a.DarwinApp()
        app.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    finally:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
