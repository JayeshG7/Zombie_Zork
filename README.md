# Zombie Zork: Distributed Text Adventure Game

A sophisticated distributed text adventure game system featuring a hub-and-spoke architecture, asynchronous communication, and persistent state management across multiple domains.

## 🎮 Features

- **Distributed Architecture**: Central hub server coordinating multiple domain servers
- **Asynchronous Communication**: Built with aiohttp for efficient real-time gameplay
- **Persistent State Management**: Robust tracking of user states and items across domains
- **Dynamic Item System**: Depth-based mechanics with unique properties and interactions
- **RESTful API**: Seamless inter-domain communication and state synchronization

## 🛠️ Technical Stack

- Python 3.x
- aiohttp for asynchronous web operations
- RESTful API architecture
- Distributed systems design

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/JayeshG7/Zombie_Zork.git
cd Zombie_Zork
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install aiohttp
```

### Running the Game

1. Start the hub server:
```bash
python hub.py
```

2. In a new terminal, start a domain server:
```bash
source venv/bin/activate
python newdomain.py
```

3. Access the game through your web browser at the URL shown in the hub server output.

## 🎯 Gameplay

- Move between different domains
- Collect and use items
- Solve puzzles and challenges
- Interact with the zombie-themed environment

## 📚 Project Structure

- `hub.py`: Central server coordinating game state and domain communication
- `newdomain.py`: Domain server implementation for individual game areas

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Jayesh Ghosh - [GitHub](https://github.com/JayeshG7)

## 🙏 Acknowledgments

- Inspired by classic text adventure games
- Built with modern distributed systems principles
- Designed for educational and entertainment purposes 