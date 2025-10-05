# LocalSync

A local package synchronization and sharing tool that allows you to share and discover packages across your local network.

## Features

- **Network Discovery**: Uses mDNS/Bonjour for automatic server discovery
- **Package Sharing**: Share cached packages with other machines on the network
- **Architecture Filtering**: Automatically filters packages compatible with your architecture
- **Web API**: RESTful API for package management
- **Command Line Interface**: Easy-to-use CLI for all operations

## Installation

### From APT Repository (Recommended)

```bash
# Add the repository key
curl -fsSL https://chamesh2019.github.io/LocalSync/public.key | sudo apt-key add -

# Add the repository
echo "deb https://chamesh2019.github.io/LocalSync stable main" | sudo tee /etc/apt/sources.list.d/localsync.list

# Update package list and install
sudo apt update
sudo apt install localsync
```

### Manual Installation

Download the latest .deb file from the [releases page](https://github.com/chamesh2019/LocalSync/releases):

```bash
wget https://github.com/chamesh2019/LocalSync/releases/latest/download/localsync_0.1.0-1_all.deb
sudo dpkg -i localsync_0.1.0-1_all.deb
sudo apt-get install -f  # Install any missing dependencies
```

### From Source

```bash
git clone https://github.com/chamesh2019/LocalSync.git
cd LocalSync
pip install -r requirements.txt
python main.py --help
```

## Usage

### Start the Server

```bash
localsync serve
```

This will:
- Start monitoring `/var/cache/apt/archives/` for packages
- Start the web server on port 53456
- Register the service for network discovery

### List Available Packages

```bash
localsync list
```

This will discover all LocalSync servers on the network and display available packages.

### Install a Package

```bash
localsync install <package-name>
```

This will:
- Search for the package on all discovered servers
- Filter packages compatible with your architecture
- Allow you to select which version/server to install from
- Download and install the package

### Get Help

```bash
localsync --help
# or
localsync h
```

## API Endpoints

When running as a server, LocalSync exposes these endpoints:

- `GET /api/cache-list` - List all cached packages
- `GET /api/server-info` - Get server information
- `GET /api/pkg/{package_name}` - Get information about a specific package
- `POST /api/download` - Download a package file (JSON body: `{"filename": "package.deb"}`)

## Architecture

LocalSync is built with a modular architecture:

```
src/
├── client/           # Client-side functionality
│   ├── cli.py       # Command-line interface
│   ├── network.py   # Network discovery
│   └── package_manager.py  # Package operations
├── server/          # Server-side functionality
│   ├── api_routes.py    # API endpoints
│   ├── app_config.py    # Application configuration
│   ├── mdns_service.py  # mDNS service management
│   └── network_utils.py # Network utilities
└── lib/             # Shared libraries
    └── cache.py     # Package cache management
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Development

### Building the Package

```bash
# Install build dependencies
sudo apt-get install debhelper dh-python python3-setuptools python3-all

# Build the package
dpkg-buildpackage -us -uc -b

# The .deb file will be created in the parent directory
```

### Running Tests

```bash
# Install in development mode
pip install -e .

# Run the application
python main.py serve
```
