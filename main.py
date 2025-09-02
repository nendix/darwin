#!/usr/bin/env python3
"""
Darwin - Genetic Algorithm Evolution Simulator
Main entry point for the application
"""

import pygame
import sys
from src.app import DarwinApp


def main():
    """Main function to start the Darwin application"""
    try:
        app = DarwinApp()
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
