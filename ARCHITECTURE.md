# 🏗️ Architecture Documentation

## 📁 Project Structure

```
snakegame/
├── game.py              # Main game entry point
├── components/          # Game components
│   ├── core/           # Core system modules
│   │   ├── config.py   # Configuration management
│   │   ├── game_state.py # Game state management
│   │   ├── event_handler.py # Event processing
│   │   ├── game_renderer.py # Rendering system
│   │   ├── game_engine.py # Core game engine
│   │   ├── achievement_manager.py # Achievement system
│   │   ├── audio_manager.py # Audio management
│   │   └── __init__.py
│   ├── entities/       # Game objects
│   │   ├── snake.py    # Snake entity
│   │   ├── food.py     # Food system
│   │   ├── powerup.py  # Power-up system
│   │   ├── obstacle.py # Obstacle system
│   │   └── __init__.py
│   └── ui/            # User interface
│       ├── base_menu.py     # Base menu class
│       ├── game_menus.py    # Game menus
│       ├── settings_menu.py # Settings interface
│       ├── score_menu.py    # High score display
│       ├── achievement_menu.py # Achievement interface
│       └── __init__.py
├── assets/             # Game assets
│   └── sounds/        # Audio files
├── requirements.txt     # Python dependencies
├── README.md           # User documentation
├── ARCHITECTURE.md     # This file
├── config.json         # User settings (auto-generated)
├── high_scores.json    # High scores (auto-generated)
└── achievements.json   # Achievement progress (auto-generated)
```

## 🎯 Technical Features

### Core Architecture
- **Clean Architecture**: Separation of Core, Entities, and UI layers
- **Object-Oriented Programming**: Inheritance and encapsulation
- **Separation of Concerns**: Logic, rendering, and UI are separate
- **Modular Design**: Easy to maintain and extend
- **Event-Driven Architecture**: Centralized event handling

### Achievement System
- **Hybrid tracking**: Session and persistent achievements
- **Real-time statistics**: Player action tracking
- **Notification queue**: Timed popup system
- **JSON persistence**: Save/load achievement progress

### Performance Optimizations
- **Font Caching**: Global font cache to avoid recreation
- **Text Surface Caching**: Cache rendered text for performance
- **Optimized Rendering**: Removed complex unnecessary effects
- **Fixed Screen Size**: 1000x700 for stable performance
- **Simplified UI**: Focus on gameplay over visual complexity
- **Optimized Game Loop**: Reduced calculations and memory allocations

### Configuration & State Management
- **JSON Configuration**: Settings stored with dot notation
- **State Management**: Efficient game state handling
- **Error Handling**: Robust error handling throughout
- **Animation System**: Math-based smooth animations
- **Collision Detection**: Accurate collision with pygame.Rect

## 🔧 Development Guidelines

### Code Organization
- Follow the established layer separation
- Keep entities focused on their specific responsibilities
- Use the event system for cross-component communication
- Maintain consistent error handling patterns

### Performance Considerations
- Cache frequently used resources (fonts, surfaces)
- Minimize object creation in game loops
- Use efficient collision detection algorithms
- Keep UI updates separate from game logic

### Adding New Features
1. Determine the appropriate layer (Core/Entities/UI)
2. Follow existing patterns and conventions
3. Add appropriate error handling
4. Update configuration if needed
5. Test performance impact