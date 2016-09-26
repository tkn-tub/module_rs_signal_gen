# Wishful R&S signal generator module

## Setup phase

### Build and install hybrid MAC from source
    cd src
    make all

The R&S binary is copied into $(VIRTUAL_ENV)/bin

## Test the module
    cd test
    wishful-agent --config config_local.yaml
